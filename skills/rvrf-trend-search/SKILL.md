---
name: rvrf-trend-search
description: RVRF(Real VR Fishing) 커뮤니티 동향 마스터 시트(DB 탭)를 검색·집계해 유저 니즈 건수, 월별 추이, 원문 인용, 링크를 뽑는다. 체감 QA, 유저 설문, Fun TC 체크리스트, 리텐션 가설, DUG Track 아이디어 우선순위, "유저들이 ~를 원하나/몇 건인가" 같은 동향 근거가 필요할 때 쓴다. docs.google.com/spreadsheets/d/1x1FMYxYK1ox7XKY2t4wKEjsRB84OBm60hIo3HRBAq4w 링크(RVRF 커뮤니티 동향 마스터)가 주어지면 시트를 직접 읽지 말고(Drive read 도구는 첫 행만 읽음) 반드시 이 스킬로 CSV를 검색한다. 구현·테스트 작업에는 쓰지 않는다.
---
# RVRF 동향 DB 검색

원본: Google Sheet "RVRF 커뮤니티 동향 마스터" id `1x1FMYxYK1ox7XKY2t4wKEjsRB84OBm60hIo3HRBAq4w`, 탭 `DB`(2,800행+, 매 회차 갱신). 건수·인용·월별 추이는 **반드시 이 DB에서 직접 센 값**만 쓴다.

## 1. CSV 확보 (PC 무관)
1. `python -I .claude/skills/rvrf-trend-search/load_csv.py --status` 로 캐시를 확인한다. 오늘 저장분이면 §2로.
2. 없거나 오래됐으면 Drive 커넥터 `download_file_content`(fileId=위 id, exportMimeType=`text/csv`)로 받는다. 결과가 길어 파일로 저장되면 그 경로를 `python -I load_csv.py <결과파일>`에 넘긴다(base64 디코드 → 임시폴더 캐시).
3. Drive 커넥터가 없으면 사용자에게 시트를 CSV로 내려받아 `-c 경로`로 지정해 달라고 요청한다. 시트를 읽기 도구로 열지 않는다.

## 2. 열 의미 (12칸)
A 출처(`YYYY-MM / YYMMDD / n`) · B 날짜 · C 구분 · D 세부항목(버그/문의/UI/UX/개선 사항/신규 기능/제안 사항/감상, 의견) · E 요약 · F 상세(원문+번역) · G 링크(URL+작성자) · H 관련의견(댓글·관리자 답변) · I 작성자 · J 대상(≤2, 13종) · K 반응(1, 10종) · L 키워드(표준 이름). 태그·키워드 사전: `tag-dictionary.md`.

## 3. 검색
```
python -I .claude/skills/rvrf-trend-search/search.py -k "<정규식>" [-s 세부항목] [--exclude-sub 문의,감상,버그] [-t 대상] [-r 반응] [-w 키워드태그] [-m 2026-10] [-n 10] [-c CSV경로]
```
출력: 총 건수, 월별 추이, 샘플(출처·세부항목·요약·원문 인용·링크). 원문은 한·영이 섞이므로 `-k`에 동의어를 `|`로 함께 넣는다(예 `프리셋|preset`).

## 4. 규칙
- 다른 문서(설문 초안 등)의 집계를 검증 없이 인용하지 않는다.
- "요구"를 셀 때는 `--exclude-sub 문의,감상,버그`로 요청성(개선/신규/제안/UI·UX)만 따로 세고, 문의·버그는 별도 표기한다.
- 인용은 F(상세) 원문에서, 링크는 G에서. 요약(E)은 인용으로 쓰지 않는다. 상세가 비면 "(상세 없음)"으로 표시한다.
- 키워드 매칭은 거칠다. 샘플을 읽어 무관한 행을 거른 뒤 "관련 글 약 N건"으로 보고하고, 건수에 쓴 행의 출처 id를 함께 남긴다.
- 근거가 동향이 아니면(기획서·베타 피드백) 출처를 구분해 적고, 동향 근거가 없으면 "근거 없음"으로 쓴다.
