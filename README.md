# rvrf-community-collector1

RVRF 커뮤니티 동향 검색·유저 리서치·DUG Track 업로드용 Claude Code 스킬 모음.

| 스킬 | 용도 |
|---|---|
| `skills/rvrf-trend-search` | 동향 마스터 시트(CSV) 검색: 건수·월별 추이·원문 인용·링크 |
| `skills/rvrf-user-research` | 체감 QA·유저 설문·Fun TC 작성 시 동향 시트를 먼저 훑는 규칙 |
| `skills/dugtrack-qa-upload` | DUG Track 업로드·해결 확인 코멘트·TC 최신화 규칙 |

## 설치
`skills/` 안의 폴더를 `~/.claude/skills/`(Windows: `C:\Users\<이름>\.claude\skills\`)로 복사하면 모든 Claude Code 세션에서 쓸 수 있다.
CSV 캐시는 OS 임시 폴더(`rvrf_trend/`)에 생기고, Drive 커넥터가 연결돼 있으면 스킬이 알아서 받는다.
스킬 안의 경로 `.claude/skills/...`는 `~/.claude/skills/...`로 읽는다.
