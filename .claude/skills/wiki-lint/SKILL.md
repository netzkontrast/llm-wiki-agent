---
name: wiki-lint
description: Executes the following: Runs the deterministic linting rules over the L2 wiki structure. Use when the user requests a health check of the wiki.
---

# wiki-lint

## Instructions

1. Execute the deterministic script: `python3 .claude/skills/wiki-lint/scripts/lint_l2.py`
2. Run standard validations: `python3 tools/validate.py --format json`
3. Analyze the standard output (stdout) for missing metadata, dead links, orphans, etc.
4. If there are contradictions between newly routed L0 facts and L2 pages, NEVER silently overwrite. Instead, append a `[!contradiction]` callout block detailing the discrepancy.
5. Report the findings to the user and suggest steps for memory defragmentation.

## Negative Constraints
- NEVER hallucinate a wikilink to a page that does not exist.
- NEVER delete existing text silently when a contradiction is found.
