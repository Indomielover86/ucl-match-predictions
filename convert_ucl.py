"""Convert the supplied OpenFootball season text format. Python standard library only.
Usage: python convert_ucl.py INPUT_FOLDER OUTPUT_FOLDER
"""
import csv, re, sys
from pathlib import Path
from datetime import datetime
from collections import Counter

src = Path(sys.argv[1] if len(sys.argv)>1 else 'upload')
out = Path(sys.argv[2] if len(sys.argv)>2 else 'output')
out.mkdir(parents=True, exist_ok=True)
rows=[]
months={m:i for i,m in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split(),1)}
for p in sorted(src.glob('????-??.txt')):
    text=p.read_text(encoding='utf-8-sig')
    start=int(p.stem[:4]); date=None; section=None; count=0
    first_month=months[re.search(r'# Date\s+\w+ (\w+)', text)[1]]
    for lineno,line in enumerate(text.splitlines(),1):
        s=line.strip()
        if not s or s.startswith(('=','#')): continue
        if s.startswith('▪'):
            section=s[1:].strip().replace('Gruppe','Group'); continue
        d=re.fullmatch(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?',s)
        if d:
            weekday,mon,day,yr=d.groups(); month=months[mon]
            year=int(yr) if yr else start+(month<first_month)
            date=datetime(year,month,int(day))
            assert date.strftime('%a')==weekday,(p.name,lineno,s,date)
            continue
        m=re.fullmatch(r'(?:\d{1,2}:\d{2}\s+)?(.+?)\s+\(([A-Z]{3})\)\s+v\s+(.+?)\s+\(([A-Z]{3})\)(?:\s+(.*))?',s)
        if not m: raise ValueError((p.name,lineno,s))
        home,hcountry,away,acountry,score=m.groups(); score=score or ''
        assert date and section
        pairs=[tuple(map(int,x)) for x in re.findall(r'(\d+)-(\d+)',score)]
        pen='pen.' in score; aet='a.e.t.' in score
        final=pairs[int(pen)] if pairs else ('','')
        pens=pairs[0] if pen else ('','')
        # The primary goals retain the score at the end of play, excluding shootouts.
        ninety=final; basis='assumed_90_no_extra_time_marker' if pairs else 'unplayed'
        if aet:
            tail=re.search(r'a\.e\.t\.\s*\((.*)\)',score)
            inner=re.findall(r'(\d+)-(\d+)',tail[1]) if tail else []
            ninety=tuple(map(int,inner[0])) if len(inner)>=2 else ((0,0) if final==(0,0) else ('',''))
            basis='explicit_90_in_source' if len(inner)>=2 else ('inferred_from_0_0_after_extra_time' if final==(0,0) else 'unknown_90')
        correction=''
        if date.strftime('%Y-%m-%d')=='2025-05-06' and home=='FC Internazionale Milano' and away=='FC Barcelona':
            assert final==(4,3)
            ninety=(3,3); aet=True; basis='verified_UEFA_correction'
            correction='https://www.uefa.com/uefachampionsleague/news/0299-1db1e0d054c8-02dafe0b7237-1000--inter-4-3-barcelona-aet-agg-7-6-davide-frattesi-settles/'
        stage='group' if section.startswith('Group') else ('league_phase' if section.startswith('League') else 'knockout')
        round_name=section.split(', ',1)[-1] if ', ' in section else section
        if section.startswith('Playoffs'): round_name='Knockout phase play-offs, '+round_name
        rows.append(dict(date=date.strftime('%Y-%m-%d'),home_team=home,away_team=away,home_goals=final[0],away_goals=final[1],stage=stage,round=round_name,season=p.stem,home_goals_90=ninety[0],away_goals_90=ninety[1],extra_time=aet,home_penalties=pens[0],away_penalties=pens[1],score_90_basis=basis,home_country=hcountry,away_country=acountry,source_file=p.name,source_line=lineno,source_score=score,correction_source=correction,source_url='https://github.com/openfootball/champions-league',licence='CC0-1.0'))
        count+=1
    declared=int(re.search(r'# Matches\s+(\d+)',text)[1]); assert count==declared,(p,count,declared)
assert rows
rows.sort(key=lambda r:(r['date'],r['home_team'],r['away_team']))
keys=[(r['date'],r['home_team'],r['away_team']) for r in rows]
assert len(keys)==len(set(keys)), 'Duplicate match'
with (out/'ucl_matches.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('Rows:',len(rows),'Missing scores:',sum(r['home_goals']=='' for r in rows))
print('Seasons:',dict(sorted(Counter(r['season'] for r in rows).items())))
print('90 minute basis:',dict(Counter(r['score_90_basis'] for r in rows)))
