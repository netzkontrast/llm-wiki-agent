# Wiki Schema Extension — Page Types & Frontmatter

## Type Coexistence

The original 4 types (`source`, `entity`, `concept`, `synthesis`) remain unchanged and serve as the **generic knowledge layer**. The 11 new types extend the wiki for **novel-specific use**. A `source` page might feed into a `character` or `rule` page via `sources:`. No existing type is replaced.

---

## Standard Fields (All Page Types)

Every wiki page — old and new — carries these frontmatter fields:

```yaml
---
title: ""
type: ""                # one of the 15 types listed below
tags: []
sources: []             # source slugs that inform this page
requires: []            # pages to load FOR context when working on this page
informs: []             # pages to UPDATE after modifying this page
valid_from: ""          # timeline-event slug (empty = from the beginning)
valid_until: ""         # timeline-event slug (empty = until the end)
traits: {}              # open key-value map for domain-specific extensions
last_updated: YYYY-MM-DD
---
```

### All Valid Types

```
source | entity | concept | synthesis
character | chapter | location | conflict | theme
timeline-event | rule | arc | dramatica | reader-state | foreshadowing
```

### The `traits:` Extension Map

An open key-value structure for project-specific metadata that the generic schema cannot anticipate. Not enforced — but recommended keys per type are listed below to give agents a shared vocabulary.

| Page Type | Recommended Keys | Example Values |
|-----------|-----------------|----------------|
| character | `voice_profile`, `somatic`, `pov_mode`, `world_rule`, `response_type` | `"staccato"`, `"chest pressure"`, `"first"`, `"entropy"`, `"freeze"` |
| chapter | `somatic_layer`, `polyphony_mode` | `"breath"`, `"single-voice"` |
| location | `sensory_dominant` | `"sterile-white"` |

Any key is valid. These recommendations exist to prevent different agents from using different names for the same concept.

### Temporal Validity (`valid_from` / `valid_until`)

These fields reference `timeline-event` page slugs (not chapter numbers). They answer: "during what period of the story is this page's content true?"

**Why timeline-event slugs instead of chapter numbers:**
- Timeline events are semantic anchors ("fragmentation-revealed") — they carry meaning
- Multiple chapters can share the same boundary event
- If chapters reorder during revision, timeline events stay stable

**Patterns for temporal content:**
- **Multi-page:** `Kael.md` (valid_until: `010-fragmentation-revealed`), `Kael-post-frag.md` (valid_from: `010-fragmentation-revealed`)
- **Multi-section:** Single `Kael.md` with sections marked by timeline-event boundaries; agent reads only the section whose window contains the target chapter

Choice is per-project, not enforced. Both patterns are valid.

**Empty values:** Pages with empty `valid_from`/`valid_until` are timeless — always loaded regardless of temporal context. Most rules, themes, and locations are timeless.

---

## New Directory Layout

```
wiki/
  index.md              # Extended with new sections
  log.md                # Append-only chronological record
  overview.md           # Living synthesis
  sources/              # (existing) One summary per source document
  entities/             # (existing) People, companies, projects
  concepts/             # (existing) Ideas, frameworks, methods
  syntheses/            # (existing) Saved query answers
  characters/           # NEW — Character profiles & arcs
  chapters/             # NEW — Chapter specs, outlines, drafts
  locations/            # NEW — World-building locations
  conflicts/            # NEW — Conflict tracking
  themes/               # NEW — Thematic threads
  timeline/             # NEW — Chronological events (temporal index)
  rules/                # NEW — Hard sci-fi rules & narrative mandates
  arcs/                 # NEW — Character/plot arc tracking
  dramatica/            # NEW — Dramatica theory elements
  reader-model/         # NEW — Reader perception state per chapter
  foreshadowing/        # NEW — Foreshadowing strand tracking
  archive/              # NEW — Deprecated content (never delete, always archive)
  meta/                 # NEW — Contradiction log, wiki-level metadata
```

---

## Page Type Specifications

### 1. `character`

**Directory:** `wiki/characters/`
**Naming:** `TitleCase.md` (e.g., `Kael.md`, `AEGIS.md`, `Nyx.md`)

```yaml
---
title: "Character Name"
type: character
role: protagonist | antagonist | guardian | alter | supporting
system: ""              # if alter: which character system they belong to (e.g., "Kael")
alter_type: ""          # if alter: ANP | EP | hybrid
arc: ""                 # slug of arc page tracking this character's transformation
relationships: []       # character page slugs
chapter_appearances: [] # chapter numbers (integers)
tags: []
sources: []
requires: []
informs: []
valid_from: ""
valid_until: ""
traits: {}
last_updated: YYYY-MM-DD
---

## Profile
Brief character description — who they are, what they want.

## Psychology
Psychological framework, motivations, fears, defense mechanisms.

## Voice
How this character speaks, thinks, narrates. Syntax patterns, register, vocabulary.

## Relationships
- [[CharacterName]] — nature of relationship, evolution

## Arc Summary
Current state in their transformation. Link to [[arc-page]] for full tracking.

## Notes
Open field for domain-specific observations.
```

### 2. `chapter`

**Directory:** `wiki/chapters/`
**Naming:** `chapter-NN.md` (zero-padded two digits, e.g., `chapter-01.md`, `chapter-39.md`)

```yaml
---
title: "Chapter N: Title"
type: chapter
chapter_number: 1         # integer
part: 1                   # which part/act (integer)
pov: ""                   # character slug who narrates
pov_reliability: high     # high | medium | low | unreliable
timeline_start: ""        # timeline-event slug
timeline_end: ""          # timeline-event slug
draft_status: concept     # concept | outline | draft-1 | draft-2 | final
characters: []            # character slugs appearing in this chapter
locations: []             # location slugs
conflicts: []             # conflict slugs active in this chapter
themes: []                # theme slugs expressed
pacing: setup             # setup | rising | climax | falling | resolution
tension_level: 1          # 1-10
style_register: ""        # prose style for this chapter
constraint_refs: []       # rule page slugs that govern this chapter's writing
max_new_concepts: 1       # reader-load cap (new ideas introduced)
tags: []
sources: []
requires: []
informs: []
valid_from: ""
valid_until: ""
traits: {}
last_updated: YYYY-MM-DD
---

## Synopsis
What happens in this chapter (2-4 sentences).

## Scene Beats
1. Beat 1 — what happens, tension direction
2. Beat 2 — ...

## Reader State
- **Knows before:** what the reader knows entering this chapter
- **Learns:** what the reader discovers
- **Foreshadowing planted:** strands seeded here
- **Foreshadowing resolved:** strands paid off here

## Constraints
- Links to rule pages that apply, with brief notes on how they constrain this chapter

## Notes
Open field.
```

### 3. `location`

**Directory:** `wiki/locations/`
**Naming:** `TitleCase.md` (e.g., `LogosPrime.md`, `MnemosyneArchipelago.md`)

```yaml
---
title: "Location Name"
type: location
world: ""                  # which world/realm (e.g., "KW1-LogosPrime")
psychological_mapping: ""  # what psychological state this place externalizes
sensory_palette: []        # dominant sensory qualities
symbolic_meaning: ""       # what this place represents thematically
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
What this place looks, sounds, feels like.

## Environmental Storytelling
How the environment communicates narrative meaning without exposition.

## Connected Characters
- [[CharacterName]] — why this place matters to them

## Rules in Effect
- [[RuleName]] — how physics/logic works differently here

## Notes
Open field.
```

### 4. `conflict`

**Directory:** `wiki/conflicts/`
**Naming:** `TitleCase.md` (e.g., `KaelVsAegis.md`, `InternalFragmentation.md`)

```yaml
---
title: "Conflict Name"
type: conflict
conflict_type: external    # internal | external | thematic | structural
parties: []                # character/entity slugs involved
stakes: ""                 # what's at risk
chapter_range: []          # chapters where this conflict is active [start, end]
resolution_status: open    # open | escalating | resolving | resolved | paradox
resolution_chapter: null   # chapter number where resolved (null if open)
self_referential: false    # true if conflict generates itself (see below)
paradox_source: ""         # mechanism of self-reference (if self_referential)
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
What the conflict is about, why it matters.

## Escalation Trajectory
How the conflict develops across chapters.

## Thematic Connection
- [[ThemeName]] — how this conflict embodies or challenges the theme

## Resolution Path
Current plan/trajectory for resolution (or why it resists resolution).

## Notes
Open field.
```

**Self-referential conflicts:** A self-referential conflict is one where the source of the conflict is identical to, or generated by, the entity trying to resolve it. Set `self_referential: true` and describe the mechanism in `paradox_source`. This pattern is common in philosophical sci-fi where antagonists embody the problem they claim to solve.

### 5. `theme`

**Directory:** `wiki/themes/`
**Naming:** `TitleCase.md` (e.g., `IntegrationVsFragmentation.md`, `ParadoxAsFeature.md`)

```yaml
---
title: "Theme Name"
type: theme
chapter_appearances: []    # chapter numbers where theme is expressed
motifs: []                 # recurring symbols, images, phrases
evolution_stages: []       # how the theme transforms across the novel
counter_theme: ""          # opposing theme slug (if dialectical)
tags: []
sources: []
requires: []
informs: []
valid_from: ""
valid_until: ""
traits: {}
last_updated: YYYY-MM-DD
---

## Statement
One-sentence thematic thesis.

## Expression
How this theme manifests in plot, character, setting.

## Motifs
- Motif 1 — where it appears, what it signifies
- Motif 2 — ...

## Evolution
How the theme's meaning shifts across the novel's arc.

## Dialectic
Relationship to counter-theme, if any. How they interact.

## Notes
Open field.
```

### 6. `timeline-event`

**Directory:** `wiki/timeline/`
**Naming:** `NNN-slug.md` (three-digit sequence + kebab-case, e.g., `001-story-begins.md`, `010-fragmentation-revealed.md`)

```yaml
---
title: "Event Name"
type: timeline-event
sequence_number: 1         # integer for ordering
timepoint: ""              # in-story time reference (e.g., "Day 1, morning")
causality_links: []        # timeline-event slugs this event causes or is caused by
chapter_ref: 1             # chapter number where this event occurs
is_boundary: false         # true if used as valid_from/valid_until reference
tags: []
sources: []
requires: []
informs: []
traits: {}
last_updated: YYYY-MM-DD
---

## Description
What happens in this event.

## Consequences
What this event causes or enables.

## Notes
Open field.
```

**Boundary events** (`is_boundary: true`) serve as temporal anchors for the `valid_from`/`valid_until` system. Agents can filter timeline events by `is_boundary` to quickly build the temporal index.

### 7. `rule`

**Directory:** `wiki/rules/`
**Naming:** `TitleCase.md` (e.g., `CoherenceTheoryOfTruth.md`, `MaxOneNewConceptPerScene.md`)

```yaml
---
title: "Rule Name"
type: rule
domain: physics            # physics | logic | world | psychology
rule_class: world          # world | narrative | structural
constraints: []            # what this rule forbids or requires
exceptions: []             # known valid exceptions
chapter_relevance: []      # chapters where this rule is especially important
tags: []
sources: []
requires: []
informs: []
valid_from: ""
valid_until: ""
traits: {}
last_updated: YYYY-MM-DD
---

## Statement
Clear, testable rule statement.

## Rationale
Why this rule exists (in-world or narrative reason).

## Exceptions
When and why the rule can be bent or broken.

## Enforcement
How an agent should check compliance with this rule.

## Notes
Open field.
```

**Rule classes:**
- **world** — "gravity works like X" — constrains the *story*. Needed for world-building, consistency checking.
- **narrative** — "max 1 new concept per scene" — constrains the *writing*. Needed for chapter-writing, lectoring.
- **structural** — "Act 2 must mirror Act 1 inversely" — constrains the *architecture*. Needed for structural revision.

### 8. `arc`

**Directory:** `wiki/arcs/`
**Naming:** `kebab-case.md` (e.g., `kael-integration-arc.md`, `aegis-escalation-arc.md`)

```yaml
---
title: "Arc Name"
type: arc
arc_type: character        # character | plot | thematic
subject: ""                # character/conflict/theme slug this arc tracks
stages: []                 # list of {stage_name, chapter_ref, description}
current_stage: ""          # which stage the arc is currently at
tags: []
sources: []
requires: []
informs: []
valid_from: ""
valid_until: ""
traits: {}
last_updated: YYYY-MM-DD
---

## Overview
What transformation this arc tracks.

## Stages
1. **Stage Name** (Chapter N) — Description
2. **Stage Name** (Chapter N) — Description

## Current State
Where the arc stands now in development.

## Notes
Open field.
```

### 9. `dramatica`

**Directory:** `wiki/dramatica/`
**Naming:** `TitleCase.md` (e.g., `MainCharacterThroughline.md`, `Act2Signpost.md`)

```yaml
---
title: "Element Name"
type: dramatica
element_type: throughline   # throughline | signpost | storypoint | genre
throughline: ""             # MC | IC | RS | OS (if applicable)
act: null                   # act number (if signpost)
related_characters: []      # character slugs
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
What this Dramatica element represents.

## Mapping
How this element maps to specific chapters, characters, conflicts.

## Notes
Open field.
```

### 10. `reader-state`

**Directory:** `wiki/reader-model/`
**Naming:** `chapter-NN-state.md` (e.g., `chapter-01-state.md`)

```yaml
---
title: "Reader State — Chapter N"
type: reader-state
chapter_ref: 1                    # chapter number
knows: []                         # facts the reader knows BEFORE this chapter
learns: []                        # facts the reader discovers IN this chapter
foreshadowing_planted: []         # foreshadowing slugs seeded here
foreshadowing_resolved: []        # foreshadowing slugs paid off here
dramatic_irony_active: []         # what the reader knows that characters don't
tension_level: 1                  # 1-10
constraints_active: []            # rule page slugs applying at this story-point
terminology_permitted: []         # concepts the reader has been introduced to (CUMULATIVE)
tags: []
sources: []
requires: []
informs: []
traits: {}
last_updated: YYYY-MM-DD
---

## Reader Experience
What the reader should feel, think, wonder at this point.

## Disclosure Strategy
What is being revealed, withheld, or misdirected.

## Notes
Open field.
```

**`terminology_permitted` is a one-way ratchet.** See `docs/reader-model.md` for accumulation rules.

### 11. `foreshadowing`

**Directory:** `wiki/foreshadowing/`
**Naming:** `kebab-case.md` (e.g., `the-cage-motif.md`, `aegis-true-nature.md`)

```yaml
---
title: "Strand Name"
type: foreshadowing
strand_name: ""               # human-readable name
planted_chapter: null          # chapter number where first planted
resolved_chapter: null         # chapter number where resolved (null if unresolved)
intermediate_refs: []          # chapter numbers where reinforced
status: planted               # planted | reinforced | resolved
related_themes: []             # theme slugs
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
What is being foreshadowed and how.

## Planting
How and where the strand is first introduced.

## Reinforcement
Intermediate appearances that build the pattern.

## Resolution
How the strand pays off (or remains deliberately unresolved).

## Notes
Open field.
```

---

## Extended Index Format

```markdown
# Wiki Index

## Overview
- [Overview](overview.md) — living synthesis

## Sources
- [Title](sources/slug.md) — summary

## Entities
- [Name](entities/Name.md) — description

## Concepts
- [Name](concepts/Name.md) — description

## Syntheses
- [Title](syntheses/slug.md) — question answered

## Characters
- [Name](characters/Name.md) — role, brief

## Chapters
- [Chapter N: Title](chapters/chapter-NN.md) — draft_status, pov

## Locations
- [Name](locations/Name.md) — world, brief

## Conflicts
- [Name](conflicts/Name.md) — type, status

## Themes
- [Name](themes/Name.md) — brief statement

## Timeline
- [NNN Event](timeline/NNN-slug.md) — timepoint

## Rules
- [Name](rules/Name.md) — class, brief

## Arcs
- [Name](arcs/slug.md) — type, subject

## Dramatica
- [Name](dramatica/Name.md) — element_type

## Reader Model
- [Chapter N](reader-model/chapter-NN-state.md) — tension_level

## Foreshadowing
- [Name](foreshadowing/slug.md) — status
```

---

## Naming Conventions (Complete)

| Category | Convention | Example |
|----------|-----------|---------|
| Source slugs | `kebab-case` matching filename | `bridging-narrative-theory.md` |
| Entity pages | `TitleCase.md` | `MelanieAnnePhillips.md` |
| Concept pages | `TitleCase.md` | `DualKernelTheory.md` |
| Character pages | `TitleCase.md` | `Kael.md`, `AEGIS.md` |
| Chapter pages | `chapter-NN.md` (zero-padded) | `chapter-01.md` |
| Location pages | `TitleCase.md` | `LogosPrime.md` |
| Conflict pages | `TitleCase.md` | `KaelVsAegis.md` |
| Theme pages | `TitleCase.md` | `IntegrationVsFragmentation.md` |
| Timeline events | `NNN-slug.md` (three-digit + kebab) | `010-fragmentation-revealed.md` |
| Rule pages | `TitleCase.md` | `MaxOneNewConceptPerScene.md` |
| Arc pages | `kebab-case.md` | `kael-integration-arc.md` |
| Dramatica pages | `TitleCase.md` | `MainCharacterThroughline.md` |
| Reader-state pages | `chapter-NN-state.md` | `chapter-01-state.md` |
| Foreshadowing pages | `kebab-case.md` | `the-cage-motif.md` |
| Multi-word TitleCase | No spaces, no hyphens | `MnemosyneArchipelago.md` |
