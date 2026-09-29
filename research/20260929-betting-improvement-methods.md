# Betting improvement methods — Phase 0 research pack

**Date:** Tuesday, September 29, 2026
**Web sources accessed:** 2026-09-29
**Desk:** Tim Moulton / Prediction Desk. Phase 0 paper dry-runs on college football, NFL, and MLB.
**Venues for any future new risk:** Polymarket US and Novig only. Kalshi sports and politics stay out. International Polymarket stays close-only.
**This page is:** a process research memo. It is not legal advice, not a Tim-approve trade card, not an order, and not a claim that any method has a proven edge.

Companion URL index: [20260929-betting-improvement-methods-sources.md](20260929-betting-improvement-methods-sources.md).

Deterministic fee, de-vig, and staking math belongs in tested code (`scripts/math_fees_arb.py` and future unit tests). Figures below that check the recent paper sample are arithmetic on stated stakes, so a reader can see the sample size. They are not a sizing sheet.

## Executive summary

The recent paper run is too small to judge a method. The operator's stated ledger is about 5 wins and 10 losses, roughly −$112 on $300 staked. At a flat $20 risked to win $18.18 (American −110), five wins and ten losses settle at \(5 \times 18.18 - 10 \times 20 = -109.10\). A few prices shorter than −110 cover the gap to −$112. The committed scorecard in this repo grades only the Saturday college tickets that were final at pull time: 2–2, −$3.64 on $80, which is the −110 hold on a 50 percent hit rate (`research/20260926-1626-pt-cfb-nfl-paper-scorecard.md`). NFL tickets on that card were still open. Break-even at −110 is \(110/210 \approx 52.38\) percent. Five wins in fifteen tries is 33 percent. The standard error of a coin-flip rate at \(n = 15\) is about 13 percentage points. That sample can describe a cold week. It cannot identify skill, and it cannot clear a method.

Serious shops measure a price against the market, then size only after the probability is calibrated. The public record of that craft is old and specific: Bill Benter's 1994 Hong Kong report combined a fundamental model with the public's implied probabilities and then staked with a fractional Kelly rule, after years of database work. Pinnacle teaches closing line value (CLV) as the skill score. Peer-reviewed work says wagering prices are, to a first approximation, efficient forecasts, that price changes improve those forecasts, and that "who won" is a noisy grade because even the best team is far from a lock (Sauer 1998; Lopez, Matthews, and Baumer 2018). Proper scores for a probability are the Brier score and the log score (Brier 1950; Gneiting and Raftery 2007). Kaggle's March Machine Learning Mania contest grades log loss for the same reason.

For this desk, the next month of process return comes from recording, on every paper ticket, the contract identity, the fee, a devigged probability, the closing price on the venue that could actually be traded, and a Brier score after the game. The paper log schema already has `clv`, `brier`, and `log_loss` columns. They are the unused part of the system. A model earns a lean only when its Brier beats the devigged venue price on the same tickets. Hit rate by conference is a slice printed with its sample size. It is a poor kill-switch inside thirty days.

Build that loop in-repo. Keep stakes flat. Add one pre-registered baseline per sport (an Elo or points model for NFL, a run model for MLB, an Elo for college) and log it beside the market. Buy a closing-odds history only if Tim wants a US-book benchmark the public venue reads do not already store; the long-running vendor is `the-odds-api.com`, about $30 a month for the 20,000-credit plan as listed on that site on 2026-09-29. Leave OddsJam, Unabated, RebelBetting, and Bet Angel on the shelf for this phase. They screen sportsbooks this desk is not using for new risk, and several of them market the screen as profit.

Refuse auto-bet loops, wash trading, parlays, full Kelly, an LLM as the price, and any sentence that calls an edge proven. Jev remains a completeness gate after the card is packed. It does not pick the side.

## How evidence is graded

| Grade | Meaning in this pack |
| --- | --- |
| High | Peer-reviewed result, or a primary document whose formula can be re-derived and tested |
| Moderate | Reproducible public method, or an operator essay that is also an advertisement for the operator's book |
| Low | Single backtest, preprint that never faces a closing line, or a rule of thumb |
| Vendor | The page sells the product it describes. Useful for what the tool is. Weak as proof it makes money |

Fit is for **this** desk: Phase 0 paper, college football / NFL / MLB, new-risk venues Polymarket US and Novig, Cursor cloud as a research bench, attention ranked behind CalmBinderPress and Website Landlord.

## What the recent paper sample can support

| Fact | Figure | Where it comes from |
| --- | --- | --- |
| Operator-stated recent paper | 5–10, about −$112 on $300 staked | Brief for this pack. The fifteen tickets are not reconstructed here. |
| Arithmetic at −110, five wins, ten losses, $20 flat | −$109.10 | \(20 \times 100/110 = 18.18\) per win, the same convention as `scripts/paper_grade.py` |
| In-repo graded slice | CFB 2–2, −$3.64 on $80 | `research/20260926-1626-pt-cfb-nfl-paper-scorecard.md`, pull 2026-09-26 4:26 p.m. PT |
| Break-even hit rate at −110 | 52.38 percent | \(110/210\). Borghesi (2008) uses this threshold in the NFL totals literature |
| Coin-flip standard error at n = 15 | about 13 points | \(\sqrt{0.5 \times 0.5 / 15}\) |

A 2–2 Saturday at −110 losing $3.64 is the price of the hold when the hit rate is 50 percent. The larger 5–10 figure is a worse draw from the same family of bets. The process response is a better scorecard, with pre-registered probabilities, so the next fifteen tickets can be graded against the market price. A new story fitted to these fifteen results would chase noise.

## 1. Methods catalog

| Method | What it is | Evidence | Fit for this desk | Cost / effort |
| --- | --- | --- | --- | --- |
| Closing line value (CLV) | Compare the price taken with the price of the same contract just before the event, after removing margin. Positive CLV means the ticket beat the close. | Moderate–high. Pinnacle's education page defines it and sells Pinnacle as the place to practice it. Sauer (1998) finds that informed order flow moves prices and that those moves improve forecasts. | High. Make it the weekly score. Use the Polymarket US or Novig close as the executable close. A Pinnacle or US-book close is a benchmark only. | Low. Schema fields exist. Needs a timestamped close and a locked de-vig. |
| De-vig (basic and Shin) | Turn two-way odds into probabilities. Basic normalization divides implied probabilities by their sum. Shin's model (1991–1993) puts more of the overround on longshots. | High. Štrumbelj (2014) found Shin probabilities forecast better than basic normalization across bookmakers; the gap shrinks in large markets. | High. NFL spreads near 50/50 barely move. MLB moneylines and futures do. Lock one method in code and store the name on the row. | Low. Unit tests next to `scripts/test_math_fees_arb.py`. Open implementation: `mberk/shin`. |
| Line shopping | Take the best price on one contract across books that will actually deal. | High as arithmetic. The hold is smaller when the price is better. Levitt (2004) shows books also shade prices toward public bias, so "the consensus number" is a blend of skill and demand. | High inside Polymarket US vs Novig, and as a read of a public book. The MLB Sunday pack already found venue totals (7.5, 8.5) that were a different contract from a DraftKings 8. | Low. A compare table with an explicit "same number?" flag. |
| Market-making | Post both sides, earn the spread, manage inventory and adverse selection. | High as a description of Pinnacle and of exchanges. Smartodds hires researchers to study market-making and execution. That is a firm with staff, models, and flow. | Out for Phase 0. This desk is a paper taker with Tim-approve on any live order. | A trading stack, cancel latency, and inventory rules. Forbidden here as an auto loop. |
| Steam | A fast multi-book move, often off a market-making book, read as informed flow. | Moderate. Sauer's review supports "late money improves the forecast." The retail habit of chasing the move after it prints often buys the close. | Medium as a logged feature (open, mid, close, and which book moved first). Low as a trigger to fire. | Needs a history of prices. Public venue snapshots first. |
| Sharp vs square signals | Ticket counts, "public %" bars, and outlier-book flags sold as smart money. | Low for ticket percentages. Levitt's NFL dataset showed bookmakers beating the public by shading the price, and little evidence of bettors who systematically beat the book. Dollars and tickets diverge. | Low. Log a public-% read only beside the price. An outlier price is a candidate for the compare table, then a fee check. | Action Network-style products. Skip until the close log exists. |
| Consensus vs outlier books | Average of many books versus one book far from that average. | Moderate. Fragmented books do post different numbers. Whether the outlier is a mistake or a sharper view depends on which book and on the close. | Medium as a benchmark. The executable question is the Polymarket US and Novig price after fees. | A multi-book snapshot. Optional paid odds API. |
| Power ratings and Elo | One number per team. Win probability from the rating gap, usually a logistic curve. Update after each game. | High as a baseline. Elo (1978). FiveThirtyEight's NFL recipe is in public code: K = 20, home field 65 Elo points, revert one-third to the mean between seasons (`fivethirtyeight/nfl-elo-game`). Glicko (Glickman 1999) adds uncertainty. Hvattum and Arntzen (2010) used Elo on football results. | High as the first model, logged beside the market. College needs a larger home term and dies on tiny samples. | A few hundred lines and public results. The live FiveThirtyEight site shut down on 2025-03-05; use the GitHub recipe and the Wayback copy. |
| Glicko / Glicko-2 | Elo plus a rating deviation, so a team with few games stays uncertain. | High for the rating math (Glickman 1999, 2001). | Medium. Worth it in college, where schedules are short and uneven. Extra moving parts versus plain Elo. | Glickman's papers are public. Implement after plain Elo is logging. |
| Bayesian state-space / hierarchical | Team strength wanders week to week and season to season. Home advantage can vary. | High. Glickman and Stern (1998) on NFL point margin. Lopez, Matthews, and Baumer (2018) fit the same family with betting-market data across NFL, NBA, NHL, and MLB. Baio and Blangiardo (2010) is the hierarchical Bayesian football (soccer) version. | Medium-high as the "serious" NFL/MLB team model after Elo is boring and measured. Heavy for a 30-day paper loop. | Stan or a Kalman filter. Days of careful code, then a season to judge. |
| Poisson / Dixon-Coles / negative binomial | Model goals or runs as counts. Dixon-Coles adds a low-score correction and time decay. Negative binomial allows extra variance. | High for soccer scores (Maher 1982; Dixon and Coles 1997; Karlis and Ntzoufras 2003). Dixon and Coles reported a positive return on 1995–96 English odds; that is a historical result, not a 2026 price. | Medium for MLB totals. Low for NFL points, which are not Poisson counts. College totals are high-variance. | `penaltyblog` implements Dixon-Coles in Python. Use it as a library to study, with tests, on a sport whose scores match the model. |
| Pythagorean expectation | Season run differential turned into a win rate. Bill James's baseball baseline. | Moderate-high as a team-strength prior. It ignores the probable pitcher and today's price. | Medium as an MLB prior that then yields to the market price. | Trivial once runs are in a table. |
| EPA / DVOA-style efficiency | Value each play against a situational baseline, then adjust for opponent. | High for EPA as a public, reproducible stat: Yurko, Ventura, and Horowitz (2019), implemented in nflfastR. DVOA is the proprietary cousin, now documented by FTN. | Medium. Strong NFL features. They describe teams. The bet is the residual versus the posted number. | nflverse is free. DVOA itself is a paid FTN product. Prefer nflfastR. |
| Player-prop models | A distribution for a player counting stat, a playing-time model, and a posted line. | Low as a published beating-the-close result. The count-model math is the same family as Poisson / negative binomial. Prop closes are noisy and the line (3.5 vs 4.5) changes the contract. | Later. Data-hungry. Easy to leak playing time. | High. Defer past 90 days except when a paper ticket is already a prop and needs a complete card. |
| Fractional Kelly and flat stakes | Kelly (1956) sizes a bet to maximize long-run log wealth when the edge and the odds are known. Fractional Kelly shrinks that fraction because the edge is estimated. | High for the theorem. High for the warning: Benter used a fractional rule after a model that had already beaten the public odds. Full Kelly with a wrong probability overbets. | High. Flat $20 paper stakes until a model beats the market Brier out of sample. A quarter-Kelly column can be computed and ignored. | The formula is short. The hazard is feeding it a made-up edge. Keep it in tested code. |
| Correlation and parlays | Kelly and "add the edges" assume bets that do not share a factor. Same-game parlays share the game. A Saturday of weather unders shares the forecast. | High as portfolio math. Novig's own fee page prices parlays at coefficient 0.10, inside the quote, and states parlays cannot be taken through the API. | Out for Phase 0 staking. A single study ticket may be logged so the correlation is visible. | The fee is the expensive part. The variance is the rest. |
| Arbitrage | Buy every side for less than the payout, after fees. | High as arithmetic, already in `scripts/math_fees_arb.py`. Low as a durable business: books limit accounts, quotes move, and both legs must fill. | Low. Paper-scan only, with the arb-gate fields on the trade card (same event, same line, overtime and void rules, settlement match). Novig HTTP 201 queued is an accepted order, not a fill. | Code exists. Blind retry is forbidden. |
| Middling | Bet both sides of a number that moved, so a result in the gap wins both. | Moderate as a description. Requires two fills, a real gap, and matched settlement. A 7.5 at one venue and an 8 at another are different contracts, which the Sunday MLB notes already treated as such. | Low. Log the gap. Paper both sides only when the rules match. | Same as arb, plus the push rules. |
| Injury and news latency | A material fact reaches a price with a delay. | Moderate. The mechanism is real. The half-life on a liquid book is short. Official designations (NFL.com injury table, team sites, MLB probables) beat a paraphrase. | Medium. A timestamped checklist on the card. The price model stays numeric. | Manual at this volume. An LLM can extract fields from a quoted report. |
| Weather | Heat, wind, and rain lower NFL scoring. Temperature also shows up in spread errors in older samples. | Moderate. Borghesi, *Applied Financial Economics* (2008), on totals, 1984–2004, with an out-of-sample win rate above 52.38 percent in that study. Borghesi, *Journal of Economics and Business* (2007), on temperature and the spread. Markets may have absorbed this since. | Medium for NFL and MLB totals, as a pre-registered feature joined to a forecast from weather.gov, which this desk already reads. | Low. The test is the residual versus the total, logged before the lean. |
| Rest and travel | Short weeks and coast-to-coast trips move win rates in older NFL samples. West Coast teams were strong in night games in 1978–1987. | Moderate and old. Jehue, Street, and Huizenga, *Medicine & Science in Sports & Exercise* 25(1), 1993, on 1978–1987 win-loss records. A letter under the same title ran in the same journal later that year (25(11), 1298–1299). | Low-medium. One binary feature (short week, cross-country, night). Grade it against the market residual. | Low to log. Easy to overfit. |
| Umpire / referee tendencies | Called-zone size and status bias shift balls, strikes, and run environments. | Moderate for the existence of umpire differences (Kim and King, *Management Science*, 2014, on status bias). Low as a standalone total rule. Samples per umpire-week are thin. | Low until MLB paper volume is large. If used: Baseball Savant called-pitch data, shrunk toward the league, joined after the assignment is official, compared with the price. | Medium. Defer the model. Log the plate umpire name when the card is a total. |

### Notes that cut across the catalog

**CLV needs a definition this desk can actually settle.** Record two closes when both exist:

1. Executable close: last Polymarket US or Novig price on that contract before the scheduled start, after the fee that would have applied to a taker.
2. Benchmark close: a devigged US-book or Pinnacle number for the same statistic (spread −3.5, total 44.5, moneyline). Label the book.

Beating a book the desk will not bet is a research result. It becomes a fill only on a venue in scope, at a size that was resting, with the fee included. Pinnacle's CLV essay (accessed 2026-09-29) tells readers to bet early and to treat a beaten close as skill. That is operator education from a low-margin book. Use the definition. Treat the promise of long-run profit as their claim.

**Steam and "sharp money" are easy to fake in a newsletter.** The durable version is a stored path of prices. If the path is missing, the word "steam" does not go on the card.

**The market price is the default forecast.** Benter's practical contribution was a second-stage combination of his handicapping probabilities with the public's implied probabilities. Lopez and collaborators' 2014 March Madness winner blended the point spread with possession stats in a logistic regression. A model that ignores the posted number is arguing with a summary of everyone else's information.

## 2. AI and ML models

| Model / approach | Typical use | Caveats |
| --- | --- | --- |
| Logistic regression | Win probability from a rating gap, a market price, and a few pre-registered features. The Kaggle-winning college basketball pattern. | The right first supervised model. It will look boring. That is the point. Time-ordered split. |
| Gradient boosting (XGBoost, LightGBM, CatBoost) | Tabular residuals: efficiency stats, rest, weather, pitcher, market probability as a feature. nflfastR already uses XGBoost inside some expected-yard models. | Chen and Guestrin (2016); Ke and coauthors (2017); Prokhorenkova and coauthors (2018) are the software papers. They do not show a sportsbook edge. Leakage (training on the close, scoring against the close) manufactures a fake CLV. Fit only after the Elo baseline is logging. |
| Random forests | Same tabular job, often worse than boosting, more stable to tune badly. | A reasonable baseline inside an ensemble. Rarely the model that changes a decision here. |
| Elo / Glicko update rules | Online team ratings without a heavy fit. | Under-react to a quarterback change unless that is an explicit input. College samples are short. |
| Poisson, Dixon-Coles, negative binomial, hierarchical Bayes | Scorelines and team strengths, mostly soccer and run environments. | Dixon and Coles' 1990s betting return is not a license. MLB run totals can use the count family. NFL scoring needs a points or margin model (Glickman and Stern). |
| LSTM or Transformer on the odds path | Sequence models that try to forecast the next price or the game from the line history. | Low evidence that they beat "the latest price" as a forecast of the game. The latest price already summarizes the path. Publishing a profit usually means the close leaked into the features. |
| Graph neural nets on players | Papers such as HIGFormer (arXiv:2507.10626, 2025) predict soccer results from player-team graphs on Wyscout data. Most other GNN soccer papers detect passes and events from tracking, which is a different task. | Preprint. Tracking data this desk does not have. No demonstrated gain versus a closing line after fees. Out of the 90-day build. |
| LLM (news summary, injury parse) | Turn a quoted injury report or weather discussion into structured fields: player, status, source URL, timestamp. | Real as a parser. A hallucinated "out" is worse than silence. Require the source sentence in the row. The probability stays in the numeric model. |
| LLM as the price | Ask a chat model who covers. | Hype. It has no locked de-vig, no fee, and no calibration. Refuse as the forecast. |
| Ensembles | Average a market probability with one statistical probability, or stack them in a logistic layer fit on past games. | Average only after both numbers are probabilities. Refit the stack on a past window. Grade on a later window. |
| Calibration | Reliability bins, Brier, log loss. A constant 0.5 forecast scores Brier 0.25. | At n = 15, one bin is the whole chart. Report the score anyway so the habit exists. Hit rate hides a model that is confident and wrong. |
| Accuracy ("who wins") | Share of tickets on the right side of the number. | Secondary. A 53 percent side at −110 can lose money. A 50 percent side that always beat the close can be the better process. Lopez, Matthews, and Baumer (2018) put the median chance that the best team wins a neutral-site game near 64 percent in the NFL and 56 percent in MLB, which is why one Saturday lies. |

### Named public reference points

- **FiveThirtyEight NFL Elo.** Recipe in `github.com/fivethirtyeight/nfl-elo-game` (`forecast.py`: home field 65, K = 20, one-third reversion). The 538 site was shut down on 2025-03-05 (Guardian, 2025-03-05). Cite the code and the Wayback copy of "Introducing NFL Elo Ratings," not a live 538 article URL.
- **Pinnacle Betting Resources.** Primary operator essays on CLV and on how a low-margin book thinks. Read them as the bookmaker's account.
- **Benter (1994).** "Computer Based Horse Race Handicapping and Wagering Systems: A Report," in the Hausch, Lo, and Ziemba volume on racetrack efficiency. The shop pattern: fundamental model, then a logit blend with public odds, then fractional Kelly, then years of operations. Horse racing is a parimutuel pool. The pattern transfers. The edge does not.
- **Hubáček, Šourek, and Železný (2019),** *International Journal of Forecasting*. They decorrelated an NBA model from the bookmaker's odds on purpose, used a convolutional net on player stats, and sized with a portfolio rule. The profit is on 2007–2014 odds. Limits, voids, and fees are thinner in the paper than on a live venue. Read it as a design (residual versus the book, plus sizing), with the profit claim left in 2014.
- **Kaggle March Machine Learning Mania.** Log loss on tournament games. The contest teaches the metric. It does not pay a sportsbook.
- **Štrumbelj (2014).** How to turn odds into probabilities, and the finding that bookmakers differ, with the gap shrinking as the market gets large.

## 3. Research types and data sources

| Source | What it actually is | Access on 2026-09-29 | Role here |
| --- | --- | --- | --- |
| Polymarket US public gateway | `https://gateway.polymarket.us`. Fee schedule at `https://docs.polymarket.us/fees`. | Theta 0.0695 on standard taker fees, exchange-wide from 12:00 a.m. ET on 2026-09-25. Maker rebate −0.0125. Banker's rounding to the cent. Combo taker fee is a steeper curve. A table-tennis coefficient change was scheduled for 2026-09-30. | In-scope venue. Fee code in this repo already uses 0.0695. Re-read the page on the day of any card. International `docs.polymarket.com` listed a sports fee rate of 0.05 on the same day. That page is a different product. |
| Novig Help Center, fees | `https://support.novig.com/en/articles/16195057-fees-on-novig` | Updated "over 2 weeks" before 2026-09-29. Pregame straight taker fee 0. Live straight taker 0.03. Futures taker 0.06. Parlay 0.10 inside the quote. Makers 0. Parlays cannot be taken via the API. | In-scope venue. Historical CSVs at `https://data.novig.com` per `docs/OPS.md`. |
| The Odds API (`the-odds-api.com`) | Multi-book odds, including a historical snapshot endpoint. | Homepage listed 500 credits free, then $30 / 20k, $59 / 100k, $119 / 5M, $249 / 15M credits per month. Historical odds from 2020-06-06 (10-minute, then 5-minute from September 2022) on paid plans, at 10 credits per region per market. | Best paid option if Tim wants US-book closes. Confirm the live price page before subscribing. |
| `theoddsapi.com` (no hyphens) | A different site with its own $0 / $29 / $99 tiers and an archive it dates from 2026-05-13. | Seen in search on 2026-09-29. | Name collision. Do not treat it as the vendor above. |
| OddsJam, Action Network public pages | Odds screens, "positive EV," arbitrage copy, betting splits. | OddsJam's own education pages describe outlier books as mistakes and advertise user profits. That is vendor copy. | See software table. Skeptical. |
| Betfair Exchange | A real exchange. API docs at `https://developer.betfair.com/`. | Primary for exchange microstructure. | Research benchmark only. New risk stays on Polymarket US and Novig. |
| Sportradar, Opta / Stats Perform | Enterprise event and tracking feeds. | `https://sportradar.com/`, `https://www.statsperform.com/`. No public shelf price retrieved. | Shop infrastructure. Out of proportion for this desk's next 90 days. |
| ESPN scoreboard and MLB Stats API | Schedules, status, linescores, probables. | Already used in this repo's packs and in `scripts/paper_grade.py`. | Grade paper tickets. Official status (`STATUS_FINAL`) before a hit/miss. |
| NFL.com injury table and schedules | Designations and kickoffs. | Used in the Week 3 pack. A blank game-status cell stays blank. | Injury checklist. |
| Baseball Savant | MLB Statcast search, expected stats, pitch-level calls. `https://baseballsavant.mlb.com/statcast_search` | Public. `pybaseball` wraps it and is a scraper, so pin a version and expect breakage. | MLB features after the team-run baseline. |
| nflfastR / nflverse | NFL play-by-play and EPA. `https://nflfastr.com/`, `https://github.com/nflverse/nflfastR` | CRAN package, MIT license. | NFL efficiency features. |
| cfbfastR and CollegeFootballData | College play-by-play. cfbfastR wraps the CFBD API and needs a key (`register_cfbd`). | Package manual current on r-universe. | College EPA once Elo is logging. Key stays out of git. |
| Baseball-Reference, Basketball-Reference, FanGraphs, Retrosheet, Pro Football Reference | Public season and historical stats. | Standard. | Priors and audits. `pybaseball` and `baseballr` scrape several of them. |
| weather.gov | National Weather Service point forecasts. | Already cited in the MLB Sunday sources file. | Weather feature. Store the issuance time. |
| X / social | Posts about injuries, "sharp action," and weather. | No stable feed was added for this pack. | Alarm only. A ticket field waits for the official report. Sentiment studies in other markets have a poor replication record. Public posting is part of what the price already reflects. |
| Scraped line history (OddsPortal and similar) | Convenient open-to-close grids. | Often against the site's terms, delayed, and wrong on the number. | Avoid as a system of record. Prefer this desk's own timestamped public reads, Novig's historical CSVs, and a paid odds API if Tim approves one. |

## 4. Software

| Product | Category | Notes, as of the 2026-09-29 read |
| --- | --- | --- |
| OddsJam | Retail +EV and arbitrage screen across many sportsbooks | Vendor pages frame outlier prices as mistakes and publish profit anecdotes. A third-party 2026 review quotes about $99 and $199 per month. This pack did not confirm those numbers on an OddsJam pricing page, so they are not a budget. Poor fit: the books it screens are outside new-risk scope, and the marketing is the kind this desk refuses to repeat. |
| Unabated | Odds screens, a house "Unabated Line," prop simulators, NFL futures tools | Vendor pricing page listed monthly tiers at $99 (Props+), $199, and $799. An Unabated post described Premium at $199 per month or $1,584 billed annually. Re-check before any spend. Useful only if the question is "what are many market-makers posting?" The desk cannot take those prices as new risk. |
| RebelBetting | Value-bet and sure-bet scanner | Vendor pricing page: Starter $99 per month ($69 per month billed annually), Pro $209 per month ($139 per month billed annually). Same scope problem as OddsJam. Account limits are the product's own fine print in the category. |
| Bet Angel | Betfair trading terminal | Vendor compare page: Trader £5 per month, Professional £12.50 per month. Betfair execution software. Out of venue scope. |
| Action Network (including Pro) | Media, odds, public betting percentages | A newspaper of splits. Ticket share is a weak proxy for informed money (see Levitt). Price not confirmed in this pass. Optional later as a logged feature, with the percentage stored next to the price. |
| Smartodds | Professional modelling firm, London, founded 2004 | Their privacy policy and job posts describe statistical research and software for a small client set of professional bettors and football clubs, including execution research on books, exchanges, and prediction markets. This is a shop. It is not a seat license for Phase 0. |
| The Odds API | Developer odds feed | See section 3. The one paid feed that matches a "store the close" job. |
| Betfair API | Exchange connectivity | Docs only, for research. |
| Spreadsheet + CLV tracker | Manual | Enough for a month of paper tickets at this volume. Columns: contract key, price taken, fee, p_market, p_model, close, CLV, outcome, Brier. The repo schema is the same idea in JSONL. |
| Python, pandas, a later LightGBM, an odds read | Custom stack | The right 90-day shape. Phase 0 code in this repo stays public-fetch, paper grade, and fee math. No order module. |
| nflfastR, cfbfastR, pybaseball, penaltyblog, `mberk/shin`, `fivethirtyeight/nfl-elo-game` | Open source | Use these as libraries and as references. Pin versions. Keep API keys out of the repo. |
| Random GitHub "Kelly calculator" and "surebet" repos | Scripts of unknown quality | Reimplement the two formulas this desk needs, under unit tests. A copied staking bot is an auto-bet loop waiting for a key. |

## 5. Ranked process levers

Ranked by expected value to the **process** on this desk over the next month. "Expected value to the process" means faster learning and fewer donated mistakes per hour of attention. It is not a forecast of betting profit.

| Rank | Lever | Why it is this high | Effort |
| --- | --- | --- | --- |
| 1 | Fill CLV, Brier, and log loss on every paper ticket | The current grade is hit/miss and P/L, which at n = 15 mostly measures noise and the hold. The schema already reserved the columns. | Low |
| 2 | Same-contract check before a lean | A 7.5 and an 8 are different bets. The Sunday MLB pack hit this. It is the cleanest way to stop donating on a compare. | Low |
| 3 | Fee in the EV snapshot, re-read on the day | Polymarket US theta 0.0695 since 2026-09-25, with a different combo curve. Novig pregame straights at 0, parlays at 0.10. International Polymarket's 0.05 table is the wrong document. | Low. Code started. |
| 4 | Market probability as the baseline forecast | Shops blend into the price (Benter; the 2014 Kaggle winner). A model that cannot beat the market Brier stays in the log and off the lean. | Low to adopt as a rule. |
| 5 | Flat stakes; quarter-Kelly as a shadow column only | Full Kelly needs a true edge. This sample does not contain one. | Low |
| 6 | One pre-registered baseline per sport | NFL Elo or margin model, MLB run model, college Elo. Public data. Logged beside the market. | Medium |
| 7 | Lock the de-vig (basic and Shin, both stored) | CLV is incomparable if the margin method changes mid-month. Shin matters more on lopsided moneylines. | Low |
| 8 | Timestamped injury, weather, rest fields | Latency is a real mechanism and a tempting story. The field is filled before the lean, from an official source, with the clock. | Low |
| 9 | A correlation cap on the slate | Several weather unders, or two tickets on the same game, are one bet. The paper P/L then double-counts a single miss. | Low |
| 10 | A US-book close as a labeled benchmark | Tells you whether the venue price was the slow one. Optional $30 feed after Tim's yes. | Low money, some engineering |
| 11 | LightGBM or logistic residual, time-split, market price as a feature | The first ML step that matches the papers. After the baseline has a month of rows. | Medium. 90-day item. |
| 12 | Props, graph nets, sequence models, retail +EV terminals | Real literatures or real products, and a mismatch to this desk's data, venues, and sample size. | High spend or high leakage risk |

## 6. Build, buy, and leave

### Next 30 days — build

- A paper-row writer that fills the existing schema, plus sport, conference, market family, line, period, settlement source, de-vig name, and `p_market`.
- A close snapshot from the public Polymarket US and Novig reads already stubbed in `scripts/`. Stamp the time. Grade with `scripts/paper_grade.py`'s settlement rule (`STATUS_FINAL`).
- Unit-tested basic and Shin de-vig, next to the fee tests. No new order path.
- One Elo (or the public 538 NFL recipe) and one MLB runs baseline, output as probabilities, written onto the row.
- A one-page weekly scorecard: n, completeness, mismatch count, mean CLV, Brier of market, Brier of model, Brier of 0.5, hit rate, P/L.

### Next 30 days — buy only with an explicit yes

- `the-odds-api.com` at the published $30 / 20,000-credit tier, if the public venue snapshots are too thin to store a benchmark close. One month. No lookalike domain.

### Next 30 days — leave

- OddsJam, Unabated, RebelBetting, Bet Angel, Action Network Pro, Smartodds, Sportradar, Opta.
- Any scraper whose terms forbid the pull.
- Player-prop models, GNNs, and a transformer on the odds tape.

### Around 90 days — build if the log is complete

- A time-ordered backtest. Training rows end before the ticket's decision time. The closing price is a label for CLV, never a feature for the pick.
- A logistic or LightGBM model whose features include `p_market` and the pre-registered extras. Score log loss and Brier against the market on a later slice.
- A quarter-Kelly shadow. The paper stake stays flat unless a separate Tim decision changes the paper unit.
- Revisit a screen product only if the log shows a missing fact ("we cannot see the benchmark close") that the $30 feed did not fix.

## 7. Refuse

These stay refused in Phase 0, including when framed as a backtest, a bot, or a "proven" vendor result.

- Auto-submit, unsupervised order loops, and market-order auto fire.
- Wash trading or self-matching.
- A claim that this desk, a model, or a subscription has a proven edge. Fifteen tickets, a vendor testimonial, and an in-sample accuracy number do not carry that claim.
- An LLM as the probability.
- Parlays and same-game parlays as sized bets. Novig's parlay coefficient is 0.10 and the API will not take them.
- Arb or middle paper that skips fees, a mismatched number, overtime or void rules, or a Novig 201 that has not filled.
- Full Kelly.
- VPN, proxy, or location spoofing.
- Kalshi sports and politics while the court block holds. International Polymarket for new risk.
- Secrets in the repo: keys, cookies, `.env`.
- Jev as the picker. Jev checks completeness, risk, and reversibility after the state is packed.

## 8. Thirty-day experiment

Pre-register this before the next slate. Changing the grade after a bad Saturday is how the 5–10 record turns into a new story.

### Protocol

1. Every new paper ticket is one row. Flat paper risk $20, so P/L stays comparable to the recent ledger. Holds and refusals are rows too.
2. The row stores a contract key: venue, market id, sport, conference if college, market family, line, period, settlement source, decision time.
3. The row stores the price, the fee coefficient used that day, `p_market` from the locked de-vig, and `p_model` when a baseline ran. The skeptic line is filled in words. Jev may flag a missing field. Jev does not supply the probability.
4. A lean requires three yeses: the contract matches across every book named in the reason; the absolute gap between `p_model` and `p_market` exceeds the taker fee at that price; the skeptic line names a concrete way the lean is wrong.
5. If the baseline has not been fit yet, `p_model` stays empty and the lean stays a hold. The market price is still logged.
6. Near scheduled start, store the venue close. After `STATUS_FINAL`, store the outcome, CLV, Brier, and log loss.
7. Conference hit rate is printed with n. A conference sentence waits until that cell has at least 20 settled tickets.

### Scorecard metrics

| Metric | Definition | 30-day reading |
| --- | --- | --- |
| Completeness | Share of new rows with contract key, price, fee, sources, and a close or an explicit "close missing" reason | Target 100 percent. This is the pass/fail for the month. |
| Contract mismatches | Rows where two named numbers differ and the row still carries a lean | Target 0. |
| Brier, market | Mean \((p - y)^2\) using `p_market` and the 0/1 outcome | The number to beat. |
| Brier, model | The same, on rows where `p_model` was filled before the game | Useful when it is lower than the market Brier on those same rows. |
| Brier, constant 0.5 | 0.25 if scored that way on binary outcomes | The ignorant floor. |
| Log loss | Mean \(-\log p_y\), probabilities clipped away from 0 and 1 (Kaggle clips for the same reason) | Companion to Brier. Punishes confident misses. |
| Mean CLV | Mean of (probability taken − devigged close probability), sign set so positive means the ticket beat the close. Report n and a standard error. | A diagnostic. A positive month at this n is a description, not an edge. |
| Hit rate, overall and by conference | Wins / settled, with n | Descriptive. The −110 break-even marker is 52.38 percent. |
| Paper P/L | Flat $20, −110 convention unless the logged price says otherwise | Report beside the hold. A −4.5 percent ROI at a 50 percent hit rate is the juice. |
| Shadow quarter-Kelly | Computed, not staked | Inspect for absurd fractions, which flag a bad probability. |

### Decision rule at day 30

- The logging loop stays, whatever the P/L.
- A baseline that loses to the market on Brier remains a feature column.
- A baseline that beats the market Brier on the pre-registered rows earns another month of paper leans under the same flat stake.
- Nothing in the month authorizes a live order, a larger paper unit, a parlay, or a sentence that the desk has an edge.

### What would falsify the plan

- Closes cannot be stored reliably from public reads, and Tim declines a paid history. Then CLV waits, and the month grades Brier against the decision-time venue price only.
- Baselines are fit with the closing number in the feature list. Those rows are discarded.
- A conference or weather split is promoted because one weekend hit. That split goes back to "n too small."

## 9. Source list

Full URLs, access date 2026-09-29 unless noted. The companion file repeats these as a table with the caution on each.

### Primary literature

1. Kelly, J. L., Jr. (1956). A new interpretation of information rate. *Bell System Technical Journal*, 35(4), 917–926.
2. Benter, W. (1994). Computer based horse race handicapping and wagering systems: A report. In D. B. Hausch, V. S. Y. Lo, & W. T. Ziemba (Eds.), *Efficiency of Racetrack Betting Markets*. A circulating copy read for this pack: `https://gwern.net/doc/statistics/decision/1994-benter.pdf`
3. Sauer, R. D. (1998). The economics of wagering markets. *Journal of Economic Literature*, 36(4), 2021–2064. `https://ideas.repec.org/a/aea/jeclit/v36y1998i4p2021-2064.html`
4. Levitt, S. D. (2004). Why are gambling markets organised so differently from financial markets? *The Economic Journal*, 114(495), 223–246. Working-paper PDF: `https://pricetheory.uchicago.edu/levitt/Papers/LevittHowDoMarketsFunction2004.pdf` NBER w9422: `https://www.nber.org/papers/w9422`
5. Shin, H. S. (1993). Measuring the incidence of insider trading in a market for state-contingent claims. *The Economic Journal*, 103(420), 1141–1153.
6. Štrumbelj, E. (2014). On determining probability forecasts from betting odds. *International Journal of Forecasting*, 30(4), 934–943. `https://doi.org/10.1016/j.ijforecast.2014.02.008`
7. Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, 78(1), 1–3.
8. Gneiting, T., & Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *Journal of the American Statistical Association*, 102(477), 359–378. `https://doi.org/10.1198/016214506000001437` Author PDF: `https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf`
9. Dixon, M. J., & Coles, S. G. (1997). Modelling association football scores and inefficiencies in the football betting market. *Journal of the Royal Statistical Society Series C*, 46(2), 265–280. `https://doi.org/10.1111/1467-9876.00065`
10. Maher, M. J. (1982). Modelling association football scores. *Statistica Neerlandica*, 36(3), 109–118. `https://doi.org/10.1111/j.1467-9574.1982.tb00782.x`
11. Karlis, D., & Ntzoufras, I. (2003). Analysis of sports data by using bivariate Poisson models. *The Statistician*, 52(3), 381–393.
12. Baio, G., & Blangiardo, M. (2010). Bayesian hierarchical model for the prediction of football results. *Journal of Applied Statistics*, 37(2), 253–264.
13. Glickman, M. E. (1999). Parameter estimation in large dynamic paired comparison experiments. *Applied Statistics*, 48, 377–394. `https://www.glicko.net/research/glicko.pdf`
14. Glickman, M. E., & Stern, H. S. (1998). A state-space model for National Football League scores. *Journal of the American Statistical Association*, 93, 25–35. `https://glicko.net/research/nfl.pdf`
15. Yurko, R., Ventura, S., & Horowitz, M. (2019). nflWAR: a reproducible method for offensive player evaluation in football. *Journal of Quantitative Analysis in Sports*. arXiv: `https://arxiv.org/abs/1802.00998` DOI: `https://doi.org/10.1515/jqas-2018-0010`
16. Hubáček, O., Šourek, G., & Železný, F. (2019). Exploiting sports-betting market using machine learning. *International Journal of Forecasting*, 35(2), 783–796. `https://doi.org/10.1016/j.ijforecast.2019.01.001` Author PDF: `http://ida.felk.cvut.cz/zelezny/pubs/ijf.2019.pdf`
17. Lopez, M. J., Matthews, G. J., & Baumer, B. S. (2018). How often does the best team win? A unified approach to understanding randomness in North American sport. *Annals of Applied Statistics*. `https://doi.org/10.1214/18-AOAS1165` PDF: `https://scholarworks.smith.edu/mth_facpubs/49/`
18. Borghesi, R. (2008). Weather biases in the NFL totals market. *Applied Financial Economics*, 18(12), 947–953. SSRN: `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2149710`
19. Borghesi, R. (2007). The home team weather advantage and biases in the NFL betting market. *Journal of Economics and Business*, 59(4). SSRN: `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2149682`
20. Jehue, R., Street, D., & Huizenga, R. (1993). Effect of time zone and game time changes on team performance: National Football League. *Medicine & Science in Sports & Exercise*, 25(1), 127–131. `https://doi.org/10.1249/00005768-199301000-00017`
21. Kim, J. W., & King, B. G. (2014). Seeing stars: Matthew effects and status bias in Major League Baseball umpiring. *Management Science*, 60(11).
22. Hvattum, L. M., & Arntzen, H. (2010). Using ELO ratings for match result prediction in association football. *International Journal of Forecasting*, 26(3), 460–470.
23. Elo, A. E. (1978). *The Rating of Chessplayers, Past and Present*. Arco.
24. Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *KDD*.
25. Ke, G., et al. (2017). LightGBM: A highly efficient gradient boosting decision tree. *NeurIPS*.
26. Prokhorenkova, L., et al. (2018). CatBoost: unbiased boosting with categorical features. *NeurIPS*.
27. Wolfers, J., & Zitzewitz, E. (2004). Prediction markets. *Journal of Economic Perspectives*, 18(2), 107–126.
28. Snowberg, E., & Wolfers, J. (2010). Explaining the favorite–long shot bias: Is it risk-love or misperceptions? *Journal of Political Economy*, 118(4), 723–746.

### Operator documents, data, code, and products

29. Pinnacle, "What Is Closing Line Value (CLV) in Sports Betting?" `https://www.pinnacle.com/betting-resources/en/educational/what-is-closing-line-value-clv-in-sports-betting`
30. Polymarket US fee schedule. `https://docs.polymarket.us/fees`
31. Polymarket (international) trading fees, different coefficient table. `https://docs.polymarket.com/trading/fees`
32. Novig, "Fees on Novig." `https://support.novig.com/en/articles/16195057-fees-on-novig`
33. The Odds API homepage and v4 docs. `https://the-odds-api.com/` `https://the-odds-api.com/liveapi/guides/v4/` `https://the-odds-api.com/historical-odds-data/`
34. Lookalike domain, not the vendor in item 33. `https://theoddsapi.com/pricing`
35. FiveThirtyEight NFL Elo code. `https://github.com/fivethirtyeight/nfl-elo-game/blob/master/forecast.py`
36. Wayback of "Introducing NFL Elo Ratings." `https://web.archive.org/web/20171004105151/https://fivethirtyeight.com/features/introducing-nfl-elo-ratings/`
37. Guardian, 2025-03-05, on the 538 shutdown. `https://www.theguardian.com/us-news/2025/mar/05/abc-news-538-shut-down`
38. nflfastR. `https://nflfastr.com/` `https://github.com/nflverse/nflfastR`
39. cfbfastR manual. `https://sportsdataverse.r-universe.dev/cfbfastR/doc/manual.html`
40. Baseball Savant Statcast search. `https://baseballsavant.mlb.com/statcast_search`
41. pybaseball. `https://github.com/jldbc/pybaseball`
42. penaltyblog. `https://github.com/martineastwood/penaltyblog/`
43. Shin Python implementation and its references. `https://github.com/mberk/shin`
44. FTN, "Learn more about DVOA." `https://ftnfantasy.com/learn-more-about-dvoa`
45. Unabated pricing. `https://tools.unabated.com/pricing` and `https://unabated.com/post/benefits-of-unabated-premium-membership`
46. RebelBetting pricing. `https://www.rebelbetting.com/pricing`
47. Bet Angel compare. `https://www.betangel.com/trader/compare/`
48. OddsJam education pages (vendor). `https://oddsjam.com/betting-education/positive-ev-betting-how-and-why-to-bet-based-on-the-market` and `https://oddsjam.com/betting-education/arbitrage-betting-faqs`
49. Smartodds privacy policy (what the firm says it is). `https://www.smartodds.co.uk/privacy-policy/`
50. Smartodds quantitative analyst job post (execution and market-making research). `https://www.smartodds.co.uk/jobs/quantitative-analyst-execution-research/`
51. Kaggle March Machine Learning Mania evaluation (log loss). Example rules: `https://www.kaggle.com/competitions/mens-machine-learning-competition-2018/overview/evaluation`
52. HIGFormer preprint. `https://arxiv.org/abs/2507.10626`
53. Betfair developer docs. `https://developer.betfair.com/`
54. Sportradar. `https://sportradar.com/`
55. Stats Perform. `https://www.statsperform.com/`

### In this repo

56. `docs/paper-log-schema.md` — `clv`, `brier`, `log_loss` already defined.
57. `docs/OPS.md` — venue scope, refuse list, Novig public data.
58. `schemas/trade-card.md` — immutable card, arb-gate fields.
59. `scripts/math_fees_arb.py` and `scripts/test_math_fees_arb.py` — Polymarket US theta 0.0695 and Novig coefficients.
60. `research/20260926-1626-pt-cfb-nfl-paper-scorecard.md` — graded Saturday slice.
61. `AGENTS.md` — paper first, no auto-submit, quant in code, Jev as a gate.
