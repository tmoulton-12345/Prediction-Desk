# Sources for the 2026-09-27 MLB Sunday paper pack

**Stamped:** 2026-09-26 7:15 p.m. Pacific Time. **Revised:** 2026-09-26 7:18 p.m. PT.
**Window:** reads from about 7:04 p.m. to 7:13 p.m. PT on 2026-09-26, except where a page prints its own clock.
**Phase 0:** Public reads only. No order was placed.

ESPN's site API was not used. The MLB Stats API answered. Public X posts were not used as injury, lineup, or price evidence.

## Schedule, parks, pitchers, standings, recent scores

| What | URL | When |
| --- | --- | --- |
| Sunday schedule, probables, records, empty weather object | https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-27&hydrate=probablePitcher,team,venue,weather | about 7:04 p.m. PT |
| Lineup hydrate, still empty | https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-27&hydrate=lineups,probablePitcher | about 7:13 p.m. PT |
| Venue roof and coordinates | https://statsapi.mlb.com/api/v1/venues/{id}?hydrate=location,fieldInfo,timezone | about 7:05 p.m. PT |
| 2026 season pitching lines for the 22 listed probables | https://statsapi.mlb.com/api/v1/people?personIds=640455,687792,669358,695684,607259,554430,682227,453286,663738,683003,689981,647336,579328,669302,669022,665152,607536,641743,702275,676083,669467,694819&hydrate=stats(group=[pitching],type=[season],season=2026) | about 7:05 p.m. PT |
| Standings, runs, clinch flags | https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&season=2026&standingsTypes=regularSeason | about 7:08 p.m. PT. Record `lastUpdated` values on that payload run from 2026-09-26T21:39:55Z to 2026-09-27T02:06:01Z |
| Division names for ids 200-205 | https://statsapi.mlb.com/api/v1/divisions/{id} | about 7:13 p.m. PT |
| Finals from 2026-09-17 through 2026-09-26 | https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=2026-09-17&endDate=2026-09-26&hydrate=linescore,team | about 7:08 p.m. PT |

## Weather

National Weather Service forecast endpoints, read about 7:10 p.m. PT. The update time is the forecast's own `updateTime`.

| Park | Points URL | Forecast update |
| --- | --- | --- |
| Yankee Stadium | https://api.weather.gov/points/40.8292,-73.9265 | 2026-09-26T19:21:52Z |
| Nationals Park | https://api.weather.gov/points/38.8729,-77.0075 | 2026-09-26T23:53:12Z |
| Oracle Park | https://api.weather.gov/points/37.7784,-122.3894 | 2026-09-26T20:26:51Z |
| Sutter Health Park | https://api.weather.gov/points/38.5799,-121.5125 | 2026-09-26T21:00:46Z |
| Citizens Bank Park | https://api.weather.gov/points/39.9054,-75.1672 | 2026-09-26T20:11:13Z |
| Kauffman Stadium | https://api.weather.gov/points/39.0516,-94.4805 | 2026-09-26T22:41:50Z |
| Comerica Park | https://api.weather.gov/points/42.3391,-83.0487 | 2026-09-26T20:26:16Z |
| Petco Park | https://api.weather.gov/points/32.7079,-117.1573 | 2026-09-26T19:53:11Z |
| Target Field | https://api.weather.gov/points/44.9818,-93.2779 | 2026-09-26T23:12:14Z |
| Rate Field | https://api.weather.gov/points/41.8300,-87.6342 | 2026-09-26T19:46:09Z |
| American Family Field | https://api.weather.gov/points/43.0284,-87.9710 | 2026-09-27T01:31:57Z |
| T-Mobile Park | https://api.weather.gov/points/47.5913,-122.3325 | 2026-09-26T18:26:46Z |
| loanDepot park | https://api.weather.gov/points/25.7780,-80.2195 | 2026-09-26T20:17:42Z |

Rogers Centre points lookup `43.6416,-79.3892` returned HTTP 404. No Toronto forecast is cited.

## Consensus sportsbook boards

| Board | URL | Clock |
| --- | --- | --- |
| Covers MLB odds (moneyline, run line, total). Page text: "Last updated Sep 26, 2026, 10:06 PM ET." | https://www.covers.com/sport/baseball/mlb/odds | Page clock is 7:06 p.m. PT. Fetched in the same window. |
| CBS Sports MLB odds board for Sun Sep 27 | https://www.cbssports.com/mlb/odds/ | Fetched about 7:06 p.m. PT. The page does not print a separate update clock. Several Sunday rows are dashes. |

Covers' first book column is the consensus number used when a sportsbook price is named. American odds in the pack that start from a Covers fraction are converted from the fraction printed on that page (9/10 is -111, 8/7 is +114, 7/10 is -143, 13/11 is +118, 5/6 is -120, 1/3 is -300, 43/17 is +253). The page also prints a decimal next to the fraction.

CBS rows that this pack uses, as the converter showed them: Mets -110 / Nationals +100, Mets -1.5 +146, total cell o8 -120 and u8.5 -114. Orioles +115 / Yankees -134, Yankees -1.5 +158, Orioles +1.5 -182, total cell o7.5 -104 and u8 -108. Rays +126 / Phillies -132. Reds +150 / Blue Jays -172. Pirates -122 / Tigers +109, Pirates -1.5 +129. Angels +160 / Mariners -186. Braves -108 / Marlins -108, Braves -1.5 +152, total o8.5 -120. Rockies +183 / White Sox -196, White Sox -1.5 +105, total cells o8.5 -105 and u8.5 -112. Cardinals +205 / Brewers -238, Brewers -1.5 +101. Blank rows: Cubs-Red Sox, Astros-Athletics, Dodgers-Giants, Guardians-Royals, Rangers-Twins, Diamondbacks-Padres.

The CBS total column does not always print the same number on both rows. Where that happens, the total used for a pick is the Covers number, and CBS is quoted beside it.

Pages that were opened and not used as the card, because they conflict with the MLB probable feed or with each other: FanDuel Research Orioles-Yankees and Mets-Nationals notes, a CBS gametracker that lists Carlos Rodón for the Yankees, an ESPN Singapore preview that lists Blake Snell and Matt Wilkinson for Sunday's Dodgers-Giants game (Covers shows that pair on the Saturday final), a FOX Sports box page that lists Matt Boyd and Patrick Sandoval for Cubs-Red Sox, and Doc's Sports moneyline blurbs whose records do not match the standings feed.

## Polymarket US and Novig

Both venues list MLB. Catalogs were read with the repo's public GET helpers. No order route was called.

| What | URL | When |
| --- | --- | --- |
| League list, MLB slug `mlb` is operational | https://gateway.polymarket.us/v2/leagues | about 7:05 p.m. PT |
| MLB events, limit 100, 15 Sunday games inside the PT day | https://gateway.polymarket.us/v2/leagues/mlb/events?limit=100 | about 7:06 p.m. PT |
| Novig events, league MLB, startsAfter 1790492400000, startsBefore 1790578800000 | https://api.novig.us/v3/public/catalog/events?league=MLB&startsAfter=1790492400000&startsBefore=1790578800000&limit=100 | about 7:06 p.m. PT |
| Novig markets, types SPREAD,TOTAL,MONEY, 216 open full-game markets | https://api.novig.us/v3/public/catalog/markets?league=MLB&marketType=SPREAD,TOTAL,MONEY&startsAfter=1790492400000&startsBefore=1790578800000&limit=5000 | about 7:06 p.m. PT |
| Novig books | https://api.novig.us/v3/public/catalog/markets/{marketId}/book | about 7:07 p.m. to 7:12 p.m. PT |

Polymarket US prices in the pack are executable asks: best ask on the long side, and one minus the best bid on the short side. The fee coefficient on the Sunday full-game markets that were read is 0.0695. Novig's fee object on these markets is coefficient 0.03, charged `WHEN_LIVE`, so a pregame take is treated as $0. Novig asks are one minus the other outcome's best bid. Void text on the Novig markets is `FMV`. Polymarket descriptions say a game that does not finish and is not replayed inside two weeks settles to the last fair price. This pack does not treat the two void rules as the same contract.

Snapshot of the prices used: `snapshots/20260926-1915-pt-mlb-sunday-lines.json`.

## Desk line files, then a live check

The local desk attached four files. They are the line source this revision starts from.

| File | What it actually contains |
| --- | --- |
| Schedule markdown, stamp about 7:04 p.m. PT | 15 games, probables, and an explicit Tropicana vs Fenway warning |
| Schedule raw JSON | Same 15 games. Cubs at Red Sox gamePk 824705, description "at Tropicana Field", venue id 12 |
| `20260926-1905-pt-mlb-sunday-espn-core-odds` | 15 event ids. Every row is a parser error: `'$ref'` on 9 games and `list index out of range` on 6. No prices in the file. |
| `20260926-1905-pt-mlb-sunday-espn-dk-odds` | ESPN odds page, DraftKings widget, section "Sunday, September 27", 9 games with ML, run line, and total |

The core file was not ignored. It has no numbers to quote. The widget file does. A live read of the same DraftKings feed on the ESPN scoreboard, at 7:18 p.m. PT, confirms those 9 games and still returns no `odds` array on the 6 that the core file marked `list index out of range`.

https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates=20260927

Provider on every priced row: DraftKings. Clean extract: `snapshots/20260926-1918-pt-mlb-sunday-espn-dk-lines.json`.

Widget vs live scoreboard, same provider, about 13 minutes apart. Totals and run lines on the widget match the live close except where noted.

| Game | Widget 7:05 p.m. PT | Live scoreboard 7:18 p.m. PT |
| --- | --- | --- |
| Rays ML | +109 / Phillies -132 | +113 / Phillies -137 |
| Phillies -1.5 | +163 | +167 |
| White Sox -1.5 | -102 | -105 |
| Rockies +1.5 | -118 | -115 |

Everything else on the 9-game widget matches the live close, including Mets run line OFF, Yankees total 8, Phillies total 7, Pirates total 8, Brewers total 7, Mariners total 7.

## What was missing on DraftKings

No DraftKings moneyline, run line, or total on the live scoreboard for: Cubs at Red Sox (Tropicana, neutral, rescheduled from 9/26), Astros at Athletics, Dodgers at Giants, Guardians at Royals, Rangers at Twins, Diamondbacks at Padres. Those six totals stay MISSING. No number was filled in. Sides on those six use Polymarket US or Novig and are labeled venue-only.

Novig has no full-game spread book for Dodgers-Giants, Cubs-Red Sox, Astros-Athletics, Guardians-Royals, or Diamondbacks-Padres. The Rangers-Twins 1.5 market was listed with no bids. Polymarket US and Novig do list MLB. They are not empty.
