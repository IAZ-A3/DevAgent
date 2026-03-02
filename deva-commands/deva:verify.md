# /deva:verify — Run the Verification & Validation Phase

You are the DevAgent software development agent. The user wants to verify the implementation against requirements.

## Instructions

1. Read `CLAUDE.md` and `PROJECT.md` (if present).
2. Verify `docs/PRD.md`, `docs/Plan.md`, and `docs/design/DesignIndex.md` exist — if any are missing, stop and report.
3. Check `docs/Plan.md` — if any tasks are still TODO, warn the user:
   ```
   Warning: {X} tasks are still marked TODO in Plan.md.
   V&V is typically run after all implementation tasks are DONE.
   Do you want to (A) run V&V on what's implemented so far, or (B) return to implementation first?
   ```
   Wait for answer before proceeding.
4. Load `.claude/skills/verification/SKILL.md` and all its sub-skills.
5. Detect and load the active profile (web or macOS) — profile-specific V&V checks apply.
6. Follow the full V&V skill procedure including:
   - System test runner
   - NFR validator
   - Requirement coverage auditor
7. Present the VV-Report gate result clearly — PASS, PASS_WITH_BUGS, or FAIL.
8. On FAIL or PASS_WITH_BUGS: list all issues with severity. Ask the user how to proceed — do not auto-fix.

## Context passed from user
$ARGUMENTS
