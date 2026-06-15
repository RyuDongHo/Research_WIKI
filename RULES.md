# RULES — Agent 운영 규칙 (빠른 컨텍스트)

> 이 저장소에서 작업하는 모든 AI 에이전트(Claude Code, Codex)가 따르는 핵심 규칙 요약본이다.
> 전체 운영 절차는 [AGENTS.md](./AGENTS.md), 에이전트 권한 명세는 [specs/agent-spec.md](./specs/agent-spec.md)를 본다.

## 1. 이 저장소는 무엇인가

자신의 자료(PDF)를 `raw/papers/`에 넣고 MCP 도구로 정리하면, Git으로 관리되는 Markdown WIKI(`wiki/`)와 로컬 뷰어 GUI가 생성되는 **개인/연구실용 LLM Wiki 제품**이다. 코드는 `tools/`, 에이전트 운영 컨텍스트는 `harness/`에 있다.

## 2. 절대 규칙

1. **Markdown이 원본이다.** `wiki/`의 `.md`가 canonical, `data/`의 SQLite는 언제든 재생성 가능한 파생물이다. DB를 source of truth로 다루지 않는다.
2. **에이전트 쓰기는 항상 `status: draft`로 저장한다.** `reviewed` 승격은 사람(연구자)만 한다.
3. **출처를 남긴다.** PDF 기반 페이지는 `sources`에 파일 경로, 본문에 페이지/수식 앵커(`p.3`, `Eq.1`)를 기록한다.
4. **MCP를 통해서만 WIKI를 쓴다.** canonical Markdown을 서버 밖에서 직접 수정하지 않는다(사람의 GUI/수동 편집 제외).
5. **언어 기본값은 한국어.** 영어 정리는 사용자가 명시적으로 요청할 때만, `language: en`으로.
6. **자동 산출물 경계.** 논문 1편 반영의 자동 결과는 `source`+`concept`뿐이다. `comparison`은 사용자 요청 시, `claim`/`question`은 사용자 입력이 있어야 만든다.

## 3. 첫 통합 요청을 받으면 (핵심 워크플로)

사용자가 "이 자료로 위키 만들어줘"라고 하면 [`wiki-ingest` 스킬](./.claude/skills/wiki-ingest/SKILL.md)을 따른다:

1. `pdf_extract_text` 또는 `pdf_render_screenshots`로 PDF를 읽는다.
2. 근거 중심 한국어 `source` 페이지를 `wiki_save_page`로 저장한다(draft).
3. 재사용 가능한 메커니즘을 `concept` 페이지로 분리 저장한다.
4. `wiki_rebuild_index`로 인덱스를 갱신한다.
5. 사용자에게 GUI(`http://127.0.0.1:8780`)에서 확인하도록 안내한다.

## 4. 금지

- 근거 없는 내용을 `confidence: high`로 저장
- 사용자 지시 없는 `reviewed` 승격·리비전 복원·대량 일괄 수정
- `journal.md` 수정/삭제 (append-only)
- 공유 토큰 등 비밀값을 Git에 커밋
