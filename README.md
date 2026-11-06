# Hot Rod Breakdown

The digital edition of the Hot Rod Fantasy Football Boys weekly breakdown.

## Layout

- `site/` is the published website (Netlify publishes only this folder, set in `netlify.toml`).
  - `site/index.html`: the latest issue.
  - `site/week-N/index.html`: each week's issue, kept permanently.
  - `site/archive/index.html`: list of every issue.
- `data/` is the league archive and model inputs. It is not published.
  - `scores_2021_2026.csv`: every regular-season score, 2021 (CBS) through the current 2026 week. Jonathan's games are listed under Castano.
  - `lineups_2026_wk1-8.json`: 2026 starters and bench by week, from ESPN.
  - `model_params_after_wk8.json`: the odds model's inputs after Week 8.

## League conventions

- Seeding: record, then points-for. Divisions affect scheduling only. Top 6 make the playoffs; seeds 1–2 get byes.
- Regular season: weeks 1–14. A week is final after Monday Night Football.
- Records exclude ineligible zero-point lineups (a 2021 CBS rule); those games still count as losses.
- Lineup accuracy: points scored ÷ best possible lineup, averaged across weeks.

## Odds model

Each team's scoring level is its season average pulled toward the league average (equivalent to adding 34 weeks of league-average scoring), with uncertainty of 22.2 / √(weeks + 34). Weekly scores vary by ±22.2 points. This was fitted on the 2021–2025 archive, where about a fifth of a team's first-half scoring edge carried into weeks 9–14.
