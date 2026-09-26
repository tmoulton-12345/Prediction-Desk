"""NFL Week 3 paper arb scan: Polymarket US vs Novig.

Public GET only. Prices and fees are computed here. Nothing is ordered.

Window: Sunday 2026-09-27 (14 games) and Monday 2026-09-28 PHI @ CHI.
Thursday night is outside the start window.
"""

from __future__ import annotations

import json
import sys
import time
import traceback
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fetch_novig_public import fetch_book as fetch_novig_book
from fetch_novig_public import fetch_events as fetch_novig_events
from fetch_novig_public import fetch_markets as fetch_novig_markets
from fetch_polymarket_us_public import fetch_market_book, fetch_nfl_events
from math_fees_arb import (
    edge_pct_of_payout,
    novig_taker_fee_per_dollar,
    pm_taker_fee_exact,
    pm_taker_fee_rounded,
    round_trip_cost,
)

ROOT = Path(__file__).resolve().parents[1]
PT = ZoneInfo("America/Los_Angeles")
ONE = Decimal("1")
HUNDRED = Decimal("100")
# Sunday 2026-09-27 00:00 EDT, exclusive lower bound on Novig startsTs.
STARTS_AFTER_MS = 1790481600000
# Tuesday 2026-09-29 02:00 EDT, exclusive upper bound. Covers Monday 8:15 p.m. ET.
STARTS_BEFORE_MS = 1790661600000
LIQUID_ML_CONTRACTS = Decimal("100")
PM_TYPES = {
    "football_team_full_game_spread": "spread",
    "football_team_full_game_total": "total",
    "football_team_full_game_winner": "moneyline",
}


def canon_abbr(raw: str) -> str:
    key = raw.strip().lower()
    return {"jac": "JAX", "jax": "JAX", "was": "WAS", "wsh": "WAS"}.get(key, key.upper())


def line_token(value: Decimal) -> str:
    return format(value.quantize(Decimal("0.1")), "f")


def money(value: Decimal) -> str:
    return format(value.quantize(Decimal("0.0001")), "f")


def pct(value: Decimal) -> str:
    return format(value.quantize(Decimal("0.001")), "f")


@dataclass
class Outcome:
    label: str
    team: str | None = None


@dataclass
class VenueMarket:
    venue: str
    kind: str
    game: frozenset[str]
    line: str | None
    key: tuple
    outcomes: dict[str, Outcome]
    ref: str
    title: str
    description: str
    fee_coefficient: Decimal
    fee_charged: str
    event_status: str
    voids: str | None
    long_label: str | None = None
    catalog_bid: Decimal | None = None
    catalog_ask: Decimal | None = None
    asks: dict[str, tuple[Decimal, Decimal]] = field(default_factory=dict)
    bids: dict[str, tuple[Decimal, Decimal]] = field(default_factory=dict)
    price_source: str = "unpriced"
    book_note: str = ""


def spread_key(pairs: set[tuple[str, str]], line: Decimal) -> tuple:
    return ("spread", tuple(sorted(pairs)), line_token(line))


def total_key(teams: frozenset[str], line: Decimal) -> tuple:
    return ("total", tuple(sorted(teams)), line_token(line))


def money_key(teams: frozenset[str]) -> tuple:
    return ("moneyline", tuple(sorted(teams)), None)


def parse_pm_market(event: dict, market: dict) -> VenueMarket | None:
    kind = PM_TYPES.get(market.get("sportsMarketType") or "")
    if kind is None or market.get("closed") or not market.get("active"):
        return None
    slug = market.get("slug") or ""
    if any(token in slug for token in ("-1h-", "-2h-", "-1q-", "-2q-", "-3q-", "-4q-", "-tt-")):
        return None
    parts = event["slug"].split("-")
    if len(parts) < 4:
        return None
    game = frozenset(canon_abbr(part) for part in parts[1:3])
    sides = market.get("marketSides") or []
    if len(sides) != 2:
        return None
    theta_raw = market.get("feeCoefficient")
    theta = Decimal(str(theta_raw)) if theta_raw is not None else None
    if theta is None:
        return None
    outcomes: dict[str, Outcome] = {}
    long_label = None
    if kind == "spread":
        pairs: set[tuple[str, str]] = set()
        line = None
        for side in sides:
            desc = side.get("description") or ""
            if not desc or desc[0] not in "+-":
                return None
            team = side.get("team") or {}
            abbr = canon_abbr(team.get("abbreviation") or "")
            if abbr not in game:
                return None
            number = Decimal(desc[1:])
            sign = desc[0]
            if line is None:
                line = number
            elif line != number:
                return None
            label = f"{abbr} {sign}{line_token(number)}"
            outcomes[label] = Outcome(label, abbr)
            pairs.add((abbr, sign))
            if side.get("long"):
                long_label = label
        if line is None or long_label is None or len(outcomes) != 2:
            return None
        key = spread_key(pairs, line)
        line_s = line_token(line)
    elif kind == "total":
        line = _line_from_slug(slug)
        if line is None and market.get("line") is not None:
            line = Decimal(str(market["line"]))
        if line is None:
            return None
        for side in sides:
            name = (side.get("description") or "").strip().lower()
            if name not in {"over", "under"}:
                return None
            label = f"{name.capitalize()} {line_token(line)}"
            outcomes[label] = Outcome(label, None)
            if side.get("long"):
                long_label = label
        if long_label is None or len(outcomes) != 2:
            return None
        key = total_key(game, line)
        line_s = line_token(line)
    else:
        for side in sides:
            team = side.get("team") or {}
            abbr = canon_abbr(team.get("abbreviation") or "")
            if abbr not in game:
                return None
            outcomes[abbr] = Outcome(abbr, abbr)
            if side.get("long"):
                long_label = abbr
        if long_label is None or len(outcomes) != 2:
            return None
        key = money_key(game)
        line_s = None
    bid = _quote(market.get("bestBidQuote"))
    ask = _quote(market.get("bestAskQuote"))
    return VenueMarket(
        venue="polymarket_us",
        kind=kind,
        game=game,
        line=line_s,
        key=key,
        outcomes=outcomes,
        ref=slug,
        title=market.get("title") or slug,
        description=market.get("description") or "",
        fee_coefficient=theta,
        fee_charged="ALWAYS",
        event_status="PREGAME",
        voids=None,
        long_label=long_label,
        catalog_bid=bid,
        catalog_ask=ask,
    )


def _line_from_slug(slug: str) -> Decimal | None:
    marker = None
    for token in slug.split("-"):
        if "pt" in token and token[0].isdigit():
            marker = token
    if marker is None or "pt" not in marker:
        return None
    whole, frac = marker.split("pt", 1)
    if not whole.isdigit() or not frac.isdigit():
        return None
    return Decimal(f"{whole}.{frac}")


def _quote(node: dict | None) -> Decimal | None:
    if not node or node.get("value") in (None, ""):
        return None
    return Decimal(str(node["value"]))


def parse_novig_market(market: dict, event_status: str, teams: frozenset[str]) -> VenueMarket | None:
    kind_raw = market.get("marketType")
    kind = {"SPREAD": "spread", "TOTAL": "total", "MONEY": "moneyline"}.get(kind_raw or "")
    if kind is None or market.get("status") != "OPEN":
        return None
    description = market.get("description") or ""
    lowered = description.lower()
    if any(token in lowered for token in ("1h", "2h", "q1", "q2", "q3", "q4", "half", "quarter")):
        return None
    fee = market.get("fee") or {}
    coefficient = Decimal(str(fee.get("coefficient")))
    charged = str(fee.get("charged") or "")
    outcomes_raw = market.get("outcomes") or []
    if len(outcomes_raw) != 2:
        return None
    outcomes: dict[str, Outcome] = {}
    if kind == "spread":
        pairs: set[tuple[str, str]] = set()
        line = None
        for outcome in outcomes_raw:
            name = outcome.get("name") or ""
            bits = name.split()
            if len(bits) != 2 or bits[1][0] not in "+-":
                return None
            abbr = canon_abbr(bits[0])
            number = Decimal(bits[1][1:])
            sign = bits[1][0]
            if line is None:
                line = number
            elif line != number:
                return None
            label = f"{abbr} {sign}{line_token(number)}"
            outcomes[label] = Outcome(label, abbr)
            pairs.add((abbr, sign))
        if line is None or teams != frozenset(abbr for abbr, _sign in pairs):
            return None
        key = spread_key(pairs, line)
        line_s = line_token(line)
    elif kind == "total":
        line = Decimal(str(market["strike"]))
        for outcome in outcomes_raw:
            name = outcome.get("name") or ""
            bits = name.split()
            if len(bits) != 2 or bits[0] not in {"Over", "Under"}:
                return None
            if Decimal(bits[1]) != line:
                return None
            label = f"{bits[0]} {line_token(line)}"
            outcomes[label] = Outcome(label, None)
        key = total_key(teams, line)
        line_s = line_token(line)
    else:
        for outcome in outcomes_raw:
            abbr = canon_abbr(outcome.get("name") or "")
            outcomes[abbr] = Outcome(abbr, abbr)
        if frozenset(outcomes) != teams:
            return None
        key = money_key(teams)
        line_s = None
    # Keep Novig outcome ids on the book note path via ref, and stash id map on title? 
    id_map = {outcome["name"]: outcome["outcomeId"] for outcome in outcomes_raw}
    listed = VenueMarket(
        venue="novig",
        kind=kind,
        game=teams,
        line=line_s,
        key=key,
        outcomes=outcomes,
        ref=market["marketId"],
        title=description,
        description=description,
        fee_coefficient=coefficient,
        fee_charged=charged,
        event_status=event_status,
        voids=market.get("voids"),
    )
    listed.book_note = json.dumps(id_map)
    return listed


def apply_novig_book(listed: VenueMarket, book: dict) -> None:
    id_map = json.loads(listed.book_note)
    label_by_id = {}
    for raw_name, outcome_id in id_map.items():
        label = _novig_raw_to_label(listed.kind, raw_name)
        label_by_id[outcome_id] = label
    best: dict[str, tuple[Decimal, int]] = {}
    for outcome_id, orders in (book.get("orders") or {}).items():
        label = label_by_id.get(outcome_id)
        if label is None:
            continue
        for order in orders or []:
            px = Decimal(str(order["price"]))
            qty = int(order["qty"])
            prev = best.get(label)
            if prev is None or px > prev[0]:
                best[label] = (px, qty)
            elif px == prev[0]:
                best[label] = (px, prev[1] + qty)
    labels = list(listed.outcomes)
    if len(labels) != 2:
        listed.price_source = "book_unusable"
        return
    left, right = labels
    if left in best and right in best and best[left][0] + best[right][0] >= ONE:
        listed.book_note = "crossed"
    else:
        listed.book_note = ""
    for label, (px, qty) in best.items():
        listed.bids[label] = (px, Decimal(qty) / HUNDRED)
    if right in best:
        px, qty = best[right]
        listed.asks[left] = (ONE - px, Decimal(qty) / HUNDRED)
    if left in best:
        px, qty = best[left]
        listed.asks[right] = (ONE - px, Decimal(qty) / HUNDRED)
    listed.price_source = "book"


def _novig_raw_to_label(kind: str, raw_name: str) -> str:
    if kind == "moneyline":
        return canon_abbr(raw_name)
    if kind == "total":
        side, number = raw_name.split()
        return f"{side} {line_token(Decimal(number))}"
    abbr, signed = raw_name.split()
    sign = signed[0]
    return f"{canon_abbr(abbr)} {sign}{line_token(Decimal(signed[1:]))}"


def apply_pm_book(listed: VenueMarket, book: dict) -> None:
    data = book.get("marketData") or {}
    bids = data.get("bids") or []
    offers = data.get("offers") or []
    best_bid = None
    best_ask = None
    if bids:
        top = max(bids, key=lambda row: Decimal(str(row["px"]["value"])))
        best_bid = (Decimal(str(top["px"]["value"])), Decimal(str(top["qty"])))
    if offers:
        top = min(offers, key=lambda row: Decimal(str(row["px"]["value"])))
        best_ask = (Decimal(str(top["px"]["value"])), Decimal(str(top["qty"])))
    if listed.long_label is None:
        listed.price_source = "book_unusable"
        return
    short_label = next(label for label in listed.outcomes if label != listed.long_label)
    if best_bid and best_ask and best_bid[0] >= best_ask[0]:
        listed.book_note = "crossed"
    if best_bid:
        listed.bids[listed.long_label] = best_bid
        listed.asks[short_label] = (ONE - best_bid[0], best_bid[1])
        listed.bids[short_label] = (ONE - best_ask[0], best_ask[1]) if best_ask else listed.bids.get(short_label, best_bid)
    if best_ask:
        listed.asks[listed.long_label] = best_ask
        if best_bid:
            listed.bids[short_label] = (ONE - best_ask[0], best_ask[1])
    listed.price_source = "book"


def apply_pm_catalog(listed: VenueMarket) -> None:
    if listed.long_label is None or listed.catalog_bid is None or listed.catalog_ask is None:
        return
    short_label = next(label for label in listed.outcomes if label != listed.long_label)
    listed.bids[listed.long_label] = (listed.catalog_bid, Decimal("0"))
    listed.asks[listed.long_label] = (listed.catalog_ask, Decimal("0"))
    listed.asks[short_label] = (ONE - listed.catalog_bid, Decimal("0"))
    listed.bids[short_label] = (ONE - listed.catalog_ask, Decimal("0"))
    listed.price_source = "catalog_bbo_no_size"


def fee_per_dollar(listed: VenueMarket, price: Decimal) -> Decimal:
    if listed.venue == "polymarket_us":
        return pm_taker_fee_exact(price, ONE, listed.fee_coefficient)
    return novig_taker_fee_per_dollar(
        price, listed.fee_coefficient, listed.fee_charged, listed.event_status
    )


def best_direction(pm: VenueMarket, nv: VenueMarket) -> dict | None:
    labels = list(pm.outcomes)
    if set(labels) != set(nv.outcomes):
        return None
    directions = []
    for bought in labels:
        other = next(label for label in labels if label != bought)
        pm_ask = pm.asks.get(bought)
        nv_ask = nv.asks.get(other)
        if pm_ask is None or nv_ask is None:
            continue
        pm_fee = fee_per_dollar(pm, pm_ask[0])
        nv_fee = fee_per_dollar(nv, nv_ask[0])
        cost = round_trip_cost(pm_ask[0], pm_fee, nv_ask[0], nv_fee)
        rounded_100 = pm_taker_fee_rounded(pm_ask[0], HUNDRED, pm.fee_coefficient)
        cost_100 = (
            pm_ask[0] * HUNDRED
            + rounded_100
            + nv_ask[0] * HUNDRED
            + nv_fee * HUNDRED
        )
        directions.append(
            {
                "pm_side": bought,
                "pm_ask": pm_ask[0],
                "pm_qty": pm_ask[1],
                "pm_fee": pm_fee,
                "novig_side": other,
                "novig_ask": nv_ask[0],
                "novig_qty": nv_ask[1],
                "novig_fee": nv_fee,
                "cost": cost,
                "edge_pct": edge_pct_of_payout(cost),
                "over_by": cost - ONE,
                "touch_qty": min(pm_ask[1], nv_ask[1]),
                "pm_fee_100_rounded": rounded_100,
                "cost_100": cost_100,
                "cost_100_per_contract": cost_100 / HUNDRED,
            }
        )
    if not directions:
        return None
    directions.sort(key=lambda row: (row["cost"], -row["touch_qty"]))
    return directions[0]


def ot_void_gate(pm: VenueMarket, nv: VenueMarket) -> dict:
    pm_ot = "Overtime is included" in pm.description
    nv_full_game = True
    ot_match = pm_ot and nv_full_game
    pm_void = (
        "two weeks" in pm.description
        and "last fair market price" in pm.description
    )
    nv_fmv = nv.voids == "FMV"
    void_match = False
    detail = (
        f"OT: Polymarket text {'includes overtime' if pm_ot else 'does not say overtime is included'}. "
        "Novig full-game spread, total, and winner contracts include overtime "
        "(Ludlow NFL spread, total, and winner anchors). "
        f"Void: Polymarket {'uses a two-week replay window then last fair market price' if pm_void else 'void sentence was not the two-week last-fair-price sentence'}. "
        f"Novig voids field is {nv.voids}. A Novig void on these contracts settles on the fair-value composite "
        "(30-minute window), and a regular-season game that does not start within 24 hours or resume within 48 hours voids. "
        "Those void prices and windows are not the same rule."
    )
    return {"pass": bool(ot_match and void_match), "detail": detail}


def settlement_gate(pm: VenueMarket, nv: VenueMarket) -> dict:
    pm_gov = "governing body" in pm.description or "sourced from NFL" in pm.description
    detail = (
        "Primary grade on a completed game is the NFL official result on both: "
        "Polymarket US says the outcome is sourced from the relevant governing body, "
        "and the Novig NFL anchors name the NFL as source agency. "
        "Fallback ladders are not identical. Polymarket US may use one wire service. "
        "Novig's fourth step asks for two independent sources. "
        f"Polymarket description names a governing-body source: {pm_gov}. Novig voids field {nv.voids} is not the grade source."
    )
    return {"pass": bool(pm_gov), "detail": detail}


def gates_for(pm: VenueMarket, nv: VenueMarket, direction: dict) -> dict:
    same_event = pm.game == nv.game
    same_line = pm.key == nv.key
    return {
        "same_event": {
            "pass": same_event,
            "detail": f"Teams {sorted(pm.game)} on both venues." if same_event else "Team sets differ.",
        },
        "same_line": {
            "pass": same_line,
            "detail": f"{pm.kind} key {pm.key[2] if pm.line else 'winner'} sides {direction['pm_side']} vs {direction['novig_side']}.",
        },
        "ot_void": ot_void_gate(pm, nv),
        "settlement_source": settlement_gate(pm, nv),
    }


def all_pass(gates: dict) -> bool:
    return all(item["pass"] for item in gates.values())


def mid_distance(listed: VenueMarket) -> tuple[Decimal, Decimal, Decimal] | None:
    labels = list(listed.outcomes)
    if not labels:
        return None
    label = listed.long_label or labels[0]
    bid = listed.bids.get(label)
    ask = listed.asks.get(label)
    if bid is None or ask is None:
        return None
    mid = (bid[0] + ask[0]) / 2
    size = min(bid[1], ask[1])
    return (abs(mid - Decimal("0.5")), ask[0] - bid[0], -size)


def pick_main(markets: list[VenueMarket]) -> VenueMarket | None:
    ranked = []
    for market in markets:
        score = mid_distance(market)
        if score is None:
            continue
        ranked.append((score, market))
    if not ranked:
        return None
    ranked.sort(key=lambda item: item[0])
    return ranked[0][1]


def game_label(teams: frozenset[str], novig_events: dict[frozenset[str], dict]) -> str:
    event = novig_events.get(teams)
    if event:
        return event["description"].replace(" @ ", " @ ")
    return " / ".join(sorted(teams))


def kickoff_pt(teams: frozenset[str], novig_events: dict[frozenset[str], dict]) -> str:
    event = novig_events.get(teams)
    if not event:
        return ""
    moment = datetime.fromtimestamp(event["startsTs"] / 1000, tz=timezone.utc).astimezone(PT)
    return moment.strftime("%Y-%m-%d %I:%M %p PT").replace(" 0", " ")


def row_public(direction: dict, pm: VenueMarket, nv: VenueMarket, gates: dict) -> dict:
    def dec(value: Decimal) -> str:
        return format(value, "f")

    return {
        "game": sorted(pm.game),
        "kind": pm.kind,
        "line": pm.line,
        "pm_market": pm.ref,
        "pm_side": direction["pm_side"],
        "pm_ask": dec(direction["pm_ask"]),
        "pm_fee_per_contract": dec(direction["pm_fee"]),
        "pm_touch_qty": dec(direction["pm_qty"]),
        "pm_price_source": pm.price_source,
        "novig_market": nv.ref,
        "novig_side": direction["novig_side"],
        "novig_ask": dec(direction["novig_ask"]),
        "novig_fee_per_contract": dec(direction["novig_fee"]),
        "novig_touch_qty_dollar_contracts": dec(direction["novig_qty"]),
        "novig_price_source": nv.price_source,
        "round_trip_cost": dec(direction["cost"]),
        "over_1_by": dec(direction["over_by"]),
        "edge_pct_of_payout": dec(direction["edge_pct"]),
        "touch_qty_dollar_contracts": dec(direction["touch_qty"]),
        "pm_bankers_fee_on_100": dec(direction["pm_fee_100_rounded"]),
        "round_trip_per_contract_after_pm_cent_round_on_100": dec(direction["cost_100_per_contract"]),
        "book_flags": [note for note in (pm.book_note, nv.book_note) if note],
        "gates": gates,
        "true_arb": all_pass(gates) and direction["cost"] < ONE and direction["touch_qty"] > 0,
    }


def main() -> None:
    stamped = datetime.now(PT)
    stamp = stamped.strftime("%Y%m%d-%H%M")
    print(f"stamp {stamp} PT", flush=True)
    pm_payload = fetch_nfl_events()
    nv_events_payload = fetch_novig_events("NFL", STARTS_AFTER_MS, STARTS_BEFORE_MS)
    nv_markets_payload = fetch_novig_markets(
        "NFL", "SPREAD,TOTAL,MONEY", STARTS_AFTER_MS, STARTS_BEFORE_MS
    )

    pm_markets: list[VenueMarket] = []
    pm_games = []
    for event in pm_payload.get("events") or []:
        slug = event.get("slug") or ""
        if "2026-09-27" not in slug and "2026-09-28" not in slug:
            continue
        pm_games.append(slug)
        for market in event.get("markets") or []:
            parsed = parse_pm_market(event, market)
            if parsed:
                pm_markets.append(parsed)

    status_by_event = {event["eventId"]: event for event in nv_events_payload.get("items") or []}
    teams_by_event: dict[str, frozenset[str]] = {}
    novig_events_by_game: dict[frozenset[str], dict] = {}
    for market in nv_markets_payload.get("items") or []:
        if market.get("marketType") != "MONEY":
            continue
        teams = frozenset(canon_abbr(outcome["name"]) for outcome in market["outcomes"])
        teams_by_event[market["eventId"]] = teams
        event = status_by_event.get(market["eventId"])
        if event and " @ " in (event.get("description") or ""):
            novig_events_by_game[teams] = event

    nv_markets: list[VenueMarket] = []
    for market in nv_markets_payload.get("items") or []:
        teams = teams_by_event.get(market["eventId"])
        event = status_by_event.get(market["eventId"])
        if teams is None or event is None or " @ " not in (event.get("description") or ""):
            continue
        parsed = parse_novig_market(market, event["status"], teams)
        if parsed:
            nv_markets.append(parsed)

    print(f"pm markets {len(pm_markets)} novig markets {len(nv_markets)}", flush=True)
    for index, listed in enumerate(nv_markets, start=1):
        if index == 1 or index % 100 == 0:
            print(f"novig book {index}/{len(nv_markets)}", flush=True)
        try:
            apply_novig_book(listed, fetch_novig_book(listed.ref))
        except Exception as exc:  # noqa: BLE001 — keep the scan, record the miss
            listed.price_source = f"book_error: {exc}"

    by_key_pm: dict[tuple, VenueMarket] = {}
    by_key_nv: dict[tuple, list[VenueMarket]] = defaultdict(list)
    for listed in pm_markets:
        by_key_pm[listed.key] = listed
    for listed in nv_markets:
        by_key_nv[listed.key].append(listed)

    slugs_needed = []
    for key, pm in by_key_pm.items():
        if key in by_key_nv:
            slugs_needed.append(pm)
    pm_mains_preview: dict[tuple[frozenset[str], str], VenueMarket | None] = {}
    pm_by_game: dict[frozenset[str], dict[str, list[VenueMarket]]] = defaultdict(lambda: defaultdict(list))
    for listed in pm_markets:
        apply_pm_catalog(listed)
        pm_by_game[listed.game][listed.kind].append(listed)
    for game, kinds in pm_by_game.items():
        for kind, rows in kinds.items():
            pm_mains_preview[(game, kind)] = pick_main(rows)
            chosen = pm_mains_preview[(game, kind)]
            if chosen and chosen not in slugs_needed:
                slugs_needed.append(chosen)

    seen_slugs = set()
    unique_pm = []
    for listed in slugs_needed:
        if listed.ref in seen_slugs:
            continue
        seen_slugs.add(listed.ref)
        unique_pm.append(listed)
    print(f"pm books {len(unique_pm)}", flush=True)
    for index, listed in enumerate(unique_pm, start=1):
        if index == 1 or index % 50 == 0:
            print(f"pm book {index}/{len(unique_pm)}", flush=True)
        time.sleep(0.08)
        try:
            apply_pm_book(listed, fetch_market_book(listed.ref))
        except Exception as exc:  # noqa: BLE001
            listed.price_source = f"book_error: {exc}; kept catalog" if listed.asks else f"book_error: {exc}"
            if not listed.asks:
                apply_pm_catalog(listed)

    pairs = []
    no_touch = 0
    for key, pm in by_key_pm.items():
        for nv in by_key_nv.get(key, []):
            direction = best_direction(pm, nv)
            if direction is None or direction["touch_qty"] <= 0:
                no_touch += 1
                continue
            if pm.kind == "moneyline" and direction["touch_qty"] < LIQUID_ML_CONTRACTS:
                no_touch += 1
                continue
            gate = gates_for(pm, nv, direction)
            pairs.append((pm, nv, direction, gate))

    true_arbs = []
    price_locks = []
    overs = []
    for pm, nv, direction, gate in pairs:
        public = row_public(direction, pm, nv, gate)
        if public["true_arb"]:
            true_arbs.append(public)
        elif direction["cost"] < ONE:
            price_locks.append(public)
        else:
            overs.append(public)
    true_arbs.sort(key=lambda row: Decimal(row["edge_pct_of_payout"]), reverse=True)
    price_locks.sort(key=lambda row: Decimal(row["over_1_by"]))
    overs.sort(key=lambda row: Decimal(row["over_1_by"]))
    near = overs[:10]
    liquid = [row for row in overs if Decimal(row["touch_qty_dollar_contracts"]) >= LIQUID_ML_CONTRACTS][:8]
    pulled = datetime.now(PT)

    games = []
    line_shop = []
    for teams, event in sorted(novig_events_by_game.items(), key=lambda item: item[1]["startsTs"]):
        entry = {
            "game": event["description"],
            "kickoff_pt": kickoff_pt(teams, novig_events_by_game),
            "event_status": event["status"],
            "markets": {},
        }
        for kind in ("spread", "total", "moneyline"):
            pm_main = pick_main(pm_by_game[teams][kind])
            nv_main = pick_main([row for row in nv_markets if row.game == teams and row.kind == kind])
            pm_line = pm_main.line if pm_main else None
            nv_line = nv_main.line if nv_main else None
            same = pm_main is not None and nv_main is not None and pm_main.key == nv_main.key
            entry["markets"][kind] = {
                "pm_main_line": pm_line,
                "pm_main_ref": pm_main.ref if pm_main else None,
                "pm_main_title": pm_main.title if pm_main else None,
                "novig_main_line": nv_line,
                "novig_main_ref": nv_main.ref if nv_main else None,
                "novig_main_title": nv_main.title if nv_main else None,
                "mains_same_line": same,
            }
            if pm_main and nv_main and not same and kind != "moneyline":
                line_shop.append(
                    {
                        "game": event["description"],
                        "kind": kind,
                        "pm_line": pm_line,
                        "pm_title": pm_main.title,
                        "pm_ref": pm_main.ref,
                        "novig_line": nv_line,
                        "novig_title": nv_main.title,
                        "novig_ref": nv_main.ref,
                        "note": "Different lines. Not an arb.",
                    }
                )
        closest = [
            row
            for row in overs + price_locks + true_arbs
            if frozenset(row["game"]) == teams
        ]
        closest.sort(key=lambda row: abs(Decimal(row["over_1_by"])))
        entry["closest_same_line"] = closest[0] if closest else None
        games.append(entry)

    fee_pm = sorted({str(row.fee_coefficient) for row in pm_markets})
    fee_nv = sorted({f"{row.fee_coefficient}|{row.fee_charged}|{row.event_status}" for row in nv_markets})
    file_stamp = stamp
    result = {
        "file_stamp": file_stamp,
        "stamped_pt": stamped.strftime("%Y-%m-%d %H:%M %Z"),
        "pull_finished_pt": pulled.strftime("%Y-%m-%d %H:%M %Z"),
        "arb": bool(true_arbs),
        "true_arb_count": len(true_arbs),
        "games_scanned": len(games),
        "pm_game_slugs": sorted(pm_games),
        "same_line_pairs_priced": len(pairs),
        "same_line_pairs_no_executable_touch_or_thin_moneyline": no_touch,
        "fees": {
            "polymarket_us_taker_theta_seen": fee_pm,
            "polymarket_us_formula": "theta * contracts * p * (1 - p), exact per contract; order fee rounded half-even to the cent",
            "polymarket_us_rebate": "none assumed",
            "novig_fee_seen": fee_nv,
            "novig_formula": "c * p * (1 - p) per $1 contract when charging; WHEN_LIVE is 0 while status is not OPEN_INGAME",
            "novig_qty_unit": "book qty is 1-cent contracts; dollar contracts = qty / 100",
            "sides": "taker on both venues (lift the offer). Maker rebates are not credited.",
        },
        "liquidity_rule": {
            "spreads_totals": "priced at the touch; size is a caveat, not a gate",
            "moneyline_min_dollar_contracts_at_touch": str(LIQUID_ML_CONTRACTS),
        },
        "true_arbs": true_arbs,
        "price_locks_failed_gate": price_locks[:20],
        "near_misses": near,
        "near_misses_min_touch_100": liquid,
        "line_shop": line_shop,
        "games": games,
        "sources": {
            "polymarket_us_events": "https://gateway.polymarket.us/v2/leagues/nfl/events",
            "polymarket_us_book": "https://gateway.polymarket.us/v1/markets/{slug}/book",
            "polymarket_us_fees": "https://docs.polymarket.us/fees",
            "polymarket_us_sports_faq": "https://docs.polymarket.us/faqs/sports-faqs",
            "novig_events": "https://api.novig.us/v3/public/catalog/events",
            "novig_markets": "https://api.novig.us/v3/public/catalog/markets",
            "novig_book": "https://api.novig.us/v3/public/catalog/markets/{id}/book",
            "novig_fees": "https://docs.novig.com/api/concepts/fees",
            "novig_nfl_spread_anchor": "https://ludlow-filings.s3.us-east-1.amazonaws.com/NFL-spread-anchor-cl-a.pdf",
            "novig_nfl_total_anchor": "https://ludlow-filings.s3.us-east-1.amazonaws.com/NFL-total-anchor-cl-a.pdf",
            "novig_nfl_winner_anchor": "https://ludlow-filings.s3.us-east-1.amazonaws.com/nfl-winner-anchor-cl-a.pdf",
        },
    }

    research = ROOT / "research"
    snapshots = ROOT / "snapshots"
    research.mkdir(exist_ok=True)
    snapshots.mkdir(exist_ok=True)
    md_path = research / f"{stamp}-pt-nfl-week3-pm-novig-arb-scan.md"
    json_path = research / f"{stamp}-pt-nfl-week3-pm-novig-arb-scan.json"
    snap_path = snapshots / f"{stamp}-pt-nfl-week3-books.json"
    md_path.write_text(render_markdown(result, snap_path.relative_to(ROOT).as_posix()))
    json_path.write_text(json.dumps(result, indent=2) + "\n")
    snap_path.write_text(json.dumps(snapshot(result, pm_markets, nv_markets), indent=2) + "\n")
    print(f"wrote {md_path}")
    print(f"true_arb_count {result['true_arb_count']} pairs {result['same_line_pairs_priced']}")


def snapshot(result: dict, pm_markets: list[VenueMarket], nv_markets: list[VenueMarket]) -> dict:
    def touch(listed: VenueMarket) -> dict:
        return {
            "venue": listed.venue,
            "ref": listed.ref,
            "kind": listed.kind,
            "game": sorted(listed.game),
            "line": listed.line,
            "title": listed.title,
            "price_source": listed.price_source,
            "book_note": listed.book_note,
            "asks": {label: [format(px, "f"), format(qty, "f")] for label, (px, qty) in listed.asks.items()},
            "bids": {label: [format(px, "f"), format(qty, "f")] for label, (px, qty) in listed.bids.items()},
            "fee_coefficient": str(listed.fee_coefficient),
            "fee_charged": listed.fee_charged,
            "event_status": listed.event_status,
            "voids": listed.voids,
        }

    return {
        "stamped_pt": result["stamped_pt"],
        "note": "Top of book used for the scan. Novig qty in this file is already dollar contracts (raw qty / 100).",
        "polymarket_us": [
            touch(row)
            for row in pm_markets
            if row.price_source == "book" or row.price_source.startswith("book_error")
        ],
        "novig": [touch(row) for row in nv_markets],
    }


def render_markdown(result: dict, snap_rel: str) -> str:
    yes = "yes" if result["arb"] else "no"
    lines = [
        "# NFL Week 3 Polymarket US vs Novig arb scan",
        "",
        f"**Stamped:** {result['stamped_pt']} (catalog pull). Order books were read in that same run and written at {result['pull_finished_pt']}.",
        "**Phase 0.** Public reads only. No order was placed, queued, or submitted.",
        "",
        "## Tim",
        "",
        f"- Arb: **{yes}**",
        f"- True arb count: **{result['true_arb_count']}**",
        f"- Games scanned: **{result['games_scanned']}** (Sunday Sep 27 plus Monday PHI @ CHI). TNF not in the window.",
        f"- Same-line pairs with an executable touch: **{result['same_line_pairs_priced']}**",
        f"- Report: `research/{result['file_stamp']}-pt-nfl-week3-pm-novig-arb-scan.md`",
        f"- JSON: `research/{result['file_stamp']}-pt-nfl-week3-pm-novig-arb-scan.json`",
        f"- Books snapshot: `{snap_rel}`",
        "",
        "## Fees assumed",
        "",
        f"- Polymarket US taker theta on these markets: {', '.join(result['fees']['polymarket_us_taker_theta_seen'])}.",
        "- Formula: theta × contracts × p × (1 − p). The scan uses the exact per-contract fee. A 100-contract order is also shown after Polymarket's half-even cent rounding. No volume rebate.",
        f"- Novig fee rows seen (coefficient | when it charges | event status): {', '.join(result['fees']['novig_fee_seen'])}.",
        "- Novig WHEN_LIVE is $0 on a pregame take. A live take would use coefficient × p × (1 − p) per $1 contract. Maker credit is not subtracted.",
        "- Both legs are priced as takes: Polymarket offer, or one minus the best bid for the short side; Novig ask = 1 − best bid on the other outcome.",
        "- Novig book qty is a 1-cent contract. Dollar contracts in this report are qty / 100.",
        "- Tables below are rounded to four decimal places. The JSON file keeps the exact fee.",
        f"- Moneyline is included only when the touch on the priced direction is at least {result['liquidity_rule']['moneyline_min_dollar_contracts_at_touch']} dollar contracts on each venue. Spreads and totals are priced at the touch with size as a caveat.",
        "",
        "## Gates",
        "",
        "A true arb needs every gate to pass and a fee-adjusted round trip under $1.",
        "",
        "- Same event: same two teams.",
        "- Same line: same signed spread, or the same total, or the same winner market. The other direction of a spread (BUF −7.5 versus BUF +7.5) is a different contract.",
        "- OT / void: full-game overtime matches. The void window does not. Polymarket US market text uses two weeks, then last fair market price. Novig regular-season anchors use 24 hours to start and 48 hours to resume, then a fair-value composite (`voids=FMV`). That gate fails on these listings.",
        "- Settlement source: both use the NFL official result as the primary grade. Fallback ladders differ. That gate passes on the primary source.",
        "",
        "## Games",
        "",
        "| Game | Kickoff (PT) | PM main spread | Novig main spread | Mains match | PM main total | Novig main total | Totals match |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for game in result["games"]:
        spread = game["markets"]["spread"]
        total = game["markets"]["total"]
        lines.append(
            "| {game} | {kick} | {ps} | {ns} | {sm} | {pt} | {nt} | {tm} |".format(
                game=game["game"],
                kick=game["kickoff_pt"],
                ps=spread["pm_main_line"] or "—",
                ns=spread["novig_main_line"] or "—",
                sm="yes" if spread["mains_same_line"] else "no",
                pt=total["pm_main_line"] or "—",
                nt=total["novig_main_line"] or "—",
                tm="yes" if total["mains_same_line"] else "no",
            )
        )
    lines.extend(["", "## True arbs", ""])
    if not result["true_arbs"]:
        lines.append("None. No same-line pair cleared every gate with a round trip under $1.")
    else:
        for row in result["true_arbs"]:
            lines.extend(_hit_block(row))
    lines.extend(["", "## Price sums under $1 that still fail a gate", ""])
    if not result["price_locks_failed_gate"]:
        lines.append("None. No same-line touch was under $1 after fees.")
    else:
        lines.append("These are not true arbs. The void gate fails, so the payout is not locked if the game is postponed or cut short.")
        lines.append("")
        for row in result["price_locks_failed_gate"]:
            lines.extend(_hit_block(row))
    lines.extend(["", "## Nearest same-line misses", ""])
    lines.append(
        "Round trip after the fees above, minus $1. Smaller is closer. Different lines are not in this list. "
        "Every row fails the OT/void gate, so a sum under $1 would still not be a true arb."
    )
    lines.append("")
    if not result["near_misses"]:
        lines.append("No same-line pair had two executable asks.")
    else:
        lines.append("| Game | Market | PM side @ ask | PM fee | Novig side @ ask | Novig fee | Sum | Over $1 by | Edge % of $1 | Touch $ contracts |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for row in result["near_misses"]:
            lines.append(_miss_row(row))
    lines.extend(["", "## Nearest misses with at least 100 dollar contracts at the touch", ""])
    lines.append("Same rule as the table above. The size floor drops one-lot quotes.")
    lines.append("")
    liquid_rows = result.get("near_misses_min_touch_100") or []
    if not liquid_rows:
        lines.append("No same-line touch had 100 dollar contracts on both asks.")
    else:
        lines.append("| Game | Market | PM side @ ask | PM fee | Novig side @ ask | Novig fee | Sum | Over $1 by | Edge % of $1 | Touch $ contracts |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for row in liquid_rows:
            lines.append(_miss_row(row))
    lines.extend(["", "## Line shop only", ""])
    lines.append("Each venue's main line is the full-game listing whose touch midpoint is closest to 50 cents. A mismatch is not an arb.")
    lines.append("")
    if not result["line_shop"]:
        lines.append("Main spreads and main totals matched on every game.")
    else:
        lines.append("| Game | Kind | Polymarket main | Novig main |")
        lines.append("| --- | --- | --- | --- |")
        for row in result["line_shop"]:
            lines.append(
                f"| {row['game']} | {row['kind']} | {row['pm_line']} ({row['pm_title']}) | {row['novig_line']} ({row['novig_title']}) |"
            )
    lines.extend(
        [
            "",
            "## Closest same-line pair on each game",
            "",
            "| Game | Kind | Line | Sum | Over $1 by | Touch $ contracts |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for game in result["games"]:
        row = game["closest_same_line"]
        if not row:
            lines.append(f"| {game['game']} | — | — | — | — | — |")
            continue
        lines.append(
            f"| {game['game']} | {row['kind']} | {row['line'] or 'ML'} | {_d(row['round_trip_cost'])} | {_d(row['over_1_by'])} | {_qty(row['touch_qty_dollar_contracts'])} |"
        )
    lines.extend(
        [
            "",
            "## What this scan did not do",
            "",
            "- No Kalshi. No international Polymarket. No live order, no queued order, no retry of an order.",
            "- No paper-pick card. This file is the cross-venue scan only.",
            "- Prices are the touch at pull time. They are not a sweep of the book and not a promise the size is still there.",
            "",
            "## Sources",
            "",
        ]
    )
    for name, url in result["sources"].items():
        lines.append(f"- {name}: {url}")
    lines.append("")
    return "\n".join(lines)


def _d(value: str, places: str = "0.0001") -> str:
    return format(Decimal(value).quantize(Decimal(places)), "f")


def _qty(value: str) -> str:
    text = format(Decimal(value).quantize(Decimal("0.01")), "f")
    if text.endswith(".00"):
        return text[:-3]
    return text.rstrip("0").rstrip(".") if "." in text else text


def _miss_row(row: dict) -> str:
    return "| {teams} | {kind} {line} | {ps} @ {pa} | {pf} | {ns} @ {na} | {nf} | {cost} | {over} | {edge} | {qty} |".format(
        teams=" / ".join(row["game"]),
        kind=row["kind"],
        line=row["line"] or "ML",
        ps=row["pm_side"],
        pa=_d(row["pm_ask"]),
        pf=_d(row["pm_fee_per_contract"]),
        ns=row["novig_side"],
        na=_d(row["novig_ask"]),
        nf=_d(row["novig_fee_per_contract"]),
        cost=_d(row["round_trip_cost"]),
        over=_d(row["over_1_by"]),
        edge=_d(row["edge_pct_of_payout"], "0.001"),
        qty=_qty(row["touch_qty_dollar_contracts"]),
    )


def _hit_block(row: dict) -> list[str]:
    teams = " / ".join(row["game"])
    gates = ", ".join(
        f"{name} {'PASS' if item['pass'] else 'FAIL'}" for name, item in row["gates"].items()
    )
    return [
        f"### {teams} {row['kind']} {row['line'] or 'winner'}",
        "",
        f"- Polymarket US: buy {row['pm_side']} at {_d(row['pm_ask'])}, fee {_d(row['pm_fee_per_contract'])} per contract, touch qty {_qty(row['pm_touch_qty'])} ({row['pm_market']}).",
        f"- Novig: buy {row['novig_side']} at {_d(row['novig_ask'])}, fee {_d(row['novig_fee_per_contract'])} per contract, touch {_qty(row['novig_touch_qty_dollar_contracts'])} dollar contracts ({row['novig_market']}).",
        f"- Round trip {_d(row['round_trip_cost'])}. Over $1 by {_d(row['over_1_by'])}. Edge {_d(row['edge_pct_of_payout'], '0.001')}% of the $1 payout.",
        f"- 100-contract Polymarket fee after cent rounding: {_d(row['pm_bankers_fee_on_100'], '0.01')}. Per-contract round trip on that order: {_d(row['round_trip_per_contract_after_pm_cent_round_on_100'])}.",
        f"- Size caveat: locked size at the touch is {_qty(row['touch_qty_dollar_contracts'])} dollar contracts, the smaller quote.",
        f"- Gates: {gates}.",
        "",
    ]


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
