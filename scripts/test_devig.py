"""Unit tests for basic and Shin de-vig. No network."""

from __future__ import annotations

import unittest
from decimal import Decimal

from devig import basic_devig, devig_pair, implied_from_american, shin_probabilities


class BasicDevigTests(unittest.TestCase):
    def test_symmetric_minus_110_is_one_half(self):
        implied = implied_from_american(-110)
        self.assertEqual(implied, Decimal("110") / Decimal("210"))
        probs = basic_devig([implied, implied])
        self.assertEqual(probs[0], Decimal("0.5"))
        self.assertEqual(probs[1], Decimal("0.5"))

    def test_favorite_and_dog_share_the_overround(self):
        # -150 is 3/5. +130 is 10/23. The normalized favorite is 69/119.
        favorite = implied_from_american(-150)
        dog = implied_from_american(130)
        probs = basic_devig([favorite, dog])
        self.assertEqual(probs[0], Decimal(69) / Decimal(119))
        self.assertEqual(probs[1], Decimal(50) / Decimal(119))
        self.assertEqual(probs[0] + probs[1], Decimal(119) / Decimal(119))

    def test_fair_book_is_unchanged(self):
        probs = basic_devig([Decimal("0.4"), Decimal("0.6")])
        self.assertEqual(probs, [Decimal("0.4"), Decimal("0.6")])


class ShinDevigTests(unittest.TestCase):
    def test_three_way_matches_published_mberk_fixture(self):
        # mberk/shin test_calculate_implied_probabilities_full_output.
        # Decimal odds 2.6, 2.4, 4.3. Published to 7 decimals.
        implied = [Decimal(1) / Decimal(odds) for odds in ("2.6", "2.4", "4.3")]
        probs, z = shin_probabilities(implied)
        expected = [Decimal("0.3729941"), Decimal("0.4047794"), Decimal("0.2222265")]
        for got, want in zip(probs, expected):
            self.assertLess(abs(got - want), Decimal("1e-6"))
        self.assertLess(abs(z - Decimal("0.01694251")), Decimal("1e-6"))
        self.assertLess(abs(sum(probs, Decimal("0")) - Decimal("1")), Decimal("1e-8"))

    def test_two_way_matches_additive_method(self):
        # mberk/shin: with two outcomes, Shin equals Clarke's additive method.
        implied = [Decimal(1) / Decimal("1.5"), Decimal(1) / Decimal("2.74")]
        total = sum(implied, Decimal("0"))
        probs, _z = shin_probabilities(implied)
        for raw, fair in zip(implied, probs):
            additive = raw - (total - 1) / 2
            self.assertLess(abs(fair - additive), Decimal("1e-18"))

    def test_symmetric_book_is_one_half(self):
        implied = implied_from_american(-110)
        probs, _z = shin_probabilities([implied, implied])
        self.assertLess(abs(probs[0] - Decimal("0.5")), Decimal("1e-18"))
        self.assertLess(abs(probs[1] - Decimal("0.5")), Decimal("1e-18"))

    def test_shin_removes_more_overround_from_the_longshot(self):
        favorite = implied_from_american(-300)
        dog = implied_from_american(250)
        basic = basic_devig([favorite, dog])
        shin, _z = shin_probabilities([favorite, dog])
        self.assertGreater(shin[0], basic[0])
        self.assertLess(shin[1], basic[1])

    def test_pair_stores_both_and_selects_the_named_method(self):
        implied = implied_from_american(-110)
        p_market, p_basic, p_shin = devig_pair("basic", implied, implied)
        self.assertEqual(p_market, p_basic)
        self.assertLess(abs(p_shin - Decimal("0.5")), Decimal("1e-18"))
        p_market_shin, _basic, p_shin_again = devig_pair("shin", implied, implied)
        self.assertEqual(p_market_shin, p_shin_again)


if __name__ == "__main__":
    unittest.main()
