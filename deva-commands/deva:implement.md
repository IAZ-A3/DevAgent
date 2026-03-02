# /deva:implement — Run the Implementation Phase

You are the DevAgent software development agent. The user wants to implement features from the plan.

## Instructions

1. Read `CLAUDE.md` and `PROJECT.md` (if present).
2. Verify `docs/PRD.md`, `docs/Plan.md`, and `docs/design/DesignIndex.md` all exist — if any are missing, stop and tell the user which prerequisites are needed and which commands to run first.
3. Load `.claude/skills/implementation/SKILL.md` and all its sub-skills.
4. Detect and load the active profile (web or macOS) — profile-specific coding rules and sub-skills apply.
5. Read `docs/Plan.md` — identify the first TODO task. Present it to the user:
   ```
   Next task: TASK-XXX — {task description}
   Feature:   FEAT-XXX — {feature name}
   Estimated: {size}
   
   Shall I begin implementation?
   ```
6. If the user specified a task or feature in `$ARGUMENTS`, implement that instead of the next TODO task.
7. Wait for user confirmation before writing any code.
8. Follow the full Implementation skill procedure — use code-generator, code-reviewer, test-writer, and integrator sub-skills as appropriate.
9. After each task: update Plan.md task status to DONE, write checkpoint, report to user.

## Context / target task passed from user
$ARGUMENTS
