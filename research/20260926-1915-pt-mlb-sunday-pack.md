# MLB Sunday research pack: 2026-09-27

**Stamped:** 2026-09-26 7:15 p.m. Pacific Time. **Revised:** 2026-09-26 7:18 p.m. PT. Consensus prices are DraftKings on ESPN. The desk widget file covers 9 games. A live scoreboard read at 7:18 p.m. PT matches those 9 and still has no odds on the other 6. Polymarket US and Novig both list MLB. They are the price used only when they beat DraftKings on the same side and line, or when DraftKings has no line.
**Slate:** 15 games, first pitch 10:05 a.m. to 12:10 p.m. PT. Schedule file: `research/20260926-1915-pt-mlb-sunday-schedule.md`.
**Venues:** Polymarket US and Novig both list this MLB slate. Quotes are in the picks file and in `snapshots/20260926-1915-pt-mlb-sunday-lines.json`.
**Phase 0:** Paper only. These notes are research. They are not a Tim-approve trade card, not an order, and not a sizing sheet beyond the $20 paper examples in the picks file.

## How to read the facts

Standings, runs, clinch flags, and recent finals are the MLB Stats API. The standings payload's own `lastUpdated` stamps run from 2026-09-26 2:39 p.m. PT (AL East) to 2026-09-26 7:06 p.m. PT (NL West and AL Central). Recent form is regular-season finals from Sep 17 through Sep 26 with a score on the feed. Four Sep 26 games were still in progress at 7:12 p.m. PT, so they are not in the win-loss counts: Rays-Phillies, Diamondbacks-Padres, Astros-Athletics, Angels-Mariners.

Clinch letters below are the feed's `clinchIndicator`, next to `divisionChamp` and `clinched`. A division elimination number of E means the feed has that club out of the division race. A wild-card elimination number of E means the feed has that club out of the wild-card race. This pack does not add a playoff story past those fields.

Batting orders were not on the schedule feed. No injury list is used. Secondary pages disagreed on a few starters (Rodón vs Rodríguez, Snell vs a blank Sunday slot, Boyd vs a blank Sunday slot). The probable is the MLB feed. Where that feed is blank, the starter is MISSING.

## Standings that touch Sunday

| Division | Club | W-L | GP | RS | RA | RD | Flag on the feed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AL East | Rays | 97-63 | 160 | 721 | 642 | +79 | clinched, indicator z, division champ |
| AL East | Yankees | 93-68 | 161 | 739 | 601 | +138 | clinched, indicator w |
| AL East | Red Sox | 87-74 | 161 | 687 | 605 | +82 | clinched, indicator w |
| AL East | Orioles | 79-82 | 161 | 718 | 739 | -21 | wild-card elimination E |
| AL East | Blue Jays | 78-83 | 161 | 643 | 693 | -50 | wild-card elimination E |
| AL Central | Guardians | 85-76 | 161 | 676 | 664 | +12 | clinched, indicator y, division champ |
| AL Central | White Sox | 83-78 | 161 | 772 | 718 | +54 | clinched, indicator w |
| AL Central | Twins | 76-85 | 161 | 733 | 793 | -60 | wild-card elimination E |
| AL Central | Tigers | 76-85 | 161 | 721 | 648 | +73 | wild-card elimination E |
| AL Central | Royals | 68-93 | 161 | 687 | 808 | -121 | wild-card elimination E |
| AL West | Rangers | 80-81 | 161 | 669 | 713 | -44 | magic number 2, division rank 1 |
| AL West | Astros | 79-81 | 160 | 712 | 764 | -52 | 0.5 GB, division elimination number 2, wild-card elimination E |
| AL West | Mariners | 74-86 | 160 | 649 | 715 | -66 | division and wild-card elimination E |
| AL West | Athletics | 64-96 | 160 | 697 | 915 | -218 | eliminated on both numbers |
| AL West | Angels | 62-98 | 160 | 648 | 737 | -89 | eliminated on both numbers |
| NL East | Braves | 94-67 | 161 | 739 | 621 | +118 | clinched, indicator y, division champ |
| NL East | Phillies | 87-73 | 160 | 705 | 683 | +22 | division elimination E, wild-card elimination number is a dash, not clinched |
| NL East | Marlins | 79-82 | 161 | 710 | 709 | +1 | wild-card elimination E |
| NL East | Nationals | 76-85 | 161 | 815 | 811 | +4 | wild-card elimination E |
| NL East | Mets | 74-87 | 161 | 695 | 725 | -30 | wild-card elimination E |
| NL Central | Brewers | 102-59 | 161 | 826 | 614 | +212 | clinched, indicator z, division champ |
| NL Central | Cubs | 88-73 | 161 | 844 | 701 | +143 | clinched, indicator w |
| NL Central | Pirates | 81-80 | 161 | 763 | 737 | +26 | wild-card elimination E |
| NL Central | Cardinals | 77-84 | 161 | 716 | 743 | -27 | wild-card elimination E |
| NL Central | Reds | 75-86 | 161 | 665 | 821 | -156 | wild-card elimination E |
| NL West | Dodgers | 99-62 | 161 | 796 | 599 | +197 | clinched, indicator y, division champ |
| NL West | Padres | 89-71 | 160 | 703 | 670 | +33 | clinched, indicator w |
| NL West | D-backs | 86-74 | 160 | 728 | 711 | +17 | wild-card elimination number 2, 1.0 GB in the wild card |
| NL West | Giants | 65-96 | 161 | 668 | 755 | -87 | wild-card elimination E |
| NL West | Rockies | 58-103 | 161 | 750 | 940 | -190 | wild-card elimination E |

## Game notes

### Mets at Nationals, 10:05 a.m. PT

Manaea (6-7, 4.67, 144.2 IP) against Herz (0-1, 9.00, 4.0 IP, one start). Nationals Park is open. NWS Sunday period, update 4:53 p.m. PT: 66 F, northwest 12 to 18 mph, a 52 percent chance of light rain. Mets are 5-4 in nine finals since Sep 17 (45 runs scored, 32 allowed). Nationals are 5-3 in eight (37 scored, 36 allowed). Sep 26 final on the feed: Mets 7, Nationals 1. Both clubs are out of the wild card on the elimination field. The moneyline is a pick'em. The run line pays plus money on the Mets.

### Orioles at Yankees, 10:05 a.m. PT

Baz (6-15, 4.11, 179.2 IP, 31 starts) against Elmer Rodríguez (0-3, 5.40, 26.2 IP, 6 starts). A CBS gametracker still names Carlos Rodón. The MLB probable is Rodríguez, and the moneyline is a short favorite price, which fits the thin Yankees line. Yankee Stadium is open. NWS Sunday period, update 12:21 p.m. PT: 66 F, northeast wind 22 to 26 mph, 95 percent precip, heavy rain. That forecast is several hours old and can change before 10:05 a.m. PT. Yankees are 5-4 in nine finals (42 scored, 40 allowed) with a season run differential of +138. Orioles are 4-4 in eight (30 scored, 25 allowed) and are eliminated in the wild card. The game is still Scheduled. A later postponement would be a void risk, not a result.

### Cubs at Red Sox, 12:05 p.m. PT, Tropicana Field

This is a neutral-site game on the ESPN scoreboard, with the note "Rescheduled from 9/26." Stats API and ESPN both name Tropicana Field. The park is a dome. Probables are blank on both feeds. DraftKings has no moneyline, run line, or total on the ESPN scoreboard, which matches the empty odds row in the desk core file (`list index out of range` on event 401817089). Cubs are 88-73, clinched, indicator w, +143 run differential, 3-5 in eight finals (27 scored, 27 allowed). Red Sox are 87-74, clinched, indicator w, +82, 5-4 in nine finals and only 19 runs scored and 19 allowed in those nine. Polymarket US has a moneyline and a 1.5 run line and no full-game total. Novig has a moneyline and no total and no 1.5 book.

### Astros at Athletics, 12:05 p.m. PT

Probables are blank on the MLB feed and on the desk schedule. ESPN's 7:18 p.m. scoreboard lists Brady Basso for the Athletics and leaves Houston blank. DraftKings has no odds on this game. Sutter Health Park is open and the Sunday period is mostly sunny, 76 F, wind 6 mph, precip 1 percent. Astros are 79-81, 0.5 games back of Texas, division elimination number 2, wild-card elimination E, so Sunday is a division game only. Athletics are 64-96 with a -218 run differential. The Saturday game in this series was still in progress at 7:12 p.m. PT. Covers has a moneyline and no run line or total.

### Dodgers at Giants, 12:05 p.m. PT

Probables are blank. Covers' Saturday final row shows Blake Snell and Matt Wilkinson, score Dodgers 4, Giants 3. That pair is Saturday, not the Sunday probable. Oracle Park is open. Sunday period: 62 F, west 7 to 13 mph, 15 percent drizzle. Dodgers are 99-62, division champ, indicator y, +197, 7-2 in nine finals (45 scored, 21 allowed). Giants are 65-96, 1-7 in eight finals (19 scored, 36 allowed). Covers moneyline is a heavy Dodgers favorite (first column 1/3, which is -300) with no run line and no total. Polymarket US and Novig both price the Dodgers moneyline at -277, and Polymarket prices Dodgers -1.5 at +111.

### Rays at Phillies, 12:05 p.m. PT

Martinez (15-5, 2.94, 177.1 IP, WHIP 1.07) against Wheeler (13-5, 3.06, 156.0 IP, 188 strikeouts, WHIP 1.06). Citizens Bank Park is open. NWS Sunday period, update 1:11 p.m. PT: 66 F, north wind 15 mph, 97 percent chance of rain showers. Rays are 97-63, division champ, indicator z, 5-4 in nine finals (33 scored, 25 allowed). Phillies are 87-73, division elimination E, wild-card elimination number still a dash, not clinched, 3-5 in eight finals (24 scored, 33 allowed). The Saturday game was still in progress, so the Sunday bullpens are not a known quantity. DraftKings' close at 7:18 p.m. PT is 7, under -103 and over -117. The 7:05 p.m. widget had the same total.

### Reds at Blue Jays, 12:07 p.m. PT

Williamson (5-4, 4.89, 49.2 IP) against Scherzer (3-9, 6.14, 77.2 IP). Rogers Centre is retractable and the roof position was not on the feed. The NWS points call for that coordinate returned 404, so no outdoor forecast is applied. Blue Jays are 2-6 in eight scored finals since Sep 17 (24 scored, 37 allowed) and are eliminated in the wild card. Reds are 4-5 in nine (34 scored, 42 allowed), also eliminated. Sep 26 final: Reds 5, Blue Jays 1. Covers total is 8.5, with the over a slight favorite (first column 6/7, which is -117).

### Guardians at Royals, 12:10 p.m. PT

Guardians probable is blank. Royals list Daniel Lynch IV (6-6, 4.13, 80.2 IP, 9 starts in 55 appearances). Kauffman is open. Sunday period: 78 F, wind 7 mph, 36 percent chance of showers and thunderstorms. Guardians are 85-76, division champ, indicator y, 7-1 in eight finals (45 scored, 26 allowed). Royals are 68-93, -121 run differential, 1-8 in nine finals (46 scored, 74 allowed). Sep 26 final: Guardians 11, Royals 5. Covers has a moneyline and no run line or total. Polymarket's -1.5 book is wide (bid 0.410, ask 0.500 on the Guardians -1.5 side).

### Pirates at Tigers, 12:10 p.m. PT

Jones (5-6, 3.87, 97.2 IP, 118 strikeouts, WHIP 1.12) against Ryan (0-0, 0.00, 3.0 IP, one start). Comerica is open and the Sunday period is dry, 73 F, north 6 to 12 mph. Pirates are 6-3 in nine finals (40 scored, 35 allowed). Tigers are 4-5 in nine (38 scored, 41 allowed) with a season run differential of +73 and a wild-card elimination of E. Sep 26 final: Pirates 3, Tigers 4. Ryan's line is one short outing. It can be an opener. Covers total is 8.5, under favored (first column 3/4 on the under, -133).

### Diamondbacks at Padres, 12:10 p.m. PT

Soroka is listed (9-5, 3.31, 111.1 IP). The Padres probable is blank. Petco is open, 83 F, northwest 5 mph, 11 percent precip. Diamondbacks are 86-74, wild-card elimination number 2, 1.0 games back, 6-1 in seven finals (50 scored, 33 allowed). Padres are 89-71, clinched, indicator w, 6-2 in eight finals (44 scored, 34 allowed). The Saturday game was still in progress. Covers prices San Diego as a small favorite and leaves the run line and total blank. Polymarket is the board that pays plus money on Arizona.

### Angels at Mariners, 12:10 p.m. PT

Kikuchi (1-6, 4.88, 62.2 IP, WHIP 1.55) against Gilbert (12-11, 3.81, 182.0 IP, 197 strikeouts, WHIP 1.10). T-Mobile Park is retractable. The Sunday outdoor period is dry and light, and the roof position was not posted, so weather is not an input. Mariners are 74-86 and eliminated, 3-4 in seven finals (25 scored, 35 allowed). Angels are 62-98, 4-4 in eight (34 scored, 45 allowed). The Saturday game was still in progress. DraftKings' close is Mariners -186, Mariners -1.5 +123, and a total of 7 with the under at +101. Novig pays +130 on that same -1.5.

### Rangers at Twins, 12:10 p.m. PT

Gore (8-11, 4.59, 170.2 IP) against Kremer (4-5, 4.97, 83.1 IP). Target Field is open. Sunday period: 69 F, wind 0 to 5 mph, 29 percent chance of a shower early, then mostly cloudy. Rangers are 80-81 with magic number 2 and the AL West lead. Astros can only catch them in the division. Twins are 76-85 and eliminated in the wild card, 5-4 in nine finals (41 scored, 28 allowed). Sep 26 final: Rangers 6, Twins 2. Covers has a short Texas moneyline and no run line or total. Polymarket lists 7.5, 8.5, and 9.5 with no bid and no ask. Novig's 1.5 market has no bids.

### Rockies at White Sox, 12:10 p.m. PT

Freeland (4-11, 6.58, 131.1 IP, WHIP 1.52) against Kay (9-9, 4.53, 153.0 IP). Rate Field is open, mostly sunny, 65 F, wind 0 to 10 mph, precip 1 percent. Rockies are 58-103, -190 run differential, 2-7 in nine finals (35 scored, 55 allowed), and they have allowed 940 runs. White Sox are 83-78, clinched, indicator w, 6-3 in nine finals (61 scored, 41 allowed), and they have scored 772 runs. Sep 26 final: Rockies 9, White Sox 6, so the total already cleared 8.5 yesterday. Covers' Sunday total is 8.5 and is close to a pick'em. The White Sox moneyline is about -199. The -1.5 is plus money.

### Braves at Marlins, 12:10 p.m. PT

Ritchie (1-4, 4.79, 67.2 IP) against Junk (6-9, 4.31, 119.0 IP). loanDepot park is retractable. The outdoor Sunday period is sunny and 86 F with a 5 mph wind. Roof position was not posted, so that forecast is not a total input. Braves are 94-67, division champ, indicator y, +118, 5-3 in eight finals. Marlins are 79-82, wild-card elimination E, 3-5 in eight finals. Sep 26 final: Braves 8, Marlins 3. The moneyline is a pick'em on CBS (both -108) and on both venues. The Braves -1.5 is plus money.

### Cardinals at Brewers, 12:10 p.m. PT

Pallante (12-8, 3.61, 157.0 IP) against Misiorowski (15-5, 1.86, 169.1 IP, 247 strikeouts, WHIP 0.80). American Family Field is retractable. The outdoor Sunday period is mostly sunny, 68 F, wind 0 to 5 mph. Roof position was not posted. Brewers are 102-59, indicator z, division champ, +212, 826 runs scored and 614 allowed, 7-2 in nine finals (38 scored, 26 allowed). Cardinals are 77-84, 2-6 in eight finals (23 scored, 36 allowed). Sep 26 final: Cardinals 2, Brewers 3. DraftKings' close is Brewers -250, Brewers -1.5 +101, and a total of 7 with the under at -120. Novig and Polymarket pay +108 on that same -1.5. Their moneyline is -223, a different price from DraftKings -250.
