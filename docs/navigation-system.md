# Navigation & Dependency System

## Overview

Every wiki page declares its relationships to other pages via two frontmatter fields: `requires:` (what to load for context) and `informs:` (what to update after changes). Combined with temporal filtering via `valid_from/valid_until`, this system tells agents exactly which pages to load for any given task — minimizing context window usage while ensuring completeness.

---

## Core Dependency Fields

### `requires: []`

Pages to load **before** working on this page. These provide the context an agent needs to read, write, or revise the target page correctly.

```yaml
requires:
  - characters/Kael
  - characters/Nyx
  - locations/LogosPrime
  - rules/CoherenceTheoryOfTruth
```

**Usage:** When an agent opens a page for editing, it loads all pages in `requires:` to understand the context. The slugs are relative to `wiki/` — e.g., `characters/Kael` resolves to `wiki/characters/Kael.md`.

### `informs: []`

Pages to **update** after modifying this page. These are downstream dependents whose content may need revision.

```yaml
informs:
  - chapters/chapter-03
  - arcs/kael-integration-arc
  - reader-model/chapter-01-state
```

**Usage:** After editing a page, the agent checks each `informs:` target. If the edit changes facts that the target page relies on, the agent marks the target as stale or updates it directly.

---

## Traversal Rules

### Depth Limit: Max-Depth = 2

When loading a page's `requires:` chain:

1. **Depth 0:** The target page itself
2. **Depth 1:** Pages listed in the target's `requires:`
3. **Depth 2:** Pages listed in *those* pages' `requires:`
4. **STOP.** No further traversal.

If a workflow needs deeper context, it must explicitly list pages in the workflow spec — no recursive crawling beyond depth 2.

### Deduplication

If the same page appears at multiple depths, load it once. Track loaded pages to avoid cycles.

### Load Order

1. Target page (read frontmatter first to discover dependencies)
2. Depth-1 requires (in frontmatter order)
3. Depth-2 requires (in frontmatter order)
4. Apply temporal filter (see below)
5. Apply context ceiling (see below)

---

## Temporal Filtering

When a workflow has a **chapter target** (e.g., "write chapter 5"), the agent must filter loaded pages by temporal validity.

### Resolution Protocol

1. Determine the target chapter's timeline position by reading its `timeline_start` field (a timeline-event slug)
2. Resolve that timeline-event's `sequence_number`
3. For each page loaded via `requires:`:
   - If `valid_from` is empty AND `valid_until` is empty → **always load** (timeless)
   - If `valid_from` is set → resolve its sequence_number; skip page if target chapter is before this event
   - If `valid_until` is set → resolve its sequence_number; skip page if target chapter is after this event
   - If both are set → load only if target chapter falls within the window
4. If a page is skipped due to temporal filtering, check for **sibling pages** (same base name, different temporal window) and load the correct one

### Building the Temporal Index

To resolve temporal positions efficiently:
1. Grep `wiki/timeline/` for pages with `is_boundary: true`
2. Sort by `sequence_number`
3. This gives the ordered list of boundary events that `valid_from/valid_until` reference

### Temporal Filter in Workflows

Every workflow that operates in chapter context includes:
```
temporal_filter: resolve from chapter target
```
This is a reminder to the agent to apply the temporal filtering protocol above.

---

## Context Ceilings

Each workflow has a **hard page-count ceiling** — the maximum number of wiki pages loaded into context. If the `requires:` chain (after temporal filtering) exceeds this ceiling, pages are dropped according to the **priority-drop order**.

### Ceiling Table

| Workflow | Ceiling | Priority Drop (shed first → last) |
|----------|---------|-----------------------------------|
| chapter-writing | 20 | themes → older conflicts → locations not in current scene |
| character-dev | 10 | chapter summaries → distant arc stages |
| revision | 30 | themes → dramatica → distant timeline events |
| lectoring | 15 | arcs → dramatica → non-POV characters |
| world-building | 10 | timeline events → arcs → distant locations |
| conflict-resolution | 15 | dramatica → distant timeline events |
| reader-model | 10 | reinforced foreshadowing → distant reader-states |
| brainstorming | 15 | oldest sources → distant entities |

### Drop Protocol

1. Count pages after temporal filtering
2. If count > ceiling, start dropping from the first category in the priority-drop list
3. Within a category, drop the page with the fewest connections to the target page
4. Continue until count <= ceiling
5. Log dropped pages in the agent's working notes so the user can request them if needed

---

## Staleness Detection

After modifying a page, check its `informs:` targets:

1. Read the target page's `last_updated` date
2. If the target's `last_updated` is older than the modified page's `last_updated`, the target is **stale**
3. Stale targets should either be updated immediately or flagged in `wiki/meta/contradiction-log.md`

### Quick Staleness Grep

At session start (per meta/README.md protocol), agents can run a quick check:
1. Grep all `informs:` fields across the wiki
2. For each target, compare `last_updated` dates
3. Flag any target that is older than its informing page

---

## Workflow Context-Loading Specifications

### chapter-writing
- **Always load:** `wiki/index.md`, target chapter page
- **From frontmatter:** `requires:` chain (depth 2), `constraint_refs` rule pages, previous chapter's `reader-state`
- **Temporal filter:** resolve from chapter target
- **Ceiling:** 20

### character-dev
- **Always load:** `wiki/index.md`, target character page
- **From frontmatter:** `arc` page, `relationships` targets, chapter appearances (frontmatter only, not full pages)
- **Temporal filter:** if chapter context given, apply; otherwise load all temporal versions
- **Ceiling:** 10

### revision
- **Always load:** `wiki/index.md`, all chapter pages in target range
- **From frontmatter:** timeline events in range, all rule pages, character arcs spanning range
- **Temporal filter:** apply per-chapter within range
- **Ceiling:** 30

### lectoring
- **Always load:** `wiki/index.md`, target chapter page, target chapter's reader-state
- **From frontmatter:** rule pages with `rule_class: narrative`, POV character's voice traits
- **Temporal filter:** resolve from chapter target
- **Ceiling:** 15

### world-building
- **Always load:** `wiki/index.md`, target location or rule page
- **From frontmatter:** connected characters, timeline context, other rules in same domain
- **Temporal filter:** if chapter context given, apply
- **Ceiling:** 10

### conflict-resolution
- **Always load:** `wiki/index.md`, target conflict page
- **From frontmatter:** `parties` character pages, timeline events in `chapter_range`, theme connections
- **Temporal filter:** resolve from conflict's chapter_range midpoint
- **Ceiling:** 15

### reader-model
- **Always load:** `wiki/index.md`, target reader-state page, corresponding chapter page
- **From frontmatter:** foreshadowing strands referenced, previous reader-state, dramatic irony refs
- **Temporal filter:** resolve from chapter target
- **Ceiling:** 10

### brainstorming
- **Always load:** `wiki/index.md`, `wiki/overview.md`
- **From frontmatter:** concept/theme pages matching topic, source pages, entity pages
- **Temporal filter:** none (brainstorming is atemporal)
- **Ceiling:** 15
