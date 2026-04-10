# Dramatica Theory Integration

## Overview

Dramatica Theory models a story as a "Story Mind" — a single human mind working through a problem. Every complete story has four throughlines, signposts marking progression, and story points that together form a Grand Argument. This document specifies how Dramatica elements map to wiki pages.

---

## Core Dramatica Concepts

### Four Throughlines

| Throughline | Abbreviation | Perspective | Question |
|-------------|-------------|-------------|----------|
| Overall Story | OS | "They" | What's the big-picture problem everyone deals with? |
| Main Character | MC | "I" | What's the personal crisis the protagonist faces? |
| Influence Character | IC | "You" | Who challenges the MC's worldview? |
| Relationship Story | RS | "We" | How does the central relationship evolve? |

Each throughline gets a wiki page: `wiki/dramatica/OverallStoryThroughline.md`, `wiki/dramatica/MainCharacterThroughline.md`, etc.

### Signposts

Each throughline progresses through 4 signposts (one per act). A signpost marks a shift in the throughline's domain. In the wiki:

```yaml
---
title: "MC Signpost 2: Learning"
type: dramatica
element_type: signpost
throughline: MC
act: 2
related_characters: [Kael]
chapter_ref: [10, 11, 12]    # chapters where this signpost plays out
---
```

Signpost pages connect throughlines to specific chapters, making it possible for the chapter-writing workflow to know which Dramatica beat applies.

### Story Points

Story points are specific dramatic elements within signposts:
- **Problem/Solution** — what drives and resolves each throughline
- **Symptom/Response** — what appears to be the problem and the reaction to it
- **Benchmark** — how progress is measured in each throughline
- **Prerequisites/Preconditions** — what must happen before resolution

These are modeled as wiki pages when they're significant enough to track:

```yaml
---
title: "MC Problem: Test"
type: dramatica
element_type: storypoint
throughline: MC
related_characters: [Kael]
---
```

### Genre

Dramatica defines genre as a combination of four elements:
- **Domain** (Universe, Mind, Physics, Psychology) — assigned to each throughline
- **Concern** — the area within the domain that creates conflict
- **Issue** — the thematic focus
- **Problem** — the core driver

Genre choices are documented at the throughline level, not as separate pages.

---

## Mapping to the Novel Wiki

### Throughline → Character/Conflict

Each throughline maps to specific characters and conflicts:
- MC throughline → protagonist character page + internal conflicts
- IC throughline → influence character page + the challenge they pose
- RS throughline → relationship between MC and IC (tracked as a conflict page)
- OS throughline → the overarching plot conflicts

### Signpost → Chapter

Each signpost spans a range of chapters. The chapter pages reference their signpost via `requires:` or by listing the dramatica page in frontmatter:

```yaml
# In chapter-05.md
requires:
  - dramatica/MCSignpost1
```

This ensures the chapter-writing agent knows which Dramatica beat it's serving.

### Theme → Dramatica Issue

Dramatica's "Issue" level maps directly to theme pages in the wiki. A theme page can reference its Dramatica origin:

```yaml
# In wiki/themes/IntegrationVsFragmentation.md
traits:
  dramatica_issue: "Commitment vs. Responsibility"
  dramatica_throughline: MC
```

---

## Workflow Integration

### When to Load Dramatica Pages

- **chapter-writing:** Load the signpost page for the target chapter's act (if mapped)
- **conflict-resolution:** Load the throughline page if the conflict maps to a throughline
- **revision:** Load all signpost pages in the revision range to verify act structure
- **brainstorming:** Load relevant throughline if brainstorming touches story structure

Dramatica pages are in the **priority-drop** list for most workflows — they provide structural context but are lower priority than character, conflict, and reader-state pages.

### When to Create Dramatica Pages

- During ingestion of source documents that discuss narrative structure
- When explicitly working on story architecture
- During structural revision passes

Not every novel needs full Dramatica mapping. These pages are optional but powerful for structurally complex novels where throughline tracking prevents drift.

---

## Template

```yaml
---
title: "Element Name"
type: dramatica
element_type: throughline    # throughline | signpost | storypoint | genre
throughline: MC              # MC | IC | RS | OS
act: null                    # 1-4 (for signposts)
related_characters: []
chapter_ref: []              # chapters where this element plays out
tags: []
sources: []
requires: []
informs: []
valid_from: ""
valid_until: ""
traits: {}
last_updated: YYYY-MM-DD
---

## Description
What this element represents in the story.

## Mapping
Specific chapters, characters, and conflicts this element connects to.

## Notes
Open field.
```
