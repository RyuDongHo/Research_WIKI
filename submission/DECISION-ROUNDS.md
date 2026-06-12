# Research MCP WIKI Tool Discussion Rounds

Append planning discussion outcomes here. Keep earlier rounds intact when adding later answers or corrections.

## Round 0 - Project Initiation

- Date: 2026-06-01
- Status: recorded
- Prompt: Create a lab-wide MCP-based WIKI Tool whose domain concept is helping research itself. Document discussion and decision rounds before implementation.
- Outcome: Initialized the planning harness, wrote the brief, and opened four decision rounds.
- Recorded decisions:
  - The tool is intended for shared lab use.
  - MCP is a core interface.
  - The domain focus is research assistance.
  - Requirements and implementation remain open until the decision rounds are resolved.

## Round 1 - Product Center And Users

- Date opened: 2026-06-01
- Status: awaiting user response
- Goal: Decide what the first version is fundamentally for and who participates in the shared knowledge system.
- Questions:
  1. What should be the center of gravity of the first usable version: shared research memory, executable research workflow tools, or a balanced combination?
  2. Who are the initial users, and what read, contribute, curate, and admin roles do they need?
  3. Which knowledge objects must the WIKI handle first?

## Planned Later Rounds

- Round 2: canonical storage, ingestion, provenance, and review.
- Round 3: MCP tool surface, client support, and extensibility.
- Round 4: hosting, security, MVP exclusions, and implementation constraints.

## Round 1 Response - Workflow Scope And Collaboration

- Date recorded: 2026-06-01
- Status: follow-up required
- User response:
  1. Use the skills under `C:\Users\thffh\Desktop\MonteCarlo-research-WIKI\codex-skills` as a reference. The tool should extract paper PDFs, summarize content, separate WIKI pages by paper topic, create claims, extract and organize reusable core ideas from prior work, assess claim fitness, and validate novelty for suitable claims.
  2. Every lab member should be able to edit freely.
  3. The earlier knowledge-object question was too abstract and must be asked more concretely.
- Reference inspection:
  - `maintain-research-wiki` defines `source`, `concept`, `comparison`, `claim`, and `system` maintenance workflows.
  - The existing WIKI schema additionally includes `question` and `skill` pages.
  - `read-research-pdf` and `write-paper-context` define PDF extraction and durable paper-context workflows.
  - `validate-research-novelty` and `research-novelty-analyzer` define mechanism-level claim review and novelty validation workflows.
- Recorded decisions:
  - Build a workflow-integrated shared research WIKI rather than WIKI CRUD alone.
  - Permit all lab members to read, contribute, and edit shared content.
  - Use the MonteCarlo research WIKI skills and artifact schema as a planning reference.
- Follow-up question:
  - When a member adds one paper PDF, which pages should be saved into the shared WIKI automatically, and which should wait for human confirmation?

## Round 1 Follow-Up Response - Paper Ingestion Outputs

- Date recorded: 2026-06-01
- Status: resolved, with one deferred GUI detail
- User response:
  1. Persist `source` and `concept` pages by default.
  2. Generate or update `comparison` pages when selected as an option by the user.
  3. If a GUI is implemented, show paper-list status using colors: registered or processed papers in blue and unread papers in red. The exact role of optional comparison processing in the transition needs confirmation.
  4. Do not treat `claim` and `question` pages as outputs of one paper alone. They require additional user input and belong to separate workflows.
- Recorded decisions:
  - Baseline paper ingest writes `source` and `concept`.
  - Comparison synthesis is user-selected.
  - Claim and question maintenance are user-driven workflows.
  - GUI status colors are useful but the exact transition is deferred until GUI scope is selected.

## Round 2 - Storage, Ingestion, Provenance, And Review

- Date opened: 2026-06-01
- Status: awaiting user response
- Goal: Decide where the shared knowledge lives and how edits remain recoverable in an open-editing lab environment.
- Questions:
  1. Should Markdown files in Git remain the canonical source of truth, should a database become canonical, or should Markdown remain canonical with a database index for search and GUI performance?
  2. Besides local PDF upload, which ingestion entry points are needed first: DOI or arXiv URL, web URL, an existing shared-paper folder, or only PDF upload?
  3. Since all members may edit freely, should every change retain author, timestamp, source links, and Git-style revision history so accidental edits can be reviewed and recovered?

## Round 2 Partial Response - Markdown And PDF Reading Modes

- Date recorded: 2026-06-01
- Status: follow-up required
- User response:
  1. When reading a PDF, separate text-extraction reading from screenshot-based integrated image-plus-text reading and let the user choose.
  2. WIKI data is generally stored as Markdown files.
- Recorded decisions:
  - WIKI knowledge artifacts are Markdown files.
  - PDF ingest exposes a user-selectable text-extraction mode.
  - PDF ingest exposes a user-selectable screenshot-based image-plus-text mode.
- Still open:
  - Whether Markdown files require Git revision history.
  - Whether a derived search or GUI database index is allowed.
  - Whether screenshot mode processes every page or supports selected page ranges.
  - Which PDF entry points belong in the first version beyond local or uploaded PDF files.

## Round 2 Follow-Up Response - Canonical Store And Local PDF Boundary

- Date recorded: 2026-06-01
- Status: provenance follow-up required
- User response:
  1. Manage Markdown WIKI files with Git.
  2. Allow a database index for search and GUI performance.
  3. Support only local PDF files as paper-ingestion inputs in the first version.
  4. Support selected page ranges in screenshot-based image-plus-text reading mode.
- Recorded decisions:
  - Git-managed Markdown files are canonical.
  - A database may serve as a rebuildable derived index.
  - First-version paper ingest accepts local PDF files only.
  - Screenshot-based reading supports page-range selection.
- Remaining Round 2 question:
  - Decide provenance and review status rules for human edits and AI-generated WIKI content.

## Round 2 Final Response - Provenance And Review

- Date recorded: 2026-06-01
- Status: resolved
- User response: proceed with the proposed trust policy.
- Recorded decisions:
  - Record author, modification time, source PDF path, and page or section evidence.
  - Mark AI-generated WIKI content as `status: draft`.
  - Promote confirmed content to `status: reviewed`.
  - Keep editing open to all lab members and use Git history for recovery.

## Round 3 - MCP Server Surface And Clients

- Date opened: 2026-06-01
- Status: awaiting user response
- Goal: Define the first MCP server implementation boundary.
- User correction:
  - The project must implement the MCP server itself.
- Official MCP reference check:
  - MCP servers can expose `resources`, `tools`, and `prompts`.
  - `Streamable HTTP` is the modern remote-server transport.
  - `stdio` is available for local process-spawned integrations.
- Questions:
  1. Should the first version support shared `Streamable HTTP`, local `stdio`, or both?
  2. Which clients must work first: Codex, Claude Code, both, or additional MCP clients?
  3. For the MVP, should the server expose all three MCP primitives below?
     - `resources`: read WIKI pages, paper metadata, and index views.
     - `tools`: search, ingest local PDF, choose reading mode and page range, write or edit Markdown, review drafts, request optional comparisons, create user-driven claims and questions, assess claim fitness, and run novelty review.
     - `prompts`: reusable guided workflows for paper ingest, claim refinement, and novelty review.

## Documentation Deliverables - PRD And README

- Date recorded: 2026-06-01
- Status: required
- User direction:
  1. Produce a PRD or specification suitable for executing the project and achieving its goal.
  2. Produce a `README.md` that explains the project, lists MCP Tools used or planned, explains their behavior, and documents how to run the project.
- Recorded decision:
  - Treat both documents as required project deliverables.
  - Write their finalized content after blocking planning questions are resolved so that the documents describe an agreed implementation target.

## Round 3 Partial Response - MCP Primitives And Clients

- Date recorded: 2026-06-01
- Status: transport follow-up required
- User response:
  1. Read and write operations are both required.
  2. Support both Codex and Claude Code.
  3. Expose `resources`, `tools`, and `prompts`.
- Recorded decisions:
  - MCP must support both WIKI reads and writes.
  - Support Codex and Claude Code as first-version clients.
  - Expose all three MCP primitives.
- Clarification:
  - Read and write capability does not choose the MCP transport. Transport selection remains open.
- Remaining Round 3 question:
  - Should the first version implement shared `Streamable HTTP`, local `stdio`, or both?

## Round 3 Final Response - MCP Transports

- Date recorded: 2026-06-01
- Status: resolved
- User response: implement option 2.
- Recorded decision:
  - Support shared `Streamable HTTP`.
  - Support local `stdio`.

## Round 4 - Hosting, Security, MVP Boundary, And Stack

- Date opened: 2026-06-01
- Status: awaiting user response
- Goal: Choose a practical first deployment and implementation boundary before writing the PRD and README.
- Questions:
  1. Where should the shared `Streamable HTTP` server run first: one lab workstation or server on the internal network, an externally reachable server, or local-only during the first milestone?
  2. For the first milestone, what access control is required: internal-network access without login, a shared token, or individual user accounts?
  3. Should GUI implementation be part of the first milestone, or should MCP server, Markdown WIKI, Git history, and rebuildable search index come first?
  4. Is Python with the official MCP Python SDK acceptable as the implementation stack?

## Round 4 Partial Response - Local Milestone And Python Stack

- Date recorded: 2026-06-01
- Status: final follow-up required
- User response:
  1. Validate local execution only in the first milestone.
  2. Use shared-token authentication.
  3. Include the GUI.
  4. Use Python and the official MCP Python SDK.
- Recorded decisions:
  - First milestone validation is local.
  - Streamable HTTP uses a shared token.
  - GUI is included in the first milestone.
  - Implementation uses Python and the official MCP Python SDK.
- Remaining Round 4 details:
  - Confirm whether Git recovery is sufficient backup for the first milestone.
  - Confirm GUI paper-list colors and optional comparison marker.
  - Confirm MVP exclusions so the PRD remains implementable.

## Round 4 Final Response - Recovery, GUI, And MVP Exclusions

- Date recorded: 2026-06-01
- Status: resolved
- User response:
  1. Git history recovery is sufficient for the first milestone; separate automatic backup is not required.
  2. Use red for papers not yet ingested, blue after `source` and `concept` reflection, and retain blue with a separate badge after optional `comparison` generation.
  3. Exclude external deployment, remote URL ingest, shared-folder watching, per-user accounts, fine-grained authorization, and automatic backup beyond Git.
  4. Allow a reasonably detailed GUI in the first milestone.
- Recorded decision:
  - All blocking planning questions are resolved. Proceed to requirements, PRD, README, contract, and validation drafting.

## Architecture Follow-Up - Model Execution Boundary

- Date opened: 2026-06-01
- Status: awaiting user response
- Reason for reopening clarification:
  - The agreed workflows include model-dependent reasoning: paper summarization, concept extraction, claim-fitness assessment, and novelty review.
  - The GUI is included in the first milestone, so it matters whether GUI actions can invoke an LLM-backed server workflow directly or only prepare tasks for a connected Codex or Claude Code client.
- Question:
  - Should model-dependent work run in connected Codex or Claude Code clients through MCP, in the MCP server through a configured LLM API, or through both paths?

## Architecture Follow-Up Response - Client-Side Model Reasoning

- Date recorded: 2026-06-01
- Status: resolved
- User response: use option 1 for now.
- Recorded decision:
  - Connected Codex or Claude Code clients perform PDF summarization, concept extraction, claim-fitness assessment, and novelty review through MCP.
  - The first-milestone server provides deterministic storage, search, PDF extraction, Git, authentication, indexing, and GUI support without invoking a separate LLM API.

## PDF Implementation Follow-Up - Output Language

- Date recorded: 2026-06-01
- Status: resolved
- User direction:
  - Use Korean by default.
  - Allow English extraction or reflection as an option.
- Recorded decision:
  - Keep original PDF text unchanged.
  - Attach `ko` or `en` as the requested client-side reflection language.
  - Store WIKI page language in frontmatter and expose language filtering through the derived index.

## GUI Follow-Up - MCP Capability Management

- Date recorded: 2026-06-02
- Status: resolved and implemented
- User direction:
  - Add MCP management to the GUI.
  - Add `MCP 상태` to the left navigation.
  - Show what the current MCP contains and allow modifications.
- Recorded decision:
  - List MCP resources, tools, and prompts with descriptions.
  - Allow maintainers to enable or disable each capability.
  - Save choices to `mcp-settings.json`.
  - Apply changes on the next server start so an active MCP client connection is not interrupted.
## Round 8 - Canonical WIKI Image Attachments

### User Request

- Allow WIKI source summaries to include images while organizing a paper.
- Improve the MCP Tool so visual evidence can be preserved in the source page.

### Outcome

- Keep raw screenshot previews reproducible and ignored by Git.
- Add a Git-managed `wiki/assets/<source-slug>/` attachment store for selected PDF pages.
- Add `wiki_publish_pdf_screenshots` and inline GUI rendering for Markdown image attachments.

## Round 9 - Discussion Capture And WIKI Browsing

### User Request

- While Research WIKI MCP is connected, automatically add discussion outcomes that belong in source, claim, comparison, concept, or related WIKI pages.
- Browse WIKI pages by knowledge-object category.
- Reduce excessive scrolling caused by the small WIKI page list.
- Browse WIKI categories by paper as well.

### Outcome

- Add client-invoked `wiki_capture_discussion`; connected models call it when durable knowledge emerges.
- Preserve the server boundary: MCP does not monitor conversations autonomously.
- Add WIKI object-type tabs, linked-paper filtering, reflected-paper navigation, and an expanded dedicated WIKI list.

## Numbering Note

- Date recorded: 2026-06-13
- Rounds 5-7 correspond to post-milestone user-feedback iterations on the GUI (PDF reading defaults and sidebar navigation, review-control wording, workbench navigation separation). They were resolved interactively and recorded as journal.md entries on 2026-06-01 20:13, 20:18, and 20:22 instead of formal round sections, so the formal numbering resumes at Round 8.


---

# Appendix: Implementation Journal (append-only work log)

# Media Ai Mcp Journal

Append only. Do not edit or delete previous entries.

- [2026-06-01 18:50] Planning harness initialized - wrote the project brief and opened decision rounds for a lab-wide research MCP WIKI Tool.
- [2026-06-01 18:50] Harness validation passed - scaffold check reported `harness complete`; planning remains open with Round 1 awaiting user response.
- [2026-06-01 18:56] Round 1 partially resolved - recorded workflow-integrated research WIKI scope, open collaborative editing, reference skill inspection, and a concrete follow-up question about persisted page types.
- [2026-06-01 19:01] Round 1 resolved - paper ingest persists source and concept pages by default, comparison is user-selected, claim and question workflows require additional user input, and GUI color detail was deferred.
- [2026-06-01 19:04] Round 2 partially resolved - recorded Markdown WIKI artifacts and user-selectable text-extraction versus screenshot-based image-plus-text PDF reading modes.
- [2026-06-01 19:07] Round 2 storage and input boundary resolved - Git-managed Markdown is canonical, a rebuildable DB index is allowed, local PDFs are the first-version input, and screenshot reading supports page ranges.
- [2026-06-01 19:11] Round 2 trust policy resolved and Round 3 opened - recorded provenance and draft-review states, and elevated MCP server implementation to a required deliverable.
- [2026-06-01 19:12] Documentation deliverables recorded - require an implementation-ready PRD or goal specification and a README covering project purpose, MCP Tool behavior, and execution instructions.
- [2026-06-01 19:15] Round 3 partially resolved - require MCP reads and writes, expose resources tools and prompts, support Codex and Claude Code, and leave transport selection open.
- [2026-06-01 19:16] Round 3 resolved and Round 4 opened - support Streamable HTTP and stdio, then decide hosting, access control, GUI milestone, and implementation stack.
- [2026-06-01 19:18] Round 4 partially resolved - validate locally with shared-token HTTP auth, include GUI, and use Python with the official MCP Python SDK.
- [2026-06-01 19:20] Round 4 resolved - use Git-only recovery for the first milestone, include a detailed workflow GUI with paper-state colors and comparison badges, and close MVP exclusions.
- [2026-06-01 19:20] Architecture clarification reopened - model-dependent workflow execution must be assigned to connected clients, a server-side LLM API, or both before Stage 2 drafting.
- [2026-06-01 19:23] Architecture clarification resolved - Codex or Claude Code clients perform model reasoning through MCP; the first-milestone server does not call an LLM API.
- [2026-06-01 19:23] Stage 2 draft written - added requirements, acceptance criteria, contract, procedure, preferences, validation gates, implementation-ready PRD, and planning README.
- [2026-06-01 19:23] Stage 2 document validation passed - scaffold reported `harness complete`, no unresolved planning markers remain, and `specs/plan-closed.md` correctly remains absent pending user approval.
- [2026-06-01 19:25] Planning closed by explicit user approval - wrote `specs/plan-closed.md`, opened implementation tasks, and selected the Python and Git foundation scaffold.
- [2026-06-01 19:27] Foundation scaffold completed - initialized Git, added the Python package and canonical WIKI layout, added configuration defaults and one focused test, and passed unittest, compileall, harness, and plan-closed checks.
- [2026-06-01 19:32] Markdown WIKI storage completed - added validated page models, strict frontmatter rendering and parsing, provenance metadata, Git-backed save history review and restore operations, aligned seed pages, and passed 4 tests plus compileall and harness checks.
- [2026-06-01 19:36] Rebuildable WIKI index completed - added derived SQLite rebuild and filtered search, fixed Windows connection cleanup, indexed the root WIKI index page, and passed 7 tests plus compileall, harness, and a 2-page workspace rebuild smoke check.
- [2026-06-01 19:41] Local PDF extraction completed - added validated page ranges, PyMuPDF text and PNG-plus-text screenshot artifacts, pypdf text fallback, Korean-default and English-optional reflection metadata, language-aware WIKI indexing, and passed 13 tests plus compileall, harness, and workspace index rebuild checks.
- [2026-06-01 19:49] MCP stdio core completed - added official MCP SDK dependencies, deterministic service layer, FastMCP resources tools and Korean-default prompts, stdio entry point, SDK ClientSession subprocess smoke test, and passed 16 tests plus compileall, harness, and CLI help checks.
- [2026-06-01 19:52] Streamable HTTP completed - added token-protected `/mcp` ASGI middleware, environment-only shared-token loading, HTTP CLI options, and an SDK HTTP-client subprocess smoke test covering missing invalid and valid tokens; passed 18 tests plus compileall, harness, and CLI help checks.
- [2026-06-01 20:04] Local GUI completed - added a Korean-first Starlette dashboard with paper-state colors and comparison badges, WIKI browsing and Git-backed editing, draft review, search, PDF text or screenshot preview settings with page ranges and language options, and index rebuild; passed 20 tests plus compileall, GUI CLI help, browser rendering, editor-loading, PDF-tab, and browser-error-log checks.
- [2026-06-01 20:13] Local GUI usability correction completed - added an explicit default `전체 읽기` PDF option with opt-in page ranges, connected sidebar navigation to active states and focused content views, and enforced hidden-section rendering; passed 20 tests, compileall, and harness checks. Browser interaction verified the PDF range toggle and both sidebar views before the in-app browser stopped reattaching during the final CSS-only recheck.
- [2026-06-01 20:18] WIKI review controls clarified - removed the editable status dropdown, renamed `초안 저장` to `저장`, renamed `검토 완료` to `검토 완료로 표시`, and preserved automatic draft creation plus explicit reviewed promotion; passed 20 tests, compileall, harness checks, and a local HTTP markup smoke check. The in-app browser remained unavailable at webview attach.
- [2026-06-01 20:22] Workbench navigation separation completed - removed the mixed-purpose sidebar `WORKFLOW` actions, kept the left sidebar knowledge-navigation only, added top-level and in-panel workbench close controls with a reopen button, and expanded the center column when the workbench is closed; passed 20 tests, compileall, harness checks, and local HTTP markup verification. The in-app browser remained unavailable at webview attach.
- [2026-06-01 21:06] First local milestone finalized - documented Codex and Claude Code stdio and token-protected HTTP setup, added shared Claude Code `.mcp.json`, finalized the Korean README, corrected paper blue-state logic to require both source and concept reflections, isolated Git subprocess stdin from MCP stdio, and added an MCP end-to-end PDF reflection test covering comparison review search and rebuild; passed 21 tests, compileall, harness, CLI-help, and JSON checks.
- [2026-06-02 00:12] Initial research corpus reflected - read the 6 PDFs under `raw/papers`, saved Korean source summaries and 8 reusable concept pages through the local MCP, refreshed the WIKI index, and verified all 6 GUI paper states as blue.
- [2026-06-02 00:24] Public repository package prepared - excluded local PDF inputs from Git and organized the MCP server, GUI, documentation, tests, harness, and canonical Markdown WIKI for GitHub publication.
- [2026-06-02 11:49] GUI MCP capability management completed - added the left-nav MCP status view, version-managed startup toggles for 17 resources tools and prompts, restart-safe application semantics, documentation, and regression coverage; passed 25 tests, compileall, harness checks, browser toggle-save verification, and browser error-log inspection.
- [2026-06-02 13:22] Exemplar-CNN source deepened - visually inspected key figures and tables, added page-grounded Eq. 1-7 analysis, classification and descriptor-matching evidence, limitations, and open questions, then rebuilt the WIKI index.
- [2026-06-02 13:44] Git-managed WIKI image attachments completed - added `wiki_publish_pdf_screenshots`, canonical `wiki/assets` storage, screenshot-mode source embedding, inline GUI rendering, schema and README guidance, 6 Exemplar-CNN visual pages, and regression coverage; passed 26 tests, compileall, harness checks, diff checks, HTTP asset serving, browser rendering, and browser error-log inspection.
- [2026-06-02 13:51] Proactive discussion capture and WIKI browsing completed - added client-invoked `wiki_capture_discussion` with append, create, dedupe, draft-review, and provenance behavior; added object-type tabs, linked-paper filtering, reflected-paper navigation, expanded WIKI lists, documentation, and regression coverage; passed 28 tests, compileall, harness checks, diff checks, browser filter verification, and browser error-log inspection.
- [2026-06-02 13:56] Gradient-guided patch construction question captured - recorded the Exemplar-CNN-inspired distinction between gradient-weighted crop sampling and gradient-guided patch generation, including risks and ablation questions, then prepared WIKI history for push.
- [2026-06-13 14:10] Submission deliverables completed - wrote DOMAIN.md knowledge-domain definition, restored the 6 reference PDFs, captured 4 MVP GUI screenshots, and packaged the assignment zip.
- [2026-06-13 14:40] Comparison and claim workflows demonstrated - saved comparison/pretext-vs-self-distillation across all 6 papers, created claim/gradient-guided-patch-efficiency, promoted exemplar-cnn source and instance-discrimination concept to reviewed, and rebuilt the 19-page index.
- [2026-06-13 14:50] Agent SPEC consolidated - wrote specs/agent-spec.md defining wiki agent roles, permissions, allowed capabilities, capture criteria, and prohibitions; inlined acceptance checks into PRD section 12; cleaned README paths; added SimCLR as a visible un-ingested red-state paper and refreshed MVP captures.
