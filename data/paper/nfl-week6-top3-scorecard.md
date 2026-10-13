# NFL Week 6 paper top-3 scorecard

Paper only. This scorecard does not submit an order. It does not support an edge claim.
Flat $20. Realized P/L uses the logged American price via `paper_grade.settle` (win profit half-up to the cent). `fee_used` is the venue taker snapshot stored beside that P/L. `ev_usd` is the expectation under `p_market`.
At -110, break-even hit rate is 110/210, about 52.38%.

## Summary

| Metric | Value |
| --- | --- |
| n | 3 |
| Week | 6 |
| Completeness | 100% (3/3) |
| Contract mismatches | 0 |
| Mean CLV | close missing (n=0) |
| Market Brier | n/a |
| Brier, constant 0.5 | n/a |
| Model Brier | n=0 |
| Log loss | n/a |
| Hit rate | 0 wins, 0 losses, 0 pushes |
| Paper P/L | n/a |
| Shadow quarter-Kelly | n=0. Not staked. |

CLV = devigged close probability of the side minus `p_market`. Positive means the ticket beat the close. A missing close is the status `close missing`, and that row is left out of the mean.

A row is complete when it has a contract key, `p_market`, a fee method and `fee_used`, sources, and either a same-contract close or `close missing`.

## Tickets

| Ticket | Contract | Result | P/L | p_market | CLV | Brier | Close | Mismatch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PAPER-NFL-W6-01 | total over 53.5 FG | OPEN |  | 0.483182 |  |  | close missing |  |
| PAPER-NFL-W6-02 | total over 41.5 FG | OPEN |  | 0.471370 |  |  | close missing |  |
| PAPER-NFL-W6-03 | total under 50.5 FG | OPEN |  | 0.492658 |  |  | close missing |  |
