# Research MCP WIKI Tool

연구실 구성원이 함께 편집할 수 있는 로컬 연구 WIKI입니다. Canonical 지식은 Git으로 관리되는 Markdown 파일이며, Codex와 Claude Code는 MCP를 통해 논문을 읽고 `source`, `concept`, `comparison`, `claim`, `question` 페이지를 저장합니다.

구현 목표와 경계는 [PRD.md](./PRD.md), 상세 클라이언트 연결 방법은 프로젝트 저장소의 `docs/client-setup.md`를 참고하세요.

## 주요 기능

- 로컬 PDF 텍스트 추출 또는 이미지 + 텍스트 스크린샷 추출
- 선택한 PDF 페이지를 `wiki/assets/<source-slug>/`에 Git 관리 이미지로 게시하고 Markdown 본문에 삽입
- PDF 전체 읽기 또는 선택 페이지 범위 읽기
- 한국어 정리 기본값과 영어 정리 옵션
- Git 이력이 남는 Markdown WIKI 저장과 복원
- Markdown에서 다시 만들 수 있는 SQLite 검색 인덱스
- 연구자 검토 전 `draft`, 검토 후 `reviewed` 상태 표시
- Codex 및 Claude Code용 MCP `resources`, `tools`, `prompts`
- 로컬 `stdio` 또는 토큰 보호 `Streamable HTTP` 전송
- 논문 반영 상태, WIKI 검색, 편집, PDF 설정, 인덱스 재생성, MCP capability 관리를 제공하는 로컬 GUI

## WIKI 객체

| 유형 | 역할 |
| --- | --- |
| `source` | 한 논문의 근거 중심 정리 |
| `concept` | 재사용 가능한 핵심 아이디어 |
| `comparison` | 사용자가 요청한 논문 간 비교 |
| `claim` | 사용자 입력을 바탕으로 발전시키는 연구 주장 |
| `question` | 사용자 입력을 바탕으로 관리하는 연구 질문 |
| `system` | WIKI 운영 문서 |
| `skill` | 재사용 가능한 에이전트 워크플로 |

`raw/papers`의 PDF는 처음에 빨간색입니다. 같은 PDF 경로를 출처로 가진 `source`와 `concept` 페이지가 모두 저장되면 파란색이 됩니다. `comparison` 페이지까지 저장되면 비교 분석 완료 배지가 추가됩니다.

## MCP 기능

Resources:

- `wiki://index`
- `wiki://papers`
- `wiki://page/{page_type}/{slug}`

Tools:

- `wiki_search`, `wiki_read_page`, `wiki_save_page`
- `wiki_create_research_page`, `wiki_review_page`
- `wiki_capture_discussion`
- `wiki_list_revisions`, `wiki_restore_revision`, `wiki_rebuild_index`
- `pdf_extract_text`, `pdf_render_screenshots`
- `wiki_publish_pdf_screenshots`
- `prepare_comparison_workflow`

`wiki_capture_discussion`은 연결된 Codex 또는 Claude Code가 대화 중 재사용 가치가 있는 논문 해석, concept, comparison, claim, question을 발견했을 때 호출합니다. MCP 서버가 채팅을 감시하는 방식은 아닙니다. 모델이 판단하여 호출하면 기존 페이지에 Discussion Capture를 추가하거나 새 draft 페이지를 만들고 Git 이력을 남깁니다.

Prompts:

- `paper_ingest_workflow`
- `claim_refinement_workflow`
- `novelty_review_workflow`

서버는 LLM API를 호출하지 않습니다. 논문 요약, 아이디어 추출, claim 적합성 검토, novelty 검토는 연결된 Codex 또는 Claude Code가 수행하고 결과를 MCP로 저장합니다.

연결된 에이전트의 역할, 권한, 허용/금지 기능은 [PRD.md? Appendix: Wiki Agent SPEC](./PRD.md)에 정리되어 있습니다. 핵심 규칙: 에이전트 쓰기는 항상 `draft`로 저장되고, `reviewed` 승격은 연구자만 수행합니다.

## MCP capability 관리

GUI 왼쪽 내비게이션의 `MCP 상태`에서 현재 서버가 제공하는 `resources`, `tools`, `prompts` 목록을 확인할 수 있습니다. 체크박스로 각 항목을 활성화하거나 비활성화하면 프로젝트 루트의 [`mcp-settings.json`](./mcp-settings.json)에 저장됩니다.

GUI의 `WIKI 페이지` 화면은 `source`, `concept`, `comparison`, `claim`, `question`, `system`, `skill` 유형별 탭과 논문별 필터를 제공합니다. 반영된 논문 카드를 누르면 해당 PDF를 출처로 연결한 WIKI 페이지만 모아서 볼 수 있습니다.

저장한 변경은 실행 중인 MCP 연결을 강제로 끊지 않습니다. Codex 또는 Claude Code가 MCP 서버를 다시 시작하거나 새 세션에서 서버를 다시 연결할 때 적용됩니다. 기본 설정은 모든 capability 활성화입니다.

## 설치

Python 3.11 이상과 Git이 필요합니다. PowerShell에서:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

## GUI 실행

```powershell
research-wiki-gui --host 127.0.0.1 --port 8780 --root .
```

브라우저에서 `http://127.0.0.1:8780`을 엽니다. GUI는 첫 마일스톤에서 로컬 전용입니다.

## MCP 실행

로컬 `stdio` 서버는 MCP 클라이언트가 직접 실행합니다. 수동 확인이 필요할 때:

```powershell
research-wiki-mcp --root .
```

토큰 보호 HTTP 서버:

```powershell
$env:RESEARCH_WIKI_MCP_TOKEN = "replace-with-a-local-shared-token"
research-wiki-mcp --transport streamable-http --host 127.0.0.1 --port 8765 --root .
```

엔드포인트는 `http://127.0.0.1:8765/mcp`이며 요청에는 `Authorization: Bearer <shared token>` 헤더가 필요합니다. 토큰은 Git에 저장하지 않습니다.

## Codex 연결

로컬 `stdio` 연결:

```powershell
codex mcp add research-wiki -- research-wiki-mcp --root "C:\path\to\Research_WIKI"
codex mcp list
```

HTTP 연결:

```powershell
$env:RESEARCH_WIKI_MCP_TOKEN = "replace-with-a-local-shared-token"
codex mcp add research-wiki-http --url http://127.0.0.1:8765/mcp --bearer-token-env-var RESEARCH_WIKI_MCP_TOKEN
codex mcp list
```

## Claude Code 연결

프로젝트에는 공유 가능한 프로젝트 저장소의 `.mcp.json`이 포함되어 있습니다. 각 구성원은 패키지를 설치한 뒤 이 프로젝트에서 Claude Code를 실행하고 프로젝트 MCP 서버 사용을 승인하면 됩니다.

직접 다시 등록하려면:

```powershell
claude mcp add --transport stdio --scope project research-wiki -- research-wiki-mcp --root '${CLAUDE_PROJECT_DIR:-.}'
claude mcp list
```

HTTP 연결과 토큰 환경 변수 사용 방법은 프로젝트 저장소의 `docs/client-setup.md`에 정리했습니다.

## 검증

```powershell
python -m unittest discover -s tests -v
python -m compileall -q src tests
research-wiki-mcp --help
research-wiki-gui --help
```

`tests/test_e2e_workflow.py`는 실제 MCP `stdio` 연결을 통해 PDF 추출, `source` 및 `concept` 반영, 파란 논문 상태, 비교 배지, 검토 완료, 검색, 인덱스 재생성을 검증합니다.

## 저장 구조

- `wiki/`: Git으로 관리하는 canonical Markdown
- `raw/papers/`: 로컬 PDF 입력
- `raw/screenshots/`: 다시 만들 수 있는 PDF 스크린샷 산출물
- `wiki/assets/`: WIKI Markdown 본문에 삽입하는 Git 관리 이미지
- `data/wiki-index.sqlite3`: 다시 만들 수 있는 검색 인덱스

## 첫 마일스톤 제외 범위

- 외부 서버 배포
- DOI, arXiv URL, 웹 URL 입력
- 공유 폴더 자동 감시
- 사용자별 계정과 세부 권한
- Git 이외의 자동 백업
- 서버 내부 LLM API 호출
