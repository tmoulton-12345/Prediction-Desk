"""Grade a paper spread, total, or moneyline from a final score.

American -110 on a flat stake unless the caller passes another price.
No order placement. Spreads, totals, and moneylines use the final score,
including overtime when the source total includes it. A game that is not
final is not graded.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")
STAKE_USD = Decimal("20")
AMERICAN_ODDS = -110


def q(value: Decimal | str | int) -> Decimal:
    return value if isinstance(value, Decimal) else Decimal(str(value))


def cents(amount: Decimal) -> Decimal:
    """Round half away from zero, to the cent."""
    return q(amount).quantize(CENT, rounding=ROUND_HALF_UP)


def american_win_profit(stake: Decimal = STAKE_USD, american: int = AMERICAN_ODDS) -> Decimal:
    """Profit on a winning ticket, before the cent round.

    At -110, profit = stake * 100 / 110. On a $20 stake that is
    2000/110 = 18.1818..., which rounds to $18.18.
    """
    stake = q(stake)
    price = Decimal(american)
    if price == 0:
        raise ValueError("american odds cannot be 0")
    if price < 0:
        return stake * Decimal(100) / abs(price)
    return stake * price / Decimal(100)


def win_pl_usd(stake: Decimal = STAKE_USD, american: int = AMERICAN_ODDS) -> Decimal:
    return cents(american_win_profit(stake, american))


def settle(result: str, stake: Decimal = STAKE_USD, american: int = AMERICAN_ODDS) -> Decimal:
    """P/L for a settled result. W, L, or P."""
    if result == "W":
        return win_pl_usd(stake, american)
    if result == "L":
        return -q(stake)
    if result == "P":
        return Decimal("0")
    raise ValueError(f"unsettled result {result!r}")


def _result_from_margin(margin: Decimal) -> str:
    if margin > 0:
        return "W"
    if margin < 0:
        return "L"
    return "P"


def grade_spread(pick_score: int, opp_score: int, line: Decimal | str | int) -> dict:
    """Cover margin = pick_score + line - opponent_score.

    Positive margin covers. Zero is a push. Negative misses.
    `line` is the pick's spread (Iowa +5.5 is Decimal('5.5')).
    """
    line_q = q(line)
    margin = Decimal(pick_score) + line_q - Decimal(opp_score)
    result = _result_from_margin(margin)
    return {"margin": margin, "result": result, "hit": _hit(result)}


def grade_total(away_score: int, home_score: int, side: str, line: Decimal | str | int) -> dict:
    """Under margin = line - combined. Over margin = combined - line."""
    side_norm = side.strip().lower()
    if side_norm not in ("under", "over"):
        raise ValueError(f"total side must be Under or Over, got {side!r}")
    combined = Decimal(away_score + home_score)
    line_q = q(line)
    if side_norm == "under":
        margin = line_q - combined
    else:
        margin = combined - line_q
    result = _result_from_margin(margin)
    return {
        "combined": combined,
        "margin": margin,
        "result": result,
        "hit": _hit(result),
    }


def grade_moneyline(pick_score: int, opp_score: int) -> dict:
    """Moneyline margin = pick score − opponent score. A tie is a push."""
    margin = Decimal(pick_score) - Decimal(opp_score)
    result = _result_from_margin(margin)
    return {"margin": margin, "result": result, "hit": _hit(result)}


def _hit(result: str) -> str:
    return {"W": "hit", "L": "miss", "P": "push"}[result]


def summarize_settled(results: list[str], stake: Decimal = STAKE_USD, american: int = AMERICAN_ODDS) -> dict:
    """Wins, losses, pushes, net P/L, and ROI on settled tickets only."""
    wins = results.count("W")
    losses = results.count("L")
    pushes = results.count("P")
    if wins + losses + pushes != len(results):
        raise ValueError("summarize_settled expects only W, L, P")
    net = sum((settle(r, stake, american) for r in results), Decimal("0"))
    risked = q(stake) * Decimal(len(results))
    roi = (net / risked) if risked else None
    return {
        "settled": len(results),
        "wins": wins,
        "losses": losses,
        "pushes": pushes,
        "net_pl_usd": net,
        "stake_settled_usd": risked,
        "roi": roi,
    }
