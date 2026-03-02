# /deva:fix — Fix a Bug or Run Maintenance

You are the DevAgent software development agent. The user wants to fix a bug or run a maintenance task.

## Instructions

1. Read `CLAUDE.md` and `PROJECT.md` (if present).
2. Load `.claude/skills/maintenance/SKILL.md` and all its sub-skills.
3. Determine the bug input source — in priority order:
   a. If `$ARGUMENTS` contains a BUG-ID (e.g. "BUG-003"): load that bug from `.claude/skills/state/maintenance/input-queue.md`
   b. If `$ARGUMENTS` contains a bug description: use it as the bug report input
   c. If no arguments: check `.claude/skills/state/maintenance/input-queue.md` for open items and present them:
      ```
      Open maintenance items:
      BUG-001 [HIGH]   — {description}
      BUG-002 [MEDIUM] — {description}
      
      Which bug would you like to fix? Or describe a new one.
      ```
   d. If queue is empty and no arguments: ask the user to describe the bug.
4. For any bug: always check upstream impact first — does this bug require a PRD or design doc update before the code fix?
5. Follow the full Maintenance skill procedure — bug-fixer and regression-runner sub-skills.
6. After fix: run regression check, update MAINTENANCE-LOG.md, mark bug as RESOLVED in queue.
7. Write checkpoint after each resolved bug.

## Bug ID or description passed from user
$ARGUMENTS
