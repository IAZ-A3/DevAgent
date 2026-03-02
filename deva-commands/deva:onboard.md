# /deva:onboard — Onboard an Existing Project

You are the DevAgent software development agent. The user has an existing project that was started without the agent and needs to be brought under agent control.

## Instructions

1. Read `CLAUDE.md` completely before doing anything else.
2. Confirm that source code exists — if this appears to be a brand new empty project, stop and tell the user to use `/deva:new` instead.
3. Check if `docs/PRD.md` already exists — if it does, ask the user: "A PRD already exists. Do you want to (A) use it as-is and resume from the appropriate phase, or (B) re-run onboarding to reconstruct it from the current codebase?"
4. Load `.claude/skills/onboarding/SKILL.md` and all its sub-skills.
5. Begin with Sub-phase A (Project Detection) using the project-detector sub-skill at `.claude/skills/_shared/project-detector.md`.
6. Follow the full onboarding procedure through all 8 sub-phases.
7. At Sub-phase H (Re-entry Decision), present the user with the re-entry options and wait for their choice before loading the next skill.

## Context passed from user
$ARGUMENTS
