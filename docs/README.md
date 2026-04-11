# Docs — Reference Specifications

Detailed design documents for the novel-author wiki extension. These are **reference specs**, not implementation instructions. Load them only when a `todo/` task explicitly references them.

## Documents

| File | Covers |
|------|--------|
| [wiki-schema.md](wiki-schema.md) | 11 new page types, frontmatter schemas, `traits:` extension mechanism, temporal validity fields, naming conventions, directory layout |
| [navigation-system.md](navigation-system.md) | `requires:`/`informs:` dependency system, traversal depth limits, context ceilings, priority-drop rules, temporal filtering |
| [agent-workflows.md](agent-workflows.md) | 8 novel-specific workflows with trigger patterns, context loads, output specs, validation steps |
| [reader-model.md](reader-model.md) | Reader progressive disclosure, knowledge-state tracking, `terminology_permitted` ratchet, foreshadowing, tension curves |
| [dramatica-integration.md](dramatica-integration.md) | Dramatica Theory mapping: throughlines, signposts, story points as wiki pages |
| [writing-pipeline.md](writing-pipeline.md) | Beats, outlines, manuscripts: the 4-stage writing pipeline with page types and workflows |

## How to Use

- Do NOT read these files at session start
- Read a specific doc ONLY when a `todo/phase-*/README.md` task says to
- These are the "what" — implementation instructions (the "how") live in `todo/`

## Developer Enhancements
- `jules/` - Contains specs and conceptual proposals developed during implementation, such as decoupling agent operational instructions from system development context.
