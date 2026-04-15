# LLM Wiki Agent — Schema & Workflow Instructions

This wiki is maintained entirely by Gemini CLI. No API key or Python scripts needed — just open this repo with `gemini` and talk to it.

## How to Use

Describe what you want in plain English:
- *"Ingest this file: raw/papers/my-paper.md"*
- *"What does the wiki say about transformer models?"*
- *"Check the wiki for orphan pages and contradictions"*
- *"Build the knowledge graph"*

Or use shorthand triggers:
- `ingest <file>` → runs the Ingest Workflow
- `query: <question>` → runs the Query Workflow
- `lint` → runs the Lint Workflow
- `build graph` → runs the Graph Workflow
- `wiki-chapter` → runs the Chapter Writing Workflow
- `wiki-character` → runs the Character Dev Workflow
- `wiki-worldbuild` → runs the Worldbuilding Workflow
- `wiki-timeline` → runs the Timeline Workflow
- `wiki-conflict` → runs the Conflict Resolution Workflow
- `wiki-reader-model` → runs the Reader Model Workflow
- `wiki-revise` → runs the Revision Workflow
- `wiki-lector` → runs the Lectoring Workflow
- `wiki-brainstorm` → runs the Brainstorming Workflow

---

## Directory Layout

```
raw/          # Immutable source documents — waiting for ingestion
processed/    # Source documents that have been ingested — moved from raw/
wiki/         # Agent owns this layer entirely
  index.md    # Catalog of all pages — update on every ingest
  log.md      # Append-only chronological record
  overview.md # Living synthesis across all sources
  knowledge/  # Routing layer: concepts, entities, sources, rules, timeline
  narrative/  # Routing layer: characters, chapters, locations, conflicts, themes, arcs, dramatica, beats, outlines, manuscripts
  reader_state/ # Routing layer: reader-model, foreshadowing
  meta/       # Routing layer: archive, ingest, logs, contradiction-log, protocols
graph/        # Auto-generated graph data
tools/        # Optional standalone Python scripts
```

---

## Ingestion Queue

The ingestion queue is managed by file location, and visualized in `queue.md`:

- `raw/` — files waiting to be ingested (queue)
- `processed/` — files that have been successfully ingested (done)

**After every successful ingest**, move the source file and update `queue.md`:
```bash
mv raw/<filename> processed/<filename>
~/self_created_tools/update_queue.sh
```

To see what's left to ingest:
```bash
ls raw/*.md | wc -l    # count remaining
ls raw/*.md             # list remaining
```

To see what's been processed:
```bash
ls processed/*.md | wc -l
```

---

## Page Format

Every wiki page uses this frontmatter:

```yaml
---
title: "Page Title"
type: source | entity | concept | synthesis | character | chapter | location | conflict | theme | timeline-event | rule | arc | dramatica | reader-state | foreshadowing
tags: []
sources: []
last_updated: YYYY-MM-DD
---
```

Use `[[PageName]]` wikilinks to link to other wiki pages.

---

## Ingest Workflow

Triggered by: *"ingest <file>"*

Steps (orchestrated by `.claude/skills/wiki-ingest-workflow/SKILL.md`):
1. **Route**: Execute `ingest_router.py` to route to L0 (immutable fact node) and L1 (episode node).
2. **Chunk**: Run `python3 tools/chunk.py memory/L0_facts/<file>` to chunk the file semantically.
3. **Compile & Decompose**: For each chunk, run `compile_context.py` to build the prompt, then call `wiki-decompose` to generate a comprehensive plan.
4. **Layer Passes**: Call `wiki-ingest-knowledge`, `wiki-ingest-narrative`, and `wiki-ingest-reader` iteratively for each chunk based on the generated plan.
5. **Merge Check**: Use `index_manager.py` to check for duplicates and prevent schema conflicts.
6. **Validation Loop**: Each pass validates its output using `validate.py` and retries on failure (up to 3x).
7. **Cleanup**: Rebuild index, append to `log.md`, and clean up temporary chunks. NEVER move or delete from `raw/`.

### Source Page Format

```markdown
---
title: "Source Title"
type: source
tags: []
date: YYYY-MM-DD
source_file: raw/...
---

## Summary
2–4 sentence summary.

## Key Claims
- Claim 1

## Key Quotes
> "Quote here"

## Connections
- [[EntityName]] — how they relate

## Contradictions
- Contradicts [[OtherPage]] on: ...
```

---

## Query Workflow

Triggered by: *"query: <question>"*

1. Read `wiki/index.md` — identify relevant pages
2. Read those pages
3. Synthesize answer with `[[PageName]]` citations
4. Offer to save as `wiki/syntheses/<slug>.md`

---

## Lint Workflow

Triggered by: *"lint"*

Check for: orphan pages, broken links, contradictions, stale content, missing entity pages, data gaps.

---

## Graph Workflow

Triggered by: *"build graph"*

Try `python tools/build_graph.py --open` first. If unavailable, build graph.json and graph.html manually from wikilinks.

---

## Naming Conventions

- Source slugs: `kebab-case`
- Entity/Concept pages: `TitleCase.md`

## Log Format

`## [YYYY-MM-DD] <operation> | <title>`

## Developer Enhancements
See `docs/jules/dev-process.md` for future proposals on splitting Wiki Operations from System Development to improve token efficiency.
## Developer Enhancements
See `docs/jules/dev-process.md` for future proposals on splitting Wiki Operations from System Development to improve token efficiency.
