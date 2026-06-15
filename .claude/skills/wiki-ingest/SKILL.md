---
name: wiki-ingest
description: 사용자가 raw/papers의 PDF(또는 새로 넣은 자료)를 LLM Wiki로 통합/정리해달라고 할 때 사용한다. "이 논문/자료 위키로 만들어줘", "정리해줘", "ingest", "반영", "통합" 같은 요청, 또는 raw/papers에 새 PDF가 추가된 상황에 적용한다. PDF를 읽어 근거 중심 source 페이지와 재사용 가능한 concept 페이지를 MCP로 저장하고 인덱스를 갱신한 뒤 GUI 확인을 안내한다.
---

# Skill: Wiki Ingest (자료 → WIKI 페이지 통합)

이 저장소의 핵심 워크플로다. 한 건의 자료(PDF)를 받아 검토 가능한 WIKI 페이지로 만든다. 전제 규칙은 [RULES.md](../../../RULES.md)와 [specs/agent-spec.md](../../../specs/agent-spec.md)를 따른다.

## 사용 시점

- 사용자가 특정 PDF/자료를 "위키로 만들어줘 / 정리해줘 / 반영해줘 / ingest"라고 요청할 때
- `raw/papers/`에 새 PDF가 들어온 것을 확인하고 통합을 진행할 때

## 사전 조건

- MCP 서버 `research-wiki`가 연결되어 있어야 한다(`.mcp.json` 참고). 도구 이름: `pdf_extract_text`, `pdf_render_screenshots`, `wiki_save_page`, `wiki_rebuild_index`.
- 대상 PDF가 `raw/papers/` 아래에 있어야 한다.

## 절차

1. **대상 확인**: 사용자가 지정한 PDF 경로를 확인한다. 미지정이면 `raw/papers/`를 나열하고 어떤 자료인지 묻는다.

2. **읽기 모드 선택**:
   - 텍스트가 충분한 일반 논문 → `pdf_extract_text` (기본).
   - 그림·수식·표가 핵심이라 시각 근거가 필요하면 → `pdf_render_screenshots`로 페이지 범위를 지정해 이미지+텍스트를 받고, 핵심 figure는 `wiki_publish_pdf_screenshots`로 `wiki/assets/`에 게시해 본문에 인용한다.

3. **source 페이지 작성** (`wiki_save_page`, `page_type="source"`):
   - 언어 기본 한국어. `status`는 명시하지 않아 자동 `draft`.
   - `sources`에 PDF 경로를 넣고, 본문에 핵심 주장 / 방법 / 근거(페이지·수식 앵커) / 한계 / 연결 개념을 정리한다.
   - 근거 없는 단정은 피하고 `confidence`는 보수적으로 설정한다.

4. **concept 페이지 분리** (`wiki_save_page`, `page_type="concept"`):
   - 이 논문에서 다른 논문에도 재사용 가능한 메커니즘 1~3개를 골라 독립 `concept` 페이지로 저장한다.
   - source 및 관련 concept를 `[[slug]]` 위키링크로 연결한다.

5. **인덱스 갱신**: `wiki_rebuild_index`를 호출한다.

6. **확인 안내**: GUI(`research-wiki-gui` 실행 후 `http://127.0.0.1:8780`)의 `논문 보관함`에서 해당 논문이 파란색으로 바뀌었는지, `WIKI 페이지`에서 새 draft 페이지가 보이는지 사용자에게 확인하도록 안내한다.

## 경계

- `comparison`은 사용자가 비교를 요청할 때만 만든다.
- `claim`/`question`은 사용자 입력을 받아 `wiki_create_research_page`로 만든다.
- 작성한 페이지를 직접 `reviewed`로 승격하지 않는다. 검토는 사람의 몫이다.

## 완료 보고

반영한 page_type/slug 목록, 사용한 읽기 모드, 인덱스 페이지 수, GUI 확인 방법을 한 번에 보고한다.
