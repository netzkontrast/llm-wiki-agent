# Narrative Layer (K1)

**Type:** Routing Layer
**Content:** Plot States, Outlines, Manuscripts

This layer manages mutating plot states, the temporal unfolding of the story, and scene composition.

Unlike the Knowledge Layer, characters here do not exist as absolute definitions, but as dynamic state machines in `states/`, which store temporary deltas (e.g., "State of Character X after Chapter 3: injured and isolated").

Each chapter generated merely creates a diff (delta) upon the base state of the Knowledge Layer. This prevents retroactive, destructive overwriting of historical truths.
