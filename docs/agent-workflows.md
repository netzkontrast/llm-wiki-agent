# Agent Workflows — Novel-Specific

## Overview

Twelve novel-specific workflows extend the base wiki workflows (ingest, query, lint, graph). Eight core workflows plus four writing-pipeline workflows. Each defines explicit trigger patterns, context-loading rules, output specifications, and validation steps.

> **Writing pipeline workflows** (outline-writing, beat-detailing, manuscript-drafting, manuscript-revision) are fully specified in `docs/writing-pipeline.md`. The chapter-writing workflow below serves as an orchestrator that delegates to these sub-workflows.

All workflows follow the navigation system defined in `docs/navigation-system.md` — including depth limits, temporal filtering, and context ceilings.

---

## Workflow: chapter-writing (Orchestrator)

**Triggers:** "write chapter N", "draft chapter N", "continue chapter N", "work on chapter N"

This workflow now serves as an **orchestrator** that delegates to the writing pipeline sub-workflows based on current state:

1. If chapter has no outline → trigger `outline-writing` (see `docs/writing-pipeline.md`)
2. If outline exists but beats aren't detailed → trigger `beat-detailing`
3. If beats are detailed but no manuscript → trigger `manuscript-drafting`
4. If manuscript exists → trigger `manuscript-revision`

**Temporal filter:** resolve from chapter target

**Context load:**
1. Read target chapter page (`wiki/chapters/chapter-NN.md`)
2. Read outline page via `outline_ref` to determine pipeline state
3. Read manuscript page via `manuscript_ref` to determine prose state
4. Follow `requires:` chain (depth 2) — typically characters, locations, conflicts
5. Load `constraint_refs` rule pages (narrative mandates governing this chapter)
6. Load previous chapter's reader-state (`wiki/reader-model/chapter-(N-1)-state.md`)
7. Apply temporal filter: skip pages outside the chapter's temporal window
8. Apply ceiling (20 pages)

**Output:**
- Delegates to appropriate sub-workflow; see `docs/writing-pipeline.md` for specific outputs
- Updated or created reader-state page (`wiki/reader-model/chapter-NN-state.md`)
- Mark `informs:` targets as stale if chapter content changed materially

**Validation:**
- `constraint_refs` compliance: verify chapter content respects all referenced rule pages
- `max_new_concepts` not exceeded: count new concepts introduced vs. cap
- `terminology_permitted` respected: check no term is used that hasn't been introduced in a prior reader-state
- Run contradiction check per `todo/meta/README.md` validation rules

---

## Workflow: character-dev

**Triggers:** "develop character X", "character profile for X", "update character X", "who is X"

**Temporal filter:** if chapter context given, apply; otherwise load all temporal versions

**Context load:**
1. Read target character page (`wiki/characters/Name.md`)
2. Load `arc` page for the character's transformation tracking
3. Load `relationships` targets (other character pages, depth 1 only)
4. Load chapter pages where character appears (frontmatter only — read `characters:` field to verify, don't load full chapter content)
5. Apply ceiling (10 pages)

**Output:**
- Updated character page (profile, psychology, voice, relationships)
- Updated arc page if transformation stage changed
- Updated relationship targets if relationship dynamics changed

**Validation:**
- Character must be listed in `characters:` field of every chapter in `chapter_appearances`
- If alter: verify `system` field points to valid host character
- Check for contradictions with existing character descriptions in source pages

---

## Workflow: revision

**Triggers:** "revise chapter N", "revise chapters N-M", "consistency check", "continuity review", "revision pass"

**Temporal filter:** apply per-chapter within range

**Context load:**
1. Read all chapter pages in target range
2. Load all timeline events with `chapter_ref` in range
3. Load all rule pages (all classes: world, narrative, structural)
4. Load character arc pages for characters appearing in range
5. Load foreshadowing strands with `planted_chapter` or `intermediate_refs` in range
6. Apply ceiling (30 pages)

**Output:**
- Revision notes (specific issues found, with page references)
- Updated chapter pages (fixes applied)
- Updated timeline events if ordering issues found
- Updated foreshadowing statuses if strands resolved in range

**Validation:**
- Timeline consistency: events in range must be causally coherent
- Character arc continuity: no arc stage is skipped
- Physics/rule compliance: no chapter violates world or structural rules
- Foreshadowing status: planted strands within range must have intermediate_refs or resolution
- Reader-state consistency: `terminology_permitted` is monotonically increasing

---

## Workflow: lectoring

**Triggers:** "lector chapter N", "editorial review of chapter N", "style check chapter N", "proofread chapter N"

**Temporal filter:** resolve from chapter target

**Context load:**
1. Read target chapter page (full content if draft exists)
2. Load reader-state for this chapter
3. Load rule pages with `rule_class: narrative` (style, pacing, concept-load rules)
4. Load POV character page — specifically the `Voice` section and `traits.voice_profile`
5. Load theme pages referenced in chapter's `themes:` field (for thematic consistency)
6. Apply ceiling (15 pages)

**Output:**
- Editorial notes (style issues, voice inconsistencies, pacing problems)
- Suggested revisions (specific, with reasoning tied to rules or character voice)
- Updated chapter page if fixes are straightforward

**Validation:**
- Voice consistency: prose matches POV character's documented voice profile
- Pacing compliance: tension_level trajectory matches `pacing` field
- Reader-load: `max_new_concepts` respected
- Terminology: no jargon used before `terminology_permitted` includes it
- Style register: prose matches chapter's `style_register` field

---

## Workflow: world-building

**Triggers:** "build world element X", "develop location X", "define rule X", "world-building for X", "how does X work in this world"

**Temporal filter:** if chapter context given, apply; otherwise none

**Context load:**
1. Read target location or rule page
2. Load connected characters (from location's `Connected Characters` section or rule's `chapter_relevance`)
3. Load timeline events providing historical context
4. Load other rule pages in same `domain` (for consistency)
5. Load other locations in same `world` (for coherence)
6. Apply ceiling (10 pages)

**Output:**
- Updated or created location/rule page
- Flagged inconsistencies with existing world rules
- Updated `informs:` targets if changes affect chapters

**Validation:**
- New rules must not contradict existing rules in same domain
- Locations must be internally consistent with their `world` grouping
- Changes must be logged if they affect existing chapter content

---

## Workflow: conflict-resolution

**Triggers:** "resolve conflict X", "analyze conflict X", "conflict status for X", "how does X resolve", "develop conflict X"

**Temporal filter:** resolve from conflict's `chapter_range` midpoint

**Context load:**
1. Read target conflict page
2. Load `parties` character pages
3. Load timeline events within `chapter_range`
4. Load theme pages from `related themes` or `Thematic Connection` section
5. Load dramatica elements if conflict maps to a throughline
6. Apply ceiling (15 pages)

**Output:**
- Updated conflict page (escalation trajectory, resolution path)
- Updated `resolution_status` if status changed
- If resolved: set `resolution_chapter`, update chapter pages in `informs:`

**Validation:**
- Resolution must be consistent with character arcs (no character acts out of established pattern without justification)
- If `self_referential: true`, resolution must address the paradox mechanism
- Thematic implications of resolution must align with theme pages

---

## Workflow: reader-model

**Triggers:** "reader state for chapter N", "what does the reader know at chapter N", "update reader model", "progressive disclosure check", "foreshadowing status"

**Temporal filter:** resolve from chapter target

**Context load:**
1. Read target reader-state page (or create if doesn't exist)
2. Read corresponding chapter page
3. Load previous chapter's reader-state (for `terminology_permitted` inheritance)
4. Load foreshadowing strands referenced in `foreshadowing_planted` and `foreshadowing_resolved`
5. Load dramatic irony references
6. Apply ceiling (10 pages)

**Output:**
- Updated or created reader-state page
- Updated foreshadowing strand statuses
- Flagged disclosure issues (concepts used before introduction, foreshadowing gaps)

**Validation:**
- `terminology_permitted` must be superset of previous chapter's list (one-way ratchet)
- `knows` list must be superset of previous chapter's `knows` + `learns`
- Every foreshadowing strand with `status: planted` that appears in `foreshadowing_resolved` must be updated to `status: resolved`
- `constraints_active` must reference valid, existing rule pages

---

## Workflow: brainstorming

**Triggers:** "brainstorm about X", "explore idea X", "what if X", "research X for the novel", "how could X work"

**Temporal filter:** none (brainstorming is atemporal)

**Context load:**
1. Read `wiki/overview.md` for global context
2. Load concept/theme pages matching the brainstorming topic
3. Load source pages relevant to the topic
4. Load entity pages if topic involves real-world references
5. Apply ceiling (15 pages)

**Output:**
- Synthesis of relevant wiki knowledge applied to the brainstorming question
- Optionally: new concept, theme, or synthesis page if the brainstorming produces a reusable insight
- Ask user if output should be filed as `wiki/syntheses/<slug>.md`

**Validation:**
- New ideas must not contradict existing rule pages (flag if they do)
- Cross-reference with existing concept pages to avoid duplication
- If brainstorming suggests a world-rule change, flag it for explicit confirmation

---

## Extended Ingest Workflow

The existing ingest workflow (9 steps in CLAUDE.md) is extended with additional steps for novel-specific page types. After the original 9 steps:

10. Create/update **character pages** for fictional characters mentioned in the source
11. Create/update **location pages** for settings described
12. Create/update **conflict pages** for conflicts identified
13. Create/update **theme pages** for thematic elements discussed
14. Create/update **rule pages** if the source defines world rules or narrative mandates
15. Link source page to relevant **chapter pages** if chapter-specific content
16. Update **timeline events** if the source establishes chronological facts
17. Create/update **foreshadowing pages** if the source discusses foreshadowing strands

The original 4 page types (source, entity, concept, synthesis) are still created as before. The new types are created *in addition*, not instead.
