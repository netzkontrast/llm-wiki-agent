# Adaptive Ingest Architecture

**Status:** Draft — spec under development  
**Phase reference:** `todo/phase-6-adaptive-ingest/`

This document specifies the architecture for token-efficient, self-improving ingest
across two agent personas (Claude Code for development, Gemini Jules for autonomous
batch ingest). Read this when the active task in Phase 6 references it.

---

## Core Principle: Plan Before You Write

Every ingest — interactive or autonomous — follows this sequence:

```
1. DECOMPOSE  →  identify known vs. new entities (cheap, uses qmd)
2. PLAN       →  generate per-file ingest TODO (SPARK-influenced)
3. WRITE      →  execute plan (all page types, merge not overwrite)
4. LOG        →  record findings in session log
5. EMBED      →  refresh qmd index
```

Step 1–2 happen before any wiki file is touched. This prevents the most common failure
mode: writing a new `Kael.md` instead of updating the existing one.

---

## Agent Personas

### Claude Code (interactive + development)

**Role:** Build and improve the system. Run interactive ingests with human review.

Governed by: `CLAUDE.md`

Responsibilities:
- Develop Python tools, skills, and spec documents
- Run `/wiki-decompose` → review plan → approve → run `/wiki-ingest`
- Run `/wiki-consolidate` periodically to improve instructions
- Never run bulk unattended ingests

Token posture: **lean orchestrator** — spawns subagents and Python scripts, reads
minimal context itself.

### Gemini Jules (autonomous batch)

**Role:** Process the ingestion queue unattended. Capture main facts, not exhaustive detail.

Governed by: `GEMINI.md`

Responsibilities:
- Process `raw/` queue in order
- Run `tools/decompose.py` before each file
- Execute the simplified autonomous ingest (capture main aspects only)
- Move processed files to `processed/`
- Log session findings; never modify specs or instructions

Token posture: **minimal and predictable** — fixed context ceiling, no adaptive behavior,
no self-modification.

**Key difference:** Interactive ingest can be deep and exhaustive. Autonomous ingest
should be shallow and reliable. Accuracy over coverage for autonomous; depth on demand
for interactive.

---

## qmd: Context Layer

qmd replaces bulk wiki-loading with targeted search. Instead of reading 20+ pages,
an agent runs one command and gets only what it needs.

### Setup (see `tools/install-qmd.sh`)

One collection per layer — not one monolithic `wiki` collection. This is what enables
per-sub-skill context isolation.

```sh
npm install -g @tobilu/qmd

# Per-layer collections
qmd collection add wiki/knowledge/    --name knowledge
qmd collection add wiki/narrative/    --name narrative
qmd collection add wiki/reader_state/ --name reader-state
qmd collection add wiki/meta/         --name meta
qmd collection add raw/               --name raw

# Context hints (shown in search results, improve relevance)
qmd context add qmd://knowledge   "Static facts: sources, entities, concepts, rules, timelines, syntheses"
qmd context add qmd://narrative   "Story structure: characters, locations, chapters, conflicts, themes, arcs, beats"
qmd context add qmd://reader-state "Reader knowledge: foreshadowing, per-chapter terminology ratchet"
qmd context add qmd://meta        "System: session logs, protocols, contradiction log, archive"
qmd context add qmd://raw         "Source documents waiting for ingestion"

qmd embed
```

### Usage patterns

```sh
# knowledge sub-skill: look up existing concepts/rules
qmd search "coherence theory" -c knowledge --files --min-score 0.4

# narrative sub-skill: look up existing characters/locations
qmd search "Kael" -c narrative --files -n 3
qmd query "LogosPrime setting" -c narrative --files --min-score 0.3

# decompose step: classify entity before deciding which layer
qmd search "AEGIS" --files --min-score 0.4   # searches all collections
qmd search "AEGIS" -c narrative --files       # scoped to narrative

# consolidate skill: search past decisions and logs
qmd search "qmd threshold" -c meta --files

# After any ingest: refresh the index
qmd embed
```

### Context ceiling rules

| Workflow | qmd collections | Max pages in context |
|---|---|---|
| `/wiki-decompose` | all (scoped search) | 5 |
| `wiki-ingest-knowledge` | `-c knowledge` only | 10 |
| `wiki-ingest-narrative` | `-c narrative` only | 15 |
| `wiki-ingest-reader` | `-c reader-state` only | 5 |
| `/wiki-ingest` (orchestrator) | none (delegates) | 5 |
| `/wiki-consolidate` | `-c meta` | 0 wiki pages (log files only) |

Claude Code can also use qmd via MCP (`claude plugin marketplace add tobi/qmd`), which
avoids shell calls and integrates directly into tool use. Gemini Jules uses CLI only.

---

## Per-File Ingest Plan (Decompose Step)

`tools/decompose.py {source-file}` produces a structured plan:

```markdown
## Ingest Plan: {filename}

### Known entities (update — do NOT overwrite)
- Kael → wiki/narrative/characters/Kael.md          [layer: narrative]
- AEGIS → wiki/narrative/characters/AEGIS.md         [layer: narrative]

### New entities (create with full frontmatter)
- LogosPrime-Station → wiki/narrative/locations/     [layer: narrative, new]
- CoherenceField → wiki/knowledge/concepts/          [layer: knowledge, new]

### Layers touched
- [x] knowledge  (source, concept)
- [x] narrative  (character, location)
- [ ] reader_state

### Sub-skills to invoke
- wiki-ingest-knowledge  (factual extraction)
- wiki-ingest-narrative  (character/location updates — interactive review recommended)

### Potential contradictions to check before writing
- "AEGIS destroyed in chapter 3" — qmd search "AEGIS" -c narrative
- Timeline marker "year 12" — qmd search "year 12" -c narrative

### Suggested qmd commands (run before writing)
qmd search "Kael" -c narrative --files
qmd search "AEGIS" -c narrative --files
```

This plan is:
- **Reviewed and approved by the user** in interactive sessions
- **Logged to `log/{branch}/{session}/plan.md`** and executed directly in autonomous runs

SPARK-influenced questions embedded in `/wiki-decompose`:
- "What assumption in this source file could be false or a narrative misdirection?"
- "Which known entity might be wrongly identified here due to name similarity?"
- "Does the timeline in this file contradict any existing boundary events?"

---

## Session Logging

Every session writes to `log/{git-branch}/{YYYY-MM-DD-HH-MM}/`:

### `plan.md`
Generated by `/wiki-decompose` or written manually. Contains:
- What files will be ingested this session
- Per-file decompose plans (output of `tools/decompose.py`)
- Any pre-session context notes

### `findings.md`
Written during/after the session. Contains:
- What was actually created vs. updated vs. skipped
- Contradictions found and how they were handled
- Entities that were harder than expected to classify
- Context loading efficiency (did qmd return useful results?)

### `decisions.md`
Architectural decisions made during the session:
- "Decided to create a new page type X because..."
- "Decided to skip foreshadowing pages for now because..."
- "qmd score threshold raised to 0.5 because too many false positives"

The `/wiki-consolidate` skill reads all `findings.md` and `decisions.md` files since
the last consolidation and proposes concrete improvements.

---

## Sub-Skill Architecture

`/wiki-ingest` is an orchestrator — it does not write pages directly. It determines
which layers a source file touches (from the decompose plan) and delegates:

```
/wiki-ingest (orchestrator)
  ├── tools/decompose.py        → per-file plan (layers, known/new, qmd commands)
  ├── /wiki-ingest-knowledge    → knowledge/sources, entities, concepts, rules, timeline
  ├── /wiki-ingest-narrative    → narrative/characters, locations, conflicts, themes, arcs…
  └── /wiki-ingest-reader       → reader_state/reader-model, foreshadowing (manual only)
  
  After all sub-skills complete:
  ├── Update wiki/index.md (all affected sections)
  ├── Append wiki/log.md
  └── mv raw/{file} processed/{file}
```

**Gemini Jules runs only `wiki-ingest-knowledge`** — factual extraction with Haiku,
predictable schema, no relationship complexity. This is the autonomous batch path.

**Claude Code runs `wiki-ingest-narrative`** interactively after reviewing the decompose
plan, since narrative updates require merge judgment and contradiction awareness.

**`wiki-ingest-reader` is never run during document ingest** — only triggered manually
after a chapter-writing session updates reader state.

---

## Subagent Orchestration

When to delegate and to what:

| Task | Model | qmd collection | Context ceiling |
|---|---|---|---|
| Entity name extraction | Haiku | — | File header only (~500 tokens) |
| Known/new classification | qmd CLI | all | No LLM |
| Per-file plan generation | Sonnet | all | Decompose output + qmd results |
| `wiki-ingest-knowledge` | Haiku | `-c knowledge` | 10 pages |
| `wiki-ingest-narrative` | Sonnet | `-c narrative` | 15 pages |
| `wiki-ingest-reader` | Sonnet | `-c reader-state` | 5 pages |
| Contradiction resolution | Claude (main) | `-c narrative` + `-c knowledge` | Conflicting pages + rules |
| Session consolidation | Claude (main) | `-c meta` | Log files only |

The orchestrator session stays at ≤5 pages. Sub-skills own their context entirely.

---

## Open Question: Single-Pass vs. Two-Pass Ingest (D4)

**Single-pass (Option X):** One LLM call produces all page types. Simpler, but
context gets large for rich source files.

**Two-pass (Option Y):**
- Pass 1 (Haiku, cheap): Extract facts → source, entity, concept pages only
- Pass 2 (Sonnet, expensive, optional): Map facts to novel layer → character, location, etc.

**Separated pipelines (Option Z):**
- Gemini Jules: ingest to basic wiki layer only (source/entity/concept)
- `wiki-synthesize` skill (Claude interactive): build novel layer on demand from basic layer

Recommendation: start with Option X. Migrate if context > 8K tokens per ingest becomes
routine. Measure with `log/` data before deciding.

---

## CLAUDE.md / GEMINI.md Split Boundary

| Content | CLAUDE.md | GEMINI.md |
|---|---|---|
| Session start protocol (dev sessions) | ✓ | |
| Session start protocol (ingest sessions) | | ✓ |
| Python tool usage (all tools) | ✓ | ✓ |
| Interactive ingest workflow | ✓ | |
| Autonomous ingest workflow | | ✓ |
| `/wiki-decompose` skill | ✓ | |
| `/wiki-ingest` skill (reference) | ✓ | ✓ |
| `/wiki-consolidate` skill | ✓ | |
| qmd usage | ✓ | ✓ |
| Codebase development rules | ✓ | |
| Wiki schema reference | ✓ | ✓ |
| Page format and frontmatter | ✓ | ✓ |
| Session logging | ✓ | ✓ (write-only) |

Rule: if an instruction is about **building the system**, it lives in `CLAUDE.md`. If
it's about **using the system to ingest content**, it lives in both or `GEMINI.md` only.
