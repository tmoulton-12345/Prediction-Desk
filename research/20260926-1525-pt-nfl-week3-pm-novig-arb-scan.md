# NFL Week 3 Polymarket US vs Novig arb scan

**Stamped:** 2026-09-26 15:25 PDT (catalog pull). Order books were read in that same run and written at 2026-09-26 15:30 PDT.
**Phase 0.** Public reads only. No order was placed, queued, or submitted.

## Tim

- Arb: **no**
- True arb count: **0**
- Games scanned: **15** (Sunday Sep 27 plus Monday PHI @ CHI). TNF not in the window.
- Same-line pairs with an executable touch: **722**
- Report: `research/20260926-1525-pt-nfl-week3-pm-novig-arb-scan.md`
- JSON: `research/20260926-1525-pt-nfl-week3-pm-novig-arb-scan.json`
- Books snapshot: `snapshots/20260926-1525-pt-nfl-week3-books.json`

## Fees assumed

- Polymarket US taker theta on these markets: 0.0695.
- Formula: theta × contracts × p × (1 − p). The scan uses the exact per-contract fee. A 100-contract order is also shown after Polymarket's half-even cent rounding. No volume rebate.
- Novig fee rows seen (coefficient | when it charges | event status): 0.03|WHEN_LIVE|OPEN_PREGAME.
- Novig WHEN_LIVE is $0 on a pregame take. A live take would use coefficient × p × (1 − p) per $1 contract. Maker credit is not subtracted.
- Both legs are priced as takes: Polymarket offer, or one minus the best bid for the short side; Novig ask = 1 − best bid on the other outcome.
- Novig book qty is a 1-cent contract. Dollar contracts in this report are qty / 100.
- Tables below are rounded to four decimal places. The JSON file keeps the exact fee.
- Moneyline is included only when the touch on the priced direction is at least 100 dollar contracts on each venue. Spreads and totals are priced at the touch with size as a caveat.

## Gates

A true arb needs every gate to pass and a fee-adjusted round trip under $1.

- Same event: same two teams.
- Same line: same signed spread, or the same total, or the same winner market. The other direction of a spread (BUF −7.5 versus BUF +7.5) is a different contract.
- OT / void: full-game overtime matches. The void window does not. Polymarket US market text uses two weeks, then last fair market price. Novig regular-season anchors use 24 hours to start and 48 hours to resume, then a fair-value composite (`voids=FMV`). That gate fails on these listings.
- Settlement source: both use the NFL official result as the primary grade. Fallback ladders differ. That gate passes on the primary source.

## Games

| Game | Kickoff (PT) | PM main spread | Novig main spread | Mains match | PM main total | Novig main total | Totals match |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Seattle Seahawks @ Washington Commanders | 2026-09-27 10:00 AM PT | 7.5 | 7.5 | yes | 39.5 | 39.5 | yes |
| Kansas City Chiefs @ Miami Dolphins | 2026-09-27 10:00 AM PT | 10.5 | 10.5 | yes | 45.5 | 44.5 | no |
| New England Patriots @ Jacksonville Jaguars | 2026-09-27 10:00 AM PT | 2.5 | 2.5 | yes | 46.5 | 46.5 | yes |
| New York Jets @ Detroit Lions | 2026-09-27 10:00 AM PT | 6.5 | 6.5 | yes | 48.5 | 48.5 | yes |
| Los Angeles Chargers @ Buffalo Bills | 2026-09-27 10:00 AM PT | 7.5 | 7.5 | yes | 49.5 | 49.5 | yes |
| Carolina Panthers @ Cleveland Browns | 2026-09-27 10:00 AM PT | 2.5 | 1.5 | no | 42.5 | 42.5 | yes |
| Houston Texans @ Indianapolis Colts | 2026-09-27 10:00 AM PT | 1.5 | 1.5 | yes | 42.5 | 42.5 | yes |
| Cincinnati Bengals @ Pittsburgh Steelers | 2026-09-27 10:00 AM PT | 3.5 | 3.5 | yes | 42.5 | 42.5 | yes |
| Tennessee Titans @ New York Giants | 2026-09-27 10:00 AM PT | 2.5 | 2.5 | yes | 37.5 | 37.5 | yes |
| Arizona Cardinals @ San Francisco 49ers | 2026-09-27 1:05 PM PT | 7.5 | 7.5 | yes | 47.5 | 48.5 | no |
| Minnesota Vikings @ Tampa Bay Buccaneers | 2026-09-27 1:05 PM PT | 1.5 | 1.5 | yes | 42.5 | 42.5 | yes |
| Las Vegas Raiders @ New Orleans Saints | 2026-09-27 1:25 PM PT | 3.5 | 3.5 | yes | 43.5 | 43.5 | yes |
| Baltimore Ravens @ Dallas Cowboys | 2026-09-27 1:25 PM PT | 3.5 | 3.5 | yes | 53.5 | 53.5 | yes |
| Los Angeles Rams @ Denver Broncos | 2026-09-27 5:20 PM PT | 2.5 | 1.5 | no | 44.5 | 44.5 | yes |
| Philadelphia Eagles @ Chicago Bears | 2026-09-28 5:15 PM PT | 3.5 | 3.5 | yes | 42.5 | 41.5 | no |

## True arbs

None. No same-line pair cleared every gate with a round trip under $1.

## Price sums under $1 that still fail a gate

None. No same-line touch was under $1 after fees.

## Nearest same-line misses

Round trip after the fees above, minus $1. Smaller is closer. Different lines are not in this list. Every row fails the OT/void gate, so a sum under $1 would still not be a true arb.

| Game | Market | PM side @ ask | PM fee | Novig side @ ask | Novig fee | Sum | Over $1 by | Edge % of $1 | Touch $ contracts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DET / NYJ | total 47.5 | Over 47.5 @ 0.5300 | 0.0173 | Under 47.5 @ 0.4600 | 0.0000 | 1.0073 | 0.0073 | -0.731 | 1.05 |
| KC / MIA | spread 10.5 | KC +10.5 @ 0.9650 | 0.0023 | MIA -10.5 @ 0.0410 | 0.0000 | 1.0083 | 0.0083 | -0.835 | 228 |
| LV / NO | spread 3.5 | NO +3.5 @ 0.7400 | 0.0134 | LV -3.5 @ 0.2550 | 0.0000 | 1.0084 | 0.0084 | -0.837 | 0.67 |
| CIN / PIT | total 64.5 | Over 64.5 @ 0.0550 | 0.0036 | Under 64.5 @ 0.9500 | 0.0000 | 1.0086 | 0.0086 | -0.861 | 91.05 |
| JAX / NE | spread 9.5 | NE -9.5 @ 0.1500 | 0.0089 | JAX +9.5 @ 0.8500 | 0.0000 | 1.0089 | 0.0089 | -0.886 | 38.71 |
| DET / NYJ | spread 5.5 | DET +5.5 @ 0.8500 | 0.0089 | NYJ -5.5 @ 0.1500 | 0.0000 | 1.0089 | 0.0089 | -0.886 | 13.47 |
| JAX / NE | total 26.5 | Over 26.5 @ 0.9350 | 0.0042 | Under 26.5 @ 0.0700 | 0.0000 | 1.0092 | 0.0092 | -0.922 | 95 |
| MIN / TB | spread 10.5 | TB -10.5 @ 0.1600 | 0.0093 | MIN +10.5 @ 0.8400 | 0.0000 | 1.0093 | 0.0093 | -0.934 | 44.2 |
| LV / NO | spread 14.5 | NO +14.5 @ 0.9250 | 0.0048 | LV -14.5 @ 0.0800 | 0.0000 | 1.0098 | 0.0098 | -0.982 | 205 |
| DET / NYJ | spread 9.5 | DET +9.5 @ 0.9150 | 0.0054 | NYJ -9.5 @ 0.0900 | 0.0000 | 1.0104 | 0.0104 | -1.041 | 20 |

## Nearest misses with at least 100 dollar contracts at the touch

Same rule as the table above. The size floor drops one-lot quotes.

| Game | Market | PM side @ ask | PM fee | Novig side @ ask | Novig fee | Sum | Over $1 by | Edge % of $1 | Touch $ contracts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| KC / MIA | spread 10.5 | KC +10.5 @ 0.9650 | 0.0023 | MIA -10.5 @ 0.0410 | 0.0000 | 1.0083 | 0.0083 | -0.835 | 228 |
| LV / NO | spread 14.5 | NO +14.5 @ 0.9250 | 0.0048 | LV -14.5 @ 0.0800 | 0.0000 | 1.0098 | 0.0098 | -0.982 | 205 |
| ARI / SF | moneyline ML | SF @ 0.7800 | 0.0119 | ARI @ 0.2200 | 0.0000 | 1.0119 | 0.0119 | -1.193 | 4019.8 |
| KC / MIA | spread 10.5 | MIA +10.5 @ 0.5100 | 0.0174 | KC -10.5 @ 0.4850 | 0.0000 | 1.0124 | 0.0124 | -1.237 | 19038.24 |
| SEA / WAS | moneyline ML | SEA @ 0.7650 | 0.0125 | WAS @ 0.2350 | 0.0000 | 1.0125 | 0.0125 | -1.249 | 555.03 |
| BAL / DAL | spread 3.5 | DAL -3.5 @ 0.2550 | 0.0132 | BAL +3.5 @ 0.7450 | 0.0000 | 1.0132 | 0.0132 | -1.320 | 130.04 |
| DEN / LAR | total 24.5 | Over 24.5 @ 0.9450 | 0.0036 | Under 24.5 @ 0.0650 | 0.0000 | 1.0136 | 0.0136 | -1.361 | 112 |
| KC / MIA | moneyline ML | KC @ 0.8550 | 0.0086 | MIA @ 0.1500 | 0.0000 | 1.0136 | 0.0136 | -1.362 | 2927.85 |

## Line shop only

Each venue's main line is the full-game listing whose touch midpoint is closest to 50 cents. A mismatch is not an arb.

| Game | Kind | Polymarket main | Novig main |
| --- | --- | --- | --- |
| Kansas City Chiefs @ Miami Dolphins | total | 45.5 (Over 45.5 total points) | 44.5 (KC @ MIA t44.5) |
| Carolina Panthers @ Cleveland Browns | spread | 2.5 (Carolina Panthers wins by over 2.5 points) | 1.5 (CLE +1.5) |
| Arizona Cardinals @ San Francisco 49ers | total | 47.5 (Over 47.5 total points) | 48.5 (ARI @ SF t48.5) |
| Los Angeles Rams @ Denver Broncos | spread | 2.5 (Los Angeles Rams wins by over 2.5 points) | 1.5 (DEN +1.5) |
| Philadelphia Eagles @ Chicago Bears | total | 42.5 (Over 42.5 total points) | 41.5 (PHI @ CHI t41.5) |

## Closest same-line pair on each game

| Game | Kind | Line | Sum | Over $1 by | Touch $ contracts |
| --- | --- | --- | --- | --- | --- |
| Seattle Seahawks @ Washington Commanders | moneyline | ML | 1.0125 | 0.0125 | 555.03 |
| Kansas City Chiefs @ Miami Dolphins | spread | 10.5 | 1.0083 | 0.0083 | 228 |
| New England Patriots @ Jacksonville Jaguars | spread | 9.5 | 1.0089 | 0.0089 | 38.71 |
| New York Jets @ Detroit Lions | total | 47.5 | 1.0073 | 0.0073 | 1.05 |
| Los Angeles Chargers @ Buffalo Bills | total | 32.5 | 1.0154 | 0.0154 | 1394 |
| Carolina Panthers @ Cleveland Browns | spread | 9.5 | 1.0130 | 0.0130 | 11 |
| Houston Texans @ Indianapolis Colts | spread | 7.5 | 1.0139 | 0.0139 | 54.2 |
| Cincinnati Bengals @ Pittsburgh Steelers | total | 64.5 | 1.0086 | 0.0086 | 91.05 |
| Tennessee Titans @ New York Giants | total | 35.5 | 1.0119 | 0.0119 | 15.02 |
| Arizona Cardinals @ San Francisco 49ers | moneyline | ML | 1.0119 | 0.0119 | 4019.8 |
| Minnesota Vikings @ Tampa Bay Buccaneers | spread | 10.5 | 1.0093 | 0.0093 | 44.2 |
| Las Vegas Raiders @ New Orleans Saints | spread | 3.5 | 1.0084 | 0.0084 | 0.67 |
| Baltimore Ravens @ Dallas Cowboys | spread | 10.5 | 1.0121 | 0.0121 | 1 |
| Los Angeles Rams @ Denver Broncos | total | 54.5 | 1.0125 | 0.0125 | 3.02 |
| Philadelphia Eagles @ Chicago Bears | spread | 3.5 | 1.0130 | 0.0130 | 17 |

## What this scan did not do

- No Kalshi. No international Polymarket. No live order, no queued order, no retry of an order.
- No paper-pick card. This file is the cross-venue scan only.
- Prices are the touch at pull time. They are not a sweep of the book and not a promise the size is still there.

## Sources

- polymarket_us_events: https://gateway.polymarket.us/v2/leagues/nfl/events
- polymarket_us_book: https://gateway.polymarket.us/v1/markets/{slug}/book
- polymarket_us_fees: https://docs.polymarket.us/fees
- polymarket_us_sports_faq: https://docs.polymarket.us/faqs/sports-faqs
- novig_events: https://api.novig.us/v3/public/catalog/events
- novig_markets: https://api.novig.us/v3/public/catalog/markets
- novig_book: https://api.novig.us/v3/public/catalog/markets/{id}/book
- novig_fees: https://docs.novig.com/api/concepts/fees
- novig_nfl_spread_anchor: https://ludlow-filings.s3.us-east-1.amazonaws.com/NFL-spread-anchor-cl-a.pdf
- novig_nfl_total_anchor: https://ludlow-filings.s3.us-east-1.amazonaws.com/NFL-total-anchor-cl-a.pdf
- novig_nfl_winner_anchor: https://ludlow-filings.s3.us-east-1.amazonaws.com/nfl-winner-anchor-cl-a.pdf
