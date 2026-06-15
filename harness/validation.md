# Research MCP WIKI Tool Validation

## Planning Gates

- [x] brief: `specs/brief.md` exists with a problem statement.
- [x] clarify: no `blocking` items remain in `specs/clarifications.md`.
- [x] spec-closed: `specs/plan-closed.md` exists after explicit user sign-off.

## Engineering Gates

- [x] structure: required harness files exist.
- [x] specs: requirements and acceptance criteria are filled.
- [x] task: exactly one implementation item is selected for the iteration.
- [x] preflight: Python, Git, official MCP SDK, and required PDF backends are present.
- [x] unit: focused tests pass.
- [x] mcp-stdio: local stdio server smoke test passes.
- [x] mcp-http: local Streamable HTTP and shared-token checks pass.
- [x] e2e: MCP PDF reflection, paper states, comparison badge, review, search, and rebuild flow passes.
- [x] index: derived index rebuild test passes.
- [x] gui: local GUI smoke test passes.
- [x] report: `journal.md` is updated.

## Commands

Run now during planning:

```powershell
python "C:\Users\thffh\.codex\skills\start-project-harness\scripts\scaffold_project_harness.py" --check .
rg -n "\| blocking \|" .\specs\clarifications.md
Test-Path .\specs\plan-closed.md
```

Current foundation checks:

```powershell
$env:PYTHONPATH = "tools"
python -m unittest discover -s tests -v
python -m compileall -q tools tests
```

PDF extraction checks are included in the unittest suite. Screenshot tests run when PyMuPDF is available.

Current MCP end-to-end check:

```powershell
python -m unittest discover -s tests -p test_e2e_workflow.py -v
```

The end-to-end test connects through MCP `stdio`, extracts a local PDF, saves `source` and `concept` reflections, captures a durable discussion outcome, verifies the red-to-blue paper transition, saves a comparison page, checks the GUI badge state, promotes a page to `reviewed`, searches the WIKI, and rebuilds the index.

Current stdio MCP launch:

```powershell
research-wiki-mcp --root .
```

The unittest suite contains an SDK `ClientSession` subprocess smoke test for stdio MCP resources, tools, and prompts.

Current local GUI launch:

```powershell
research-wiki-gui --host 127.0.0.1 --port 8780 --root .
```

The unittest suite validates GUI dashboard loading, WIKI save/read/review, index rebuild, PDF text preview, screenshot preview, screenshot artifact serving, MCP capability status, and MCP setting persistence. Browser verification checks the rendered Korean dashboard, WIKI type filters, linked-paper filtering, expanded WIKI lists, MCP-status navigation, PDF-reading tab, WIKI editor loading, and browser error log.

Current Streamable HTTP MCP launch:

```powershell
$env:RESEARCH_WIKI_MCP_TOKEN = "replace-with-a-local-shared-token"
research-wiki-mcp --transport streamable-http --host 127.0.0.1 --port 8765 --root .
```

The unittest suite starts an HTTP subprocess and verifies missing-token rejection, invalid-token rejection, and a valid-token MCP tool call.

Client configuration guidance:

```powershell
codex mcp add --help
claude mcp add --help
claude mcp add-json --help
python -m json.tool .mcp.json
```

`README.md`, `docs/client-setup.md`, and `.mcp.json` document Codex and Claude Code `stdio` setup plus token-protected HTTP alternatives.

Current index rebuild smoke check:

```powershell
$env:PYTHONPATH = "tools"
@'
from research_wiki_mcp import AppConfig, WikiIndex
index = WikiIndex(AppConfig.from_root("."))
print(f"rebuilt={index.rebuild()}")
'@ | python -
```

## Failure Budget

- Stop after three failed attempts with the same approach.
- Append the failure state to `journal.md`.
- Report the blocker instead of trying a fourth time.
