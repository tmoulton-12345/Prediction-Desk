"""Basic and Shin de-vig. Deterministic. No prices invented here.

Callers pass implied probabilities (American or decimal already converted).
Basic normalization divides each implied probability by their sum.
Shin follows the Python optimiser in mberk/shin (Shin 1993; the two-outcome
closed form and the n-outcome fixed point published in that package).

NFL spreads and totals are two-outcome books. Moneylines are two-outcome
books. The three-outcome path exists so the Shin numbers can be checked
against the published fixture.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction


def as_decimal(value: Decimal | str | int | float) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, float):
        return Decimal(format(value, "f"))
    return Decimal(str(value))


def implied_from_american(american: Decimal | str | int | float) -> Decimal:
    """Raw implied probability of one American price, vig still inside."""
    price = as_decimal(american)
    if price == 0:
        raise ValueError("american odds cannot be 0")
    if price < 0:
        return abs(price) / (abs(price) + Decimal("100"))
    return Decimal("100") / (price + Decimal("100"))


def basic_devig(implied: list[Decimal]) -> list[Decimal]:
    """Proportional de-vig. Each output is implied / sum(implied)."""
    if len(implied) < 2:
        raise ValueError("basic de-vig needs at least two outcomes")
    probs = [as_decimal(p) for p in implied]
    if any(p <= 0 for p in probs):
        raise ValueError("implied probabilities must be positive")
    # Fraction keeps a symmetric book at exactly 1/2. Decimal division of
    # 110/210 by itself otherwise stops one ulp short of 0.5.
    parts = [Fraction(p) for p in probs]
    total = sum(parts, Fraction(0))
    return [_fraction_to_decimal(part / total) for part in parts]


def _fraction_to_decimal(part: Fraction) -> Decimal:
    return Decimal(part.numerator) / Decimal(part.denominator)


def shin_probabilities(implied: list[Decimal]) -> tuple[list[Decimal], Decimal]:
    """Return (fair probabilities, z).

    `z` is Shin's insider proportion. Implied probabilities may sum to more
    than 1. For two outcomes the `z` formula is the closed form in mberk/shin.
    For three or more, `z` is the same fixed-point iteration as that
    package's Python optimiser. Probabilities then use

        (sqrt(z^2 + 4 (1-z) pi^2 / sum(pi)) - z) / (2 (1-z))
    """
    if len(implied) < 2:
        raise ValueError("Shin de-vig needs at least two outcomes")
    with localcontext() as ctx:
        ctx.prec = 50
        probs_in = [as_decimal(p) for p in implied]
        if any(p <= 0 for p in probs_in):
            raise ValueError("implied probabilities must be positive")
        total = sum(probs_in, Decimal("0"))
        n = len(probs_in)
        if n == 2:
            z = _shin_z_two(probs_in[0], probs_in[1], total)
        else:
            z = _shin_z_iterate(probs_in, total, n)
        if z == 1:
            raise ValueError("Shin z reached 1")
        # A symmetric two-way book is exactly 1/2. The sqrt form stops one
        # ulp short, which then looks like a different price in the log.
        if n == 2 and probs_in[0] == probs_in[1]:
            half = Decimal("0.5")
            return [half, half], z
        probs = [_shin_probability(pi, z, total) for pi in probs_in]
    if any(p < 0 for p in probs):
        raise ValueError("Shin probability was negative")
    return probs, z


def _shin_z_two(first: Decimal, second: Decimal, total: Decimal) -> Decimal:
    diff = first - second
    denom = total * (diff ** 2 - 1)
    if denom == 0:
        raise ValueError("degenerate two-way book")
    return ((total - 1) * (diff ** 2 - total)) / denom


def _shin_z_iterate(implied: list[Decimal], total: Decimal, n: int) -> Decimal:
    z = Decimal("0")
    threshold = Decimal("1e-24")
    for _ in range(1000):
        previous = z
        acc = sum((_shin_sqrt_term(z, pi, total) for pi in implied), Decimal("0"))
        z = (acc - 2) / Decimal(n - 2)
        if abs(z - previous) <= threshold:
            return z
    return z


def _shin_sqrt_term(z: Decimal, implied: Decimal, total: Decimal) -> Decimal:
    inside = z ** 2 + 4 * (1 - z) * implied ** 2 / total
    if inside < 0:
        raise ValueError("Shin square root of a negative")
    return inside.sqrt()


def _shin_probability(implied: Decimal, z: Decimal, total: Decimal) -> Decimal:
    return (_shin_sqrt_term(z, implied, total) - z) / (2 * (1 - z))


def devig_pair(
    method: str,
    implied_side: Decimal,
    implied_other: Decimal,
) -> tuple[Decimal, Decimal, Decimal]:
    """De-vig one side of a two-way book.

    Returns (p_market, p_basic, p_shin) for the side in `implied_side`.
    `method` chooses which of basic or shin is copied into p_market.
    Both probabilities are always computed.
    """
    method_name = method.strip().lower()
    if method_name not in {"basic", "shin"}:
        raise ValueError(f"devig method must be basic or shin, got {method}")
    basic = basic_devig([implied_side, implied_other])
    shin, _z = shin_probabilities([implied_side, implied_other])
    p_market = basic[0] if method_name == "basic" else shin[0]
    return p_market, basic[0], shin[0]
