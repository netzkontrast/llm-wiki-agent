---
name: wiki-ingest-reader
description: reader state ingest
---

Writes: `reader_state/reader-model/`, `reader_state/foreshadowing/`
Context: qmd `-c reader-state` + current chapter page; ceiling 5 pages
Triggered manually after chapter writing, not during document ingest
Monotonic-only: only add to `terminology_permitted`, never remove
