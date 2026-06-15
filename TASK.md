# Media Ai Mcp Tasks

Planning is closed. Implement exactly one topmost unfinished item per loop.

## Stage 0 — Brief
- [x] Write `specs/brief.md`.

## Stage 1 — Disambiguation
- [x] Identify open questions in `specs/clarifications.md`.
- [x] Resolve all blocking items.

## Stage 2 — Requirements
- [x] Write `specs/requirements.md`.
- [x] Write `specs/acceptance.md`.
- [x] Write the implementation-ready PRD or goal specification.
- [x] Write `README.md` with project overview, MCP Tool behavior, and execution instructions.
- [x] Record initial decisions in `specs/decisions.md`.
- [x] Confirm validation commands in `harness/validation.md`.
- [x] Get user sign-off and write `specs/plan-closed.md`.

## Implementation
- [x] Initialize Git, Python package structure, canonical WIKI directories, configuration defaults, and a focused scaffold test.
- [x] Add Markdown WIKI schema models, page storage, provenance fields, and Git-backed revision operations.
- [x] Add rebuildable database index and WIKI search.
- [x] Add local PDF text extraction and screenshot artifact extraction with page-range support.
- [x] Add MCP server resources, tools, prompts, and `stdio` transport.
- [x] Add Streamable HTTP transport with shared-token authentication.
- [x] Add local GUI for paper states, browsing, editing, ingest configuration, draft review, and index rebuild.
- [x] Add Codex and Claude Code configuration guidance, end-to-end validation, and finalized execution instructions.
- [x] Add GUI MCP status navigation, capability visibility, and startup-time enable or disable controls.
- [x] Add Git-managed WIKI image attachments for PDF screenshots, expose MCP publishing, and render attached images in the GUI.
- [x] Add proactive discussion capture through MCP and improve WIKI browsing with page-type, paper, and expanded-list views.

## Productization
- [x] Consolidate into one runnable clone-and-go product: tools/ MCP server + viewer, harness with RULES.md + skill + hook, ready-to-use wiki, bundled sample, demo/ screenshot, 30-minute README, and submission/ cleanup.
