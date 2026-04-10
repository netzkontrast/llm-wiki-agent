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

---

## Directory Layout

```
raw/          # Immutable source documents — waiting for ingestion
processed/    # Source documents that have been ingested — moved from raw/
wiki/         # Agent owns this layer entirely
  index.md    # Catalog of all pages — update on every ingest
  log.md      # Append-only chronological record
  overview.md # Living synthesis across all sources
  knowledge/  # Routing layer: characters, locations, rules, concepts, entities, timeline, sources
  narrative/  # Routing layer: chapters, outlines, beats, manuscripts, conflicts, arcs, themes, dramatica
  reader_state/ # Routing layer: reader-model, foreshadowing
  meta/       # Routing layer: logs, contradiction-log, protocols, index
  sources/    # One summary page per source document
  entities/   # People, companies, projects, products
  concepts/   # Ideas, frameworks, methods, theories
  syntheses/  # Saved query answers
graph/        # Auto-generated graph data
tools/        # Optional standalone Python scripts
```

---

## Ingestion Queue

The ingestion queue is managed by file location, not by checklist:

- `raw/` — files waiting to be ingested (queue)
- `processed/` — files that have been successfully ingested (done)

**After every successful ingest**, move the source file:
```bash
mv raw/<filename> processed/<filename>
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
type: source | entity | concept | synthesis
tags: []
sources: []
last_updated: YYYY-MM-DD
---
```

Use `[[PageName]]` wikilinks to link to other wiki pages.

---

## Ingest Workflow

Triggered by: *"ingest <file>"*

1. Read the source document fully
2. Read `wiki/index.md` and `wiki/overview.md` for current wiki context
3. Write `wiki/sources/<slug>.md` (source page format below)
4. Update `wiki/index.md` — add entry under Sources
5. Update `wiki/overview.md` — revise synthesis if warranted
6. Update/create entity and concept pages
7. Flag contradictions with existing wiki content
8. Append to `wiki/log.md`: `## [YYYY-MM-DD] ingest | <Title>`
9. Move the source file from `raw/` to `processed/`: `mv raw/<filename> processed/<filename>`

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
