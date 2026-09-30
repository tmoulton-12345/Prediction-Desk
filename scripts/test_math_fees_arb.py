"""Unit tests for fee and round-trip math. No network."""

from __future__ import annotations

import unittest
from decimal import Decimal

from math_fees_arb import (
    NOVIG_FUTURES_COEFF,
    NOVIG_STRAIGHT_LIVE_COEFF,
    PM_TAKER_THETA_DEFAULT,
    bankers_cents,
    edge_pct_of_payout,
    locked_edge,
    novig_taker_fee_per_dollar,
    pm_taker_fee_exact,
    pm_taker_fee_rounded,
    round_trip_cost,
)


class FeeTests(unittest.TestCase):
    def test_pm_published_examples_round_half_even(self):
        theta = Decimal("0.0695")
        # docs.polymarket.us fee page, 1,000 contracts.
        self.assertEqual(
            pm_taker_fee_rounded(Decimal("0.10"), Decimal("1000"), theta),
            Decimal("6.26"),
        )
        self.assertEqual(
            pm_taker_fee_rounded(Decimal("0.65"), Decimal("1000"), theta),
            Decimal("15.81"),
        )
        self.assertEqual(
            pm_taker_fee_rounded(Decimal("0.30"), Decimal("1000"), theta),
            Decimal("14.60"),
        )
        self.assertEqual(
            pm_taker_fee_rounded(Decimal("0.90"), Decimal("1000"), theta),
            Decimal("6.26"),
        )
        self.assertEqual(
            pm_taker_fee_rounded(Decimal("0.50"), Decimal("1000"), theta),
            Decimal("17.38"),
        )
        # 100-lot table row at $0.50 is $1.74.
        self.assertEqual(
            pm_taker_fee_rounded(Decimal("0.50"), Decimal("100"), theta),
            Decimal("1.74"),
        )

    def test_pm_fee_is_symmetric_in_price(self):
        theta = Decimal("0.0695")
        a = pm_taker_fee_exact(Decimal("0.37"), Decimal("1"), theta)
        b = pm_taker_fee_exact(Decimal("0.63"), Decimal("1"), theta)
        self.assertEqual(a, b)

    def test_novig_pregame_when_live_is_zero(self):
        fee = novig_taker_fee_per_dollar(
            Decimal("0.50"),
            Decimal("0.03"),
            "WHEN_LIVE",
            "OPEN_PREGAME",
        )
        self.assertEqual(fee, Decimal("0"))

    def test_novig_live_matches_published_10000_one_cent_contracts(self):
        # 10,000 one-cent contracts = 100 dollar contracts.
        # Published game-schedule fee at 0.50 is $0.75.
        per_dollar = novig_taker_fee_per_dollar(
            Decimal("0.50"),
            Decimal("0.03"),
            "WHEN_LIVE",
            "OPEN_INGAME",
        )
        self.assertEqual(per_dollar * Decimal("100"), Decimal("0.7500"))
        per_dollar_30 = novig_taker_fee_per_dollar(
            Decimal("0.30"),
            Decimal("0.03"),
            "WHEN_LIVE",
            "OPEN_INGAME",
        )
        self.assertEqual(per_dollar_30 * Decimal("100"), Decimal("0.6300"))

    def test_novig_always_charges_pregame(self):
        fee = novig_taker_fee_per_dollar(
            Decimal("0.50"),
            Decimal("0.06"),
            "ALWAYS",
            "OPEN_PREGAME",
        )
        self.assertEqual(fee, Decimal("0.015"))

    def test_unknown_charge_mode_raises(self):
        with self.assertRaises(ValueError):
            novig_taker_fee_per_dollar(
                Decimal("0.50"), Decimal("0.03"), "SOMETIMES", "OPEN_PREGAME"
            )


class CoefficientTests(unittest.TestCase):
    def test_named_coefficients_match_the_20260929_read(self):
        # Polymarket US standard taker theta. Novig live straight and futures.
        # Sources are the comments on the constants in math_fees_arb.py.
        self.assertEqual(PM_TAKER_THETA_DEFAULT, Decimal("0.0695"))
        self.assertEqual(NOVIG_STRAIGHT_LIVE_COEFF, Decimal("0.03"))
        self.assertEqual(NOVIG_FUTURES_COEFF, Decimal("0.06"))


class ArbTests(unittest.TestCase):
    def test_positive_edge_when_asks_plus_fees_under_one(self):
        cost = round_trip_cost(
            Decimal("0.48"),
            Decimal("0.008"),
            Decimal("0.49"),
            Decimal("0"),
        )
        self.assertEqual(cost, Decimal("0.978"))
        self.assertEqual(locked_edge(cost), Decimal("0.022"))
        self.assertEqual(edge_pct_of_payout(cost), Decimal("2.200"))

    def test_over_one_is_negative_edge(self):
        cost = round_trip_cost(
            Decimal("0.52"),
            Decimal("0.01"),
            Decimal("0.51"),
            Decimal("0"),
        )
        self.assertGreater(cost, Decimal("1"))
        self.assertLess(locked_edge(cost), Decimal("0"))

    def test_bankers_half_to_even(self):
        self.assertEqual(bankers_cents(Decimal("1.725")), Decimal("1.72"))
        self.assertEqual(bankers_cents(Decimal("1.735")), Decimal("1.74"))


if __name__ == "__main__":
    unittest.main()
