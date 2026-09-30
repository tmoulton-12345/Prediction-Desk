"""Deterministic fee and round-trip math for a paper arb scan.

Prices are dollars per contract that settles at $1. Fees are exact
(unrounded) unless a caller asks for Polymarket US cent rounding.
No order placement.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_EVEN

ONE = Decimal("1")
CENT = Decimal("0.01")

# Re-check these on the day of a card. Figures below are the 2026-09-29 read
# recorded in research/20260929-betting-improvement-methods.md.
#
# Polymarket US standard taker theta, exchange-wide from 2026-09-25 00:00 ET.
# https://docs.polymarket.us/fees
# Fee = theta * contracts * price * (1 - price), then banker's rounding to the cent.
# International docs.polymarket.com listed a sports rate of 0.05 that day.
# That page is a different product. Do not substitute it here.
PM_TAKER_THETA_DEFAULT = Decimal("0.0695")

# Novig Help Center, article 16195057, read 2026-09-29.
# https://support.novig.com/en/articles/16195057-fees-on-novig
# Pregame straights use charge mode WHEN_LIVE and are 0 while the event
# status is OPEN_PREGAME. Live straights use 0.03. Futures use 0.06.
# Parlay coefficient 0.10 is inside the quote; this paper log does not size parlays.
NOVIG_STRAIGHT_LIVE_COEFF = Decimal("0.03")
NOVIG_FUTURES_COEFF = Decimal("0.06")


def q(value: Decimal | str | int) -> Decimal:
    return value if isinstance(value, Decimal) else Decimal(str(value))


def bankers_cents(amount: Decimal) -> Decimal:
    """Round half to even, to the cent. Polymarket US standard taker fee rule."""
    return q(amount).quantize(CENT, rounding=ROUND_HALF_EVEN)


def pm_taker_fee_exact(price: Decimal, contracts: Decimal, theta: Decimal) -> Decimal:
    """Fee = theta * contracts * p * (1 - p). Exact, before cent rounding."""
    price = q(price)
    contracts = q(contracts)
    theta = q(theta)
    return theta * contracts * price * (ONE - price)


def pm_taker_fee_rounded(price: Decimal, contracts: Decimal, theta: Decimal) -> Decimal:
    return bankers_cents(pm_taker_fee_exact(price, contracts, theta))


def novig_taker_fee_per_dollar(
    price: Decimal,
    coefficient: Decimal,
    charged: str,
    event_status: str,
) -> Decimal:
    """Fee per $1-payout contract.

    Novig v3 prices a 1-cent contract as c * p * (1 - p) * 1 cent.
    One hundred of those is one $1 contract, so the per-dollar fee is
    c * p * (1 - p) when the market is charging.

    WHEN_LIVE charges only while the event status is OPEN_INGAME.
    A pregame straight (OPEN_PREGAME) is zero. ALWAYS charges in every phase.
    """
    price = q(price)
    coefficient = q(coefficient)
    if charged == "WHEN_LIVE":
        if event_status != "OPEN_INGAME":
            return Decimal("0")
    elif charged != "ALWAYS":
        raise ValueError(f"unknown Novig charge mode: {charged}")
    return coefficient * price * (ONE - price)


def round_trip_cost(ask_a: Decimal, fee_a: Decimal, ask_b: Decimal, fee_b: Decimal) -> Decimal:
    """Dollars to buy one contract of each complementary side."""
    return q(ask_a) + q(fee_a) + q(ask_b) + q(fee_b)


def locked_edge(cost: Decimal) -> Decimal:
    """Positive when the two asks plus fees cost less than the $1 payout."""
    return ONE - q(cost)


def edge_pct_of_payout(cost: Decimal) -> Decimal:
    """Locked edge as a percent of the $1 payout. Negative when the sum is over $1."""
    return locked_edge(cost) * Decimal("100")
