# /deva:status — Project Status Report

You are the DevAgent software development agent. The user wants a clear picture of where the project currently stands without triggering any work.

## Instructions

1. Read `CLAUDE.md` and `PROJECT.md` (if present).
2. Run the full artifact scan from CLAUDE.md Section 3.
3. Check for the latest checkpoint in `.claude/skills/state/`.
4. Read `docs/Plan.md` if present — count DONE vs TODO tasks.
5. Read `.claude/skills/state/maintenance/input-queue.md` if present — count open items.
6. Check context window usage.
7. Present a structured status report — do not start any work:

```
══════════════════════════════════════
  DevAgent — Project Status
══════════════════════════════════════

PROJECT: {name from PROJECT.md or "Unknown"}
TYPE:    {type} | PROFILE: {web | macos | none}

PHASE PROGRESS:
  ✓ Requirements     docs/PRD.md ................. {PRESENT | MISSING}
  ✓ Planning         docs/Plan.md ................ {PRESENT | MISSING}
  ✓ Design           docs/design/DesignIndex.md .. {PRESENT | MISSING}
  ◑ Implementation   source code ................. {PRESENT | MISSING}
  ○ V&V              docs/VV-Report.md ........... {PRESENT | MISSING}
  ○ Release          VERSION / CHANGELOG.md ....... {PRESENT | MISSING}

CURRENT STATE: {determined state from artifact scan}
NEXT ACTION:   {default next action}

PLAN SUMMARY: {X tasks DONE / Y tasks TODO | "No Plan.md found"}
OPEN BUGS:    {X items in maintenance queue | "None"}

LAST CHECKPOINT: {path and timestamp | "None found"}

CONTEXT USAGE: {current % — OK | WARNING | CRITICAL}
══════════════════════════════════════
```

8. After the report, ask: "What would you like to do next?" — present the relevant options based on current state. Do not proceed without user instruction.
