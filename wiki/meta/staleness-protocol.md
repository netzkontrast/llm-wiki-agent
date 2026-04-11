# Staleness Detection Protocol

This document outlines the protocol for checking and propagating staleness through the wiki via the `informs:` dependency chain.

Staleness detection serves two roles: real-time (during edits) and session-start (catching drift from prior sessions).

## Real-Time Protocol (Unbounded Propagation)

When a page is modified, the agent MUST follow the full `informs:` chain to prevent stale content.

1. **Modify the target page:** Record the change and update the `last_updated` date.
2. **Read `informs:` targets:** Look at the `informs:` list of the modified page.
3. **Check relevance:** For each target page, check if the change made to the source page affects the target.
   - If yes: Update the target page, then repeat the process using the target's `informs:` list.
   - If no: Mark the target as "checked, no update needed" and **do not** follow its `informs:` further.
4. **Cycle protection:** Track visited pages in a set. If a page appears again during traversal, skip it. Log the cycle in `wiki/meta/contradiction-log.md`.
5. **Continue** until all reachable targets are checked or updated.

## Session-Start Protocol (Staleness Audit)

Between sessions, external edits may leave stale pages. At session start, run a quick audit:

1. Use `tools/check_staleness.py` to recursively traverse the `informs:` chains.
2. The script compares `last_updated` dates between source pages and their `informs:` targets.
3. If a target's `last_updated` date is older than its informing page's `last_updated` date, it is marked as **stale**.
4. Review the report and either update the stale pages or flag them in `wiki/meta/contradiction-log.md`.
