"""NFL paper-log v1. Score paper tickets. Do not submit orders.

Reads a slate of locks, writes one row per ticket, grades a finals file,
and fills CLV when a same-contract close snapshot is provided. Fee, de-vig,
Brier, log loss, and the quarter-Kelly shadow are computed here. The stake
stays $20. An LLM does not set the price or the stake.

No live order path, no key loading, no network calls.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from devig import as_decimal, devig_pair, implied_from_american
from math_fees_arb import (
    NOVIG_FUTURES_COEFF,
    NOVIG_STRAIGHT_LIVE_COEFF,
    PM_TAKER_THETA_DEFAULT,
    novig_taker_fee_per_dollar,
    pm_taker_fee_rounded,
)
from paper_grade import american_win_profit, grade_moneyline, grade_spread, grade_total, settle

SCHEMA_VERSION = "nfl-paper-log-v1"
PAPER_STAKE = Decimal("20")
LOG_LOSS_EPS = Decimal("1e-15")
VENUES = {"polymarket_us", "novig", "paper_ledger"}
MARKETS = {"spread", "total", "ml"}
STAKED_DECISIONS = {"paper_lock", "propose", "lean"}
DEVIG_METHODS = {"basic", "shin"}

COLUMNS = (
    "schema_version",
    "ticket_id",
    "slate",
    "decision_time",
    "sport",
    "week",
    "event",
    "away",
    "home",
    "kick_time_pt",
    "market_type",
    "side",
    "line",
    "period",
    "venue",
    "market_id",
    "event_status",
    "american_odds",
    "american_odds_other",
    "devig_other_side",
    "stake",
    "open_price",
    "close_price",
    "close_status",
    "devig_method",
    "p_market",
    "p_basic",
    "p_shin",
    "p_close",
    "fee_method",
    "fee_coeff",
    "fee_used",
    "fee_notes",
    "same_contract_key",
    "same_contract_mismatch",
    "mismatch_detail",
    "decision",
    "hit",
    "result",
    "pnl",
    "clv",
    "brier",
    "log_loss",
    "ev_usd",
    "p_model",
    "brier_model",
    "log_loss_model",
    "quarter_kelly_shadow",
    "settlement_notes",
    "settlement_source",
    "away_score",
    "home_score",
    "margin",
    "reason",
    "sources",
    "counter_case",
    "trade_card_id",
    "price",
    "fee_assumed",
    "size_paper",
    "ts",
    "settlement_later",
)

DECIMAL_FIELDS = {
    "american_odds",
    "american_odds_other",
    "stake",
    "open_price",
    "close_price",
    "p_market",
    "p_basic",
    "p_shin",
    "p_close",
    "fee_coeff",
    "fee_used",
    "pnl",
    "clv",
    "brier",
    "log_loss",
    "ev_usd",
    "p_model",
    "brier_model",
    "log_loss_model",
    "quarter_kelly_shadow",
    "price",
    "fee_assumed",
    "size_paper",
    "margin",
}
INT_FIELDS = {"week", "away_score", "home_score"}
BOOL_FIELDS = {"same_contract_mismatch"}


def new_row() -> dict:
    row = {key: None for key in COLUMNS}
    row["schema_version"] = SCHEMA_VERSION
    row["same_contract_mismatch"] = False
    row["mismatch_detail"] = ""
    row["stake"] = PAPER_STAKE
    return row


def canon_event(event: str) -> str:
    text = " ".join(str(event).upper().split())
    text = text.replace(" AT ", " @ ")
    if " @ " not in text:
        raise ValueError(f"event must look like AWAY @ HOME, got {event!r}")
    away, home = [part.strip() for part in text.split(" @ ", 1)]
    if not away or not home or " " in away or " " in home:
        raise ValueError(f"event must be two abbreviations, got {event!r}")
    return f"{away} @ {home}"


def event_token(event: str) -> str:
    away, home = canon_event(event).split(" @ ")
    return f"{away}@{home}"


def canon_line(market_type: str, line) -> str:
    if market_type == "ml":
        if line is None or str(line).strip() == "" or str(line).strip().lower() == "ml":
            return "ML"
        raise ValueError("moneyline line must be empty or ML")
    if line is None or str(line).strip() == "":
        raise ValueError(f"{market_type} needs a line")
    rendered = format(as_decimal(line), "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    if market_type == "spread" and as_decimal(line) > 0 and not rendered.startswith("+"):
        rendered = "+" + rendered
    return rendered


def canon_side(market_type: str, side: str) -> str:
    text = str(side).strip()
    if market_type == "total":
        lowered = text.lower()
        if lowered not in {"over", "under"}:
            raise ValueError(f"total side must be over or under, got {side!r}")
        return lowered
    return text.upper()


def contract_key(
    *,
    sport: str,
    week: int,
    event: str,
    market_type: str,
    side: str,
    line: str,
    period: str,
) -> str:
    return (
        f"{sport.lower()}|week={int(week)}|event={event_token(event)}"
        f"|market={market_type}|side={side}|line={line}|period={period}"
    )


def require_stake(value) -> Decimal:
    stake = PAPER_STAKE if value is None else as_decimal(value)
    if stake != PAPER_STAKE:
        raise ValueError(
            f"NFL paper-log v1 uses a flat ${PAPER_STAKE} paper stake. Got {stake}. "
            "quarter_kelly_shadow does not change the stake."
        )
    return stake


def require_sport(value: str) -> str:
    sport = str(value).strip().upper()
    if sport != "NFL":
        raise ValueError(f"NFL paper-log v1 accepts NFL only. Got {sport}.")
    return sport


def american_int(value: Decimal) -> int:
    if value != value.to_integral_value():
        raise ValueError(f"v1 settles integer American odds, got {value}")
    return int(value)


def clip_prob(probability: Decimal) -> Decimal:
    if probability < LOG_LOSS_EPS:
        return LOG_LOSS_EPS
    if probability > 1 - LOG_LOSS_EPS:
        return Decimal("1") - LOG_LOSS_EPS
    return probability


def brier_score(probability: Decimal, outcome: int) -> Decimal:
    return (probability - Decimal(outcome)) ** 2


def log_loss_score(probability: Decimal, outcome: int) -> Decimal:
    """Natural-log loss. Probabilities are clipped to [1e-15, 1-1e-15]."""
    clipped = clip_prob(probability)
    if outcome == 1:
        return -clipped.ln()
    if outcome == 0:
        return -((Decimal("1") - clipped).ln())
    raise ValueError(f"log loss needs a binary outcome, got {outcome}")


def quarter_kelly_fraction(p_model: Decimal, american: Decimal) -> Decimal:
    """One quarter of the Kelly fraction. A negative value is left visible.

    f* = p - (1-p) / b, with b the net profit per $1 stake at the logged
    American price. The paper stake is not this fraction.
    """
    net = american_win_profit(Decimal("1"), american_int(american))
    if net <= 0:
        raise ValueError("odds pay no profit")
    full = p_model - (Decimal("1") - p_model) / net
    return full / Decimal("4")


def ev_usd(probability: Decimal, stake: Decimal, american: Decimal, fee_used: Decimal) -> Decimal:
    """Expectation under p_market at the logged American price, minus fee_used.

    Win profit is the exact stake * 100 / |odds| figure, before the cent round
    used at settlement. This is not a realized P/L and not an edge claim.
    """
    win = american_win_profit(stake, american_int(american))
    return probability * win - (Decimal("1") - probability) * stake - fee_used


def quote_fee(venue: str, open_price: Decimal, stake: Decimal, event_status: str) -> dict:
    """Dollar taker fee for a premium of `stake` at probability price `open_price`.

    Coefficients are the named constants in math_fees_arb.py. Re-check the
    venue page on the day of a card. fee_used is stored beside paper P/L and
    is not subtracted again inside paper_grade.settle.
    """
    if open_price <= 0 or open_price >= 1:
        raise ValueError(f"open_price must be between 0 and 1, got {open_price}")
    if venue == "paper_ledger":
        return {
            "fee_method": "american_hold_in_odds",
            "fee_coeff": Decimal("0"),
            "fee_used": Decimal("0"),
            "fee_notes": (
                "No separate taker fee. The American hold is removed by de-vig. "
                "fee_used is 0. paper_ledger is the flat -110 desk ledger, "
                "not a Polymarket US or Novig fill."
            ),
        }
    if venue == "polymarket_us":
        theta = PM_TAKER_THETA_DEFAULT
        contracts = stake / open_price
        fee = pm_taker_fee_rounded(open_price, contracts, theta)
        return {
            "fee_method": "polymarket_us_taker_v20260925",
            "fee_coeff": theta,
            "fee_used": fee,
            "fee_notes": (
                "theta=0.0695 from https://docs.polymarket.us/fees , read 2026-09-29, "
                "in force since 2026-09-25 00:00 ET. "
                "fee = banker's cent round of theta * contracts * p * (1-p), "
                "with contracts = stake / open_price and stake the premium. "
                "Re-check that page on the day of a card."
            ),
        }
    if venue == "novig":
        status = event_status or "OPEN_PREGAME"
        if status not in {"OPEN_PREGAME", "OPEN_INGAME"}:
            raise ValueError(f"Novig event_status must be OPEN_PREGAME or OPEN_INGAME, got {status}")
        per_contract = novig_taker_fee_per_dollar(
            open_price,
            NOVIG_STRAIGHT_LIVE_COEFF,
            "WHEN_LIVE",
            status,
        )
        contracts = stake / open_price
        charged = Decimal("0") if status == "OPEN_PREGAME" else NOVIG_STRAIGHT_LIVE_COEFF
        return {
            "fee_method": "novig_straight_taker_v20260929",
            "fee_coeff": charged,
            "fee_used": per_contract * contracts,
            "fee_notes": (
                f"Novig charge mode WHEN_LIVE, event_status={status}. "
                f"Live straight coefficient {NOVIG_STRAIGHT_LIVE_COEFF} is charged only "
                "when status is OPEN_INGAME. Pregame straights are 0. "
                f"Futures coefficient {NOVIG_FUTURES_COEFF} is not used on game tickets. "
                "Parlay coefficient 0.10 is out of scope. "
                "Help Center https://support.novig.com/en/articles/16195057-fees-on-novig "
                "read 2026-09-29. Fee = per-dollar-contract fee times contracts, "
                "contracts = stake / open_price. Re-check the article on the day of a card."
            ),
        }
    raise ValueError(
        f"venue {venue!r} is out of scope. Use polymarket_us, novig, or paper_ledger."
    )


def _text(lock: dict, slate: dict, key: str, default: str = "") -> str:
    value = lock.get(key, slate.get(key, default))
    if value is None:
        return ""
    return str(value).strip()


def build_row(lock: dict, slate: dict) -> dict:
    row = new_row()
    ticket_id = str(lock.get("ticket_id", "")).strip()
    if not ticket_id:
        raise ValueError("ticket_id is required")
    sport = require_sport(lock.get("sport", slate.get("sport", "NFL")))
    week_raw = lock.get("week", slate.get("week"))
    if week_raw is None:
        raise ValueError(f"{ticket_id} needs a week")
    week = int(week_raw)
    event = canon_event(lock["event"])
    away, home = event.split(" @ ")
    if lock.get("away") and lock["away"].strip().upper() != away:
        raise ValueError(f"{ticket_id} away does not match event")
    if lock.get("home") and lock["home"].strip().upper() != home:
        raise ValueError(f"{ticket_id} home does not match event")
    market_type = str(lock["market_type"]).strip().lower()
    if market_type not in MARKETS:
        raise ValueError(f"{ticket_id} market_type must be spread, total, or ml")
    side = canon_side(market_type, lock["side"])
    if market_type in {"spread", "ml"} and side not in {away, home}:
        raise ValueError(f"{ticket_id} side {side} is not {away} or {home}")
    line = canon_line(market_type, lock.get("line"))
    period = str(lock.get("period", "FG")).strip().upper()
    if not period:
        raise ValueError(f"{ticket_id} needs a period")
    venue = _text(lock, slate, "venue").lower()
    if venue not in VENUES:
        raise ValueError(
            f"{ticket_id} venue must be polymarket_us, novig, or paper_ledger, got {venue!r}"
        )
    kick = _text(lock, slate, "kick_time_pt")
    if not kick:
        raise ValueError(f"{ticket_id} needs kick_time_pt")
    decision_time = _text(lock, slate, "decision_time")
    if not decision_time:
        raise ValueError(f"{ticket_id} needs decision_time")
    sources = _text(lock, slate, "sources")
    if not sources:
        raise ValueError(f"{ticket_id} needs sources")
    odds_raw = lock.get("american_odds", slate.get("american_odds"))
    if odds_raw is None:
        raise ValueError(f"{ticket_id} needs american_odds")
    american = as_decimal(odds_raw)
    other_raw = lock.get("american_odds_other", slate.get("american_odds_other"))
    if other_raw is None:
        if market_type == "ml":
            raise ValueError(f"{ticket_id} moneyline needs american_odds_other")
        other = american
        other_side = "symmetric_same_american"
    else:
        other = as_decimal(other_raw)
        other_side = "quoted"
    method = _text(lock, slate, "devig_method", "basic").lower()
    if method not in DEVIG_METHODS:
        raise ValueError(f"{ticket_id} devig_method must be basic or shin")
    decision = _text(lock, slate, "decision", "paper_lock")
    event_status = _text(lock, slate, "event_status", "OPEN_PREGAME")
    stake = require_stake(lock.get("stake", slate.get("stake")))
    implied_side = implied_from_american(american)
    implied_other = implied_from_american(other)
    p_market, p_basic, p_shin = devig_pair(method, implied_side, implied_other)
    fee = quote_fee(venue, implied_side, stake, event_status)
    p_model = None
    if lock.get("p_model") is not None:
        p_model = as_decimal(lock["p_model"])
        if p_model <= 0 or p_model >= 1:
            raise ValueError(f"{ticket_id} p_model must be between 0 and 1")

    row.update(
        {
            "ticket_id": ticket_id,
            "slate": _text(lock, slate, "slate"),
            "decision_time": decision_time,
            "sport": sport,
            "week": week,
            "event": event,
            "away": away,
            "home": home,
            "kick_time_pt": kick,
            "market_type": market_type,
            "side": side,
            "line": line,
            "period": period,
            "venue": venue,
            "market_id": _text(lock, slate, "market_id"),
            "event_status": event_status,
            "american_odds": american,
            "american_odds_other": other,
            "devig_other_side": other_side,
            "stake": stake,
            "open_price": implied_side,
            "devig_method": method,
            "p_market": p_market,
            "p_basic": p_basic,
            "p_shin": p_shin,
            "fee_method": fee["fee_method"],
            "fee_coeff": fee["fee_coeff"],
            "fee_used": fee["fee_used"],
            "fee_notes": fee["fee_notes"],
            "same_contract_key": contract_key(
                sport=sport,
                week=week,
                event=event,
                market_type=market_type,
                side=side,
                line=line,
                period=period,
            ),
            "decision": decision,
            "result": "OPEN",
            "ev_usd": ev_usd(p_market, stake, american, fee["fee_used"]),
            "p_model": p_model,
            "settlement_notes": _text(lock, slate, "decision_time_note"),
            "reason": _text(lock, slate, "reason"),
            "sources": sources,
            "counter_case": _text(lock, slate, "counter_case") or None,
            "trade_card_id": _text(lock, slate, "trade_card_id") or None,
        }
    )
    if p_model is not None and decision in STAKED_DECISIONS:
        row["quarter_kelly_shadow"] = quarter_kelly_fraction(p_model, american)
    _attach_compare(row, lock.get("compare"))
    _alias(row)
    return row


def _attach_compare(row: dict, compare: dict | None) -> None:
    if not compare:
        return
    other_key = contract_key(
        sport=compare.get("sport", row["sport"]),
        week=int(compare.get("week", row["week"])),
        event=compare.get("event", row["event"]),
        market_type=str(compare.get("market_type", row["market_type"])).strip().lower(),
        side=canon_side(
            str(compare.get("market_type", row["market_type"])).strip().lower(),
            compare.get("side", row["side"]),
        ),
        line=canon_line(
            str(compare.get("market_type", row["market_type"])).strip().lower(),
            compare.get("line", row["line"]),
        ),
        period=str(compare.get("period", row["period"])).strip().upper(),
    )
    if other_key != row["same_contract_key"]:
        _flag(row, f"compare key {other_key} != lock key {row['same_contract_key']}")


def _flag(row: dict, detail: str) -> None:
    row["same_contract_mismatch"] = True
    prior = row.get("mismatch_detail") or ""
    row["mismatch_detail"] = f"{prior}; {detail}".strip("; ")


def _alias(row: dict) -> None:
    row["price"] = row["open_price"]
    row["fee_assumed"] = row["fee_used"]
    row["size_paper"] = row["stake"]
    row["ts"] = row["decision_time"]
    row["settlement_later"] = row["settlement_notes"]


def _append_note(row: dict, note: str) -> None:
    prior = row.get("settlement_notes") or ""
    row["settlement_notes"] = f"{prior} {note}".strip()
    row["settlement_later"] = row["settlement_notes"]


def load_slate(path: Path) -> list[dict]:
    slate = json.loads(path.read_text(encoding="utf-8"))
    locks = slate.get("locks")
    if not isinstance(locks, list) or not locks:
        raise ValueError("slate needs a non-empty locks list")
    rows = []
    seen = set()
    for lock in locks:
        row = build_row(lock, slate)
        if row["ticket_id"] in seen:
            raise ValueError(f"duplicate ticket_id {row['ticket_id']}")
        seen.add(row["ticket_id"])
        rows.append(row)
    return rows


def apply_finals(rows: list[dict], finals: dict) -> None:
    games = {}
    for game in finals.get("games", []):
        key = event_token(game["event"])
        if key in games:
            raise ValueError(f"duplicate final for {key}")
        games[key] = game
    pulled = finals.get("pulled", "")
    for row in rows:
        game = games.get(event_token(row["event"]))
        if game is None:
            _append_note(row, "final missing")
            continue
        status = str(game.get("status", ""))
        if status not in {"STATUS_FINAL", "FINAL"}:
            row["result"] = "OPEN"
            _append_note(row, f"not final: {status or 'unknown'}")
            continue
        if row["period"] != "FG":
            row["result"] = "OPEN"
            _append_note(row, f"period {row['period']} is not FG; v1 grades full-game finals only")
            continue
        away_score = int(game["away_score"])
        home_score = int(game["home_score"])
        away, home = row["event"].split(" @ ")
        final_event = canon_event(game["event"])
        if final_event != row["event"]:
            raise ValueError(f"final event {final_event} does not match {row['event']}")
        if str(game.get("away", away)).strip().upper() != away:
            raise ValueError(f"final away does not match {row['event']}")
        if str(game.get("home", home)).strip().upper() != home:
            raise ValueError(f"final home does not match {row['event']}")
        row["away_score"] = away_score
        row["home_score"] = home_score
        row["settlement_source"] = game.get("source") or ""
        if row["decision"] not in STAKED_DECISIONS:
            row["result"] = "OPEN"
            _append_note(row, f"{row['decision']} is not graded for P/L")
            continue
        graded = _grade_market(row, away_score, home_score)
        row["result"] = graded["result"]
        row["hit"] = graded["hit"]
        row["margin"] = graded["margin"]
        row["pnl"] = settle(graded["result"], row["stake"], american_int(row["american_odds"]))
        outcome = {"W": 1, "L": 0, "P": None}[graded["result"]]
        if outcome is None:
            row["brier"] = None
            row["log_loss"] = None
            row["brier_model"] = None
            row["log_loss_model"] = None
        else:
            row["brier"] = brier_score(row["p_market"], outcome)
            row["log_loss"] = log_loss_score(row["p_market"], outcome)
            if row["p_model"] is not None:
                row["brier_model"] = brier_score(row["p_model"], outcome)
                row["log_loss_model"] = log_loss_score(row["p_model"], outcome)
        overtime = bool(game.get("overtime"))
        ot_note = (
            "overtime included in the final score"
            if overtime
            else "no overtime period in the source linescore"
        )
        pulled_note = f" pulled {pulled}" if pulled else ""
        _append_note(
            row,
            (
                f"STATUS_FINAL away {away_score} home {home_score}; "
                f"margin {format(graded['margin'], 'f')}; {ot_note}.{pulled_note}"
            ).strip(),
        )
        _alias(row)


def _grade_market(row: dict, away_score: int, home_score: int) -> dict:
    away, home = row["event"].split(" @ ")
    if row["market_type"] == "total":
        return grade_total(away_score, home_score, row["side"], row["line"])
    if row["side"] == away:
        pick, opp = away_score, home_score
    else:
        pick, opp = home_score, away_score
    if row["market_type"] == "spread":
        return grade_spread(pick, opp, row["line"])
    return grade_moneyline(pick, opp)


def mark_closes_missing(rows: list[dict]) -> None:
    for row in rows:
        if row.get("close_status") == "ok":
            continue
        row["close_status"] = "close missing"
        row["close_price"] = None
        row["p_close"] = None
        row["clv"] = None
        _alias(row)


def apply_closes(rows: list[dict], closes: dict) -> None:
    by_id = {row["ticket_id"]: row for row in rows}
    seen = set()
    for snap in closes.get("closes", []):
        ticket_id = str(snap.get("ticket_id", "")).strip()
        if not ticket_id:
            raise ValueError("close snapshot needs ticket_id")
        if ticket_id in seen:
            raise ValueError(f"duplicate close for {ticket_id}")
        seen.add(ticket_id)
        row = by_id.get(ticket_id)
        if row is None:
            print(f"close snapshot ticket {ticket_id} is not in the log", file=sys.stderr)
            continue
        _apply_one_close(row, snap)
    for row in rows:
        if row["ticket_id"] not in seen:
            row["close_status"] = "close missing"
            row["close_price"] = None
            row["p_close"] = None
            row["clv"] = None
        _alias(row)


def _apply_one_close(row: dict, snap: dict) -> None:
    for field in ("market_type", "side", "line", "period"):
        if field not in snap:
            raise ValueError(f"close for {row['ticket_id']} needs {field}")
    market_type = str(snap["market_type"]).strip().lower()
    side = canon_side(market_type, snap["side"])
    line = canon_line(market_type, snap["line"])
    period = str(snap["period"]).strip().upper()
    event = snap.get("event", row["event"])
    other_key = contract_key(
        sport=row["sport"],
        week=row["week"],
        event=event,
        market_type=market_type,
        side=side,
        line=line,
        period=period,
    )
    if other_key != row["same_contract_key"]:
        _flag(row, f"close key {other_key} != lock key {row['same_contract_key']}")
        row["close_status"] = "close missing"
        row["close_price"] = None
        row["p_close"] = None
        row["clv"] = None
        return
    implied_side, implied_other = _close_implied(row, snap)
    p_close, _basic, _shin = devig_pair(row["devig_method"], implied_side, implied_other)
    row["close_price"] = implied_side
    row["p_close"] = p_close
    # Positive CLV: the close assigns a higher probability to the side than
    # the price taken, so the number shortened and the ticket beat the close.
    row["clv"] = p_close - row["p_market"]
    row["close_status"] = "ok"
    _alias(row)


def _close_implied(row: dict, snap: dict) -> tuple[Decimal, Decimal]:
    if snap.get("close_implied") is not None:
        if snap.get("close_implied_other") is None:
            raise ValueError(f"close for {row['ticket_id']} needs close_implied_other")
        return as_decimal(snap["close_implied"]), as_decimal(snap["close_implied_other"])
    if snap.get("close_american") is None:
        raise ValueError(f"close for {row['ticket_id']} needs close_american or close_implied")
    side = as_decimal(snap["close_american"])
    if snap.get("close_american_other") is not None:
        other = as_decimal(snap["close_american_other"])
    elif snap.get("close_other_side") == "symmetric_same_american":
        other = side
    else:
        raise ValueError(
            f"close for {row['ticket_id']} needs close_american_other "
            "or close_other_side=symmetric_same_american"
        )
    return implied_from_american(side), implied_from_american(other)


def is_complete(row: dict) -> bool:
    if not row.get("same_contract_key"):
        return False
    if row.get("p_market") is None or row.get("open_price") is None:
        return False
    if not row.get("fee_method") or row.get("fee_used") is None:
        return False
    if not row.get("sources"):
        return False
    if row.get("close_status") not in {"ok", "close missing"}:
        return False
    if row["close_status"] == "ok" and (row.get("close_price") is None or row.get("clv") is None):
        return False
    return True


def _money(amount: Decimal) -> str:
    cents = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if cents < 0:
        return f"-${format(abs(cents), 'f')}"
    return f"${format(cents, 'f')}"


def _prob(amount: Decimal | None) -> str:
    if amount is None:
        return ""
    return format(amount.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP), "f")


def _mean(values: list[Decimal]) -> Decimal | None:
    if not values:
        return None
    return sum(values, Decimal("0")) / Decimal(len(values))


def _se(values: list[Decimal]) -> Decimal | None:
    n = len(values)
    if n < 2:
        return None
    center = _mean(values)
    assert center is not None
    var = sum(((value - center) ** 2 for value in values), Decimal("0")) / Decimal(n - 1)
    return var.sqrt()


def render_scorecard(rows: list[dict]) -> str:
    n = len(rows)
    complete = sum(1 for row in rows if is_complete(row))
    mismatches = sum(1 for row in rows if row.get("same_contract_mismatch"))
    staked = [row for row in rows if row.get("decision") in STAKED_DECISIONS]
    graded = [row for row in staked if row.get("result") in {"W", "L", "P"}]
    wins = sum(1 for row in graded if row["result"] == "W")
    losses = sum(1 for row in graded if row["result"] == "L")
    pushes = sum(1 for row in graded if row["result"] == "P")
    decided = wins + losses
    pnl_values = [row["pnl"] for row in graded if row.get("pnl") is not None]
    net = sum(pnl_values, Decimal("0"))
    risked = sum((row["stake"] for row in graded), Decimal("0"))
    briers = [row["brier"] for row in staked if row.get("brier") is not None]
    logs = [row["log_loss"] for row in staked if row.get("log_loss") is not None]
    clvs = [row["clv"] for row in rows if row.get("clv") is not None]
    model_briers = [row["brier_model"] for row in staked if row.get("brier_model") is not None]
    kellys = [row["quarter_kelly_shadow"] for row in rows if row.get("quarter_kelly_shadow") is not None]
    slate = next((row["slate"] for row in rows if row.get("slate")), "NFL paper")
    week = rows[0]["week"] if rows else ""
    if n and complete == n:
        completeness = f"100% ({complete}/{n})"
    elif n:
        pct = (Decimal(complete) / Decimal(n) * Decimal("100")).quantize(Decimal("0.1"))
        completeness = f"{format(pct, 'f')}% ({complete}/{n})"
    else:
        completeness = "n/a"
    mean_clv = _mean(clvs)
    se_clv = _se(clvs)
    if mean_clv is None:
        stamped_missing = bool(rows) and all(row.get("close_status") == "close missing" for row in rows)
        clv_cell = "close missing (n=0)" if stamped_missing else "not stamped (n=0)"
    else:
        se_text = "n=1" if se_clv is None else f"se {_prob(se_clv)}"
        clv_cell = f"{_prob(mean_clv)} (n={len(clvs)}, {se_text})"
    if decided:
        rate = Decimal(wins) / Decimal(decided)
        hit_cell = (
            f"{wins} wins, {losses} losses, {pushes} pushes "
            f"({_prob(rate)} of decided)"
        )
    else:
        hit_cell = f"0 wins, 0 losses, {pushes} pushes"
    mean_brier = _mean(briers)
    mean_log = _mean(logs)
    brier_floor = "0.250000" if briers else "n/a"
    if model_briers:
        model_cell = f"{_prob(_mean(model_briers))} (n={len(model_briers)})"
    else:
        model_cell = "n=0"
    if kellys:
        kelly_cell = (
            f"n={len(kellys)}, min {_prob(min(kellys))}, max {_prob(max(kellys))}. Not staked."
        )
    else:
        kelly_cell = "n=0. Not staked."
    pl_cell = f"{_money(net)} on {_money(risked)}" if graded else "n/a"
    lines = [
        f"# {slate} scorecard",
        "",
        "Paper only. This scorecard does not submit an order. It does not support an edge claim.",
        "Flat $20. Realized P/L uses the logged American price via `paper_grade.settle` "
        "(win profit half-up to the cent). `fee_used` is the venue taker snapshot stored beside that P/L. "
        "`ev_usd` is the expectation under `p_market`.",
        "At -110, break-even hit rate is 110/210, about 52.38%.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | --- |",
        f"| n | {n} |",
        f"| Week | {week} |",
        f"| Completeness | {completeness} |",
        f"| Contract mismatches | {mismatches} |",
        f"| Mean CLV | {clv_cell} |",
        f"| Market Brier | {_prob(mean_brier) if mean_brier is not None else 'n/a'} |",
        f"| Brier, constant 0.5 | {brier_floor} |",
        f"| Model Brier | {model_cell} |",
        f"| Log loss | {_prob(mean_log) if mean_log is not None else 'n/a'} |",
        f"| Hit rate | {hit_cell} |",
        f"| Paper P/L | {pl_cell} |",
        f"| Shadow quarter-Kelly | {kelly_cell} |",
        "",
        "CLV = devigged close probability of the side minus `p_market`. "
        "Positive means the ticket beat the close. A missing close is the status "
        "`close missing`, and that row is left out of the mean.",
        "",
        "A row is complete when it has a contract key, `p_market`, a fee method and "
        "`fee_used`, sources, and either a same-contract close or `close missing`.",
        "",
        "## Tickets",
        "",
        "| Ticket | Contract | Result | P/L | p_market | CLV | Brier | Close | Mismatch |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        contract = f"{row['market_type']} {row['side']} {row['line']} {row['period']}"
        pnl = _money(row["pnl"]) if row.get("pnl") is not None else ""
        lines.append(
            "| {ticket} | {contract} | {result} | {pnl} | {p} | {clv} | {brier} | {close} | {mismatch} |".format(
                ticket=row["ticket_id"],
                contract=contract,
                result=row.get("result") or "",
                pnl=pnl,
                p=_prob(row.get("p_market")),
                clv=_prob(row.get("clv")),
                brier=_prob(row.get("brier")),
                close=row.get("close_status") or "",
                mismatch="yes" if row.get("same_contract_mismatch") else "",
            )
        )
    lines.append("")
    return "\n".join(lines)


def dumps_row(row: dict) -> dict:
    payload = {}
    for key in COLUMNS:
        value = row.get(key)
        if isinstance(value, Decimal):
            payload[key] = format(value, "f")
        else:
            payload[key] = value
    return payload


def write_jsonl(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(dumps_row(row), ensure_ascii=True) + "\n" for row in rows)
    path.write_text(text, encoding="utf-8")


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(COLUMNS), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            payload = dumps_row(row)
            writer.writerow(
                {
                    key: ("true" if payload[key] else "false")
                    if isinstance(payload[key], bool)
                    else ("" if payload[key] is None else payload[key])
                    for key in COLUMNS
                }
            )


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        raw = json.loads(line)
        row = new_row()
        for key in COLUMNS:
            if key not in raw:
                continue
            value = raw[key]
            if value is None or value == "":
                row[key] = None if key in DECIMAL_FIELDS or key in INT_FIELDS else value
                if key in BOOL_FIELDS:
                    row[key] = False
                continue
            if key in DECIMAL_FIELDS:
                row[key] = Decimal(str(value))
            elif key in INT_FIELDS:
                row[key] = int(value)
            elif key in BOOL_FIELDS:
                row[key] = bool(value)
            else:
                row[key] = value
        rows.append(row)
    return rows


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_week(locks: Path, finals: Path | None, closes: Path | None, out: Path, csv_path: Path | None, scorecard: Path | None) -> str:
    rows = load_slate(locks)
    if finals is not None:
        apply_finals(rows, _load_json(finals))
    if closes is None:
        mark_closes_missing(rows)
    else:
        apply_closes(rows, _load_json(closes))
    write_jsonl(rows, out)
    if csv_path is not None:
        write_csv(rows, csv_path)
    text = render_scorecard(rows)
    if scorecard is not None:
        scorecard.parent.mkdir(parents=True, exist_ok=True)
        scorecard.write_text(text, encoding="utf-8")
    return text


def _cmd_ingest(args: argparse.Namespace) -> int:
    rows = load_slate(Path(args.locks))
    write_jsonl(rows, Path(args.out))
    if args.csv:
        write_csv(rows, Path(args.csv))
    print(render_scorecard(rows), end="")
    return 0


def _cmd_week(args: argparse.Namespace) -> int:
    text = run_week(
        Path(args.locks),
        Path(args.finals) if args.finals else None,
        Path(args.closes) if args.closes else None,
        Path(args.out),
        Path(args.csv) if args.csv else None,
        Path(args.scorecard) if args.scorecard else None,
    )
    print(text, end="")
    return 0


def _cmd_scorecard(args: argparse.Namespace) -> int:
    rows = read_jsonl(Path(args.log))
    text = render_scorecard(rows)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="NFL paper-log v1. Grades paper tickets. Does not submit orders."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="Write lock rows before the games. Does not grade or stamp a close")
    ingest.add_argument("--locks", required=True)
    ingest.add_argument("--out", required=True)
    ingest.add_argument("--csv")
    ingest.set_defaults(func=_cmd_ingest)

    week = sub.add_parser("week", help="Ingest locks, grade finals, stamp closes, write the scorecard")
    week.add_argument("--locks", required=True, help="Slate JSON of paper locks")
    week.add_argument("--finals", help="Finals JSON. Omit to leave tickets OPEN")
    week.add_argument("--closes", help="Same-contract close snapshot. Omit to stamp close missing")
    week.add_argument("--out", required=True, help="Derived JSONL path")
    week.add_argument("--csv", help="Optional CSV view of the same rows")
    week.add_argument("--scorecard", help="Optional markdown scorecard path")
    week.set_defaults(func=_cmd_week)

    card = sub.add_parser("scorecard", help="Print a scorecard from a derived JSONL log")
    card.add_argument("--log", required=True)
    card.add_argument("--out")
    card.set_defaults(func=_cmd_scorecard)
    return parser


def main(argv: list[str] | None = None) -> int:
    args_in = list(sys.argv[1:] if argv is None else argv)
    if any(flag in {"--submit", "--live", "--order"} for flag in args_in):
        print("nfl_paper_log does not submit orders.", file=sys.stderr)
        return 2
    parser = build_parser()
    args = parser.parse_args(args_in)
    try:
        return args.func(args)
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
