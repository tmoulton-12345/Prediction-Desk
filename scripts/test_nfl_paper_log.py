"""NFL paper-log v1 tests. No network. No order placement."""

from __future__ import annotations

import csv
import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from math_fees_arb import (
    NOVIG_STRAIGHT_LIVE_COEFF,
    PM_TAKER_THETA_DEFAULT,
    novig_taker_fee_per_dollar,
    pm_taker_fee_rounded,
)
from nfl_paper_log import (
    COLUMNS,
    apply_closes,
    apply_finals,
    build_row,
    contract_key,
    is_complete,
    load_slate,
    main,
    read_jsonl,
    render_scorecard,
    run_week,
)

ROOT = Path(__file__).resolve().parents[1]
LOCKS = ROOT / "fixtures" / "nfl" / "week3-top5-locks.json"
FINALS = ROOT / "fixtures" / "nfl" / "week3-top5-finals.json"

REQUIRED = (
    "sport",
    "week",
    "event",
    "kick_time_pt",
    "market_type",
    "side",
    "line",
    "period",
    "venue",
    "american_odds",
    "stake",
    "open_price",
    "close_price",
    "p_market",
    "fee_method",
    "fee_used",
    "same_contract_key",
    "same_contract_mismatch",
    "hit",
    "pnl",
    "clv",
    "brier",
    "log_loss",
    "settlement_notes",
    "decision_time",
)


def slate_defaults() -> dict:
    return {
        "sport": "NFL",
        "week": 3,
        "decision_time": "2026-09-25T21:46:00-07:00",
        "venue": "paper_ledger",
        "american_odds": -110,
        "stake": "20",
        "slate": "unit",
    }


def lock(**overrides) -> dict:
    base = {
        "ticket_id": "T1",
        "event": "SEA @ WAS",
        "market_type": "spread",
        "side": "SEA",
        "line": "-7.5",
        "period": "FG",
        "kick_time_pt": "2026-09-27T10:00:00-07:00",
        "sources": "https://example.test/source",
    }
    base.update(overrides)
    return base


def final_game(**overrides) -> dict:
    game = {
        "event": "SEA @ WAS",
        "away": "SEA",
        "home": "WAS",
        "away_score": 31,
        "home_score": 33,
        "status": "STATUS_FINAL",
        "overtime": False,
        "source": "https://www.espn.com/nfl/boxscore/_/gameId/401872955",
    }
    game.update(overrides)
    return game


class SchemaTests(unittest.TestCase):
    def test_columns_cover_the_canonical_fields(self):
        for name in REQUIRED:
            self.assertIn(name, COLUMNS)

    def test_built_row_has_every_column(self):
        row = build_row(lock(), slate_defaults())
        self.assertEqual(set(row), set(COLUMNS))
        self.assertEqual(row["schema_version"], "nfl-paper-log-v1")
        self.assertEqual(row["stake"], Decimal("20"))
        self.assertEqual(row["size_paper"], Decimal("20"))
        self.assertEqual(row["price"], row["open_price"])
        self.assertEqual(row["ts"], row["decision_time"])


class ScopeTests(unittest.TestCase):
    def test_non_nfl_is_rejected(self):
        with self.assertRaises(ValueError) as caught:
            build_row(lock(sport="CBB"), slate_defaults())
        self.assertIn("NFL", str(caught.exception))
        with self.assertRaises(ValueError):
            build_row(lock(sport="MLB"), slate_defaults())

    def test_stake_other_than_20_is_rejected(self):
        with self.assertRaises(ValueError):
            build_row(lock(stake="25"), slate_defaults())

    def test_kalshi_is_rejected(self):
        with self.assertRaises(ValueError):
            build_row(lock(venue="kalshi"), slate_defaults())

    def test_moneyline_needs_the_other_side(self):
        with self.assertRaises(ValueError):
            build_row(lock(market_type="ml", side="SEA", line=None), slate_defaults())

    def test_submit_flag_does_not_run(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["--submit"]), 2)
            self.assertEqual(main(["week", "--submit"]), 2)


class ContractTests(unittest.TestCase):
    def test_half_point_and_integer_are_different_contracts(self):
        row = build_row(
            lock(compare={"market_type": "spread", "side": "SEA", "line": "-8", "period": "FG"}),
            slate_defaults(),
        )
        self.assertTrue(row["same_contract_mismatch"])
        self.assertIn("line=-7.5", row["same_contract_key"])
        self.assertNotIn("line=-8", row["same_contract_key"])
        other = contract_key(
            sport="NFL",
            week=3,
            event="SEA @ WAS",
            market_type="spread",
            side="SEA",
            line="-8",
            period="FG",
        )
        self.assertNotEqual(row["same_contract_key"], other)

    def test_same_line_is_not_a_mismatch(self):
        row = build_row(
            lock(compare={"market_type": "spread", "side": "SEA", "line": "-7.5", "period": "FG"}),
            slate_defaults(),
        )
        self.assertFalse(row["same_contract_mismatch"])

    def test_mismatched_close_is_not_used(self):
        row = build_row(lock(), slate_defaults())
        apply_closes(
            [row],
            {
                "closes": [
                    {
                        "ticket_id": "T1",
                        "market_type": "spread",
                        "side": "SEA",
                        "line": "-8",
                        "period": "FG",
                        "close_american": -120,
                        "close_american_other": -110,
                    }
                ]
            },
        )
        self.assertTrue(row["same_contract_mismatch"])
        self.assertEqual(row["close_status"], "close missing")
        self.assertIsNone(row["clv"])
        self.assertIsNone(row["close_price"])


class PriceTests(unittest.TestCase):
    def test_polymarket_fee_uses_the_documented_theta(self):
        row = build_row(lock(venue="polymarket_us"), slate_defaults())
        contracts = row["stake"] / row["open_price"]
        expected = pm_taker_fee_rounded(row["open_price"], contracts, PM_TAKER_THETA_DEFAULT)
        self.assertEqual(row["fee_method"], "polymarket_us_taker_v20260925")
        self.assertEqual(row["fee_coeff"], Decimal("0.0695"))
        self.assertEqual(row["fee_used"], expected)
        self.assertEqual(row["fee_assumed"], expected)
        self.assertIn("0.0695", row["fee_notes"])

    def test_novig_pregame_straight_fee_is_zero(self):
        row = build_row(lock(venue="novig", event_status="OPEN_PREGAME"), slate_defaults())
        self.assertEqual(row["fee_method"], "novig_straight_taker_v20260929")
        self.assertEqual(row["fee_coeff"], Decimal("0"))
        self.assertEqual(row["fee_used"], Decimal("0"))

    def test_novig_live_fee_uses_the_live_coefficient(self):
        row = build_row(lock(venue="novig", event_status="OPEN_INGAME"), slate_defaults())
        per_contract = novig_taker_fee_per_dollar(
            row["open_price"],
            NOVIG_STRAIGHT_LIVE_COEFF,
            "WHEN_LIVE",
            "OPEN_INGAME",
        )
        contracts = row["stake"] / row["open_price"]
        self.assertEqual(row["fee_coeff"], Decimal("0.03"))
        self.assertEqual(row["fee_used"], per_contract * contracts)

    def test_clv_is_positive_when_the_side_shortens(self):
        row = build_row(lock(), slate_defaults())
        apply_closes(
            [row],
            {
                "closes": [
                    {
                        "ticket_id": "T1",
                        "market_type": "spread",
                        "side": "SEA",
                        "line": "-7.5",
                        "period": "FG",
                        "close_american": -130,
                        "close_american_other": 110,
                    }
                ]
            },
        )
        self.assertEqual(row["close_status"], "ok")
        self.assertEqual(row["clv"], row["p_close"] - row["p_market"])
        self.assertGreater(row["clv"], Decimal("0"))
        self.assertTrue(is_complete(row))

    def test_quarter_kelly_does_not_change_the_stake(self):
        row = build_row(lock(p_model="0.60"), slate_defaults())
        self.assertEqual(row["stake"], Decimal("20"))
        self.assertGreater(row["quarter_kelly_shadow"], Decimal("0"))
        apply_finals([row], {"games": [final_game(away_score=31, home_score=17)], "pulled": "2026-09-30"})
        # SEA 31, WAS 17, line -7.5 covers. P/L is the flat $20 ticket, +18.18.
        self.assertEqual(row["result"], "W")
        self.assertEqual(row["pnl"], Decimal("18.18"))
        self.assertEqual(row["stake"], Decimal("20"))

    def test_push_is_excluded_from_brier(self):
        row = build_row(lock(line="+3"), slate_defaults())
        apply_finals(
            [row],
            {"games": [final_game(away_score=17, home_score=20)], "pulled": "2026-09-30"},
        )
        self.assertEqual(row["result"], "P")
        self.assertEqual(row["hit"], "push")
        self.assertEqual(row["pnl"], Decimal("0"))
        self.assertIsNone(row["brier"])
        self.assertIsNone(row["log_loss"])

    def test_hold_is_not_in_the_pnl(self):
        row = build_row(lock(decision="hold"), slate_defaults())
        apply_finals([row], {"games": [final_game()], "pulled": "2026-09-30"})
        self.assertIsNone(row["pnl"])
        self.assertIsNone(row["brier"])
        self.assertEqual(row["result"], "OPEN")


class Week3Tests(unittest.TestCase):
    def test_top5_is_two_and_three_for_minus_23_64(self):
        rows = load_slate(LOCKS)
        apply_finals(rows, json.loads(FINALS.read_text(encoding="utf-8")))
        from nfl_paper_log import mark_closes_missing

        mark_closes_missing(rows)
        self.assertEqual([row["result"] for row in rows], ["L", "W", "L", "L", "W"])
        self.assertEqual([row["hit"] for row in rows], ["miss", "hit", "miss", "miss", "hit"])
        self.assertEqual(sum((row["pnl"] for row in rows), Decimal("0")), Decimal("-23.64"))
        self.assertEqual(sum((row["stake"] for row in rows), Decimal("0")), Decimal("100"))
        self.assertEqual(len({row["same_contract_key"] for row in rows}), 5)
        for row in rows:
            self.assertEqual(row["sport"], "NFL")
            self.assertEqual(row["p_market"], Decimal("0.5"))
            self.assertEqual(row["brier"], Decimal("0.25"))
            self.assertEqual(row["close_status"], "close missing")
            self.assertIsNone(row["clv"])
            self.assertTrue(is_complete(row))
            self.assertFalse(row["same_contract_mismatch"])
            self.assertIsNone(row["quarter_kelly_shadow"])
        card = render_scorecard(rows)
        self.assertIn("-$23.64 on $100.00", card)
        self.assertIn("close missing (n=0)", card)
        self.assertIn("2 wins, 3 losses, 0 pushes", card)
        self.assertIn("100% (5/5)", card)
        self.assertIn("| Contract mismatches | 0 |", card)
        self.assertIn("0.250000", card)

    def test_cli_week_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "week.jsonl"
            csv_path = Path(tmp) / "week.csv"
            card_path = Path(tmp) / "card.md"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "nfl_paper_log.py"),
                    "week",
                    "--locks",
                    str(LOCKS),
                    "--finals",
                    str(FINALS),
                    "--out",
                    str(out),
                    "--csv",
                    str(csv_path),
                    "--scorecard",
                    str(card_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("-$23.64 on $100.00", completed.stdout)
            self.assertIn("close missing", completed.stdout)
            rows = read_jsonl(out)
            self.assertEqual(sum((row["pnl"] for row in rows), Decimal("0")), Decimal("-23.64"))
            with csv_path.open(encoding="utf-8", newline="") as handle:
                header = next(csv.reader(handle))
            self.assertEqual(header, list(COLUMNS))
            self.assertIn("Paper only", card_path.read_text(encoding="utf-8"))

    def test_ingest_does_not_stamp_a_close_or_a_grade(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "locks.jsonl"
            with contextlib.redirect_stdout(io.StringIO()):
                code = main(["ingest", "--locks", str(LOCKS), "--out", str(out)])
            self.assertEqual(code, 0)
            rows = read_jsonl(out)
            self.assertEqual(len(rows), 5)
            for row in rows:
                self.assertIsNone(row["close_status"])
                self.assertIsNone(row["pnl"])
                self.assertEqual(row["result"], "OPEN")
                self.assertFalse(is_complete(row))

    def test_run_week_without_a_close_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "week.jsonl"
            text = run_week(LOCKS, FINALS, None, out, None, None)
            self.assertIn("close missing (n=0)", text)
            rows = read_jsonl(out)
            self.assertTrue(all(row["close_status"] == "close missing" for row in rows))


if __name__ == "__main__":
    unittest.main()
