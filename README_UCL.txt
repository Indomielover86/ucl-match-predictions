UCL MATCH DATA — conversion of 15 user-supplied OpenFootball text files

1997 match records, 2011-12 to 2025-26 inclusive, sorted by date.
2010-11 was not supplied and is NOT included. Qualifying rounds are not included.
All supplied match records have scores, including the 2025-26 final. File coverage
must not be confused with the current real-world season.
Each season's parsed count agrees with its file header: 125 each through 2023-24,
except 2019-20 (119); 2024-25 and 2025-26 each have 189.
No duplicate date/home/away keys; every parsed date matches its source weekday.
These are structural checks, not independent verification of every result.

SOURCE AND LICENCE
https://github.com/openfootball/champions-league
CC0-1.0 (CC0 1.0 Universal public-domain dedication)
https://github.com/openfootball/champions-league/blob/master/LICENSE.md
Uploaded copies were used; no original repository commit was supplied.

COLUMN DEFINITIONS
 date: ISO match date, YYYY-MM-DD. Omitted years inferred from the season and
       the first month in the file's date range; weekday checked.
 home_team, away_team: exact source team names with country suffix separated.
 home_goals, away_goals: score at the end of play, including extra time where
       played, EXCLUDING penalty shootouts. These are NOT uniformly 90-minute scores.
 stage: group, league_phase, knockout.
 round: source section detail; older files identify Group A, B, etc. rather than
       matchdays. Playoffs are labelled knockout phase play-offs.
 season: YYYY-YY.
 home_goals_90, away_goals_90: regulation-time score (including stoppage time).
       Where no extra-time marker exists, assumed equal to the source match score.
       This assumption is not independently verified for every match.
 extra_time: true when explicitly marked or corrected using the UEFA source below;
       false otherwise, and therefore not independent proof of no extra time.
 home_penalties, away_penalties: penalty-shootout scores, blank when absent.
 score_90_basis: indicates explicit, inferred, assumed, or corrected 90-minute score.
 home_country, away_country: source country codes.
 source_file, source_line, source_score: trace back to the uploaded text.
 correction_source: verification URL where a correction was applied.
 source_url, licence: dataset attribution and licence identifier.

ONE DOCUMENTED SOURCE CORRECTION
2025-05-06 Inter vs Barcelona is written as 4-3 (2-0) without an extra-time marker.
UEFA confirms 4-3 after extra time and the equaliser that made it 3-3 before extra
time. End-of-play goals remain 4-3; goals_90 are 3-3; extra_time is true.
https://www.uefa.com/uefachampionsleague/news/0299-1db1e0d054c8-02dafe0b7237-1000--inter-4-3-barcelona-aet-agg-7-6-davide-frattesi-settles/
https://www.uefa.com/uefachampionsleague/news/0299-1db33d9cfb3a-7984a434e6fb-1000--in-the-zone-unpicking-inter-s-remarkable-semi-final-win-ag/
Other unmarked source errors may remain. Review knockout scores before final modelling.

MODELLING NOTES
Team name variants across seasons are preserved, NOT normalised. Examples include
Real Madrid vs Real Madrid CF and Manchester City vs Manchester City FC. Build an
explicit alias mapping before calculating a team's historical form.
Home/away reflects the listed order and does not guarantee actual home advantage
(e.g. neutral finals). Venue/neutral status is not supplied in this CSV.
Use 90-minute goals to construct home/draw/away labels if predicting regulation
results. Never include the target match's goals, shootout scores or outcome-derived
metadata as predictive features. Compute features from earlier games only and split
chronologically. Source URLs, file line numbers and licence are metadata, not features.

REPRODUCE
Python standard library only:
  python convert_ucl.py INPUT_FOLDER OUTPUT_FOLDER
Input filenames must follow YYYY-YY.txt, in the supplied format. The converter
fails on unrecognised lines or match-count mismatches, instead of silently skipping.
