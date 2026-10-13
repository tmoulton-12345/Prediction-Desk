# NFL Week 6 Picks Thu-Mon 2026-10-13 9:10am PT

Phase 0 paper only. No order was placed, queued, or funded. Novig fund/place stays frozen at $0.

**Books:** `snapshots/20261013-0900-pt-nfl-week6-books.json` (9:00am PT raw BBOs) and `snapshots/20261013-0903-pt-nfl-week6-pm-novig-compare.json` (9:03am PT, polarity-correct same contract). Ticket prices are the taker **asks** on that compare. The board table below prints the compare file's mids.
**Locks:** `fixtures/nfl/week6-top3-locks.json`
**Open log:** `data/paper/nfl-week6-top3.jsonl` (close missing stamped)
**News:** `research/20261013-0903-pt-nfl-week6-x-injury-news.json`

## Completeness

| Check | Status |
| --- | --- |
| ESPN Week 6 kicks, 14 games, byes CIN/DET/MIA/MIN, no flex | Done. Matches the brief |
| Polymarket US + Novig main spread and total, 14/14 | Done. 09:00 / 09:03 PT |
| Fee page used for the all-in compare | Polymarket US taker θ 0.0695. Novig pregame straight 0 |
| Injury / Schefter-Rapoport notes | Done. Practice gates still open |
| Elo / totals model `p_model` | Absent. Repo has no `prediction-desk/models/nfl_elo`. Not fit this week |
| Same-contract close | OPEN. Logger status `close missing` |
| Mean CLV | OPEN (n=0) |
| Brier | OPEN |
| P/L | OPEN |
| Logger row completeness (contract, `p_market`, fee, sources, close missing) | 100% (3/3) |
| Orders | None |

Paper risk on this card is **$60** (three $20 tickets).

## Gate

No `p_model`. The Elo gate cannot clear. Cross-venue edge is the other book's basic-devig probability minus this book's all-in taker cost. It has to beat **0.017375** (θ 0.0695 × 0.5 × 0.5). Novig's pregame fee of 0 is not treated as a zero hurdle.

**0 of 14 main totals and 0 of 14 main spreads clear that hurdle.** The three tickets are the best totals under the totals-first rule, each flagged **weak / hold-candidate**. They are not a claim of edge.

| Rank | Contract | Venue ask | Edge vs other devig | Hurdle |
| --- | --- | --- | --- | --- |
| 1 | DAL @ GB Over 53.5 | Novig 0.485 | +0.0100 | 0.017375 |
| 2 | BAL @ CLE Over 41.5 | Novig 0.48 | +0.0028 | 0.017375 |
| 3 | WAS @ SF Under 50.5 | Novig 0.495 | +0.0025 | 0.017375 |

PIT @ TB Over 40.5 tied the third total at +0.0025. It stayed off the card because Baker Mayfield (thumb) is OUT for Week 6 on both the ESPN feed and the Oct 12 roundup, and that fact fights an Over. CHI −3.5 and SF −7.5 are half-point favorites. Their edges are +0.0027 and +0.0025. The half-point rule says skip those lays unless the fee-aware price shows a clear edge. They were skipped. Stake stays $20 on every ticket.

## Tickets

| ID | Type | Game | Kick PT | Side | Line | Stake | American | Venue | Conf | Close | Hit / P/L |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PAPER-NFL-W6-01 | total | DAL @ GB | Sun 10/18 5:20pm | Over | 53.5 | $20 | +106 | novig | 4 | OPEN | OPEN |
| PAPER-NFL-W6-02 | total | BAL @ CLE | Sun 10/18 10:00am | Over | 41.5 | $20 | +108 | novig | 2 | OPEN | OPEN |
| PAPER-NFL-W6-03 | total | WAS @ SF | Mon 10/19 5:15pm | Under | 50.5 | $20 | +102 | novig | 2 | OPEN | OPEN |

Logger `p_market` is the basic de-vig of the integer American pair (`scripts/nfl_paper_log.py`). `p_model` is blank. `fee_used` is $0 (Novig pregame).

### PAPER-NFL-W6-01 — weak / hold-candidate

- **Why:** Largest fee-aware gap on the slate, and it is a total. Novig Over 53.5 ask 0.485 (+106). Polymarket US ask 0.500 on `tsc-nfl-dal-gb-2026-10-18-total-53pt5`. Edge vs PM devig +0.0100.
- **Venue:** Novig `01a112eb-5435-7d80-aba2-7d94dd79c649`. Pregame fee 0 and the lower ask. PM all-in adds about 1.74¢ at this price.
- **p_model / p_market:** blank / **0.483182**. Other side on Novig −108.
- **Edge vs fees:** +0.0100 vs hurdle 0.017375. Does not clear.
- **Skeptic:** Schefter, Oct 12 10:30am PT: Green Bay is not anticipating Micah Parsons back at practice this week. That was public before the 9:00am snapshot. A 1.5 cent discount is not a new defensive edge. Sunday night can reprice 53.5.

### PAPER-NFL-W6-02 — weak / hold-candidate — injury-late annotate

- **Why:** Next total. Novig Over 41.5 ask 0.48 (+108). Polymarket US ask 0.49 on `tsc-nfl-bal-cle-2026-10-18-total-41pt5`. Edge +0.0028.
- **Venue:** Novig `01a112eb-522a-7093-8a86-0878721f01d7`. Fee 0 and the lower ask.
- **p_model / p_market:** blank / **0.471370**. Other side on Novig −117.
- **Edge vs fees:** +0.0028 vs 0.017375. Does not clear.
- **Skeptic / gate:** ESPN injuries list Lamar Jackson Out (ankle). The Oct 12 roundup still has him Questionable, and Jesse Minter said Monday he was unsure Jackson would practice Wednesday ([Ravens.com](https://www.baltimoreravens.com/news/news-notes-injury-updates-lamar-jackson-cam-jurgens-trey-hendrickson-jakobi-lane-mike-green-vega-ioane)). Shadow-void this ticket if the Week 6 quarterback designation changes before the Sunday 9:15am PT close. This Over is not a Lamar lean or a Huntley lean.

### PAPER-NFL-W6-03 — weak / hold-candidate

- **Why:** Tied PIT @ TB Over 40.5. Took the Under because Mayfield OUT fights that Over. Novig Under 50.5 ask 0.495 (+102). Polymarket US Under ask 0.500 on `tsc-nfl-was-sf-2026-10-19-total-50pt5`. Edge +0.0025.
- **Venue:** Novig `01a112eb-54e8-7823-917a-d2d076c8886c`. Fee 0 and the lower ask.
- **p_model / p_market:** blank / **0.492658**. Other side on Novig −104.
- **Edge vs fees:** +0.0025 vs 0.017375. Does not clear.
- **Skeptic:** Schefter, Oct 12: Deebo Samuel misses at least a couple of weeks; Ricky Pearsall is out for the season (PCL). Dre Greenlaw is suspended for Monday (appealing, per Rapoport). Those notes are already public. SF −7.5 was the half-point home favorite and was not ticketed. Monday can reprice after Friday's report.

## Kickoffs

ESPN scoreboard `week=6&seasontype=2&dates=2026`, read with the 9:03 PT pack. All 14 `STATUS_SCHEDULED`. No flex deltas. Byes: CIN, DET, MIA, MIN.

| Game | Kick PT | ESPN |
| --- | --- | --- |
| SEA @ DEN | Thu 10/15 5:15pm | 2026-10-16 00:15 UTC |
| HOU @ JAX (Wembley; JAX home) | Sun 10/18 6:30am | 13:30 UTC |
| CHI @ ATL, BAL @ CLE, TEN @ IND, NYJ @ NE, NO @ NYG, CAR @ PHI, PIT @ TB | Sun 10/18 10:00am | 17:00 UTC |
| ARI @ LAR | Sun 10/18 1:05pm | 20:05 UTC |
| LAC @ KC, BUF @ LV | Sun 10/18 1:25pm | 20:25 UTC |
| DAL @ GB | Sun 10/18 5:20pm | 2026-10-19 00:20 UTC |
| WAS @ SF | Mon 10/19 5:15pm | 2026-10-20 00:15 UTC |

## Main lines (mids, 9:03 PT compare)

American in this table is the compare file's mid, not the taker ask on the ticket.

| Game | PM spread mid | Novig same contract | PM total mid | Novig total mid |
| --- | --- | --- | --- | --- |
| SEA @ DEN | SEA −2.5 0.538 (−116) | 0.538 (−116) | Over 40.5 0.502 | 0.502 |
| HOU @ JAX | HOU +2.5 0.472 (+112) | 0.480 (+108) | Over 42.5 0.502 | 0.502 |
| CHI @ ATL | CHI −3.5 0.468 (+114) | 0.463 (+116) | Over 49.5 0.497 | 0.490 |
| BAL @ CLE | BAL −4.5 0.497 (+101) | 0.510 (−104) | Over 41.5 0.482 | 0.470 |
| TEN @ IND | TEN +6.5 0.468 (+114) | 0.468 (+114) | Over 44.5 0.482 | 0.480 |
| NYJ @ NE | NYJ +6.5 0.468 (+114) | 0.468 (+114) | Over 43.5 0.515 | 0.510 |
| NO @ NYG | NO −1.5 0.472 (+112) | 0.475 (+111) | Over 45.5 0.490 | 0.490 |
| CAR @ PHI | CAR +1.5 0.528 (−112) | 0.525 (−111) | Over 41.5 0.505 | 0.502 |
| PIT @ TB | PIT −2.5 0.502 (−101) | 0.502 (−101) | Over 40.5 0.497 | 0.492 |
| ARI @ LAR | ARI +12.5 0.497 (+101) | 0.492 (+103) | Over 52.5 0.497 | 0.495 |
| LAC @ KC | LAC +8.5 0.508 (−103) | 0.512 (−105) | Over 42.5 0.487 | 0.487 |
| BUF @ LV | BUF −5.5 0.502 (−101) | 0.497 (+101) | Over 53.5 0.497 | 0.502 |
| DAL @ GB | DAL +1.5 0.512 (−105) | 0.512 (−105) | Over 53.5 0.495 | 0.482 |
| WAS @ SF | WAS +7.5 0.497 (+101) | WSH +7.5 0.505 (−102) | Over 50.5 0.502 | 0.508 |

## Fees

- Polymarket US taker: fee = 0.0695 × contracts × p × (1 − p). About 1.74¢ per $1 contract at 50¢. Confirmed on [docs.polymarket.us/fees](https://docs.polymarket.us/fees) this session. Taker θ is unchanged. Rebate tiers move at 1:00pm ET on Oct 19; this paper desk is Tier 1 (no taker rebate). Ticket math uses the taker ask, not the maker rebate.
- Novig pregame straights: fee 0 on app and API. Catalog still says coefficient 0.03 charged `WHEN_LIVE`, which is 0 while status is `OPEN_PREGAME`. Live straights are 0.03. Source: [Novig Help Center](https://support.novig.com/en/articles/16195057-fees-on-novig), page updated the week of this lock.
- Same contract, same side. Novig wins a tie or a gap inside the PM fee. On these three tickets Novig also had the lower raw ask.

## Injuries cited

Wire file: `research/20261013-0903-pt-nfl-week6-x-injury-news.json`. ESPN scoreboard and the parent injury pack.

- **BAL @ CLE (ticket 02 gate):** Lamar Jackson, ankle. ESPN status Out. Minter, Monday: doing better, Wednesday practice unclear. Oct 12 roundup: Questionable. Annotate. Shadow-void on a quarterback change.
- **CHI @ ATL (not ticketed):** Caleb Williams, hamstring, ESPN Out. Rapoport/roundup: could return, practice pending. Michael Penix ribs, Schefter Oct 12 12:13pm PT: not considered serious, might play, practice first. Also a −3.5 lay, skipped.
- **PIT @ TB (not ticketed):** Baker Mayfield, thumb, OUT Week 6. Consistent across ESPN and the Oct 12 roundup.
- **DAL @ GB:** Micah Parsons not expected to practice this week. Schefter Oct 12 10:30am PT.
- **WAS @ SF:** Deebo Samuel multi-week hamstring. Pearsall season-ending PCL. Schefter Oct 12 12:26pm PT. Dre Greenlaw suspended one game. Schefter Oct 12 11:02am PT. Marcus Mariota is Out on the Washington list in the parent pack.
- **Other slate notes, not tickets:** TreVeyon Henderson high ankle, multi-week (Schefter Oct 13 7:16am PT). David Montgomery groin, week-to-week (Schefter Oct 12). Anton Harrison expected knee scope after London (Rapoport Oct 13 4:01am PT). Marvin Harrison Jr. to Houston pending physical (Rapoport Oct 12 11:05am PT). Carson Schwesinger Grade 1 ankle and Quinshon Judkins day-to-day (Rapoport Oct 12 11:23am PT).

TNF estimated report (Seahawks.com, Monday): Jaxon Smith-Njigba limited ankle, Zach Charbonnet unlikely, Pat Surtain II and Talanoa Hufanga estimated DNP. No Thursday ticket. Final TNF designations are Wednesday.

## One-shot schedule

Times are America/Los_Angeles. Each run is paper only: re-pull the same contract, write the snapshot, do not place, queue, or fund.

| Name | When | Cron (PT) | Prompt |
| --- | --- | --- | --- |
| nfl-w6-pre-tnf-refresh | Thu Oct 15, 4:00pm | `0 16 15 10 *` | Refresh Week 6 paper locks before TNF (SEA @ DEN, 5:15pm PT). Re-pull Polymarket US and Novig for PAPER-NFL-W6-01/02/03 only, same side and line. Note injury designations. Do not order. If a price moved, write a new snapshot and leave the 9:10am lock unchanged until Tim says to replace it. |
| nfl-w6-injury-late | Fri Oct 16, 3:00pm | `0 15 16 10 *` | Week 6 injury-late gate. Read the Friday practice report for Lamar Jackson (BAL @ CLE) and Caleb Williams / Michael Penix (CHI @ ATL). If the Ravens' Week 6 quarterback designation changed, mark PAPER-NFL-W6-02 shadow-void and say so. Do not order. Do not add a CHI −3.5 or SF −7.5 ticket. |
| nfl-w6-close-sun-10am | Sun Oct 18, 9:15am | `15 9 18 10 *` | Same-contract close for PAPER-NFL-W6-02 only (BAL @ CLE Over 41.5, Novig and the PM slug). Kick is 10:00am PT. Save close American on that line. Do not order. |
| nfl-w6-close-snf | Sun Oct 18, 4:45pm | `45 16 18 10 *` | Same-contract close for PAPER-NFL-W6-01 only (DAL @ GB Over 53.5). Kick is 5:20pm PT. Do not order. |
| nfl-w6-close-mnf | Mon Oct 19, 4:30pm | `30 16 19 10 *` | Same-contract close for PAPER-NFL-W6-03 only (WAS @ SF Under 50.5). Kick is 5:15pm PT. Do not order. |
| nfl-w6-grade-tue | Tue Oct 20, 7:30am | `30 7 20 10 *` | Grade Week 6 after Monday night, not Monday morning. Week 5 missed MNF when the grade ran Monday. Settle PAPER-NFL-W6-01/02/03 from the ESPN final score on the same contract. Fill hit, P/L, Brier, and CLV where the close exists. Then ask Tim the weekly reassessment: keep A+B+C unless the evidence says otherwise. Do not order. |

## Reassessment for Tim

Keep A+B+C. This slate did not clear a model or fee gate, and the Elo wire is still the Week 5 TODO, so the plan stays. Keep the injury-late annotate / shadow-void (Lamar and Caleb Williams are the live case). Keep CLV and Brier as the primary scores. Grade Tuesday morning after MNF.
