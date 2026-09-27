# MLB Sunday paper picks: 2026-09-27

**Stamped:** 2026-09-26 7:15 p.m. Pacific Time. **Revised:** 2026-09-26 7:18 p.m. PT.
**Desk:** Prediction Desk for Tim Moulton. Phase 0 paper dry run.
**Line source:** DraftKings via ESPN. The desk widget (9 games, stamp 7:05 p.m. PT) is the attached board. A live scoreboard read at 7:18 p.m. PT is the check. Where those two differ, the live close is the DraftKings number and the widget number is shown beside it. The attached core-odds JSON has 15 event ids and zero prices (parser errors only).
**Slate:** 15 games. Each has a side. Nine have a DraftKings total. Six totals are MISSING because DraftKings posted no number, and Polymarket US and Novig did not post a full-game total either.
**This is not a live bet.** No order is placed, queued, or requested. Nothing here is a guaranteed edge, a profit claim, or a legal opinion.

Schedule: `research/20260926-1915-pt-mlb-sunday-schedule.md`
Research: `research/20260926-1915-pt-mlb-sunday-pack.md`
Sources: `research/20260926-1915-pt-mlb-sunday-sources.md`
DraftKings extract: `snapshots/20260926-1918-pt-mlb-sunday-espn-dk-lines.json`
Venue asks: `snapshots/20260926-1915-pt-mlb-sunday-lines.json`

## How a price was chosen

The consensus number is the DraftKings close on ESPN. Polymarket US and Novig both list this MLB slate. They are not empty. An ask on those books is the price to buy that side. Polymarket US fee coefficient on these markets is 0.0695, applied as coefficient times price times (1 minus price). Novig's fee is `WHEN_LIVE` only, so a pregame take is $0. If either venue lists the same side and the same line at a better price after that fee, the card uses the venue. If DraftKings has the line OFF or has no odds row, the card says so and uses the venue. A different total (6.5 versus 7, or 7.5 versus 8) is not the same bet.

Several DraftKings totals are whole numbers (7 or 8). A push is possible. Paper P/L on a push is $0.

Paper stake is $20. Profit on a plus-money price is $20 times the price over 100. Profit on a minus price is $20 times 100 over the absolute price. A loss is $20. If juice were missing, the assumption would be -110, which pays $18.18. Every priced ticket below has a posted juice.

Hit, Actual, and P/L stay blank for scoring after the games.

## Card

DK is DraftKings on ESPN at 7:18 p.m. PT. Widget is the 7:05 p.m. desk file when it differs.

| Game (PT) | Side | Card price | Conf | Total | Card price | Conf |
| --- | --- | --- | --- | --- | --- | --- |
| Mets at Nationals, 10:05 a.m. | Mets -1.5 | Novig +160. DK run line is OFF. DK moneyline is -110 both sides. | 5 | Under 8.5 | Novig -115. DK under -120, over +100. | 5 |
| Orioles at Yankees, 10:05 a.m. | Orioles ML | Novig +125. DK +114 (widget same). | 5 | Under 8 | DK -108. Over is -112. Venues quote 7.5 and 8.5, not 8. | 6 |
| Cubs at Red Sox, 12:05 p.m. | Cubs -1.5 | PM +144. DK odds row absent. Tropicana, neutral, rescheduled from 9/26. | 4 | MISSING | No DK total. No venue full-game total. | 1 |
| Astros at Athletics, 12:05 p.m. | Astros ML | Novig -138. DK odds row absent. | 4 | MISSING | No DK total. No venue full-game total. | 1 |
| Dodgers at Giants, 12:05 p.m. | Dodgers -1.5 | PM +111. DK odds row absent. PM and Novig moneyline both -277. | 5 | MISSING | No DK total. No venue full-game total. | 1 |
| Rays at Phillies, 12:05 p.m. | Rays ML | Novig +122. DK live +113. Widget was +109. | 5 | Under 7 | DK -103. Over is -117. Widget same. Venues quote 7.5, not 7. | 5 |
| Reds at Blue Jays, 12:07 p.m. | Reds ML | Novig +147. DK +142. PM +150 before fee, about +140 after. | 5 | Over 8.5 | PM -106 (about -114 after fee). DK over -120. | 4 |
| Guardians at Royals, 12:10 p.m. | Guardians ML | Novig -117. DK odds row absent. | 4 | MISSING | No DK total. No venue full-game total. | 1 |
| Pirates at Tigers, 12:10 p.m. | Pirates ML | Novig -122. DK -131 (widget same). | 6 | Under 8 | DK -108. Over is -112. Venues quote 8.5, not 8. | 5 |
| Diamondbacks at Padres, 12:10 p.m. | Diamondbacks ML | PM +104. DK odds row absent. Novig has Arizona at -102. | 3 | MISSING | No DK total. No venue full-game total. | 1 |
| Angels at Mariners, 12:10 p.m. | Mariners -1.5 | Novig +130. PM +130 before fee, about +121 after. DK +123. | 6 | Under 7 | DK +101. Over is -122. Widget same. Venues quote 7.5, not 7. | 6 |
| Rangers at Twins, 12:10 p.m. | Rangers ML | Novig -117. DK odds row absent. | 4 | MISSING | PM lists 7.5, 8.5, 9.5 with empty quotes. No DK total. | 1 |
| Rockies at White Sox, 12:10 p.m. | White Sox -1.5 | Novig +106. DK live -105. Widget was -102. | 6 | Over 8.5 | Novig +102. DK over -105. | 6 |
| Braves at Marlins, 12:10 p.m. | Braves -1.5 | Novig +160. DK +145 (widget same). | 5 | Over 8.5 | Novig -117. DK over -122. | 4 |
| Cardinals at Brewers, 12:10 p.m. | Brewers -1.5 | Novig +108. PM +108 before fee, about +101 after. DK +101. | 7 | Under 7 | DK -120. Over is +100. Widget same. Venues quote 6.5, not 7. | 5 |

## Ranked sides

| Rank | Pick | Conf |
| --- | --- | --- |
| 1 | Brewers -1.5, Novig +108 (DK +101) | 7 |
| 2 | White Sox -1.5, Novig +106 (DK -105) | 6 |
| 3 | Mariners -1.5, Novig +130 (DK +123) | 6 |
| 4 | Pirates ML, Novig -122 (DK -131) | 6 |
| 5 | Dodgers -1.5, PM +111 (DK off the board) | 5 |
| 6 | Mets -1.5, Novig +160 (DK run line OFF) | 5 |
| 7 | Braves -1.5, Novig +160 (DK +145) | 5 |
| 8 | Orioles ML, Novig +125 (DK +114) | 5 |
| 9 | Rays ML, Novig +122 (DK +113) | 5 |
| 10 | Reds ML, Novig +147 (DK +142) | 5 |
| 11 | Guardians ML, Novig -117 (DK off) | 4 |
| 12 | Astros ML, Novig -138 (DK off) | 4 |
| 13 | Rangers ML, Novig -117 (DK off) | 4 |
| 14 | Cubs -1.5, PM +144 (DK off, Tropicana) | 4 |
| 15 | Diamondbacks ML, PM +104 (DK off) | 3 |

## Ranked totals

| Rank | Pick | Conf |
| --- | --- | --- |
| 1 | Yankees game Under 8, DK -108 | 6 |
| 2 | Mariners game Under 7, DK +101 | 6 |
| 3 | White Sox game Over 8.5, Novig +102 (DK -105) | 6 |
| 4 | Nationals game Under 8.5, Novig -115 (DK -120) | 5 |
| 5 | Phillies game Under 7, DK -103 | 5 |
| 6 | Tigers game Under 8, DK -108 | 5 |
| 7 | Brewers game Under 7, DK -120 | 5 |
| 8 | Blue Jays game Over 8.5, PM -106 (DK -120) | 4 |
| 9 | Marlins game Over 8.5, Novig -117 (DK -122) | 4 |
| 10 | Cubs at Red Sox | MISSING, conf 1 |
| 11 | Astros at Athletics | MISSING, conf 1 |
| 12 | Dodgers at Giants | MISSING, conf 1 |
| 13 | Guardians at Royals | MISSING, conf 1 |
| 14 | Diamondbacks at Padres | MISSING, conf 1 |
| 15 | Rangers at Twins | MISSING, conf 1 |

## Mixed top 5

These five are the $20 paper tickets. Rank 3 and rank 5 are the same Mariners game.

| Rank | Paper ticket | Conf | If it wins | If it loses | Hit | Actual | P/L |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Brewers -1.5, Novig +108 | 7 | +$21.60 | -$20.00 | | | |
| 2 | White Sox -1.5, Novig +106 | 6 | +$21.20 | -$20.00 | | | |
| 3 | Mariners -1.5, Novig +130 | 6 | +$26.00 | -$20.00 | | | |
| 4 | Orioles at Yankees Under 8, DK -108 | 6 | +$18.52 | -$20.00 | | | |
| 5 | Angels at Mariners Under 7, DK +101 | 6 | +$20.20 | -$20.00 | | | |

A total of exactly 8 pushes rank 4. A total of exactly 7 pushes rank 5. Five $20 tickets is $100 of paper risk. If all five win and none push, the paper profit is $107.52. That sum is arithmetic on these prices. It is not a projection.

## Why, and the counter-case

### Mets -1.5 +160, conf 5

Herz is 0-1 with a 9.00 ERA in 4.0 innings, Manaea is 6-7 with a 4.67 ERA in 144.2 innings, DraftKings has the run line OFF, and Novig pays +160 to lay 1.5 while both moneyline sides are -110 on DraftKings.

Counter-case: one bad start is a tiny sample, and the consensus board taking the run line down is a sign the number is unstable.

### Nationals game Under 8.5 -115, conf 5

The NWS Sunday period at Nationals Park is a 52 percent chance of light rain with a northwest wind of 12 to 18 mph, and Novig's under at 8.5 is -115 against DraftKings -120.

Counter-case: the Nationals have scored 815 runs, and a 9.00 ERA spot start can dump runs before the wind matters.

### Orioles ML +125, conf 5

Baz is 6-15 with a 4.11 ERA across 179.2 innings, Rodríguez is 0-3 with a 5.40 ERA in 26.2 innings, Yankee Stadium's Sunday period is heavy rain and a 22 to 26 mph northeast wind, and Novig pays +125 against DraftKings +114.

Counter-case: the Yankees are 93-68 with a +138 run differential, the forecast update is from 12:21 p.m. PT, and a postponement voids the ticket.

### Yankees game Under 8 -108, conf 6

DraftKings' close is 8, under -108 and over -112, in heavy rain and a 22 to 26 mph wind at an open park. The venues' 7.5 is a different contract, so the card stays on the DraftKings 8.

Counter-case: exactly 8 runs pushes, the forecast period is the whole daytime, and the game can be postponed.

### Cubs -1.5 +144, conf 4

Polymarket pays +144 to lay 1.5 with the Red Sox stuck at 19 runs scored and 19 allowed across nine recent finals, and DraftKings has no row. ESPN and the Stats API both place the game at Tropicana Field, neutral, rescheduled from Sep 26.

Counter-case: both probables are blank, the number can move when starters post, and there is no total.

### Cubs at Red Sox total, MISSING, conf 1

No full-game total on DraftKings, Polymarket US, or Novig. No number is invented.

### Astros ML -138, conf 4

The standings feed has Houston 0.5 games back with a division elimination number of 2, the Athletics are 64-96 with a -218 run differential, and Novig is -138. DraftKings has no row. ESPN lists Brady Basso for the Athletics. The Stats API still has both probables blank.

Counter-case: the starter slot is not agreed, and the Saturday game in the series was still in progress at 7:12 p.m. PT.

### Astros at Athletics total, MISSING, conf 1

No quoted full-game total. No ticket.

### Dodgers -1.5 +111, conf 5

The Dodgers are 99-62 with a +197 run differential and a 7-2 mark in nine recent finals, the Giants are 1-7 in eight finals, and Polymarket pays +111 to lay 1.5 while the moneyline is -277 on both venues. DraftKings has no row.

Counter-case: Sunday's starter is blank on both feeds, so this can be a bullpen game that stays inside one run.

### Dodgers at Giants total, MISSING, conf 1

No quoted full-game total. No ticket.

### Rays ML +122, conf 5

Martinez is 15-5 with a 2.94 ERA and a 1.07 WHIP, Wheeler is 13-5 with a 3.06 ERA, and Novig pays +122 against a DraftKings live price of +113 (the 7:05 p.m. widget was +109).

Counter-case: Wheeler is at home, DraftKings makes Philadelphia -137, and the Saturday game was still in progress.

### Phillies game Under 7 -103, conf 5

Citizens Bank Park's Sunday period is rain showers at 97 percent with a 15 mph north wind, both starters have ERAs under 3.10, and DraftKings has the under at 7 for -103 against an over at -117.

Counter-case: exactly 7 runs pushes, and the forecast update is from 1:11 p.m. PT.

### Reds ML +147, conf 5

Scherzer is 3-9 with a 6.14 ERA in 77.2 innings, Toronto is 2-6 in eight recent scored finals, and Novig pays +147 against DraftKings +142.

Counter-case: Williamson is 4.89 in 49.2 innings, and the Jays are home in a retractable park with no roof call.

### Blue Jays game Over 8.5 -106, conf 4

Scherzer's 6.14 ERA sits on DraftKings' 8.5, and Polymarket's over is -106 against DraftKings -120.

Counter-case: the roof position is unknown, and Williamson's sample is 49.2 innings.

### Guardians ML -117, conf 4

Cleveland is 7-1 in eight recent finals and a division champ on the feed, Kansas City is 1-8 in nine finals with a -121 run differential, and Novig is -117. DraftKings has no row.

Counter-case: the Guardians probable is blank, and Lynch has nine starts in 55 appearances.

### Guardians at Royals total, MISSING, conf 1

No quoted full-game total. Kauffman's 36 percent storm chance is not turned into a number.

### Pirates ML -122, conf 6

Jones is 5-6 with a 3.87 ERA, 118 strikeouts, and a 1.12 WHIP in 97.2 innings, Ryan is 0-0 with 3.0 innings on the season line, and Novig is -122 against DraftKings -131 in a dry Comerica forecast.

Counter-case: three innings can be an opener, and Detroit won the Sep 26 game 4-3.

### Tigers game Under 8 -108, conf 5

DraftKings' close is 8, under -108 and over -112. Jones misses bats, and Ryan's line gives no evidence of a long start. The venues' 8.5 is a different number.

Counter-case: exactly 8 runs pushes, and the market's two sides are both minus prices.

### Diamondbacks ML +104, conf 3

Soroka is 9-5 with a 3.31 ERA in 111.1 innings, the Padres probable is blank, DraftKings has no row, and Polymarket is the board paying plus money on Arizona.

Counter-case: Novig prices Arizona at -102, the Padres are clinched at 89-71, and the Saturday game was still in progress.

### Diamondbacks at Padres total, MISSING, conf 1

No quoted full-game total. No ticket.

### Mariners -1.5 +130, conf 6

Gilbert is 12-11 with a 3.81 ERA, 197 strikeouts, and a 1.10 WHIP in 182 innings, Kikuchi is 1-6 with a 4.88 ERA and a 1.55 WHIP in 62.2 innings, and Novig pays +130 to lay 1.5 against DraftKings +123 and a moneyline of -186.

Counter-case: Seattle is 74-86 and 3-4 in seven recent finals, so the margin is the part the club has not been producing.

### Mariners game Under 7 +101, conf 6

DraftKings' close is 7, under +101 and over -122, with Gilbert the listed starter. This ticket is correlated with Mariners -1.5.

Counter-case: exactly 7 runs pushes, the T-Mobile roof was not posted, and the Saturday game was still in progress.

### Rangers ML -117, conf 4

The standings feed shows Texas with magic number 2, the Stats API lists Gore (8-11, 4.59, 170.2 innings), and Novig is -117. DraftKings has no row. ESPN's scoreboard lists Kremer and leaves the Rangers probable blank, so Gore is not confirmed on that feed.

Counter-case: the two feeds do not agree on the Texas starter, and a magic-number game can become a parade of relievers.

### Rangers at Twins total, MISSING, conf 1

No DraftKings total. Polymarket shows total strikes with empty quotes. No number is invented.

### White Sox -1.5 +106, conf 6

Freeland is 4-11 with a 6.58 ERA and a 1.52 WHIP in 131.1 innings, the Rockies have allowed 940 runs, Novig pays +106 to lay 1.5, and DraftKings' live close is -105 (the 7:05 p.m. widget was -102). The moneyline is -225.

Counter-case: the White Sox have already clinched, and the sportsbook price being minus means the plus-money venue quote can be the stale side.

### White Sox game Over 8.5 +102, conf 6

Freeland's 6.58 ERA and the Rockies' 940 runs allowed sit on an 8.5 that Novig prices at +102 on the over, against DraftKings -105, with a sunny, light-wind forecast at Rate Field.

Counter-case: Kay has made 30 starts at a 4.53 ERA, and Sep 26 was already a 9-6 game, which does not make Sunday the same shape.

### Braves -1.5 +160, conf 5

The Braves are 94-67 with a +118 run differential, Sep 26 was an 8-3 win in Miami, and Novig pays +160 to lay 1.5 against DraftKings +145. The moneyline is -112 / -108.

Counter-case: Junk's ERA is better than Ritchie's (4.31 against 4.79), and a clinched club can shorten a starter.

### Marlins game Over 8.5 -117, conf 4

Both starters have ERAs in the mid-4s, and Novig's over at 8.5 is -117 against DraftKings -122.

Counter-case: the roof position is unknown, so the sunny outdoor forecast is not evidence.

### Brewers -1.5 +108, conf 7

Misiorowski is 15-5 with a 1.86 ERA, a 0.80 WHIP, and 247 strikeouts in 169.1 innings, Pallante is 12-8 with a 3.61 ERA, and Novig pays +108 to lay 1.5 against DraftKings +101. The moneyline is -250 on DraftKings and -223 on both venues.

Counter-case: Milwaukee has clinched, and an ace can be lifted early in a game the club no longer needs.

### Brewers game Under 7 -120, conf 5

DraftKings' close is 7, under -120 and over +100, with Misiorowski listed. The venues' 6.5 is a different contract, so the card uses 7.

Counter-case: the over is the plus-money side at +100, the Brewers have scored 826 runs, and exactly 7 runs pushes.

## Scoring block

Fill after the games. Leave these blank until then.

| Ticket | Hit? | Actual | P/L |
| --- | --- | --- | --- |
| Mixed 1 Brewers -1.5 +108 | | | |
| Mixed 2 White Sox -1.5 +106 | | | |
| Mixed 3 Mariners -1.5 +130 | | | |
| Mixed 4 Under 8 Yankees -108 | | | |
| Mixed 5 Under 7 Mariners +101 | | | |
