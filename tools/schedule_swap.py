"""Schedule swap: every team's record if it had played every other team's schedule.

Usage: python3 tools/schedule_swap.py [through_week]
Reads data/scores_2021_2026.csv (2026 rows) and writes data/schedule_swap_wk<N>.json.
Rule: team X on Y's schedule faces Y's opponent each week, using that opponent's real score.
If Y's opponent that week is X itself, X faces Y instead.
"""
import csv, json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = [r for r in csv.DictReader(open(ROOT / "data/scores_2021_2026.csv")) if r["season"] == "2026"]
last = max(int(r["week"]) for r in rows)
thru = int(sys.argv[1]) if len(sys.argv) > 1 else last
rows = [r for r in rows if int(r["week"]) <= thru]

pts, opp = {}, {}
for r in rows:
    w, m = int(r["week"]), r["manager"]
    pts[(m, w)] = float(r["points"]); opp[(m, w)] = r["opponent_manager"]
teams = sorted({r["manager"] for r in rows})
weeks = list(range(1, thru + 1))
W = {t: sum(pts[(t, w)] > pts[(opp[(t, w)], w)] for w in weeks) for t in teams}
PF = {t: sum(pts[(t, w)] for w in weeks) for t in teams}
order = sorted(teams, key=lambda t: (-W[t], -PF[t]))

def swap(x, y):
    wins = 0
    for w in weeks:
        o = opp[(y, w)]
        if o == x: o = y
        wins += pts[(x, w)] > pts[(o, w)]
    return wins

grid = {x: {y: swap(x, y) for y in order} for x in order}
for t in order: assert grid[t][t] == W[t], t
avg = {x: sum(grid[x].values()) / len(order) for x in order}
kind = {y: sum(grid[x][y] for x in order if x != y) / (len(order) - 1) for y in order}
pa = {t: sum(pts[(opp[(t, w)], w)] for w in weeks) / len(weeks) for t in order}
out = dict(through=thru, games=len(weeks), order=order, wins=W, pf=PF, grid=grid,
           avg=avg, luck={t: W[t] - avg[t] for t in order}, kindness=kind, pa_per_week=pa)
dest = ROOT / f"data/schedule_swap_wk{thru}.json"
json.dump(out, open(dest, "w"), indent=1)
print(dest)
for x in order: print(f"{x:8}", *[grid[x][y] for y in order], f"avg {avg[x]:.1f} luck {W[x]-avg[x]:+.1f}")
