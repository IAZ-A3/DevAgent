# /deva:resume — Resume an Interrupted Session

You are the DevAgent software development agent. The user wants to continue work from where a previous session left off.

## Instructions

1. Read `CLAUDE.md` completely before doing anything else.
2. Scan `.claude/skills/state/` for all `checkpoint.md` files. Find the most recent one by timestamp.
3. Read the checkpoint file completely.
4. Present a resume summary to the user:

```
Resuming from checkpoint: {checkpoint path}
Saved: {timestamp}

Phase: {phase name}
Status: {COMPLETED | IN_PROGRESS}
Last completed step: {description}

Artifacts confirmed present:
  ✓ {artifact path} — {status}

Next step: {exact next action from checkpoint resume instruction}

Shall I continue from here?
```

5. Wait for user confirmation before proceeding.
6. On confirmation: load the skill indicated by the checkpoint's resume instruction, read all artifact paths listed, and proceed from the exact step specified.
7. If no checkpoint is found: run the artifact scan from CLAUDE.md Section 3 and report the current project state instead. Ask the user what they want to do.

## Context passed from user
$ARGUMENTS
