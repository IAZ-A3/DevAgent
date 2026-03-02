# /deva:audit — Project Health & Traceability Audit

You are the DevAgent software development agent. The user wants a comprehensive health check of the project — traceability, coverage, consistency, and quality.

## Instructions

1. Read `CLAUDE.md` and `PROJECT.md` (if present).
2. Run the full artifact scan (CLAUDE.md Section 3) to establish baseline state.
3. Perform the following checks in parallel where possible:

### Check A — Artifact completeness
For each expected artifact given the current project state:
- Is it present?
- Is it non-empty and well-formed?
- Does it have a gate result (where applicable)?

### Check B — Forward traceability
For every FEAT-XXX in `docs/PRD.md`:
- Is there at least one TASK-XXX in `docs/Plan.md` referencing it?
- Is there at least one design element in `docs/design/` covering it?
- Is there at least one test or V&V check covering it (if implementation is done)?

### Check C — Backward traceability
For every TASK-XXX in `docs/Plan.md`:
- Does it reference a valid FEAT-XXX in the PRD?

For every design doc element:
- Does it trace back to a requirement?

### Check D — Plan consistency
- Are any tasks DONE that have TODO dependencies? (ordering violation)
- Are any tasks TODO that have all dependencies DONE? (ready to implement)
- Are there XXL tasks that should be broken down?

### Check E — Maintenance queue
- How many bugs are open?
- Are any CRITICAL or HIGH severity bugs unresolved?

### Check F — Profile compliance (if active)
- Web profile: are all NFRs addressed? Is deployment config present?
- macOS profile: are entitlements complete? Is privacy manifest present?

4. Present a structured audit report — do not fix anything automatically:

```
══════════════════════════════════════════
  DevAgent — Project Audit Report
  {timestamp}
══════════════════════════════════════════

ARTIFACT COMPLETENESS
  ✓ docs/PRD.md .............. {PRESENT | MISSING}
  ✓ docs/Plan.md ............. {PRESENT | MISSING}
  ✓ docs/design/ ............. {X docs present | MISSING}
  ✓ docs/VV-Report.md ........ {PRESENT | MISSING | N/A}

TRACEABILITY
  Forward coverage: {X / Y features have full trace} — {PASS | GAPS FOUND}
  Backward coverage: {X / Y tasks trace to requirement} — {PASS | GAPS FOUND}
  Gaps: {list or "None"}

PLAN HEALTH
  Tasks DONE: {X}   Tasks TODO: {Y}
  Ready to implement: {list of unblocked TODO tasks}
  Ordering violations: {list or "None"}

MAINTENANCE QUEUE
  Open bugs: {X} ({critical}, {high}, {medium}, {low})
  {list of CRITICAL/HIGH items if any}

PROFILE COMPLIANCE: {PASS | ISSUES FOUND | N/A}
  {list of issues if any}

OVERALL HEALTH: ✓ HEALTHY | ⚠ NEEDS ATTENTION | ✗ CRITICAL ISSUES
══════════════════════════════════════════
```

5. After the report, list recommended actions in priority order. Do not execute any — wait for user instruction.

## Context passed from user
$ARGUMENTS
