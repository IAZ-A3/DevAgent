# /deva:design — Run the Design Phase

You are the DevAgent software development agent. The user wants to create or update architecture and design documents.

## Instructions

1. Read `CLAUDE.md` and `PROJECT.md` (if present).
2. Verify both `docs/PRD.md` and `docs/Plan.md` exist — if either is missing, stop and tell the user which prerequisite is needed and which command to run.
3. Check if `docs/design/DesignIndex.md` already exists:
   - **Exists:** Ask — "Design docs already exist. Do you want to (A) review and update specific documents, or (B) regenerate the full design from the current PRD and Plan?" Wait for answer.
   - **Does not exist:** Proceed directly.
4. Load `.claude/skills/design/SKILL.md` and all its sub-skills.
5. Detect and load the active profile (web or macOS) from CLAUDE.md Section 4 — profile-specific design documents apply.
6. Follow the full Design skill procedure through to gate PASS.
7. Stop after gate PASS and wait for explicit user approval before suggesting next steps.

## Context passed from user
$ARGUMENTS
