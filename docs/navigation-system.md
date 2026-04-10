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

Reading and writing have **different traversal limits**. Loading context is bounded to protect the context window. Propagating changes is unbounded to guarantee wiki integrity.

### `requires:` — Bounded (Max-Depth = 2)

When loading a page's `requires:` chain for **reading context**:

1. **Depth 0:** The target page itself
2. **Depth 1:** Pages listed in the target's `requires:`
3. **Depth 2:** Pages listed in *those* pages' `requires:`
4. **STOP.** No further traversal.

If a workflow needs deeper context, it must explicitly list pages in the workflow spec — no recursive crawling beyond depth 2.

### `informs:` — Unbounded (Full Propagation)

When a page is **modified**, the agent MUST follow the full `informs:` chain until no more targets remain. This is non-negotiable — bounded propagation would leave stale content and undetected contradictions in the wiki.

**Protocol:**
1. After modifying page A, read A's `informs:` list
2. For each target page B: check if A's changes affect B's content
3. If yes: update B, then recursively follow B's `informs:` list (repeat from step 1 with B as the modified page)
4. If no: mark B as "checked, no update needed" — do NOT follow B's `informs:` further (changes don't propagate through unchanged pages)
5. Continue until all reachable targets are checked or updated

**Cycle protection:** Track all visited pages in a set. If a page appears again during traversal, skip it. Log the cycle in `wiki/meta/contradiction-log.md` — circular `informs:` chains may indicate a structural issue that needs human review.

**Context window management:** Unbounded propagation can touch many pages. To stay within context limits:
- Read only the frontmatter + relevant section of each `informs:` target (not the full page) when checking for staleness
- Batch updates: collect all needed changes, then apply them in sequence
- If the propagation chain exceeds 20 pages in a single edit, pause and report to the user before continuing

### Deduplication

If the same page appears at multiple depths (in either direction), process it once. Track visited pages in a set to avoid cycles.

### Load Order (requires: — reading)

1. Target page (read frontmatter first to discover dependencies)
2. Depth-1 requires (in frontmatter order)
3. Depth-2 requires (in frontmatter order)
4. Apply temporal filter (see below)
5. Apply context ceiling (see below)

### Propagation Order (informs: — writing)

1. Modify the target page
2. Follow `informs:` breadth-first (all direct targets first, then their targets)
3. For each target: check relevance → update if needed → recurse if updated
4. Log all updates to `wiki/log.md`

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

Staleness detection serves two roles: **real-time** (during edits) and **session-start** (catching drift from prior sessions).

### Real-Time: Unbounded Propagation

When a page is modified, the agent follows the full `informs:` chain (see "Traversal Rules → `informs:` — Unbounded" above). Every target in the chain is either updated or confirmed current. This means **no stale content is left behind** after any edit — the wiki is always consistent after every operation.

### Session-Start: Quick Staleness Audit

Between sessions, external edits or incomplete prior sessions may leave stale pages. At session start (per `todo/meta/README.md` protocol), run a quick audit:

1. Grep all `informs:` fields across the wiki
2. For each informing→target pair, compare `last_updated` dates
3. If a target's `last_updated` is older than its informing page's `last_updated`, the target is **stale**
4. Follow the `informs:` chain from each stale target to find **transitive staleness** — if A→B→C and B is stale, C may also be stale
5. Report all stale pages, then either update them or flag them in `wiki/meta/contradiction-log.md`

The session-start audit is bounded by practical time constraints — if more than 20 stale pages are found, report the list to the user and prioritize updates for pages in the active workflow.

---

## Workflow Context-Loading Specifications

> **Reading** uses `requires:` (bounded, depth 2, subject to ceiling).
> **Writing** uses `informs:` (unbounded, full propagation, no ceiling).
> Every workflow below specifies context-loading for reads. After any modification, the agent MUST follow the full `informs:` chain regardless of workflow.

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

### outline-writing
- **Always load:** `wiki/index.md`, target chapter page, target outline page
- **From frontmatter:** characters, conflicts, themes from chapter; arc pages; previous chapter's outline
- **Temporal filter:** resolve from chapter target
- **Ceiling:** 15

### beat-detailing
- **Always load:** `wiki/index.md`, outline page, target beat page(s)
- **From frontmatter:** characters present, location, active conflicts, foreshadowing strands
- **Temporal filter:** resolve from chapter target
- **Ceiling:** 15

### manuscript-drafting
- **Always load:** `wiki/index.md`, outline page, all beat pages, manuscript page
- **From frontmatter:** POV character voice profile, narrative rules from `constraint_refs`, previous reader-state
- **Temporal filter:** resolve from chapter target
- **Ceiling:** 20

### manuscript-revision
- **Always load:** `wiki/index.md`, manuscript page, outline page, beat pages
- **From frontmatter:** character voice, narrative rules, editorial notes
- **Temporal filter:** resolve from chapter target
- **Ceiling:** 20
