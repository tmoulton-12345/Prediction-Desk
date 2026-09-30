# Sources for the 2026-09-29 betting-methods pack

**Parent:** [20260929-betting-improvement-methods.md](20260929-betting-improvement-methods.md)
**Access date:** 2026-09-29, unless a source's own date is the point (shutdowns, fee effective dates).
**Rule for this list:** primary papers and operator documents first. Vendor pages describe products. Affiliate reviews are omitted except one OddsJam price that this pack refused to treat as confirmed.

| # | Source | URL | Use | Caution |
| --- | --- | --- | --- | --- |
| 1 | Kelly 1956, *Bell System Technical Journal* 35(4) | Bibliographic. Widely reprinted from the BSTJ. | Kelly fraction theorem | The fraction assumes the edge is known |
| 2 | Benter 1994 handicapping report | https://gwern.net/doc/statistics/decision/1994-benter.pdf | Shop pattern: model, blend with public odds, fractional Kelly | Horse-pool results. The PDF is a circulating copy, not the Academic Press typeset |
| 3 | Sauer 1998, *JEL* 36(4) | https://ideas.repec.org/a/aea/jeclit/v36y1998i4p2021-2064.html | Survey: prices forecast; informed flow improves them | Survey, not a trading system |
| 4 | Levitt 2004, *Economic Journal* 114(495) | https://pricetheory.uchicago.edu/levitt/Papers/LevittHowDoMarketsFunction2004.pdf | Books shade toward public bias | One NFL dataset. NBER twin: https://www.nber.org/papers/w9422 |
| 5 | Shin 1993, *Economic Journal* 103(420) | Bibliographic (DOI 10.2307/2234240) | De-vig with more margin on longshots | \(z\) is a model parameter, not a headcount of insiders |
| 6 | Štrumbelj 2014, *IJF* 30(4) | https://doi.org/10.1016/j.ijforecast.2014.02.008 | Shin beat basic normalization; gap shrinks in large markets | Odds quality varies by book |
| 7 | Brier 1950, *Monthly Weather Review* 78(1) | Bibliographic | Brier score | — |
| 8 | Gneiting & Raftery 2007, *JASA* 102 | https://doi.org/10.1198/016214506000001437 | Proper scores (Brier, log) | Author PDF: https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf |
| 9 | Dixon & Coles 1997, *JRSS-C* 46(2) | https://doi.org/10.1111/1467-9876.00065 | Poisson score model and a 1990s betting test | Historical return |
| 10 | Maher 1982, *Statistica Neerlandica* 36(3) | https://doi.org/10.1111/j.1467-9574.1982.tb00782.x | Independent Poisson goals | — |
| 11 | Karlis & Ntzoufras 2003, *The Statistician* 52(3) | Bibliographic | Bivariate Poisson | — |
| 12 | Baio & Blangiardo 2010, *J. Applied Statistics* 37(2) | Bibliographic | Hierarchical Bayes for football | Soccer, not NFL |
| 13 | Glickman 1999 Glicko paper | https://www.glicko.net/research/glicko.pdf | Glicko | — |
| 14 | Glickman & Stern 1998, *JASA* | https://glicko.net/research/nfl.pdf | NFL state-space point model | Fit on older seasons |
| 15 | Yurko, Ventura & Horowitz, nflWAR | https://arxiv.org/abs/1802.00998 | Public EPA method. Journal DOI https://doi.org/10.1515/jqas-2018-0010 | Player WAR needs participation data |
| 16 | Hubáček, Šourek & Železný 2019, *IJF* 35(2) | https://doi.org/10.1016/j.ijforecast.2019.01.001 | Residual-to-the-book ML design. Author PDF http://ida.felk.cvut.cz/zelezny/pubs/ijf.2019.pdf | NBA 2007–2014. Costs and limits are thin |
| 17 | Lopez, Matthews & Baumer 2018, *AOAS* | https://doi.org/10.1214/18-AOAS1165 | How often the best team wins. PDF https://scholarworks.smith.edu/mth_facpubs/49/ | Uses betting markets as inputs |
| 18 | Borghesi 2008, NFL totals and weather | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2149710 | Weather vs totals, 1984–2004 | May already be in the price |
| 19 | Borghesi 2007, temperature and spreads | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2149682 | Acclimatization vs the spread | Same caveat |
| 20 | Jehue, Street & Huizenga 1993, *MSSE* 25(1) | https://doi.org/10.1249/00005768-199301000-00017 | NFL travel and kickoff time, 1978–1987 | Old; commented on in the same journal in 1993 |
| 21 | Kim & King 2014, *Management Science* 60(11) | Bibliographic | Umpire status bias | A feature, not a total system |
| 22 | Hvattum & Arntzen 2010, *IJF* 26(3) | Bibliographic | Elo on football match results | Soccer |
| 23 | Elo 1978, *The Rating of Chessplayers* | Book | Original Elo | — |
| 24 | Chen & Guestrin 2016, XGBoost, *KDD* | Bibliographic | Boosting software | A library paper, not a betting result |
| 25 | Ke et al. 2017, LightGBM, *NeurIPS* | Bibliographic | Boosting software | Same |
| 26 | Prokhorenkova et al. 2018, CatBoost, *NeurIPS* | Bibliographic | Boosting software | Same |
| 27 | Wolfers & Zitzewitz 2004, *JEP* 18(2) | Bibliographic | Prediction markets as probability tools | Economics survey |
| 28 | Snowberg & Wolfers 2010, *JPE* 118(4) | Bibliographic | Favorite–longshot bias | Another reason Shin exists |
| 29 | Pinnacle CLV essay | https://www.pinnacle.com/betting-resources/en/educational/what-is-closing-line-value-clv-in-sports-betting | Operator definition of CLV | The page also sells Pinnacle |
| 30 | Polymarket US fees | https://docs.polymarket.us/fees | Theta 0.0695 from 2026-09-25 12:00 a.m. ET; combo curve; table-tennis change noted for 2026-09-30 | Re-read on card day |
| 31 | Polymarket international fees | https://docs.polymarket.com/trading/fees | Sports fee rate 0.05 on that product | Wrong document for Polymarket US |
| 32 | Novig fees | https://support.novig.com/en/articles/16195057-fees-on-novig | Pregame straight 0; live 0.03; futures 0.06; parlay 0.10; makers 0 | Page said "updated over 2 weeks ago" |
| 33 | The Odds API | https://the-odds-api.com/ | 500 free credits; $30/20k; $59/100k; $119/5M; $249/15M. History from 2020-06-06 on paid plans | Confirm the price page before paying. Docs: https://the-odds-api.com/liveapi/guides/v4/ and https://the-odds-api.com/historical-odds-data/ |
| 34 | theoddsapi.com (different site) | https://theoddsapi.com/pricing | Name collision. Their own $0/$29/$99 list and a 2026-05-13 archive start | Do not mix with row 33 |
| 35 | NFL Elo code | https://github.com/fivethirtyeight/nfl-elo-game/blob/master/forecast.py | K=20, home 65, revert 1/3 | Recipe, not a live feed |
| 36 | Wayback, Introducing NFL Elo | https://web.archive.org/web/20171004105151/https://fivethirtyeight.com/features/introducing-nfl-elo-ratings/ | Narrative of the Elo choices | Archive snapshot from 2017 |
| 37 | Guardian, 538 shutdown | https://www.theguardian.com/us-news/2025/mar/05/abc-news-538-shut-down | Site closed 2025-03-05 | News report |
| 38 | nflfastR | https://nflfastr.com/ and https://github.com/nflverse/nflfastR | NFL play-by-play and EPA | — |
| 39 | cfbfastR manual | https://sportsdataverse.r-universe.dev/cfbfastR/doc/manual.html | College PBP. Needs a CFBD key | Key stays out of git |
| 40 | Baseball Savant search | https://baseballsavant.mlb.com/statcast_search | Statcast | pybaseball scrapes it: https://github.com/jldbc/pybaseball |
| 41 | penaltyblog | https://github.com/martineastwood/penaltyblog/ | Dixon-Coles in Python | Soccer library |
| 42 | mberk/shin | https://github.com/mberk/shin | Shin implementation with paper links | Small library. Re-test inside this repo before trusting a CLV number |
| 43 | FTN DVOA explainer | https://ftnfantasy.com/learn-more-about-dvoa | What DVOA claims to measure | Proprietary. Prefer nflfastR for a number we can recompute |
| 44 | Unabated pricing | https://tools.unabated.com/pricing | Tiers listed at $99, $199, and $799 per month | Marketing page. Annual Premium figure also at https://unabated.com/post/benefits-of-unabated-premium-membership ($199/mo or $1,584/yr). Re-check |
| 45 | RebelBetting pricing | https://www.rebelbetting.com/pricing | Starter $99/mo ($69 annual rate); Pro $209/mo ($139 annual rate) | Direct fetch returned 403; figures are from the page text retrieved in search the same day. Re-check |
| 46 | Bet Angel compare | https://www.betangel.com/trader/compare/ | £5 and £12.50 per month | Betfair software. Out of venue scope |
| 47 | OddsJam +EV and arb essays | https://oddsjam.com/betting-education/positive-ev-betting-how-and-why-to-bet-based-on-the-market and https://oddsjam.com/betting-education/arbitrage-betting-faqs | What the vendor claims | Profit anecdotes. A third-party review's $99/$199 prices were not confirmed and are not budgeted |
| 48 | Smartodds privacy policy | https://www.smartodds.co.uk/privacy-policy/ | Firm describes itself as a private modelling shop | Clients are a small professional set |
| 49 | Smartodds execution-research job | https://www.smartodds.co.uk/jobs/quantitative-analyst-execution-research/ | Shops do market-making research on books, exchanges, and prediction markets | A hiring ad |
| 50 | Kaggle log-loss rules | https://www.kaggle.com/competitions/mens-machine-learning-competition-2018/overview/evaluation | Contest metric | Bracket contest, not a book |
| 51 | HIGFormer preprint | https://arxiv.org/abs/2507.10626 | A real GNN match-outcome paper (Wyscout) | Preprint. No closing-line test |
| 52 | Betfair developer | https://developer.betfair.com/ | Exchange API exists | Research only for this desk |
| 53 | Sportradar | https://sportradar.com/ | Enterprise feed | No public shelf price retrieved |
| 54 | Stats Perform | https://www.statsperform.com/ | Opta / enterprise | Same |
| 55 | Paper log schema | `docs/paper-log-schema.md` | `clv`, `brier`, `log_loss` columns | In repo |
| 56 | Ops brief | `docs/OPS.md` | Scope and refuse list | In repo |
| 57 | Trade card | `schemas/trade-card.md` | Arb-gate fields | In repo |
| 58 | Fee code and tests | `scripts/math_fees_arb.py`, `scripts/test_math_fees_arb.py` | Theta 0.0695 and Novig coefficients already tested | In repo |
| 59 | CFB/NFL scorecard | `research/20260926-1626-pt-cfb-nfl-paper-scorecard.md` | 2–2, −$3.64 on $80 | NFL tickets were open at that pull |
| 60 | Agent rules | `AGENTS.md` | Paper first; quant in code; Jev is a gate | In repo |
