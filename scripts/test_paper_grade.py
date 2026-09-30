"""Unit tests for paper spread and total grading. No network."""

from __future__ import annotations

import unittest
from decimal import Decimal

from paper_grade import (
    american_win_profit,
    grade_moneyline,
    grade_spread,
    grade_total,
    settle,
    summarize_settled,
    win_pl_usd,
)


class GradeTests(unittest.TestCase):
    def test_twenty_at_minus_110_rounds_to_18_18(self):
        self.assertEqual(american_win_profit(), Decimal("2000") / Decimal("110"))
        self.assertEqual(win_pl_usd(), Decimal("18.18"))
        self.assertEqual(settle("W"), Decimal("18.18"))
        self.assertEqual(settle("L"), Decimal("-20"))
        self.assertEqual(settle("P"), Decimal("0"))

    def test_iowa_michigan_paper_tickets(self):
        # Final IOWA 20, MICH 19. No overtime in the source linescore.
        spread = grade_spread(20, 19, "5.5")
        self.assertEqual(spread["margin"], Decimal("6.5"))
        self.assertEqual(spread["result"], "W")
        self.assertEqual(spread["hit"], "hit")
        total = grade_total(20, 19, "Under", "38.5")
        self.assertEqual(total["combined"], Decimal("39"))
        self.assertEqual(total["margin"], Decimal("-0.5"))
        self.assertEqual(total["result"], "L")

    def test_tennessee_plus_covers_a_three_point_loss(self):
        # TEX 20, TENN 17. Tennessee +4.5.
        graded = grade_spread(17, 20, "4.5")
        self.assertEqual(graded["margin"], Decimal("1.5"))
        self.assertEqual(graded["result"], "W")

    def test_oklahoma_georgia_under_misses(self):
        # OKLA 13, UGA 41.
        graded = grade_total(13, 41, "Under", "44.5")
        self.assertEqual(graded["combined"], Decimal("54"))
        self.assertEqual(graded["margin"], Decimal("-9.5"))
        self.assertEqual(graded["result"], "L")

    def test_integer_spread_can_push(self):
        graded = grade_spread(17, 20, "3")
        self.assertEqual(graded["margin"], Decimal("0"))
        self.assertEqual(graded["result"], "P")
        self.assertEqual(graded["hit"], "push")

    def test_half_point_does_not_push_on_a_whole_margin(self):
        # Lost by 35 against +34.5.
        graded = grade_spread(14, 49, "34.5")
        self.assertEqual(graded["margin"], Decimal("-0.5"))
        self.assertEqual(graded["result"], "L")

    def test_favorite_and_over(self):
        utah = grade_spread(31, 17, "-7.5")
        self.assertEqual(utah["margin"], Decimal("6.5"))
        self.assertEqual(utah["result"], "W")
        over = grade_total(30, 27, "Over", "58.5")
        self.assertEqual(over["margin"], Decimal("-1.5"))
        self.assertEqual(over["result"], "L")

    def test_moneyline_win_loss_and_tie(self):
        win = grade_moneyline(24, 17)
        self.assertEqual(win["result"], "W")
        self.assertEqual(win["hit"], "hit")
        loss = grade_moneyline(7, 27)
        self.assertEqual(loss["result"], "L")
        tie = grade_moneyline(20, 20)
        self.assertEqual(tie["margin"], Decimal("0"))
        self.assertEqual(tie["result"], "P")
        self.assertEqual(tie["hit"], "push")

    def test_settled_cfb_book(self):
        # Two wins and two losses at $20 / -110. The open ticket is excluded.
        summary = summarize_settled(["L", "W", "W", "L"])
        self.assertEqual(summary["wins"], 2)
        self.assertEqual(summary["losses"], 2)
        self.assertEqual(summary["pushes"], 0)
        self.assertEqual(summary["net_pl_usd"], Decimal("-3.64"))
        self.assertEqual(summary["stake_settled_usd"], Decimal("80"))
        self.assertEqual(summary["roi"], Decimal("-3.64") / Decimal("80"))


if __name__ == "__main__":
    unittest.main()
