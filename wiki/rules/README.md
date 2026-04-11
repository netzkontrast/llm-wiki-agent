# Rules

Rule pages define the constraints that govern the story world and the writing process. Three rule classes exist: `world` (constrains the story), `narrative` (constrains the writing), `structural` (constrains the architecture).

## Pages
- [CoherenceTheoryOfTruth.md](CoherenceTheoryOfTruth.md) — world rule, logic domain — truth-as-coherence operating system of LogosPrime
- [MaxOneNewConceptPerScene.md](MaxOneNewConceptPerScene.md) — narrative rule, psychology domain — reader cognitive load cap

## Connections
- Referenced by: `wiki/chapters/` — chapters list governing rules in `constraint_refs:`
- Referenced by: `wiki/reader-model/` — reader-state pages list active rules in `constraints_active:`
- Related to: `wiki/locations/` — world rules are active within specific locations
- Related to: `wiki/meta/contradiction-log.md` — rule violations or contradictions are logged here

## Routing Layer
Part of the **Knowledge Layer** — see [`wiki/knowledge/README.md`](../knowledge/README.md) for loading rules and mutation constraints.

## Conventions
- Naming: `TitleCase.md` (e.g., `CoherenceTheoryOfTruth.md`, `MaxOneNewConceptPerScene.md`)
- Temporal: World and structural rules are usually timeless. Narrative rules apply across the manuscript.
- Authority: Rule pages are the highest authority in the contradiction hierarchy (`rule > source > character > chapter > synthesis`). Contradictions with rule pages must be logged, never silently resolved.
