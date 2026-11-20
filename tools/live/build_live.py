"""Build the public odds tracker (site/live/index.html) from an ESPN snapshot.
Usage: python3 tools/live/build_live.py data/live/wk10_snapshot.json
The snapshot is League Loom fantasy_get_matchups JSON (team-level is enough)."""
import json, re, sys, os
H = os.path.dirname(os.path.abspath(__file__))
snap = json.load(open(sys.argv[1]))
slim = {'matchups': [{'scoring': {'fetchedAt': m['scoring']['fetchedAt']}, 'final': m.get('final', False),
          **{s: {k: m[s][k] for k in ('teamName', 'livePoints', 'projectedPoints')} for s in ('away', 'home')}} for m in snap['matchups']]}
sim = open(f'{H}/sim.js').read().replace("if(typeof module!=='undefined')module.exports={runSim,parseMatchups};", '')
S_ = json.load(open(f'{H}/S.json')); WK = S_['week']
t = open(f'{H}/page.tpl').read().replace('__WK__', str(WK)).replace('__PREV__', str(WK-1)).replace('__SIM__', sim).replace('__S__', open(f'{H}/S.json').read()).replace('__SNAP__', json.dumps(slim))
t = (t.replace(f'<title>Week {WK} Live Odds</title>', f'<title>Hot Rod Week {WK} Odds Tracker</title>')
      .replace('<div class="kicker"><b>Hot Rod</b> · The Breakdown · Live tracker</div>', '<div class="kicker"><b>Hot Rod</b> · <a href="/" style="color:inherit">The Breakdown</a> · Odds tracker</div>')
      .replace(f'<h1>Week {WK} Live Odds</h1>', f'<h1>Week {WK} Odds Tracker</h1>'))
a = t.index('if(!SNAP)(async()=>{'); b = t.index('})();', a) + 5; t = t[:a] + t[b:]
t = re.sub(r'async function manual\(mcp\)\{.*?finally\{b\.disabled=false\}\}\n', '', t, flags=re.S)
t = re.sub(r'function onError\(e,mcp\)\{.*?\n\}\n', '', t, flags=re.S)
assert 'mcp' not in t
i = t.index('<header')
doc = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
       f'<meta property="og:title" content="Hot Rod Week {WK} Odds Tracker">\n' + t[:i] + '</head><body>\n' + t[i:] + '\n</body></html>\n')
os.makedirs('site/live', exist_ok=True); open('site/live/index.html', 'w').write(doc)
print('wrote site/live/index.html', slim['matchups'][0]['scoring']['fetchedAt'])
