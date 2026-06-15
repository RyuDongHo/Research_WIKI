"""Claude Code SessionStart hook.

Injects this repository's core operating rules into the agent's context at the
start of every session, so a newcomer's agent immediately knows how to drive
the LLM Wiki. Registered in .claude/settings.json.
"""
import json
import sys

CONTEXT = (
    "이 저장소는 자기 자료(raw/papers의 PDF)를 MCP 도구로 정리해 Git 관리 Markdown "
    "WIKI(wiki/)와 로컬 뷰어를 만드는 LLM Wiki 제품입니다.\n"
    "- 핵심 규칙: RULES.md (Markdown이 원본, 에이전트 쓰기는 항상 draft, reviewed 승격은 사람만, 출처 앵커 필수).\n"
    "- 자료 통합 요청을 받으면 .claude/skills/wiki-ingest 스킬을 따르세요.\n"
    "- MCP 서버 이름: research-wiki (.mcp.json). 뷰어: research-wiki-gui → http://127.0.0.1:8780"
)


def main() -> None:
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": CONTEXT,
        }
    }
    # Write UTF-8 bytes directly so the output is encoding-independent on Windows.
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    sys.stdout.buffer.write(data)


if __name__ == "__main__":
    main()
