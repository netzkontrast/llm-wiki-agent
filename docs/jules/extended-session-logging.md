# Extended Session Logging Specification

**Status:** Active Draft
**Purpose:** To provide total transparency into the agent's workflow, decision-making processes, tool usage, and result evaluation during complex tasks (such as ingestion). This ultra-verbose logging enables humans and system developers to trace exactly *how* an agent works, identifying bottlenecks, hallucination risks, and optimization opportunities.

## Core Principles

1. **Append-Only:** The log file is purely for recording. The agent must never read the log file back into its context window, as this would cause rapid context exhaustion. Write to it using standard append operations (e.g., `echo "..." >> path/to/trace.md`).
2. **Ultra-Verbose:** Every thought, every tool call, every parameter, and every evaluation of a tool's result must be recorded. If the agent pauses to think, it must log that thought.
3. **Continuous Evaluation:** For every tool execution, the agent must evaluate the output: Was it expected? Was it complete? How does it change the plan?

## Directory and File Structure

Extended session logs are stored within the standard session structure:
`log/{branch-name}/{timestamp}/trace.md`

This file sits alongside `plan.md`, `findings.md`, and `progress.md`, but serves a purely mechanical and chronological tracing purpose.

## Logging Schema

Each entry in `trace.md` must follow a structured schema to remain human-readable and easily parseable for future analysis.

```markdown
### [YYYY-MM-DD HH:MM:SS] {Action Type}

**Context/Intent:** What is the agent trying to achieve right now? Why?
**Action:** The specific tool or command being executed (including exact parameters, file paths, etc.).
**Result Evaluation:** (Logged after the action completes)
- *Status:* [Expected | Unexpected]
- *Quality:* [Helpful & Complete | Incomplete | Irrelevant]
- *Observations:* What did the tool actually return?
**Next Step:** How does this result influence the immediate next action? What is the pivot or continuation?
```

### Action Types
- `THOUGHT`: Pure reasoning, planning, or deciding between approaches.
- `READ`: Opening a file, grepping, or querying qmd.
- `WRITE`: Creating or modifying a file.
- `BASH`: Running a shell command (e.g., linting, decomposing).
- `COMMIT`: Saving the state of the repository.

## Execution Rules

1. **Pre-Action Logging:** Before running a tool, the agent should ideally formulate its intent. In practice, the agent can write the entire block (Intent + Action + Result + Next Step) immediately after the tool returns, reconstructing its thought process for the log.
2. **Commit Alignment:** When wrapped with a command like `/sessionlog`, the agent must create a Git commit after logical phases or major state changes, explicitly logging the commit hash or message in `trace.md`.
3. **No Summarization:** Do not summarize multiple steps into one log entry. One tool call = one log entry.
