# Drive download_file_content 결과(JSON, base64 content)를 캐시 CSV로 저장. 사용: python -I load_csv.py <결과.json> | python -I load_csv.py --status
import json, base64, os, sys, tempfile, time
CACHE = os.path.join(tempfile.gettempdir(), 'rvrf_trend', 'RVRF_trend_db_latest.csv')
if len(sys.argv) > 1 and sys.argv[1] == '--status':
    if os.path.exists(CACHE):
        print(CACHE, time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getmtime(CACHE))), '저장')
    else: print('캐시 없음:', CACHE)
    sys.exit()
d = json.load(open(sys.argv[1], encoding='utf-8'))
text = base64.b64decode(d['content']).decode('utf-8-sig')
os.makedirs(os.path.dirname(CACHE), exist_ok=True)
open(CACHE, 'w', encoding='utf-8-sig', newline='').write(text)
print('저장:', CACHE, '/ 줄 수(대략)', text.count('\n'))
