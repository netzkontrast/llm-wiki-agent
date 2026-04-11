---
name: wiki-ingest
description: Ingests raw text into the knowledge base, creating or updating source, entity, concept, and novel-specific pages according to the extended ingest workflow.
version: 1.0
triggers:
  - "ingest"
  - "process raw file"
  - "read source"
---

# wiki-ingest

Use this workflow to process new source material into the wiki.

## Context Load
- `wiki/meta/contradiction-log.md`
- `wiki/index.md`

## Steps
1. Parse the raw input.
2. Create/update a source page.
3. Create/update entity pages.
4. Create/update concept pages.
5. Create/update synthesis pages.
6. Check for contradictions against `wiki/meta/contradiction-log.md`.
7. Link pages appropriately (requires/informs).
8. Ensure frontmatter conforms to schema.
9. Write changes.
10. Create/update character pages for fictional characters mentioned in the source.
11. Create/update location pages for settings described.
12. Create/update conflict pages for conflicts identified.
13. Create/update theme pages for thematic elements discussed.
14. Create/update rule pages if the source defines world rules or narrative mandates.
15. Link source page to relevant chapter pages if chapter-specific content.
16. Update timeline events if the source establishes chronological facts.
17. Create/update foreshadowing pages if the source discusses foreshadowing strands.

## Validation
- Ensure all required fields are present in frontmatter.
- Verify `informs` chains are correct.
