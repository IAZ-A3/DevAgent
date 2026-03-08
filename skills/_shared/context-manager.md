# Context Manager — Shared Module
> Imported by all skills. Defines universal context hygiene rules.

---

## 1. Context Hygiene Approach

Context window percentage cannot be measured directly — do not attempt to estimate it.
Use only the event-based checkpoints in Section 2. They cover every situation the
percentage thresholds intended to catch.

If a task will spawn 5+ subagents or generate 10+ files, treat it as a
"long-running operation" and write a checkpoint before starting.

---

## 2. Mandatory Checkpoint Triggers

Checkpoints are written at **event-based triggers** (below).
Event-based checkpoints are written regardless of context usage level.

**Always write a checkpoint at these events:**

| Event | Status field |
|-------|-------------|
| Phase gate PASS — before user approves next phase | `COMPLETED` |
| Major sub-task complete within a phase | `IN_PROGRESS` |
| Before any long-running operation (archive, notarization, full test suite) | `IN_PROGRESS` |
| User explicitly asks to pause or end session | `IN_PROGRESS` |

Checkpoint location: `.claude/skills/state/{phase}/checkpoint.md`

**Why this matters:** after a phase gate PASS, the user may choose to clear the context window
and start a fresh session for the next phase. The checkpoint must contain everything needed
to resume without re-reading conversation history.

**Phase gate checkpoint — additional required fields beyond Section 3 format:**
```
## Phase just completed: {phase name}
## Gate result: PASS | PASS_WITH_BUGS
## Known issues carried forward: [list or "None"]
## Next phase: {phase name}
## Resume instruction: Load {next SKILL.md path}, read {key artifact paths}, proceed with {exact first step}
```

**After writing a phase gate checkpoint, always inform the user:**
```
✓ Checkpoint saved: .claude/skills/state/{phase}/checkpoint.md
  You can continue now, or start a fresh session for the {next phase} phase.
  If starting fresh: open a new session — Claude Code will resume from the checkpoint automatically.
```

---

## 3. Checkpoint Format

Each checkpoint must contain:
```
# Checkpoint — {Skill Name} — {timestamp}
## Status: IN_PROGRESS | COMPLETED | BLOCKED
## Completed Steps: [list]
## Pending Steps: [list]
## Key Decisions Made: [list]
## Artifacts Produced: [file paths]
## Next Agent Instructions: [exact instructions to resume]
```

---

## 4. Subagent Handoff

When spawning a subagent:
- Pass only the **minimum required context** (not full conversation history).
- Always include: skill name, current phase, relevant artifact paths, and specific task.
- Subagent must write its output to a defined artifact file before terminating.

---

## 5. Context Rot Prevention

- Never rely on information mentioned only in early conversation turns — always re-read from artifact files.
- If a fact is needed more than once, it must be written to an artifact file first.
- When resuming from checkpoint: re-read all artifact files before proceeding. Do not assume memory.
- If uncertain about a previously stated fact: re-read the source file, never guess.

---

## 6. Parallel Execution Rules

- Identify independent tasks at the start of each phase.
- Spawn parallel subagents for independent tasks; use sequential execution only when there is a hard dependency.
- Each parallel subagent writes to its own isolated output file to avoid conflicts.
- Orchestrator merges outputs only after all subagents complete.