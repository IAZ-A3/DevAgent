---
name: context-manager
description: Shared utility imported by all DevAgent skills. Defines mandatory checkpoint rules. This is not advisory — every skill must follow these rules. If a skill's execution flow does not have an explicit checkpoint step, the rules here apply as the fallback.
---

# Context Manager

**Status: MANDATORY. Not advisory. Not optional.**

All DevAgent skills import this file. The rules here are enforced as invariants.
If a skill's own SKILL.md has a more specific checkpoint rule (e.g., "after each bug"),
that rule applies. If the skill's flow is silent on checkpoints, **these rules apply**.

---

## Rule 1 — Per-Work-Item Checkpoint (PRIMARY RULE)

Write a checkpoint after **every work item completes**, regardless of type:
- After each bug is resolved → `maintenance/checkpoint.md`
- After each enhancement task is complete → `implementation/checkpoint.md`
- After each wave completes in implementation → `implementation/checkpoint.md`
- After each design doc is produced → `design/checkpoint.md`
- After each V&V check block completes → `verification/checkpoint.md`
- After release packaging step → `release/checkpoint.md`

"Work item" means: one BUG-xxx, one P-xxx task, one implementation wave, one design doc, one V&V block.
**Do not batch multiple work items into a single checkpoint write.**

---

## Rule 2 — Context Threshold Checkpoint (SAFETY NET)

**After approximately every 40 tool calls in a session:**

1. Stop immediately — do not finish the current step
2. Write checkpoint to the active skill's state folder
3. Note the partial state in the "In Progress" section
4. Output: `"Context threshold reached — checkpoint written at [path]. Resume with /deva:resume."`
5. Stop. Do not continue.

Count tool calls by scanning the tool-use blocks visible in your current context. This is a rough heuristic — when in doubt, checkpoint early rather than late.

This rule overrides Rule 1. If threshold is hit mid-task, write a partial checkpoint.

---

## Rule 3 — Checkpoint Before Skill Transition

Before invoking a new skill (e.g., transitioning from Maintenance to Implementation):
1. Write a final checkpoint for the current skill
2. Confirm the checkpoint is written
3. Then invoke the new skill

Do not invoke a new skill with unsaved state.

---

## Rule 4 — Checkpoint Location by Skill

| Active skill | Checkpoint path |
|-------------|----------------|
| Requirements | `.claude/skills/state/requirements/checkpoint.md` |
| Planning | `.claude/skills/state/planning/checkpoint.md` |
| Design | `.claude/skills/state/design/checkpoint.md` |
| Implementation | `.claude/skills/state/implementation/checkpoint.md` |
| Verification | `.claude/skills/state/verification/checkpoint.md` |
| Release | `.claude/skills/state/release/checkpoint.md` |
| Maintenance (BUG-FIX) | `.claude/skills/state/maintenance/checkpoint.md` |
| Maintenance (ENHANCEMENT) | `.claude/skills/state/implementation/checkpoint.md` |
| Onboarding | `.claude/skills/state/onboarding/checkpoint.md` |

**Maintenance ENHANCEMENT mode uses the implementation folder.** This is intentional.
Enhancements are implementation artifacts; they must be traceable as such.

---

## Rule 5 — Checkpoint Minimum Content

Every checkpoint must include at minimum:

```markdown
# [Skill Name] Checkpoint
Updated: [ISO 8601 timestamp]
Active sub-mode: [if applicable]

## Completed
[list of work items with IDs — or "none" if first checkpoint]

## In Progress
[current work item and what sub-steps are done / remain]

## Not Started
[remaining work items from plan.md or task list]

## Resume Instructions
[exact steps to continue: which file to read first, which task to start]
```

A checkpoint without "Resume Instructions" is incomplete and does not satisfy Rule 1.

---

## Rule 6 — Phase Gate Checkpoints

At phase gate PASS — before user approves next phase:
- Write checkpoint with status: COMPLETED
- Include: phase just completed, gate result, known issues carried forward, next phase, resume instruction

After writing a phase gate checkpoint, always inform the user:
```
✓ Checkpoint saved: .claude/skills/state/{phase}/checkpoint.md
  You can continue now, or start a fresh session for the {next phase} phase.
  If starting fresh: open a new session — Claude Code will resume from the checkpoint automatically.
```

---

## Anti-Patterns (What Breaks Checkpoints)

1. **Writing checkpoint at session end only** — violates Rule 1. One bug fixed = one checkpoint, regardless of session length.
2. **Checkpoint in wrong folder** — e.g., P1-xxx work in `maintenance/` — corrupts audit trail.
3. **Vague "In Progress" section** — "working on P1-002" with no sub-step detail is useless for resumption.
4. **Skipping checkpoint because "it's a small task"** — Rule 1 has no size exception.
5. **Batching multiple tasks into one checkpoint** — violates Rule 1. Each task gets its own checkpoint entry.
6. **No "Resume Instructions" section** — violates Rule 5. A checkpoint without resume instructions is incomplete.

---

## Subagent Handoff

When spawning a subagent:
- Pass only the **minimum required context** (not full conversation history).
- Always include: skill name, current phase, relevant artifact paths, and specific task.
- Subagent must write its output to a defined artifact file before terminating.

---

## Context Rot Prevention

- Never rely on information mentioned only in early conversation turns — always re-read from artifact files.
- If a fact is needed more than once, it must be written to an artifact file first.
- When resuming from checkpoint: re-read all artifact files before proceeding. Do not assume memory.
- If uncertain about a previously stated fact: re-read the source file, never guess.

---

## Parallel Execution Rules

- Identify independent tasks at the start of each phase.
- Spawn parallel subagents for independent tasks; use sequential execution only when there is a hard dependency.
- Each parallel subagent writes to its own isolated output file to avoid conflicts.
- Orchestrator merges outputs only after all subagents complete.
