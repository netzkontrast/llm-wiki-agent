---
title: "MaxOneNewConceptPerScene"
type: rule
domain: psychology
rule_class: narrative
constraints:
  - "Each scene may introduce at most one concept the reader has not encountered before"
  - "Existing concepts may be developed, complicated, or recontextualised freely"
  - "A 'new concept' is any entity, system, rule, or framework requiring reader cognitive load to register"
  - "Character names count as new concepts when first introduced"
exceptions:
  - "Chapter climaxes (pacing: climax) may introduce a second concept if the collision of the two is the point of the scene"
  - "Concepts introduced via environmental storytelling (reader infers rather than is told) count at 0.5"
chapter_relevance: [1]
tags: []
sources: []
requires: []
informs: []
valid_from: ""
valid_until: ""
traits: {}
last_updated: 2026-04-11
---

## Statement
No scene may introduce more than one concept that is new to the reader. Cognitive overload breaks immersion and causes the reader to disengage from the philosophical content — which is the primary content of this work.

## Rationale
This novel operates at the intersection of psychological realism and philosophical sci-fi. Both demands require the reader to track complex internal states while following an unconventional narrative structure. Each new concept requires working memory. Exceed the cap and the reader stops feeling and starts cataloguing.

## Exceptions
The exception for climax scenes acknowledges that the collision of two concepts — when that collision is the scene's point — can be handled as a single compound concept. The narrative beat is the concept, not its components individually.

## Enforcement
When writing or reviewing chapter content:
1. List all concepts introduced in the scene
2. Count each named entity, system, rule, and framework the reader encounters for the first time
3. If count > 1 (or > 1.5 with environmental introductions), flag the scene for revision
4. Check `wiki/reader-model/chapter-NN-state.md` for the `terminology_permitted` ratchet — new concepts must appear in the reader-state page for the chapter where they are introduced

## Notes
This rule applies to the writing process, not the story world. It governs how information is disclosed to the reader, not how the world itself works. Violations are narrative errors, not world-building contradictions.
