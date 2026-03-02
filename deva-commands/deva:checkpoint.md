# /deva:checkpoint — Save a Manual Checkpoint

You are the DevAgent software development agent. The user wants to manually save a checkpoint before ending their session or pausing work.

## Instructions

1. Read `CLAUDE.md` and `PROJECT.md` (if present).
2. Run the artifact scan (CLAUDE.md Section 3) to determine current project state.
3. Read `docs/Plan.md` — identify the last DONE task and next TODO task.
4. Read the latest existing checkpoint if present (`.claude/skills/state/*/checkpoint.md`) for context.
5. Determine the current phase from project state.
6. Write a checkpoint file to `.claude/skills/state/{phase}/checkpoint.md`:

```markdown
# Checkpoint — {phase} — {timestamp}
## Status: IN_PROGRESS
## Saved by: /deva:checkpoint (manual)

## Phase: {current phase}
## Last completed: {last DONE task or sub-phase}
## Next step: {next TODO task or action}

## Artifacts confirmed present:
- docs/PRD.md — {PRESENT | MISSING}
- docs/Plan.md — {PRESENT | MISSING}
- docs/design/DesignIndex.md — {PRESENT | MISSING}
- {other relevant artifacts}

## Plan summary:
- Tasks DONE: {X}
- Tasks TODO: {Y}
- Next task: TASK-XXX — {description}

## Resume instruction:
Load .claude/skills/{phase}/SKILL.md, read docs/PRD.md and docs/Plan.md,
proceed with: {exact next action}
```

7. After writing, confirm to the user:
```
✓ Checkpoint saved: .claude/skills/state/{phase}/checkpoint.md
  Saved at: {timestamp}
  Next session: type /deva:resume to continue from here.
```

## Context passed from user
$ARGUMENTS
