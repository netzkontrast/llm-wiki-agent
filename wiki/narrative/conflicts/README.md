# Conflicts

Conflict tracking pages. Each page tracks one conflict: its type, parties, stakes, escalation trajectory, and resolution status. Self-referential conflicts (where the conflict generates itself) are flagged with `self_referential: true`.

## Pages
- [KaelVsAegis.md](KaelVsAegis.md) — external, self-referential, open — the central paradox conflict

## Connections
- Related to: `wiki/narrative/characters/` — `parties:` field references character slugs
- Related to: `wiki/narrative/themes/` — conflicts link to themes they embody or challenge
- Related to: `wiki/narrative/chapters/` — chapters list active conflicts in `conflicts:` field
- Related to: `wiki/narrative/arcs/` — conflict resolution trajectories inform arc stages

## Routing Layer
Part of the **Narrative Layer** — see [`wiki/narrative/README.md`](../README.md) for loading rules and mutation constraints.

## Conventions
- Naming: `TitleCase.md` (e.g., `KaelVsAegis.md`, `InternalFragmentation.md`)
- Temporal: No — conflict pages track the full lifespan of a conflict across chapters via `chapter_range:` and `resolution_status:`.
