# NFL Week 4 paper top-5 scorecard

Paper only. This scorecard does not submit an order. It does not support an edge claim.
Flat $20. Realized P/L uses the logged American price via `paper_grade.settle` (win profit half-up to the cent). `fee_used` is the venue taker snapshot stored beside that P/L. `ev_usd` is the expectation under `p_market`.
At -110, break-even hit rate is 110/210, about 52.38%.

## Summary

| Metric | Value |
| --- | --- |
| n | 5 |
| Week | 4 |
| Completeness | 100% (5/5) |
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
| PAPER-NFL-W4-01 | spread GB -3.5 FG | OPEN |  | 0.500000 |  |  | close missing |  |
| PAPER-NFL-W4-02 | total under 40.5 FG | OPEN |  | 0.498996 |  |  | close missing |  |
| PAPER-NFL-W4-03 | spread SEA -7.5 FG | OPEN |  | 0.500000 |  |  | close missing |  |
| PAPER-NFL-W4-04 | total under 38.5 FG | OPEN |  | 0.497512 |  |  | close missing |  |
| PAPER-NFL-W4-05 | total under 38.5 FG | OPEN |  | 0.498783 |  |  | close missing |  |
