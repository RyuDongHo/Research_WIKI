# Media Ai Mcp Agent Guide

> At the start of every session, read this file and `journal.md` first.
> This file defines the local operating rules for this project.

## 0. Structure

- `RULES.md` - quick operating-rules summary; read after this file.
- `specs/` - agreed requirements, acceptance criteria, and `agent-spec.md` (agent roles/permissions).
- `specs/discussion-rounds.md` - append-only planning discussion record.
- `TASK.md` - ordered checklist; work on only the top unfinished item.
- `journal.md` - append-only local work log.
- `harness/` - contract, procedure, validation, and preferences.
- `.claude/skills/wiki-ingest/` - the material→wiki ingest skill agents follow.
- `.claude/settings.json` + `scripts/session_context_hook.py` - SessionStart hook injecting rules.
- `tools/research_wiki_mcp/` - the MCP server and local viewer GUI.
- `wiki/` - canonical Markdown wiki; `wiki/system/page-schema.md` is the schema.
- `AGENTS.md` - this file.

## 1. Planning Gate

Spec design follows three stages. Do not advance past a stage until it is complete.

**Stage 0 — Brief**
- Write `specs/brief.md` first: one paragraph problem statement, audience, and success criterion.
- Do not enumerate requirements yet.

**Stage 1 — Disambiguation**
- List every ambiguous term, unstated constraint, and open decision in `specs/clarifications.md`.
- Mark each item `blocking` or `deferred`. A `deferred` item must have a written reason it is safe to defer.
- Do not write `specs/requirements.md` until no `blocking` items remain.

**Stage 2 — Requirements**
- Write `specs/requirements.md` and `specs/acceptance.md` after all blocking clarifications are resolved.
- Record design decisions in `specs/decisions.md`.
- Append each discussion round and its outcome to `specs/discussion-rounds.md`.
- Confirm validation commands in `harness/validation.md`.
- Ask the user to review and confirm the spec.
- Write `specs/plan-closed.md` only when the user explicitly closes planning.
- Do not write production code before `specs/plan-closed.md` exists.

## 2. Implementation Loop

1. Read the last 5 lines of `journal.md`.
2. Select exactly one topmost unfinished item from `TASK.md`.
3. Read related code and docs before editing.
4. Implement only that item.
5. Run the validation commands in `harness/validation.md`.
6. If validation fails, fix until it passes or stop at the failure budget.
7. Mark the item done in `TASK.md`.
8. Append one line to `journal.md`:
   `- [YYYY-MM-DD HH:MM] <summary> - <result>`
9. Stop and wait for the next iteration.

## 3. Never Do

- Do not handle more than one task per iteration.
- Do not skip or weaken failing tests.
- Do not add dependencies without explicit user approval.
- Do not rewrite or delete `journal.md`; append only.
- Do not continue after three failed attempts with the same approach.

## 4. If Blocked

- If a requirement is ambiguous, add it to `specs/clarifications.md` and ask the user.
- If the same approach fails three times, append the situation to `journal.md` and report.
