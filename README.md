# LLM Wiki Agent & Novel-Author Extension

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**A coding agent skill for building persistent, interlinked wikis from source documents.** Drop files into `raw/`, say `/wiki-ingest` — the agent reads them, extracts knowledge, and maintains a structured wiki that compounds over time. Extended for novel authoring with an 18-type schema, temporal filtering, reader progressive disclosure, and a full writing pipeline.

> This started as a generic knowledge wiki. It's now being extended into a specialized tool for writing *Das Kohärenz-Protokoll* — a hard sci-fi novel with a DID-protagonist, 13 alter identities, an AI antagonist, 39 chapters, and layered philosophical frameworks. The extensions work for any structurally complex novel.

---

## Dual-State Wiki Architecture

The project is organized into four major layers, maintaining a clear separation of concerns to prevent context dilution for LLMs.

### 1. Knowledge Layer (`wiki/knowledge/`)
The static, general-purpose wiki handling any domain — research papers, book notes, business intelligence, or personal knowledge.
- **Workflows:** `/wiki-ingest-knowledge`, `/wiki-query`

### 2. Narrative Layer (`wiki/narrative/`)
Tracks the evolving states and elements of the story, serving as the metadata hub for the writing pipeline.
- **Workflows:** `/wiki-chapter`, `/wiki-character`, `/wiki-worldbuild`, `/wiki-conflict`

### 3. Reader State Layer (`wiki/reader_state/`)
Models what the *reader* knows at each point in the novel.
- **Workflows:** `/wiki-reader-model`

### 4. Meta Layer (`wiki/meta/`)
Governs the underlying rules, agent instructions, and maintenance of the wiki itself.
- **Key Files:** `contradiction-log.md`, `validation-protocol.md`, and session logs.

---

## Directory Layout

```
raw/                    # Immutable source documents — never modify these
processed/              # Source documents that have been ingested successfully
wiki/                   # Agent-maintained wiki layer
  index.md              # Catalog of all pages — updated on every ingest
  log.md                # Append-only chronological record
  overview.md           # Living synthesis across all sources
  knowledge/            # Base layer: concepts, entities, rules, sources, syntheses, timeline
  narrative/            # Novel layer: chapters, characters, locations, conflicts, themes, arcs, beats, dramatica, manuscripts, outlines, timeline
  reader_state/         # Progressive disclosure: foreshadowing, reader-model
  meta/                 # Contradiction log, protocols, archive, ingest
docs/                   # Reference specs (load only when needed)
  jules/                # Developer specifications and architectural proposals
todo/                   # Phased implementation plan with progress tracking
graph/                  # Auto-generated knowledge graph output
tools/                  # Python tools for linting, parsing, graphing, and queries
```

---

## Page Types (18 total)

### Generic Knowledge Layer (4 types)
| Type | Purpose |
|------|---------|
| `source` | One summary per ingested document |
| `entity` | People, companies, projects mentioned across sources |
| `concept` | Ideas, frameworks, methods — cross-referenced |
| `synthesis` | Saved query answers filed back into the wiki |

### Novel Narrative & Reader Layer (11 types)
| Type | Purpose |
|------|---------|
| `character` | Profiles, psychology, voice, alter system tracking |
| `chapter` | Metadata hub — POV, timeline, draft status, characters, constraints |
| `location` | World-building, sensory palette, symbolic meaning |
| `conflict` | Internal/external/thematic, self-referential paradoxes |
| `theme` | Thematic threads, motifs, dialectical pairs |
| `timeline-event` | Chronological anchors, causality, boundary markers |
| `rule` | World rules, narrative mandates, structural constraints |
| `arc` | Character/plot/thematic transformation stages |
| `dramatica` | Throughlines, signposts, story points |
| `reader-state` | Per-chapter reader knowledge, tension, terminology ratchet |
| `foreshadowing` | Cross-cutting strands tracked: planted → reinforced → resolved |

### Writing Pipeline (3 types)
| Type | Purpose |
|------|---------|
| `outline` | Chapter structural plan — ordered beat sequence, pacing |
| `beat` | Atomic scene moment — characters, tension, foreshadowing |
| `manuscript` | Actual written prose with revision tracking |

---

## Core Systems & Concepts

### Dependency-Driven Navigation
Every wiki page declares `requires:` (what to load for context) and `informs:` (what to update after changes) in its YAML frontmatter. Reading uses bounded traversal (max-depth 2) to protect the context window. Writing uses **unbounded propagation** — when a page changes, the agent follows the full `informs:` chain until every downstream page is updated or confirmed current.

### Writing Pipeline
The novel-writing pipeline orchestrates drafting via the `/wiki-chapter` command, delegating to sub-workflows to generate distinct page types:
```
Chapter (spec) → Outline (structure) → Beats (atomic scenes) → Manuscript (prose)
```
Each stage has its own status lifecycle and dedicated workflow within `.claude/commands/`.

### Temporal Filtering
Pages can specify `valid_from` and `valid_until` fields referencing timeline events. An agent working on chapter 15 automatically loads only the character states, world-rules, and conflicts that are true at that story-point.

### Reader Progressive Disclosure
A parallel tracking system models what the *reader* knows at each chapter. The `terminology_permitted` list is a one-way ratchet — each chapter inherits the previous chapter's list and may add but never subtract. Foreshadowing strands are tracked across their full lifecycle (planted → reinforced → resolved). Agents can't use concepts the reader hasn't encountered yet.

### Contradiction Hierarchy
When pages disagree, resolution follows a strict hierarchy: `rule > source > character > chapter > synthesis`. Contradictions are always logged in `wiki/meta/contradiction-log.md`, never silently resolved.

---

## Agent Integration

The wiki provides decoupled instructions for different agents based on their persona and tooling constraints.

| Agent | Schema file | Purpose |
|---|---|---|
| Claude Code | `CLAUDE.md` | Interactive orchestrator and system developer |
| Gemini CLI | `GEMINI.md` | Autonomous batch file processing |
| Codex / OpenCode | `AGENTS.md` | General instructions |

### Workflows (`.claude/commands/`)
Agent workflows are structured as slash commands (e.g., `/wiki-ingest`, `/wiki-lint`, `/wiki-chapter`). They run specific toolchain orchestrations, delegating down into individual markdown instructions (using `SKILL.md` frontmatter) which execute under a 100-line limit for token efficiency.

---

## Python Tooling

The `/tools/` directory contains optional standalone Python scripts to analyze and maintain the wiki logic (requires `ANTHROPIC_API_KEY` where LLMs are used).

- **`tools/lint_deterministic.py`**: A fast, programmatic tool to check basic YAML schema, frontmatter validity, directory invariants, and orphan states (no API required).
- **`tools/lint.py`**: Semantic validation with LLMs checking logic and contextual links.
- **`tools/check_staleness.py`**: Traces the `informs:` chain to identify files that might be out of sync.
- **`tools/decompose.py`**: First pass of ingestion, mapping entities before LLM action.

### The Knowledge Graph (`tools/build_graph.py`)
Two-pass build outputting to `graph/graph.html`:
1. **Deterministic** — parses all `[[wikilinks]]` and `requires:`/`informs:` edges.
2. **Semantic** — agent infers implicit relationships → edges tagged `INFERRED` with confidence scores.
Louvain community detection clusters nodes by topic. A SHA256 cache ensures only changed pages are reprocessed. No server, opens locally in any browser.

---

## Implementation Status

The original generic wiki layer has been successfully extended with the novel-author architecture. Implementation is following a phased plan defined in `todo/README.md`.

| Phase | Status | Description |
|-------|--------|-------------|
| 0 | `complete` | Infrastruktur: Ingest-Queue-Migration, Wiki-Oberschichten, Progressive Disclosure |
| 1 | `complete` | Wiki schema extension: page types, directories, frontmatter, seed templates, folder READMEs |
| 2 | `complete` | Navigation, dependencies, temporal filtering, deterministic lint rules, staleness checks |
| 3 | `complete` | Workflows, slash commands, discovery/validation hooks, SKILL.md migration |
| 4 | `complete` | CLAUDE.md integration, graph extension, deterministic lint, ingest updates |
| 5 | `complete` | Writing pipeline: beats, outlines, manuscripts, 4 new workflows |
| **6** | **`active`** | **Token-efficient ingest: qmd, decompose script, session logging, CLAUDE/GEMINI split** |
| 7 | `not-started` | Meta-Consolidation: Agent Instruction Decoupling, Multi-stage Ingestion |

---

## Install

**Requires:** [Claude Code](https://claude.ai/code), [Codex](https://openai.com/codex), [Gemini CLI](https://github.com/google-gemini/gemini-cli), or any agent that reads a config file.

```bash
git clone https://github.com/netzkontrast/llm-wiki-agent.git
cd llm-wiki-agent
```

Open in your agent — no API key or Python setup needed (except for tools):

```bash
claude      # reads CLAUDE.md + .claude/commands/
codex       # reads AGENTS.md
opencode    # reads AGENTS.md
gemini      # reads GEMINI.md
```

## Tips

- Use [Obsidian](https://obsidian.md) to browse the wiki — follow `[[wikilinks]]`, check graph view, use Dataview for frontmatter queries.
- Use [Obsidian Web Clipper](https://obsidian.md/clipper) to clip web articles directly to `raw/`.
- The wiki is a git repo — version history for free, diff prose across draft stages.

## License

MIT License — see [LICENSE](LICENSE) for details.
