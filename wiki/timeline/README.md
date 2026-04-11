# Timeline

Chronological event pages — the temporal index of the story. Boundary events (`is_boundary: true`) serve as anchors for the `valid_from`/`valid_until` system used across all other page types.

## Pages
- [001-story-begins.md](001-story-begins.md) — Day 1, morning — story opens, Kael in LogosPrime (boundary)
- [010-fragmentation-revealed.md](010-fragmentation-revealed.md) — Day 10, crisis point — Kael's fragmentation exposed (boundary)
- [028-goedel-gambit.md](028-goedel-gambit.md) — Day 28, structural climax — Kael deploys the Goedel Gambit (boundary)

## Connections
- Referenced by: All page types that use `valid_from:` or `valid_until:` — these fields must use a slug from this directory
- Related to: `wiki/chapters/` — chapters use `timeline_start:` and `timeline_end:` to reference events here
- Related to: `wiki/reader-model/` — reader-state pages are anchored to timeline positions

## Routing Layer
Part of the **Knowledge Layer** — see [`wiki/knowledge/README.md`](../knowledge/README.md) for loading rules and mutation constraints.

## Conventions
- Naming: `NNN-slug.md` (three-digit zero-padded sequence + kebab-case: `001-story-begins.md`, `028-goedel-gambit.md`)
- Temporal: These pages ARE the temporal index — they don't use `valid_from`/`valid_until` themselves
- Boundary events: Only pages with `is_boundary: true` may be referenced by `valid_from`/`valid_until` fields. Filter by `is_boundary` to build the temporal index quickly.
