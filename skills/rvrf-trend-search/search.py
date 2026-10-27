# usage: python -I search.py [-c CSV] -k "정규식" [-s 세부항목,...] [-t 대상] [-r 반응] [-w 키워드태그] [-m 2026-10] [--exclude-sub 문의,감상] [-n 8]
import csv, re, sys, argparse, os, tempfile
sys.stdout.reconfigure(encoding='utf-8')
csv.field_size_limit(10**9)
CACHE = os.path.join(tempfile.gettempdir(), 'rvrf_trend', 'RVRF_trend_db_latest.csv')
ap = argparse.ArgumentParser()
ap.add_argument('-c', '--csv', default=CACHE); ap.add_argument('-k', default=''); ap.add_argument('-s'); ap.add_argument('-t')
ap.add_argument('-r'); ap.add_argument('-w'); ap.add_argument('-m'); ap.add_argument('--exclude-sub'); ap.add_argument('-n', type=int, default=8)
a = ap.parse_args()
if not os.path.exists(a.csv): sys.exit('CSV 없음: '+a.csv+' - SKILL.md 1번대로 Drive에서 받아 load_csv.py로 저장')
rows = list(csv.reader(open(a.csv, encoding='utf-8-sig', newline='')))[1:]
def has(cell, spec): return any(x in cell for x in spec.split(','))
pat = re.compile(a.k, re.I) if a.k else None
hit = []
for r in rows:
    if len(r) < 12: continue
    if a.s and not has(r[3], a.s): continue
    if a.exclude_sub and has(r[3], a.exclude_sub): continue
    if a.t and not has(r[9], a.t): continue
    if a.r and not has(r[10], a.r): continue
    if a.w and not has(r[11], a.w): continue
    if a.m and not r[0].startswith(a.m): continue
    txt = ' '.join([r[4], r[5], r[7], r[11]])
    if pat and not pat.search(txt): continue
    hit.append(r)
bym = {}
for r in hit: bym[r[0][:7]] = bym.get(r[0][:7], 0) + 1
print(f'총 {len(hit)}건 / 전체 {len(rows)}행'); print('월별:', dict(sorted(bym.items())))
for r in hit[:a.n]:
    m = pat.search(r[5]) if pat else None
    q = r[5][max(0, m.start()-60):m.end()+100].replace('\n', ' ') if m else r[5][:160].replace('\n', ' ')
    link = re.search(r'https?://\S+', r[6]); 
    print(f'- {r[0]} [{r[3]}] {r[4][:80]} | {r[9]}/{r[10]} | {r[8]}\n    "{q}"\n    {link.group(0) if link else ""}')
