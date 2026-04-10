# LLM Wiki Agent

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**A coding agent skill for building persistent, interlinked wikis from source documents.** Drop files into `raw/`, say `/wiki-ingest` — the agent reads them, extracts knowledge, and maintains a structured wiki that compounds over time. Extended for novel authoring with a 14-type schema, temporal filtering, reader progressive disclosure, and a full writing pipeline.

> This started as a generic knowledge wiki. It's now being extended into a specialized tool for writing *Das Kohärenz-Protokoll* — a hard sci-fi novel with a DID-protagonist, 13 alter identities, an AI antagonist, 39 chapters, and layered philosophical frameworks. The extensions work for any structurally complex novel.

---

## Two Layers

### Generic Knowledge Wiki (working now)

The base wiki handles any domain — research papers, book notes, business intelligence, personal knowledge. Four page types, four workflows.

```
/wiki-ingest raw/papers/attention-is-all-you-need.md
/wiki-query "what are the main approaches to reducing hallucination?"
/wiki-lint
/wiki-graph
```

### Novel-Author Extension (in development)

Extends the wiki with 14 page types, temporal filtering, a reader model, and a writing pipeline. Designed for agents that need to maintain consistency across a complex novel while writing actual prose.

```
/wiki-chapter 5        # orchestrates: outline → beats → manuscript
/wiki-outline 5        # structure chapter 5 into beats
/wiki-beats 5          # detail each beat with characters, tension, foreshadowing
/wiki-manuscript 5     # write prose following the outline and beats
```

See [`Concept.md`](Concept.md) for the full architecture and [`handover.md`](handover.md) for open questions.

---

## Directory Layout

```
raw/                    # Immutable source documents — never modify these
wiki/                   # Agent-maintained knowledge layer
  index.md              # Catalog of all pages — updated on every ingest
  log.md                # Append-only chronological record
  overview.md           # Living synthesis across all sources
  sources/              # One summary per source document
  entities/             # People, companies, projects
  concepts/             # Ideas, frameworks, methods
  syntheses/            # Saved query answers
  characters/           # Character profiles, psychology, voice
  chapters/             # Chapter specs — POV, timeline, constraints
  outlines/             # Structural plans — ordered beat sequences
  beats/                # Atomic scene moments — tension, foreshadowing
  manuscripts/          # Actual written prose
  locations/            # World-building, environmental storytelling
  conflicts/            # Conflict tracking, self-referential paradoxes
  themes/               # Thematic threads, motifs, dialectics
  timeline/             # Chronological events, temporal anchors
  rules/                # World rules, narrative mandates, structural constraints
  arcs/                 # Character/plot/thematic transformation tracking
  dramatica/            # Dramatica Theory elements
  reader-model/         # Per-chapter reader knowledge state
  foreshadowing/        # Cross-cutting strands: planted → reinforced → resolved
  archive/              # Deprecated content (never delete, always archive)
  meta/                 # Contradiction log, protocols
docs/                   # Reference specs (load only when needed)
todo/                   # Phased implementation plan with progress tracking
graph/                  # Auto-generated knowledge graph
tools/                  # Optional standalone Python scripts
```

---

## Page Types (18 total)

### Generic Layer (4 types)
| Type | Purpose |
|------|---------|
| `source` | One summary per ingested document |
| `entity` | People, companies, projects mentioned across sources |
| `concept` | Ideas, frameworks, methods — cross-referenced |
| `synthesis` | Saved query answers filed back into the wiki |

### Novel Layer (11 types)
| Type | Purpose |
|------|---------|
| `character` | Profiles, psychology, voice, alter system tracking |
| `chapter` | Metadata hub — POV, timeline, characters, constraints |
| `location` | World-building, sensory palette, symbolic meaning |
| `conflict` | Internal/external/thematic, self-referential paradoxes |
| `theme` | Thematic threads, motifs, dialectical pairs |
| `timeline-event` | Chronological anchors, causality, boundary markers |
| `rule` | World rules, narrative mandates, structural constraints |
| `arc` | Character/plot/thematic transformation stages |
| `dramatica` | Throughlines, signposts, story points |
| `reader-state` | Per-chapter reader knowledge, tension, terminology ratchet |
| `foreshadowing` | Strands tracked: planted → reinforced → resolved |

### Writing Pipeline (3 types)
| Type | Purpose |
|------|---------|
| `outline` | Chapter structural plan — ordered beat sequence, pacing |
| `beat` | Atomic scene moment — characters, tension, foreshadowing |
| `manuscript` | Actual written prose with revision tracking |

---

## Key Concepts

### Dependency-Driven Navigation
Every page declares `requires:` (context to load) and `informs:` (pages to update after changes). Reading is bounded (depth 2, context ceilings per workflow). Writing propagation is **unbounded** — when a page changes, the full `informs:` chain is followed to guarantee consistency.

### Temporal Filtering
Pages can specify `valid_from`/`valid_until` as timeline-event slugs. An agent working on chapter 15 loads only the character states, world-rules, and conflicts that are true at that story-point.

### Reader Progressive Disclosure
`terminology_permitted` is a one-way ratchet — each chapter inherits the previous chapter's list and may add but never subtract. Foreshadowing strands are tracked across their full lifecycle. Agents can't use concepts the reader hasn't encountered yet.

### Writing Pipeline
```
Chapter (spec) → Outline (structure) → Beats (atomic scenes) → Manuscript (prose)
```
Each stage has its own status lifecycle and dedicated workflow. The `chapter-writing` command auto-delegates to the right stage.

### Contradiction Hierarchy
When pages disagree: `rule > source > character > chapter > synthesis`. Contradictions are always logged, never silently resolved.

---

## Install

**Requires:** [Claude Code](https://claude.ai/code), [Codex](https://openai.com/codex), [Gemini CLI](https://github.com/google-gemini/gemini-cli), or any agent that reads a config file.

```bash
git clone https://github.com/netzkontrast/llm-wiki-agent.git
cd llm-wiki-agent
```

Open in your agent — no API key or Python setup needed:

```bash
claude      # reads CLAUDE.md + .claude/commands/
codex       # reads AGENTS.md
opencode    # reads AGENTS.md
gemini      # reads GEMINI.md
```

---

## Usage

### Generic Wiki Commands

```
/wiki-ingest raw/papers/my-paper.md       # ingest a source into the wiki
/wiki-query "what are the main themes?"   # synthesize answer from wiki pages
/wiki-lint                                # find orphans, contradictions, gaps
/wiki-graph                               # build interactive knowledge graph
```

### Novel-Author Commands

```
/wiki-chapter 5                           # orchestrate chapter 5 work (auto-delegates)
/wiki-outline 5                           # plan chapter 5 structure and beats
/wiki-beats 5                             # detail beats with characters, tension, foreshadowing
/wiki-manuscript 5                        # write prose for chapter 5
/wiki-character Kael                      # develop character profile
/wiki-worldbuild LogosPrime               # develop location or world rule
/wiki-conflict KaelVsAegis               # analyze or resolve a conflict
/wiki-reader-model 5                      # check reader knowledge state at chapter 5
```

Plain English also works:
```
"Ingest this file: raw/papers/llama2.md"
"What does the wiki say about attention mechanisms?"
"Write prose for chapter 3 — Kael's first encounter with AEGIS"
"What does the reader know at chapter 12?"
```

---

## Implementation Status

The generic wiki layer is fully functional. The novel-author extension is designed and documented but not yet implemented. Implementation follows a phased plan:

| Phase | Status | Description |
|-------|--------|-------------|
| 1 | not-started | Schema: page types, directories, seed templates |
| 2 | not-started | Navigation: dependency system, temporal filtering |
| 3 | not-started | Workflows: slash commands, trigger patterns |
| 4 | not-started | Integration: CLAUDE.md, lint, graph, migration |
| 5 | not-started | Writing pipeline: beats, outlines, manuscripts |

See [`todo/README.md`](todo/README.md) for the full roadmap.

---

## The Graph

Two-pass build:

1. **Deterministic** — parses all `[[wikilinks]]` and `requires:`/`informs:` edges across wiki pages
2. **Semantic** — agent infers implicit relationships → edges tagged `INFERRED` with confidence scores

Louvain community detection clusters nodes by topic. SHA256 cache means only changed pages are reprocessed. Output is a self-contained `graph.html` — no server, opens in any browser.

---

## CLAUDE.md / AGENTS.md

The schema file tells the agent how to maintain the wiki — page formats, workflows, naming conventions, session-start protocol. Edit it to customize behavior.

| Agent | Schema file |
|---|---|
| Claude Code | `CLAUDE.md` |
| Codex / OpenCode | `AGENTS.md` |
| Gemini CLI | `GEMINI.md` |

---

## What Makes This Different from RAG

| RAG | LLM Wiki Agent |
|---|---|
| Re-derives knowledge every query | Compiles once, keeps current |
| Raw chunks as retrieval unit | Structured wiki pages with typed frontmatter |
| No cross-references | Cross-references pre-built via `requires:`/`informs:` |
| Contradictions surface at query time (maybe) | Flagged at ingest time, logged to contradiction-log |
| No accumulation | Every source makes the wiki richer |
| No temporal awareness | Temporal filtering loads only time-relevant content |
| No reader model | Tracks what the reader knows at every chapter |

---

## Tips

- Use [Obsidian](https://obsidian.md) to browse the wiki — follow `[[wikilinks]]`, check graph view, use Dataview for frontmatter queries
- Use [Obsidian Web Clipper](https://obsidian.md/clipper) to clip web articles directly to `raw/`
- The wiki is a git repo — version history for free, diff prose across draft stages
- Standalone Python scripts in `tools/` work without a coding agent (require `ANTHROPIC_API_KEY`)

## Tech Stack

NetworkX + Louvain + Claude + vis.js. No server, no database, runs entirely locally. Everything is plain markdown files.

## Related

- [graphify](https://github.com/safishamsi/graphify) — graph-based knowledge extraction skill (inspiration for the graph layer)
- [Vannevar Bush's Memex (1945)](https://en.wikipedia.org/wiki/Memex) — the original vision this resembles

## License

MIT License — see [LICENSE](LICENSE) for details.
