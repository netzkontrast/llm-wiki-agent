---
name: sessionlog
description: Wraps another command in ultra-verbose extended session logging.
version: 1.0.0
triggers:
  - "/sessionlog"
  - "run with session logging"
---

# /sessionlog Command Workflow

**Purpose:** Executes any standard command (like `/wiki-ingest`) but wraps its entire execution in an ultra-verbose, append-only debug trace to allow deep analysis of the agent's behavior.

**Usage:** `/sessionlog <command> [arguments]`
Example: `/sessionlog wiki-ingest raw/UmfassendesLokalitatenKonzeptFurRoman.md`

## Instructions for the Agent

When you receive this command, you are entering **Trace Mode**. You must execute the wrapped command while strictly adhering to the logging requirements defined in `docs/jules/extended-session-logging.md`.

### Step 1: Initialize the Session
1. Create a timestamped directory for the session: `log/{command-name}/$(date +%Y%m%d-%H%M%S)/`
2. Create the standard session files if required (`plan.md`, `findings.md`).
3. **Crucial:** Create the `trace.md` file in this directory.

### Step 2: The Logging Loop
For *every single action* (reading a file, using a tool, writing a file, analyzing output) you take to fulfill the wrapped command, you MUST append a log entry to `trace.md`.

Use the bash command `echo -e "..." >> log/.../trace.md` (or write to it via standard write tools in append mode).

**Required Schema for EVERY entry:**
```markdown
### [$(date +'%Y-%m-%d %H:%M:%S')] {Action Type: THOUGHT | READ | WRITE | BASH | COMMIT}

**Context/Intent:** What was I trying to achieve?
**Action:** The specific tool/command/file.
**Result Evaluation:**
- *Status:* [Expected | Unexpected]
- *Quality:* [Helpful & Complete | Incomplete | Irrelevant]
- *Observations:* What did the tool actually return?
**Next Step:** What will I do next based on this?

---
```

### Step 3: Granular Committing
Whenever you complete a logical "Phase" of the wrapped command (e.g., Decompose, Plan, Write, Wrap-up for an ingest), you must:
1. `git add .`
2. `git commit -m "chore(sessionlog): complete <phase name> phase"`
3. Append a `COMMIT` action type entry to `trace.md` noting the phase that was saved.

### Step 4: Finalization
Once the wrapped command is completely finished:
1. Append a final `THOUGHT` entry reflecting on the overall success of the session.
2. Ensure all changes are committed.
