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

### Group A — Foundation (start immediately)

> **A0 is the prerequisite for everything else in this phase.** Phase 1 was
> completed with a flat `wiki/` structure. These migration tasks move existing
> content into the 4-layer nested layout before any new tooling is built.

- [x] A0. Migrate flat wiki structure → 4-layer nested layout
  ```sh
  # Knowledge layer (rules, timeline content moved here)
  git mv wiki/rules/        wiki/knowledge/rules/
  # wiki/timeline/ held story-world events → moved to narrative/timeline/ instead

  # Narrative layer
  git mv wiki/characters/   wiki/narrative/characters/
  git mv wiki/chapters/     wiki/narrative/chapters/
  git mv wiki/locations/    wiki/narrative/locations/
  git mv wiki/conflicts/    wiki/narrative/conflicts/
  git mv wiki/themes/       wiki/narrative/themes/
  git mv wiki/arcs/         wiki/narrative/arcs/
  git mv wiki/dramatica/    wiki/narrative/dramatica/
  git mv wiki/beats/        wiki/narrative/beats/
  git mv wiki/outlines/     wiki/narrative/outlines/
  git mv wiki/manuscripts/  wiki/narrative/manuscripts/
  git mv wiki/timeline/     wiki/narrative/timeline/   # story-world boundary events

  # Reader state layer
  git mv wiki/reader-model/   wiki/reader_state/reader-model/
  git mv wiki/foreshadowing/  wiki/reader_state/foreshadowing/

  # Meta layer
  git mv wiki/archive/      wiki/meta/archive/
  ```
  - Created `wiki/knowledge/timeline/` (empty, new README for research provenance)
  - Created `wiki/knowledge/sources/`, `entities/`, `concepts/`, `syntheses/` (empty + .gitkeep)
  - Created `wiki/meta/ingest/` for session logs
  - Updated all page-type README paths and layer attributions
  - Updated `wiki/index.md` to use nested paths
  - Layer routing READMEs already correct from prior work

- [x] A1. Split CLAUDE.md / GEMINI.md
  - Move all autonomous ingest instructions, Gemini-specific workflows, and the
    "Ingest Workflow" section into `GEMINI.md`
  - Keep `CLAUDE.md` focused on: codebase development, interactive workflows,
    session start protocol, Python tool usage
  - Both files reference the same Python tools — no duplication of tool logic
  - See `docs/adaptive-ingest.md § Agent Personas` for the split boundary

- [x] A2. Create `log/` directory structure
  - `log/.gitkeep` + `log/README.md` (schema reference: what goes in each log file)
  - Session subfolders are created at runtime by `tools/session_init.py` (Group B)
  - Naming convention: `log/{git-branch-name}/YYYY-MM-DD-HH-MM/`
  - Each session folder contains: `plan.md`, `findings.md`, `decisions.md`

- [x] A3. Add `tools/install-qmd.sh`
  - Install via `npm install -g @tobilu/qmd` (fallback: `bun install -g @tobilu/qmd`)
  - Initialize **per-layer** collections (not one monolithic wiki collection):
    ```sh
    qmd collection add wiki/knowledge/   --name knowledge
    qmd collection add wiki/narrative/   --name narrative
    qmd collection add wiki/reader_state/ --name reader-state
    qmd collection add wiki/meta/        --name meta
    qmd collection add raw/              --name raw
    ```
  - Add context hints per layer:
    ```sh
    qmd context add qmd://knowledge   "Static facts: sources, entities, concepts, rules, timelines, syntheses"
    qmd context add qmd://narrative   "Story structure: characters, locations, chapters, conflicts, themes, arcs, beats"
    qmd context add qmd://reader-state "Reader knowledge: foreshadowing, per-chapter terminology ratchet"
    qmd context add qmd://meta        "System: session logs, protocols, contradiction log, archive"
    qmd context add qmd://raw         "Source documents waiting for ingestion"
    ```
  - Run initial embed: `qmd embed`
  - Document in `tools/README.md` which tool requires qmd

- [x] A4. Register qmd as Claude Code MCP plugin
  - Add to `~/.claude/settings.json` (MCP server block) or via
    `claude plugin marketplace add tobi/qmd`
  - Document in `CLAUDE.md` under Tools section
  - Note: Gemini Jules uses CLI (`qmd query ...`), not MCP — its install script handles this

---

### Group B — Python Tooling (after Phase 1 wiki dirs exist)

- [x] B1. `tools/decompose.py` — per-file entity analysis → ingest plan
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
    - Kael → wiki/narrative/characters/Kael.md  [layer: narrative]
    ### New entities (create)
    - LogosPrime-Station → wiki/narrative/locations/LogosPrime-Station.md  [layer: narrative]
    - CoherenceField → wiki/knowledge/concepts/CoherenceField.md  [layer: knowledge]
    ### Layers touched
    - [x] knowledge (source, concept)
    - [x] narrative (character, location)
    - [ ] reader_state
    ### Potential contradictions to check
    - "AEGIS destroyed in chapter 3" — check wiki/narrative/characters/AEGIS.md
    ### Suggested minimal context (qmd per layer)
    - qmd search "Kael" -c narrative
    - qmd search "AEGIS" -c narrative
    ```
  - This plan is reviewed (interactive) or logged and executed (autonomous)

- [x] B2. `tools/session_init.py` — initialize a session log folder
  - Reads current git branch name
  - Creates `log/{branch}/{timestamp}/plan.md` with empty template
  - Outputs the session log path to stdout so the calling agent can reference it
  - Called at the start of any ingest session

- [x] B3. Extend `tools/ingest.py` for novel page types
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

- [x] B4. Add `qmd embed` call to ingest post-write hook
  - Append to the successful ingest path in `tools/ingest.py`
  - Only if qmd is installed (`shutil.which("qmd") is not None`), else skip silently

---

### Group C — Skills and Commands (after Group B tooling)

- [x] C1. Rewrite `.claude/commands/wiki-ingest.md` — orchestrator only
  - The main skill now orchestrates layer sub-skills; it does NOT write pages directly
  - Steps: run decompose → determine layers touched → call sub-skills in order →
    update `wiki/index.md` (all sections) → append `wiki/log.md` → move file
  - Token budget note: orchestrator context ceiling 5 pages; sub-skills own their context

- [x] C2. Create `.claude/commands/wiki-ingest-knowledge.md` — knowledge layer ingest
  - Writes: `knowledge/sources/`, `knowledge/entities/`, `knowledge/concepts/`,
    `knowledge/rules/`, `knowledge/timeline/`, `knowledge/syntheses/`
  - Context: qmd `-c knowledge` only; ceiling 10 pages
  - Model target: Haiku (factual extraction, structured schema, predictable)
  - Used by Gemini Jules for autonomous batch ingest
  - Merge rule: always update `sources:` field; append new facts only

- [x] C3. Create `.claude/commands/wiki-ingest-narrative.md` — narrative layer ingest
  - Writes: `narrative/characters/`, `narrative/locations/`, `narrative/conflicts/`,
    `narrative/themes/`, `narrative/arcs/`, `narrative/dramatica/`, `narrative/timeline/`
  - Context: qmd `-c narrative` + any known entity pages from decompose plan; ceiling 15 pages
  - Model target: Sonnet (relationship complexity, merge logic)
  - Interactive preferred; autonomous only for well-structured sources
  - Merge rule: merge character profiles; never overwrite established traits without contradiction log entry

- [x] C4. Create `.claude/commands/wiki-ingest-reader.md` — reader state ingest
  - Writes: `reader_state/reader-model/`, `reader_state/foreshadowing/`
  - Context: qmd `-c reader-state` + current chapter page; ceiling 5 pages
  - Triggered manually after chapter writing, not during document ingest
  - Monotonic-only: only add to `terminology_permitted`, never remove

- [x] C5. Create `.claude/commands/wiki-decompose.md` — per-file planning skill
  - Trigger: "decompose raw/foo.md" or before any interactive ingest session
  - Runs `tools/decompose.py {file}` and presents the plan to the user
  - Plan shows: layers touched, known vs. new entities, qmd search commands to run
  - User reviews/edits the plan interactively
  - Approved plan saved to `log/{branch}/{session}/plan.md`
  - SPARK-influenced: asks "what in this file's framing could be wrong or misleading?"
  - Output: a validated per-file ingest plan, ready for `/wiki-ingest` execution

- [x] C6. Create `.claude/commands/wiki-consolidate.md` — continuous improvement skill
  - Trigger: "consolidate session findings" or run periodically
  - Reads all `log/{branch}/*/findings.md` files since last consolidation
  - Uses `qmd search -c meta` to find related past decisions and protocols
  - Proposes concrete improvements to: `docs/`, `CLAUDE.md`/`GEMINI.md`, wiki READMEs
  - Outputs a diff-style proposal; user approves before any file is written
  - Never writes wiki content — only improves instructions and navigation

- [x] C7. Update `CLAUDE.md` ingest workflow section to match orchestrator + sub-skill pattern
  - Reference `GEMINI.md` for autonomous variant (knowledge layer only via C2)
  - Add note: "Run `/wiki-decompose` before `/wiki-ingest` for any file > 2000 words"

---

### Group D — Orchestration Rules (spec only, no code changes)

These tasks produce sections in `docs/adaptive-ingest.md` only.

- [x] D1. Define subagent patterns
  - Which model handles which task (Haiku for entity extraction, Sonnet for synthesis,
    Opus/Claude for planning and contradiction resolution)
  - When to spawn a subagent vs. inline processing
  - How subagents receive context (qmd query output as stdin, not file reads)

- [x] D2. Define context ceilings per workflow
  - Ingest: max 20 pages in context; use qmd for additional lookups
  - Decompose: max 5 pages (the source file + 4 most relevant known entities)
  - Consolidate: reads log files only, never wiki content directly

- [x] D3. Define session log schema formally
  - `plan.md`: what this session will do (generated by `/wiki-decompose` or manually)
  - `findings.md`: what actually happened (written during/after session)
  - `decisions.md`: architectural decisions made (feeds `/wiki-consolidate`)
  - Format for each, append-only rules, what triggers a new session folder

- [x] D4. Open question (decision gate — resolve before Phase 6 C tasks begin)
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
