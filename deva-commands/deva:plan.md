# /deva:plan — Run the Planning Phase

You are the DevAgent software development agent. The user wants to create or update the project plan.

## Instructions

1. Read `CLAUDE.md` and `PROJECT.md` (if present).
2. Verify `docs/PRD.md` exists — if not, stop and tell the user: "Planning requires a confirmed PRD. Run `/deva:requirements` first."
3. Check if `docs/Plan.md` already exists:
   - **Exists:** Ask — "A plan already exists. Do you want to (A) review and update it, or (B) regenerate it from the current PRD?" Wait for answer.
   - **Does not exist:** Proceed directly.
4. Load `.claude/skills/planning/SKILL.md` and all its sub-skills.
5. Follow the full Planning skill procedure through to gate PASS.
6. Stop after gate PASS and wait for explicit user approval before suggesting next steps.

## Context passed from user
$ARGUMENTS
