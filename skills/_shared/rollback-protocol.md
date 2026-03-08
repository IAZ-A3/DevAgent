# Phase Rollback Protocol

## When to use
A later phase revealed a gap in a completed phase and the user needs to go back.
Trigger phrases: "go back to design", "redo the planning", "the design is wrong",
"start implementation over", "redesign FEAT-XXX".

## Step 1 — Assess what is invalidated

| Rolling back to | Archive these artifacts |
|----------------|------------------------|
| Requirements | Plan.md, all design docs, src/, tests/ |
| Planning | All design docs, src/, tests/ |
| Design | src/ and tests/ only |
| Implementation | tests/ only (if design is unchanged) |

## Step 2 — Archive (never delete)

Move invalidated artifacts to `.claude/archive/rollback-{date}/`.
Preserve directory structure inside the archive folder.
Ask user to confirm before moving any file.

## Step 3 — Update artifact registry

Mark rolled-back artifacts as ARCHIVED in `.claude/skills/state/artifact-registry.md`.
Do not delete registry entries — ARCHIVED records are the audit trail.

## Step 4 — Resume

Load the target phase SKILL.md. It will detect current state from the artifact registry.
Pass the user's reason for rollback so the clarification protocol can address it upfront.
