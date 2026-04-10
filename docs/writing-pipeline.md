# Writing Pipeline — Beats, Outlines, Manuscripts

## Overview

The writing pipeline separates three concerns that were previously conflated in the `chapter` page type:

1. **Chapter spec** (`wiki/chapters/`) — metadata hub: POV, timeline, characters, constraints
2. **Outline** (`wiki/outlines/`) — structural plan: ordered sequence of beats
3. **Beats** (`wiki/beats/`) — atomic story units: individual scene moments with metadata
4. **Manuscript** (`wiki/manuscripts/`) — actual written prose

The pipeline flows:

```
Chapter (spec) → Outline (structure) → Beats (atomic scenes) → Manuscript (prose)
```

Each stage has its own status, `requires:`/`informs:` chains, and workflow. Changes propagate via unbounded `informs:` traversal.

---

## Page Type: `beat`

**Directory:** `wiki/beats/`
**Naming:** `chapter-NN-beat-NN.md` (e.g., `chapter-01-beat-01.md`, `chapter-05-beat-03.md`)

A beat is the smallest narrative unit — a single scene moment where something shifts. Making beats standalone pages enables:
- Querying "which beats feature conflict X?" or "where does foreshadowing strand Y get planted?"
- Beat-level tension tracking (builds a micro-curve within each chapter)
- Beat-to-character mapping (who is present/active in each scene moment)

```yaml
---
title: "Chapter N, Beat M: Brief Name"
type: beat
chapter_ref: 1                # chapter number this beat belongs to
beat_number: 1                # sequence within chapter
characters_present: []        # character slugs active in this beat
pov_character: ""             # who perceives this beat (may differ from chapter POV for polyphony)
location: ""                  # location slug
conflicts_active: []          # conflict slugs driving this beat
tension_direction: rising     # rising | falling | static | turning-point
tension_delta: 1              # integer change to tension level (-3 to +3)
foreshadowing_action: ""      # foreshadowing slug + action: "the-cage-motif:plant" | "aegis-true-nature:reinforce" | ""
purpose: ""                   # what this beat accomplishes narratively (1 sentence)
tags: []
sources: []
requires: []                  # typically: chapter spec, characters present, location
informs: []                   # typically: outline page, manuscript page, reader-state
valid_from: ""
valid_until: ""
traits: {}
last_updated: YYYY-MM-DD
---

## Action
What happens in this beat (2-4 sentences). External events, dialogue, movement.

## Internal
Character's internal experience — thoughts, somatic response, emotional state.

## Constraints
- [[RuleName]] — how it applies to this specific beat

## Notes
Open field.
```

### Recommended `traits:` Keys for Beats

| Key | Example Values | Purpose |
|-----|---------------|---------|
| `somatic_detail` | `"chest-tightening"`, `"breath-holding"` | Body-level experience |
| `time_elapsed` | `"minutes"`, `"hours"` | In-story duration of this beat |
| `dialogue_density` | `"high"`, `"none"` | How much dialogue vs. action/internal |

---

## Page Type: `outline`

**Directory:** `wiki/outlines/`
**Naming:** `chapter-NN-outline.md` (e.g., `chapter-01-outline.md`)

An outline aggregates and sequences beats for a chapter. It's the structural plan that exists between "we know what this chapter is about" and "we're writing prose."

```yaml
---
title: "Outline: Chapter N"
type: outline
chapter_ref: 1                # chapter number
outline_status: concept       # concept | sketched | detailed | locked
beat_count: 0                 # number of beats defined
beats: []                     # ordered list of beat page slugs
arc_function: ""              # what role this chapter plays in the larger arc (setup | escalation | pivot | resolution | denouement)
estimated_word_count: 0       # target prose length
tags: []
sources: []
requires: []                  # typically: chapter spec, character arcs, conflict pages
informs: []                   # typically: beat pages, manuscript page, reader-state
valid_from: ""
valid_until: ""
traits: {}
last_updated: YYYY-MM-DD
---

## Structural Intent
What this chapter must accomplish (1-3 sentences). Why it exists in the novel.

## Beat Sequence
1. [[chapter-01-beat-01]] — Brief description
2. [[chapter-01-beat-02]] — Brief description
...

## Pacing Notes
How tension should flow across the beats. Target shape of the micro-arc.

## Open Questions
Unresolved structural decisions for this chapter.

## Notes
Open field.
```

### Outline Status Lifecycle

```
concept → sketched → detailed → locked
```

- **concept** — we know what happens, no beats defined yet
- **sketched** — beats listed with brief descriptions (1 sentence each)
- **detailed** — each beat has a full standalone beat page with action, internal, constraints
- **locked** — structure frozen for manuscript drafting; changes require explicit unlock

---

## Page Type: `manuscript`

**Directory:** `wiki/manuscripts/`
**Naming:** `chapter-NN-manuscript.md` (e.g., `chapter-01-manuscript.md`)

The manuscript page holds the actual written prose — dialogue, action, description, internal monologue. This is where the novel lives.

```yaml
---
title: "Manuscript: Chapter N"
type: manuscript
chapter_ref: 1                  # chapter number
manuscript_status: not-started  # not-started | draft-1 | draft-2 | polished | final
word_count: 0                   # actual prose word count
revision_notes: ""              # brief note on current revision focus
pov_voice_ref: ""               # character slug whose voice profile governs the prose
tags: []
sources: []
requires: []                    # typically: outline, beats, character voice, narrative rules
informs: []                     # typically: reader-state, chapter spec (word count/status sync)
valid_from: ""
valid_until: ""
traits: {}
last_updated: YYYY-MM-DD
---

## Prose

[The actual chapter text — paragraphs, dialogue, action, internal monologue.]

## Revision Log
- YYYY-MM-DD: draft-1 complete. Notes: ...
- YYYY-MM-DD: draft-2 revision. Focus: voice consistency, pacing in beats 3-5.
```

### Manuscript Status Lifecycle

```
not-started → draft-1 → draft-2 → polished → final
```

- **not-started** — outline is locked, prose writing hasn't begun
- **draft-1** — first complete pass; focus on getting the story down
- **draft-2** — revision pass; focus on voice, pacing, constraint compliance
- **polished** — lectoring pass complete; prose is clean
- **final** — locked for publication; changes require explicit unlock

### Large Chapter Handling

If a chapter's prose exceeds ~3000 words and agent context becomes tight, the manuscript page can be split:
- `chapter-01-manuscript-part-a.md` (beats 1-4)
- `chapter-01-manuscript-part-b.md` (beats 5-8)

The main `chapter-01-manuscript.md` then serves as an aggregator with `requires:` pointing to parts. This is optional — most chapters should fit in a single manuscript page.

---

## Chapter Page Refinement

The existing `chapter` type gains two new reference fields and loses one:

### Replaced
```yaml
# REMOVED
draft_status: concept     # ← replaced by outline_ref + manuscript_ref
```

### Added
```yaml
# NEW — reference fields
outline_ref: ""           # outline page slug (e.g., "outlines/chapter-01-outline")
manuscript_ref: ""        # manuscript page slug (e.g., "manuscripts/chapter-01-manuscript")
```

Status is now read from the referenced pages: `outline_status` from the outline page, `manuscript_status` from the manuscript page. The chapter page itself becomes a pure spec/metadata hub.

### Removed Section
The `## Scene Beats` section is removed from the chapter template body. Beats now live in the outline page (as a sequenced list) and as standalone beat pages (with full metadata).

### Preserved
Everything else on the chapter page stays: POV, timeline, characters, locations, conflicts, themes, pacing, tension_level, style_register, constraint_refs, max_new_concepts.

---

## Dependency Chains

### `informs:` (change propagation — unbounded)

```
chapter (spec) ──informs──→ outline
outline ──informs──→ beat pages
beat pages ──informs──→ manuscript, reader-state
manuscript ──informs──→ reader-state, chapter (word_count sync)
```

### `requires:` (context loading — bounded, depth 2)

```
manuscript ──requires──→ outline, character voice profile, narrative rules
outline ──requires──→ chapter spec, character arcs, conflict pages
beat ──requires──→ chapter spec, characters present, location, active conflicts
```

---

## Workflows

### outline-writing

**Triggers:** "outline chapter N", "structure chapter N", "plan chapter N beats"

**Context load:**
1. Read chapter spec (`wiki/chapters/chapter-NN.md`)
2. Load characters, conflicts, themes from chapter frontmatter
3. Load arc pages for characters appearing in chapter
4. Load previous chapter's outline (for continuity)
5. Apply temporal filter from chapter target
6. Apply ceiling (15 pages)

**Output:**
- Created or updated outline page with beat sequence
- Updated `outline_status`
- Created stub beat pages if `outline_status` moves to `sketched`

**Validation:**
- Beat count reasonable for chapter length (3-8 beats typical)
- Tension direction across beats forms a coherent micro-arc
- All characters in beats are listed in chapter's `characters:` field

### beat-detailing

**Triggers:** "detail beats for chapter N", "expand beat M of chapter N", "beat-level work on chapter N"

**Context load:**
1. Read outline page for the chapter
2. Read target beat page(s)
3. Load characters present in each beat
4. Load location for each beat
5. Load active conflicts
6. Load foreshadowing strands referenced
7. Apply ceiling (15 pages)

**Output:**
- Updated beat pages with full action, internal, constraints sections
- Updated outline `outline_status` to `detailed` if all beats now have full pages
- Updated foreshadowing strand pages if beats plant/reinforce/resolve strands

**Validation:**
- Every beat has a `purpose` that advances plot, character, or theme
- `tension_direction` forms coherent flow with adjacent beats
- `foreshadowing_action` references valid foreshadowing pages
- Characters present are consistent with chapter's `characters:` field

### manuscript-drafting

**Triggers:** "write prose for chapter N", "draft chapter N manuscript", "write chapter N"

**Context load:**
1. Read outline page (must be `detailed` or `locked`)
2. Read all beat pages for the chapter
3. Load POV character's voice profile (`traits.voice_profile`, `## Voice` section)
4. Load narrative rule pages from chapter's `constraint_refs`
5. Load previous chapter's reader-state (for `terminology_permitted`)
6. Apply ceiling (20 pages)

**Output:**
- Created or updated manuscript page with prose
- Updated `manuscript_status` and `word_count`
- Updated reader-state page for this chapter

**Validation:**
- Outline must be `detailed` or `locked` before drafting begins
- Prose voice matches POV character's documented voice profile
- `max_new_concepts` not exceeded
- `terminology_permitted` respected — no jargon before introduction
- All beats from outline are represented in prose

### manuscript-revision

**Triggers:** "revise chapter N prose", "polish chapter N", "second draft of chapter N", "lector chapter N manuscript"

**Context load:**
1. Read manuscript page
2. Read outline and beat pages
3. Load character voice profile
4. Load narrative rules from `constraint_refs`
5. Load any editorial/lectoring notes
6. Apply ceiling (20 pages)

**Output:**
- Updated manuscript (advanced to next draft stage)
- Revision log entry with date and focus
- Updated `manuscript_status`

**Validation:**
- Voice consistency across all beats
- Pacing matches outline's structural intent
- Constraint compliance verified against rule pages
- Word count updated

---

## Integration with Existing Workflows

The existing `chapter-writing` workflow becomes an **orchestrator** that delegates to the appropriate sub-workflow based on current state:

1. If chapter has no outline → trigger `outline-writing`
2. If outline exists but beats aren't detailed → trigger `beat-detailing`
3. If beats are detailed but no manuscript → trigger `manuscript-drafting`
4. If manuscript exists → trigger `manuscript-revision`

The `lectoring` workflow now operates on manuscript pages directly, checking voice, pacing, and constraint compliance against the prose.

The `revision` workflow now spans the full pipeline — checking outline/beat/manuscript consistency across a chapter range.

---

## Context Ceilings (New Workflows)

| Workflow | Ceiling | Priority Drop (shed first → last) |
|----------|---------|-----------------------------------|
| outline-writing | 15 | distant arcs → themes → dramatica |
| beat-detailing | 15 | distant timeline events → themes → arcs |
| manuscript-drafting | 20 | themes → distant conflicts → dramatica |
| manuscript-revision | 20 | arcs → dramatica → distant timeline events |
