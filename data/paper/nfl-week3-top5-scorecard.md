# NFL Week 3 paper top-5 scorecard

Paper only. This scorecard does not submit an order. It does not support an edge claim.
Flat $20. Realized P/L uses the logged American price via `paper_grade.settle` (win profit half-up to the cent). `fee_used` is the venue taker snapshot stored beside that P/L. `ev_usd` is the expectation under `p_market`.
At -110, break-even hit rate is 110/210, about 52.38%.

## Summary

| Metric | Value |
| --- | --- |
| n | 5 |
| Week | 3 |
| Completeness | 100% (5/5) |
| Contract mismatches | 0 |
| Mean CLV | close missing (n=0) |
| Market Brier | 0.250000 |
| Brier, constant 0.5 | 0.250000 |
| Model Brier | n=0 |
| Log loss | 0.693147 |
| Hit rate | 2 wins, 3 losses, 0 pushes (0.400000 of decided) |
| Paper P/L | -$23.64 on $100.00 |
| Shadow quarter-Kelly | n=0. Not staked. |

CLV = devigged close probability of the side minus `p_market`. Positive means the ticket beat the close. A missing close is the status `close missing`, and that row is left out of the mean.

A row is complete when it has a contract key, `p_market`, a fee method and `fee_used`, sources, and either a same-contract close or `close missing`.

## Tickets

| Ticket | Contract | Result | P/L | p_market | CLV | Brier | Close | Mismatch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PAPER-NFL-01 | spread SEA -7.5 FG | L | -$20.00 | 0.500000 |  | 0.250000 | close missing |  |
| PAPER-NFL-02 | total under 37.5 FG | W | $18.18 | 0.500000 |  | 0.250000 | close missing |  |
| PAPER-NFL-03 | spread PHI -3.5 FG | L | -$20.00 | 0.500000 |  | 0.250000 | close missing |  |
| PAPER-NFL-04 | total under 39.5 FG | L | -$20.00 | 0.500000 |  | 0.250000 | close missing |  |
| PAPER-NFL-05 | spread BUF -7.5 FG | W | $18.18 | 0.500000 |  | 0.250000 | close missing |  |
