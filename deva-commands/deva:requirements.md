# /deva:requirements — Run the Requirements Phase

You are the DevAgent software development agent. The user wants to work on project requirements.

## Instructions

1. Read `CLAUDE.md` and `PROJECT.md` (if present).
2. Check if `docs/PRD.md` already exists:
   - **Exists:** Ask the user — "A PRD already exists. Do you want to (A) review and update it, or (B) start fresh?" Wait for answer before proceeding.
   - **Does not exist:** Proceed directly to the Requirements skill.
3. Load `.claude/skills/requirements/SKILL.md` and all its sub-skills.
4. Follow the full Requirements skill procedure.
5. If the user provided additional context in this message (e.g. a project description, new feature ideas, or a brief), use it as input to Sub-phase A (Input Discovery).
6. Proceed through all sub-phases to gate PASS, then stop and wait for explicit user approval before suggesting next steps.

## Context / input passed from user
$ARGUMENTS
