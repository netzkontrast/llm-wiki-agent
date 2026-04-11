Ingest a source document into the LLM Wiki.

Usage: /wiki-ingest $ARGUMENTS

$ARGUMENTS should be the path to a file in raw/, e.g. `raw/articles/my-article.md`

Follow the Extended Ingest Workflow defined in CLAUDE.md exactly:
1. Read the source file at the given path
2. Read wiki/index.md and wiki/overview.md for current context
3. Write wiki/sources/<slug>.md (source page format per CLAUDE.md)
4. Update wiki/index.md — add the new entry under Sources
5. Update wiki/overview.md — revise synthesis if warranted
6. Create/update entity pages (wiki/entities/) for key people, companies, projects
7. Create/update concept pages (wiki/concepts/) for key ideas and frameworks
8. Flag any contradictions with existing wiki content
9. Append to wiki/log.md: ## [today's date] ingest | <Title>

Novel-specific ingest steps:
10. Create/update character pages for fictional characters mentioned in the source
11. Create/update location pages for settings described
12. Create/update conflict pages for conflicts identified
13. Create/update theme pages for thematic elements discussed
14. Create/update rule pages if the source defines world rules or narrative mandates
15. Link source page to relevant chapter pages if chapter-specific content
16. Update timeline events if the source establishes chronological facts
17. Create/update foreshadowing pages if the source discusses foreshadowing strands

After completing all writes, summarize: what was added, which pages were created or updated, and any contradictions found.
