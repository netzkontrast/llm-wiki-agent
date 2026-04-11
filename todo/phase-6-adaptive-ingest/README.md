# Phase 6: Adaptive Ingest Architecture

**Status:** `not-started`
**Prerequisites:** Phase 1 (wiki directories must exist before Group B tooling)
**Spec reference:** `docs/adaptive-ingest.md`

## Purpose

Establish the infrastructure for token-efficient, self-improving ingest — for both
interactive sessions (Claude Code) and autonomous batch runs (Gemini Jules). The
primary constraint is token economy; accuracy is achieved through structured planning
before writing, not through loading everything into context.

Three interlocking ideas drive this phase:

1. **qmd as the context layer** — replace bulk file-loading with targeted search
2. **Decompose before ingest** — generate a per-file plan identifying known vs. new
   entities before a single wiki page is written
3. **Session logs as a feedback loop** — every session leaves a trail that a consolidation
   skill uses to continuously improve navigation and instructions

---

## Groups

### Group A — Foundation (start immediately, parallel with Phase 1)

These tasks have no dependencies on Phase 1 wiki content.

- [ ] A1. Split CLAUDE.md / GEMINI.md
  - Move all autonomous ingest instructions, Gemini-specific workflows, and the
    "Ingest Workflow" section into `GEMINI.md`
  - Keep `CLAUDE.md` focused on: codebase development, interactive workflows,
    session start protocol, Python tool usage
  - Both files reference the same Python tools — no duplication of tool logic
  - See `docs/adaptive-ingest.md § Agent Personas` for the split boundary

- [ ] A2. Create `log/` directory structure
  - `log/.gitkeep` + `log/README.md` (schema reference: what goes in each log file)
  - Session subfolders are created at runtime by `tools/session_init.py` (Group B)
  - Naming convention: `log/{git-branch-name}/YYYY-MM-DD-HH-MM/`
  - Each session folder contains: `plan.md`, `findings.md`, `decisions.md`

- [ ] A3. Add `tools/install-qmd.sh`
  - Install via `npm install -g @tobilu/qmd` (fallback: `bun install -g @tobilu/qmd`)
  - Initialize wiki collection: `qmd collection add wiki/ --name wiki`
  - Initialize raw collection: `qmd collection add raw/ --name raw`
  - Add context hints:
    ```
    qmd context add qmd://wiki "LLM Wiki: characters, locations, concepts, sources, rules, themes"
    qmd context add qmd://raw  "Source documents waiting for ingestion"
    ```
  - Run initial embed: `qmd embed`
  - Document in `tools/README.md` which tool requires qmd

- [ ] A4. Register qmd as Claude Code MCP plugin
  - Add to `~/.claude/settings.json` (MCP server block) or via
    `claude plugin marketplace add tobi/qmd`
  - Document in `CLAUDE.md` under Tools section
  - Note: Gemini Jules uses CLI (`qmd query ...`), not MCP — its install script handles this

---

### Group B — Python Tooling (after Phase 1 wiki dirs exist)

- [ ] B1. `tools/decompose.py` — per-file entity analysis → ingest plan
  - Input: path to a raw source file
  - Step 1: Extract candidate entity names (regex over capitalized terms, Markdown
    headers, quoted strings, bold text)
  - Step 2: For each candidate, run `qmd search "{name}" --files --min-score 0.4`
    to classify as **known** (exists in wiki/) or **new** (not found)
  - Step 3: Detect likely page types from content heuristics (character-like language,
    location descriptions, rule definitions, timeline markers)
  - Step 4: Print a structured per-file ingest plan to stdout (Markdown format):
    ```markdown
    ## Ingest Plan: {filename}
    ### Known entities (merge, do not overwrite)
    - Kael → wiki/characters/Kael.md
    ### New entities (create)
    - LogosPrime-Station → wiki/locations/LogosPrime-Station.md (new)
    ### Likely page types needed
    - [x] source, character, location
    - [ ] conflict, theme, rule, timeline, foreshadowing
    ### Potential contradictions to check
    - "AEGIS destroyed in chapter 3" — check wiki/characters/AEGIS.md
    ### Suggested context to load before writing
    - wiki/characters/Kael.md (known, will be updated)
    - wiki/characters/AEGIS.md (contradiction risk)
    ```
  - This plan is reviewed (interactive) or logged and executed (autonomous)

- [ ] B2. `tools/session_init.py` — initialize a session log folder
  - Reads current git branch name
  - Creates `log/{branch}/{timestamp}/plan.md` with empty template
  - Outputs the session log path to stdout so the calling agent can reference it
  - Called at the start of any ingest session

- [ ] B3. Extend `tools/ingest.py` for novel page types
  - Add novel page type arrays to JSON response schema:
    `character_pages`, `location_pages`, `conflict_pages`, `theme_pages`,
    `rule_pages`, `timeline_pages`, `foreshadowing_pages`
  - Replace `index_entry: str` with `index_entries: dict[section → [entries]]`
  - Implement `update_index_multi()` (single read + multi-section insert + one write)
  - Extend `build_wiki_context()`: after 5 recent source pages, add qmd query results
    for entities mentioned in the source file (requires qmd installed)
  - Extend prompt to include `docs/wiki-schema.md` content (or key schemas)
  - Add per-type write loop (unified `NOVEL_PAGE_KEYS`)
  - `action` field per page: `"create"` or `"update"` (merge vs. new)
  - Run `qmd embed` after all writes succeed (keep index fresh)

- [ ] B4. Add `qmd embed` call to ingest post-write hook
  - Append to the successful ingest path in `tools/ingest.py`
  - Only if qmd is installed (`shutil.which("qmd") is not None`), else skip silently

---

### Group C — Skills and Commands (after Group B tooling)

- [ ] C1. Rewrite `.claude/commands/wiki-ingest.md` — 20-step extended ingest
  - Steps 1–4: context loading (uses qmd for targeted page lookup, not bulk read)
  - Steps 5–19: writes (source, entities, concepts, novel types, index, log, move)
  - Merge Rule block (mandatory: update sources: field, append only, log contradictions)
  - Token budget note: context ceiling 20 pages; use qmd for additional lookups

- [ ] C2. Create `.claude/commands/wiki-decompose.md` — per-file planning skill
  - Trigger: "decompose raw/foo.md" or before any interactive ingest session
  - Runs `tools/decompose.py {file}` and presents the plan to the user
  - User reviews/edits the plan interactively
  - Approved plan is saved to `log/{branch}/{session}/plan.md`
  - SPARK-influenced: explicitly asks "what could be wrong in this source file's framing?"
  - Output: a validated per-file ingest plan, ready for `/wiki-ingest` execution

- [ ] C3. Create `.claude/commands/wiki-consolidate.md` — continuous improvement skill
  - Trigger: "consolidate session findings" or run periodically
  - Reads all `log/{branch}/*/findings.md` files since last consolidation
  - Identifies recurring issues, missed entity types, contradictions left unresolved
  - Proposes concrete improvements to: `docs/`, `CLAUDE.md`/`GEMINI.md`, wiki READMEs
  - Outputs a diff-style proposal; user approves before any file is written
  - Never writes wiki content — only improves instructions and navigation

- [ ] C4. Update `CLAUDE.md` ingest workflow section to match 20-step spec
  - Reference `GEMINI.md` for autonomous variant
  - Add note: "For novel-specific page types, see `docs/wiki-schema.md`"
  - Add note: "Run `/wiki-decompose` before `/wiki-ingest` for any file > 2000 words"

---

### Group D — Orchestration Rules (spec only, no code changes)

These tasks produce sections in `docs/adaptive-ingest.md` only.

- [ ] D1. Define subagent patterns
  - Which model handles which task (Haiku for entity extraction, Sonnet for synthesis,
    Opus/Claude for planning and contradiction resolution)
  - When to spawn a subagent vs. inline processing
  - How subagents receive context (qmd query output as stdin, not file reads)

- [ ] D2. Define context ceilings per workflow
  - Ingest: max 20 pages in context; use qmd for additional lookups
  - Decompose: max 5 pages (the source file + 4 most relevant known entities)
  - Consolidate: reads log files only, never wiki content directly

- [ ] D3. Define session log schema formally
  - `plan.md`: what this session will do (generated by `/wiki-decompose` or manually)
  - `findings.md`: what actually happened (written during/after session)
  - `decisions.md`: architectural decisions made (feeds `/wiki-consolidate`)
  - Format for each, append-only rules, what triggers a new session folder

- [ ] D4. Open question (decision gate — resolve before Phase 6 C tasks begin)
  **Should basic-wiki ingest (source/entity/concept) be decoupled from novel-wiki ingest
  (character/location/theme/etc.)?**
  - Option X: Single ingest, both layers in one LLM call (current plan)
  - Option Y: Two-pass ingest — pass 1 captures facts (Haiku, cheap), pass 2 maps to
    novel structure (Sonnet, expensive, optional)
  - Option Z: Gemini Jules only ingests to basic layer; a separate `wiki-synthesize`
    skill maps to novel layer on demand
  - Recommendation: start with Option X; migrate to Option Y/Z if context length
    becomes a real problem (measure, don't anticipate)

---

## Completion Criteria

- `qmd` is installed, indexed, and usable from Claude Code via MCP and CLI
- `tools/decompose.py` correctly classifies known vs. new entities for a test file
- `tools/session_init.py` creates correctly named session log folders
- `tools/ingest.py` writes novel page types and updates index correctly by section
- `/wiki-decompose` produces a readable, accurate per-file ingest plan
- `/wiki-ingest` runs all 20 steps without manual correction for a test file
- `/wiki-consolidate` reads session logs and produces a concrete improvement proposal
- `CLAUDE.md` and `GEMINI.md` are cleanly separated with no duplicated prose
- Session log schema is documented in `log/README.md`
- D4 decision is resolved and documented in `log/` or `docs/`

When all tasks are checked, update `todo/README.md`: set Phase 6 to `complete`.
