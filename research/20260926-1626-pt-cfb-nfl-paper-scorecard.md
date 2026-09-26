# CFB and NFL paper scorecard

**Stamp:** Saturday, September 26, 2026, 4:26 p.m. PT (2026-09-26T16:26:49-07:00)

Phase 0 paper scoring. Locked tickets compared with ESPN finals. No bets, no live orders, no Tim-approve card.

## Score pull

- Pull timestamp: 2026-09-26T16:26:49-07:00
- College board: [https://www.espn.com/college-football/scoreboard/_/date/20260926](https://www.espn.com/college-football/scoreboard/_/date/20260926)
- College API read of that board: `https://site.web.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20260926&limit=300`
- NFL board: [https://www.espn.com/nfl/scoreboard](https://www.espn.com/nfl/scoreboard) for dates 2026-09-26, 2026-09-27, and 2026-09-28
- Pick ledger: [CFB Top 25 Saturday Picks](https://app.notion.com/p/3e755ddfbc9f81f98298e59df16973ac) and [NFL Week 3 Picks](https://app.notion.com/p/3e755ddfbc9f814b9e57ea971521cc29)
- Notion names research/20260925-2132-pt-cfb-top25-sat-picks.md and research/20260926-1131-pt-paper-tickets-top5-cfb-nfl.md. Those files are not in this repo. Sides and lines are the Notion tables.

A ticket is graded only when ESPN marks the game `STATUS_FINAL` (completed, postgame). In-progress and scheduled games stay blank on Hit? and P/L. Spreads and totals use that final score. On this pull every graded game has four linescore quarters and no overtime period, so the regulation score and the final score are the same number.

Margin for a spread is `pick score + line − opponent score`. Margin for an under is `line − combined score`. Margin for an over is `combined score − line`. Above zero is a hit, zero is a push, below zero is a miss.

Money, settled tickets only: stake $20 at −110. A win pays `+$18.18` (`20 × 100 / 110`, half-up to the cent). A loss is `−$20`. A push is `$0`. ROI is net P/L divided by stake on settled tickets. The grader is `scripts/paper_grade.py`.

## Paper tickets

| Ticket | Market | Final score (Away, Home) | Margin vs line | Result | Hit? | P/L |
| --- | --- | --- | --- | --- | --- | --- |
| PAPER-CFB-01 | Total IOWA @ MICH Under 38.5 | IOWA 20, MICH 19 | -0.5 | L | miss | -$20.00 |
| PAPER-CFB-02 | Spread IOWA @ MICH IOWA +5.5 | IOWA 20, MICH 19 | +6.5 | W | hit | +$18.18 |
| PAPER-CFB-03 | Spread TEX @ TENN TENN +4.5 | TEX 20, TENN 17 | +1.5 | W | hit | +$18.18 |
| PAPER-CFB-04 | Total OKLA @ UGA Under 44.5 | OKLA 13, UGA 41 | -9.5 | L | miss | -$20.00 |
| PAPER-CFB-05 | Spread ORE @ USC USC +3 | not started | — | OPEN | — | — |

Market text above is the locked side. Kick times from the Notion ticket table: CFB-01 and CFB-02 at 12:30 p.m. PT, CFB-03 at 9:00 a.m. PT, CFB-04 at 12:30 p.m. PT, CFB-05 at 4:30 p.m. PT.

## CFB summary

Settled tickets only: **2 wins, 2 losses, 0 pushes.** Net P/L **-$3.64** on **$80** staked. ROI **-4.55%**.

Open and not in that ROI: 1 ticket still scheduled, 0 in progress, 0 unknown.

| Ticket | Result | P/L |
| --- | --- | --- |
| PAPER-CFB-01 | L | -$20.00 |
| PAPER-CFB-02 | W | +$18.18 |
| PAPER-CFB-03 | W | +$18.18 |
| PAPER-CFB-04 | L | -$20.00 |
| PAPER-CFB-05 | OPEN | — |

## CFB Top 25 Saturday slate

One spread and one total per game, in the Notion rank order. Hit? is filled only for `STATUS_FINAL`. A live score is context and is not a grade.

### Spreads

| Rank | Game | Pick | Status | Score | Margin vs line | Hit? |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | IOWA @ MICH | IOWA +5.5 | FINAL | IOWA 20, MICH 19 | +6.5 | hit |
| 2 | TEX @ TENN | TENN +4.5 | FINAL | TEX 20, TENN 17 | +1.5 | hit |
| 3 | ORE @ USC | USC +3 | OPEN | not started | — | — |
| 4 | OM @ FLA | OM +3.5 | FINAL | OM 28, FLA 52 | -20.5 | miss |
| 5 | TAMU @ LSU | TAMU +9.5 | OPEN | not started | — | — |
| 6 | OKLA @ UGA | OKLA +13.5 | FINAL | OKLA 13, UGA 41 | -14.5 | miss |
| 7 | WAKE @ LOU | WAKE +12.5 | FINAL | WAKE 30, LOU 27 | +15.5 | hit |
| 8 | ILL @ OSU | ILL +27.5 | FINAL | ILL 19, OSU 42 | +4.5 | hit |
| 9 | ND @ PUR | PUR +27.5 | FINAL | ND 49, PUR 10 | -11.5 | miss |
| 10 | WIS @ PSU | WIS +10 | IN_PROGRESS | in progress WIS 10, PSU 20 | — | — |
| 11 | UTAH @ ISU | UTAH -7.5 | FINAL | UTAH 31, ISU 17 | +6.5 | hit |
| 12 | SC @ ALA | SC +12.5 | IN_PROGRESS | in progress SC 0, ALA 0 | — | — |
| 13 | MIZ @ MSST | MSST -6 | OPEN | not started | — | — |
| 14 | HOU @ GASO | HOU -18.5 | FINAL | HOU 42, GASO 28 | -4.5 | miss |
| 15 | CMU @ MIA | CMU +41.5 | IN_PROGRESS | in progress CMU 3, MIA 14 | — | — |
| 16 | SHSU @ TTU | SHSU +34.5 | FINAL | SHSU 14, TTU 49 | -0.5 | miss |
| 17 | MOST @ SMU | MOST +34.5 | OPEN | not started | — | — |

Final spreads: 5 hit, 5 miss, 0 push (10 final, 3 in progress, 4 not started).

### Totals

| Rank | Game | Pick | Status | Score | Margin vs line | Hit? |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | IOWA @ MICH | Under 38.5 | FINAL | IOWA 20, MICH 19 | -0.5 | miss |
| 2 | OKLA @ UGA | Under 44.5 | FINAL | OKLA 13, UGA 41 | -9.5 | miss |
| 3 | ND @ PUR | Under 57.5 | FINAL | ND 49, PUR 10 | -1.5 | miss |
| 4 | WIS @ PSU | Under 44.5 | IN_PROGRESS | in progress WIS 10, PSU 20 | — | — |
| 5 | ORE @ USC | Under 61.5 | OPEN | not started | — | — |
| 6 | UTAH @ ISU | Under 49.5 | FINAL | UTAH 31, ISU 17 | +1.5 | hit |
| 7 | TEX @ TENN | Under 54.5 | FINAL | TEX 20, TENN 17 | +17.5 | hit |
| 8 | ILL @ OSU | Under 53.5 | FINAL | ILL 19, OSU 42 | -7.5 | miss |
| 9 | SC @ ALA | Over 54.5 | IN_PROGRESS | in progress SC 0, ALA 0 | — | — |
| 10 | OM @ FLA | Over 58.5 | FINAL | OM 28, FLA 52 | +21.5 | hit |
| 11 | TAMU @ LSU | Under 51.5 | OPEN | not started | — | — |
| 12 | WAKE @ LOU | Over 58.5 | FINAL | WAKE 30, LOU 27 | -1.5 | miss |
| 13 | MIZ @ MSST | Over 58.5 | OPEN | not started | — | — |
| 14 | HOU @ GASO | Over 56.5 | FINAL | HOU 42, GASO 28 | +13.5 | hit |
| 15 | CMU @ MIA | Under 55 | IN_PROGRESS | in progress CMU 3, MIA 14 | — | — |
| 16 | SHSU @ TTU | Under 55.5 | FINAL | SHSU 14, TTU 49 | -7.5 | miss |
| 17 | MOST @ SMU | Under 59.5 | OPEN | not started | — | — |

Final totals: 4 hit, 6 miss, 0 push (10 final, 3 in progress, 4 not started).

Slate hit counts are a research tally. They are not added to the $20 ticket P/L.

### Live and scheduled notes

- ORE @ USC: OPEN (Sat, September 26th at 7:30 PM EDT). Current: no score.
- TAMU @ LSU: OPEN (Sat, September 26th at 7:30 PM EDT). Current: no score.
- WIS @ PSU: IN_PROGRESS (End of 3rd Quarter). Current: WIS 10, PSU 20.
- SC @ ALA: IN_PROGRESS (8:21 - 1st Quarter). Current: SC 0, ALA 0.
- MIZ @ MSST: OPEN (Sat, September 26th at 7:45 PM EDT). Current: no score.
- CMU @ MIA: IN_PROGRESS (12:35 - 2nd Quarter). Current: CMU 3, MIA 14.
- MOST @ SMU: OPEN (Sat, September 26th at 9:00 PM EDT). Current: no score.

## NFL paper tickets

ESPN NFL scoreboard event counts at this pull: Sep 26 `0`, Sep 27 `14`, Sep 28 `1`. Saturday has no NFL games. Sunday and Monday games are `STATUS_SCHEDULED`. None are final, so every NFL ticket stays OPEN with Hit? and P/L blank.

| Ticket | Market | Kick (PT) | ESPN status | Result | Hit? | P/L |
| --- | --- | --- | --- | --- | --- | --- |
| PAPER-NFL-01 | Spread SEA @ WAS SEA -7.5 | Sun 10:00 a.m. PT | Sun, September 27th at 1:00 PM EDT | OPEN | — | — |
| PAPER-NFL-02 | Total TEN @ NYG Under 37.5 | Sun 10:00 a.m. PT | Sun, September 27th at 1:00 PM EDT | OPEN | — | — |
| PAPER-NFL-03 | Spread PHI @ CHI PHI -3.5 | Mon 5:15 p.m. PT | Mon, September 28th at 8:15 PM EDT | OPEN | — | — |
| PAPER-NFL-04 | Total SEA @ WAS Under 39.5 | Sun 10:00 a.m. PT | Sun, September 27th at 1:00 PM EDT | OPEN | — | — |
| PAPER-NFL-05 | Spread LAC @ BUF BUF -7.5 | Sun 10:00 a.m. PT | Sun, September 27th at 1:00 PM EDT | OPEN | — | — |

Kick notes, from the ESPN start time and the Notion ticket table:

- PAPER-NFL-01 and PAPER-NFL-04, Seahawks at Commanders: Sunday, September 27, 10:00 a.m. PT (ESPN 1:00 p.m. EDT, `2026-09-27T17:00Z`). ESPN short name `SEA @ WSH`; the ticket abbreviation is WAS.
- PAPER-NFL-02, Titans at Giants: Sunday, September 27, 10:00 a.m. PT (same 1:00 p.m. EDT window).
- PAPER-NFL-05, Chargers at Bills: Sunday, September 27, 10:00 a.m. PT (same window).
- PAPER-NFL-03, Eagles at Bears: Monday, September 28, 5:15 p.m. PT (ESPN 8:15 p.m. EDT, `2026-09-29T00:15Z`).

## Sources for graded games

| Game | ESPN id | Status | Box score |
| --- | --- | --- | --- |
| IOWA @ MICH | 401858463 | STATUS_FINAL / Final | https://www.espn.com/college-football/boxscore/_/gameId/401858463 |
| TEX @ TENN | 401856704 | STATUS_FINAL / Final | https://www.espn.com/college-football/boxscore/_/gameId/401856704 |
| ORE @ USC | 401858469 | STATUS_SCHEDULED / Sat, September 26th at 7:30 PM EDT | https://www.espn.com/college-football/boxscore/_/gameId/401858469 |
| OM @ FLA | 401856699 | STATUS_FINAL / Final | https://www.espn.com/college-football/boxscore/_/gameId/401856699 |
| TAMU @ LSU | 401856702 | STATUS_SCHEDULED / Sat, September 26th at 7:30 PM EDT | https://www.espn.com/college-football/boxscore/_/gameId/401856702 |
| OKLA @ UGA | 401856700 | STATUS_FINAL / Final | https://www.espn.com/college-football/boxscore/_/gameId/401856700 |
| WAKE @ LOU | 401858243 | STATUS_FINAL / Final | https://www.espn.com/college-football/boxscore/_/gameId/401858243 |
| ILL @ OSU | 401858465 | STATUS_FINAL / Final | https://www.espn.com/college-football/boxscore/_/gameId/401858465 |
| ND @ PUR | 401858467 | STATUS_FINAL / Final | https://www.espn.com/college-football/boxscore/_/gameId/401858467 |
| WIS @ PSU | 401858466 | STATUS_IN_PROGRESS / End of 3rd Quarter | https://www.espn.com/college-football/boxscore/_/gameId/401858466 |
| UTAH @ ISU | 401856816 | STATUS_FINAL / Final | https://www.espn.com/college-football/boxscore/_/gameId/401856816 |
| SC @ ALA | 401856696 | STATUS_IN_PROGRESS / 8:21 - 1st Quarter | https://www.espn.com/college-football/boxscore/_/gameId/401856696 |
| MIZ @ MSST | 401856703 | STATUS_SCHEDULED / Sat, September 26th at 7:45 PM EDT | https://www.espn.com/college-football/boxscore/_/gameId/401856703 |
| HOU @ GASO | 401856806 | STATUS_FINAL / Final | https://www.espn.com/college-football/boxscore/_/gameId/401856806 |
| CMU @ MIA | 401858238 | STATUS_IN_PROGRESS / 12:35 - 2nd Quarter | https://www.espn.com/college-football/boxscore/_/gameId/401858238 |
| SHSU @ TTU | 401856805 | STATUS_FINAL / Final | https://www.espn.com/college-football/boxscore/_/gameId/401856805 |
| MOST @ SMU | 401858241 | STATUS_SCHEDULED / Sat, September 26th at 9:00 PM EDT | https://www.espn.com/college-football/boxscore/_/gameId/401858241 |

Team abbreviations in the tables match the ticket ledger. ESPN's own abbreviations differ for Oklahoma (`OU`, shown as OKLA), Ole Miss (`MISS`, shown as OM), Texas A&M (`TA&M`, shown as TAMU), and Washington (`WSH`, shown as WAS).

