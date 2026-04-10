# Reader Model — Progressive Disclosure

## Overview

The reader model tracks what the reader knows, can know, and should feel at every point in the novel. It serves two purposes:

1. **Disclosure tracking** — preventing the agent from using concepts, terms, or facts the reader hasn't encountered yet
2. **Experience design** — managing tension, dramatic irony, and foreshadowing across the novel's arc

---

## Knowledge-State Tracking

Each chapter has a corresponding `reader-state` page (`wiki/reader-model/chapter-NN-state.md`) that captures the reader's cumulative knowledge.

### Core Fields

- **`knows`** — facts the reader knows BEFORE reading this chapter
- **`learns`** — facts the reader discovers DURING this chapter
- **`terminology_permitted`** — concepts/terms the reader has been introduced to (cumulative)
- **`constraints_active`** — rule pages that apply at this story-point
- **`dramatic_irony_active`** — what the reader knows that characters don't
- **`tension_level`** — 1-10 scale of narrative tension

### The One-Way Ratchet

`terminology_permitted` is a **one-way ratchet**: each reader-state inherits the previous chapter's list and may ADD but never SUBTRACT.

**Agent instruction:** When creating or updating a reader-state page:
1. Read the previous chapter's reader-state (`chapter-(N-1)-state.md`)
2. Copy its `terminology_permitted` list entirely
3. Append any new terms introduced in the current chapter
4. NEVER remove a term from the inherited list

This prevents accidental regressions where chapter 12's reader-state drops a term that chapter 8 introduced.

### Knowledge Accumulation

Similar to `terminology_permitted`, the `knows` field accumulates:
- `chapter-N.knows` = `chapter-(N-1).knows` + `chapter-(N-1).learns`
- Each chapter's `knows` is the union of all prior `learns` plus its own starting knowledge

This means an agent can determine the complete reader knowledge state at any chapter by reading only that chapter's reader-state page — no need to traverse all prior chapters.

---

## Foreshadowing Management

Foreshadowing strands are tracked as standalone wiki pages (`wiki/foreshadowing/`) rather than buried in reader-state pages. This is because a single strand can span the entire novel.

### Strand Lifecycle

```
planted → reinforced → resolved
```

- **planted** — first appearance; reader may not consciously notice
- **reinforced** — subsequent appearances that strengthen the pattern
- **resolved** — the strand pays off; reader recognizes the pattern

### Strand Fields

- `planted_chapter` — where first introduced
- `intermediate_refs` — chapters where reinforced
- `resolved_chapter` — where paid off (null if still open)
- `status` — current lifecycle stage
- `related_themes` — thematic connections

### Foreshadowing in Reader-State

Each reader-state page references foreshadowing via:
- `foreshadowing_planted` — strands first appearing in this chapter
- `foreshadowing_resolved` — strands paying off in this chapter

When a strand appears in `foreshadowing_resolved`, the agent must also update the strand's own page: set `resolved_chapter` and change `status` to `resolved`.

### Foreshadowing Validation

- Every strand with `status: planted` should eventually have a `resolved_chapter` (flag if missing after the final chapter)
- `intermediate_refs` should show at least one reinforcement between planting and resolution for long-distance foreshadowing
- Strands should connect to at least one theme page (orphan foreshadowing lacks thematic grounding)

---

## Tension Curves

`tension_level` (1-10) in each reader-state page creates a tension curve across the novel when read in sequence.

### Pacing Alignment

The chapter's `pacing` field (setup|rising|climax|falling|resolution) should align with tension_level changes:
- `setup` → tension_level stable or slightly rising
- `rising` → tension_level increasing
- `climax` → tension_level at local maximum
- `falling` → tension_level decreasing
- `resolution` → tension_level at local minimum

### Structural Tension Patterns

For a three-part novel:
- Part 1: tension builds from ~2 to ~6, with small oscillations
- Part 2: tension builds from ~5 to ~9, with deeper oscillations
- Part 3: tension peaks at 10 (climax), drops sharply (resolution), may have final spike (twist)

These are guidelines, not rules. The agent should flag deviations for review but not enforce them.

---

## Concept-Load Management

The `max_new_concepts` field in chapter pages sets a cap on how many new ideas a chapter introduces. This prevents reader overload.

### How to Count

A "new concept" is any term or idea that would be added to `terminology_permitted` for the first time. If the concept already appears in a prior chapter's `terminology_permitted`, it's not new.

### Recommended Caps

- Normal chapter: 1-2 new concepts
- Exposition-heavy chapter: 2-3 new concepts (flag for review if exceeding)
- Action/climax chapter: 0-1 new concepts (reader bandwidth is spent on plot tension)

### Terminology Gates

Some concepts serve as prerequisites for others. For example, "Dual Kernel Theory" requires understanding "Coherence Theory" first. This can be modeled via `requires:` on concept pages:

```yaml
# wiki/concepts/DualKernelTheory.md
requires:
  - concepts/CoherenceTheory
  - concepts/CorrespondenceTheory
```

The agent should check: if `DualKernelTheory` is being introduced in chapter N, verify that `CoherenceTheory` and `CorrespondenceTheory` are already in `terminology_permitted` as of chapter N-1.

---

## Dramatic Irony

`dramatic_irony_active` tracks gaps between reader knowledge and character knowledge. Each entry should specify:
- What the reader knows
- Which character(s) don't know it
- When it was established
- When it resolves (or if it's ongoing)

Dramatic irony creates tension — the reader watches characters make decisions based on incomplete information. The agent should track these gaps to ensure they're resolved (or deliberately maintained) rather than forgotten.

---

## Constraints Active

`constraints_active` in reader-state pages references rule pages (from `wiki/rules/`) that apply at this story-point. This includes:
- Narrative mandates (e.g., "no jargon in Part 1")
- Style rules (e.g., "somatic layer = breath until Act 2")
- Structural rules (e.g., "mirror structure between chapters 1 and 39")

By listing active constraints in the reader-state, the agent writing any chapter can immediately see which rules are in effect without scanning all rule pages.
