---
name: maintenance
description: Post-release work on an existing DevAgent-managed codebase. Handles two sub-modes: BUG-FIX (resolving defects, regressions, crashes — triggered by /deva:fix or BUG-xxx IDs) and ENHANCEMENT (implementing pre-approved plan.md items with P-prefix IDs like P1-xxx, P2-xxx, P3-xxx — but ONLY when those tasks are already marked TODO in plan.md from a prior onboarding or change request). Do NOT use this skill for P-prefix tasks that have not yet been through /deva:feature — route those to the feature command first. Route new greenfield features to /deva:feature. Route V&V to /deva:verify. Route release to /deva:release.
---

# Maintenance Skill

Handles post-release corrective and improvement work. **Read Section 1 immediately to determine your sub-mode before doing anything else.**

---

## Section 1 — Sub-Mode Routing (MANDATORY FIRST STEP)

Identify the work item type from the task ID or user instruction:

| Work item | ID pattern | Sub-mode | State folder | Invoke instead? |
|-----------|-----------|----------|-------------|-----------------|
| Bug fix / regression / crash | `BUG-xxx` or no ID | **BUG-FIX** | `.claude/skills/state/maintenance/` | — |
| Pre-approved plan.md enhancement | `P1-xxx`, `P2-xxx`, `P3-xxx`, `P4-xxx` | **ENHANCEMENT** | `.claude/skills/state/implementation/` | Consider `/deva:implement` |
| New feature not yet in plan.md | none / description only | — | — | **STOP. Invoke `/deva:feature` first** |
| V&V / testing | — | — | — | **STOP. Invoke `/deva:verify`** |

> **Critical:** If the task ID starts with `P`, you are doing **implementation work on a planned enhancement**, not maintenance. The artifacts you produce (new source files, new services, new UI components) are implementation artifacts. Write your checkpoint to `.claude/skills/state/implementation/checkpoint.md`. Apply implementation quality criteria (NFR compliance, design linkage, test stubs). Do not conflate this with bug-fix work.

> **Why this matters:** plan.md audit trails, artifact traceability, and `/deva:audit` all rely on checkpoint location to distinguish "we fixed a crash" from "we added BatteryService."

---

## Section 2 — Pre-Flight Checks

Before any work begins:

1. Read `docs/Plan.md` — confirm the task ID exists and is marked `TODO`
2. Read `PROJECT.md` — confirm platform, conventions, active profile
3. Read `docs/PRD.md` — check NFR constraints relevant to the task
4. Load prior checkpoint if resuming: read `.claude/skills/state/[sub-mode folder]/checkpoint.md`

For **BUG-FIX**: Also confirm bug ID in `docs/MAINTENANCE-LOG.md` (or create entry).

For **ENHANCEMENT**: Also check NFR-008 if task adds collapsed pill content; read any referenced design docs from `docs/design/`.

---

## Section 3 — BUG-FIX Flow

### Change Request Detection (run before fixing any bug)

**Step 1 — Find the feature**
Search PRD.md for a FEAT-XXX whose description covers the reported behavior.
→ No matching feature → Change Request (missing spec). Redirect to `/deva:requirements`.

**Step 2 — Find the requirement**
In that feature section, find the FR or NFR governing the reported behavior.
→ No matching requirement → Change Request (unspecified behavior). Redirect.

**Step 3 — Check implementation intent**
- Code crashes, throws exception, or causes data loss → Bug (always)
- Code produces wrong output for behavior the FR explicitly defines → Bug
- Performance is below the NFR acceptance criterion → Bug
- Code correctly implements the FR but user wants different behavior → Change Request
- User wants something the FR does not mention → Change Request

### Severity Classification

| Severity | Definition |
|----------|-----------|
| CRITICAL | System crash, data loss, security vulnerability, complete feature failure |
| HIGH | Feature partially broken, NFR acceptance criterion violated |
| MEDIUM | Incorrect behavior in edge case, minor functional issue |
| LOW | Cosmetic issue, minor inconsistency |

Process order: CRITICAL first, then HIGH, MEDIUM, LOW. One bug at a time.

### Fix Execution

```
STEP 1: TRIAGE
  - Confirm bug ID in MAINTENANCE-LOG.md (or create entry)
  - State the symptom, affected component, reproduction condition

STEP 2: ROOT CAUSE
  - Read relevant source files
  - Identify the defect location (file, line range)
  - State the root cause in one sentence before writing any code

STEP 3: FIX
  - Implement the minimal fix
  - Do not refactor unrelated code in the same commit
  - Update upstream docs (PRD.md or design docs) if the bug reveals a requirement or design gap

STEP 4: VERIFY
  - Confirm the symptom no longer occurs
  - Confirm no regressions in adjacent functionality
  - Run existing tests if coverage exists

╔══════════════════════════════════════════════════════╗
║  CHECKPOINT — MANDATORY AFTER EACH BUG IS RESOLVED  ║
║  File: .claude/skills/state/maintenance/checkpoint.md║
║  Write BEFORE proceeding to the next bug             ║
║  Template: Section 7                                 ║
╚══════════════════════════════════════════════════════╝

STEP 5: LOG
  - Update MAINTENANCE-LOG.md with resolution summary
  - Mark task DONE in docs/Plan.md
```

---

## Section 4 — ENHANCEMENT Flow

Follow these steps **in order**. Do not skip steps.

```
STEP 1: DESIGN CHECK
  - Read the task entry in docs/Plan.md (notes column)
  - If notes reference a design doc, read it before coding
  - Confirm NFR-008 compliance plan if task adds collapsed pill content:
      * Declare pixel contribution in NotchCoordinator.bindContentSources()
      * Add Defaults.Key<Bool> toggle
      * Wire Settings → Notch Display toggle
      * Gate view content on that key

STEP 2: IMPLEMENTATION
  - Create new files in the correct source location
  - Follow PROJECT.md conventions (naming, MVVM pattern, etc.)
  - Do not modify files unrelated to this task

STEP 3: INTEGRATION
  - Wire the new component into the existing system
  - Confirm no regressions in adjacent functionality

STEP 4: TEST STUBS
  - Add at minimum a placeholder test file for the new component
  - Note any test gaps in the checkpoint

╔══════════════════════════════════════════════════════════╗
║  CHECKPOINT — MANDATORY AFTER EACH ENHANCEMENT IS DONE  ║
║  File: .claude/skills/state/implementation/checkpoint.md ║
║  Write BEFORE proceeding to the next task                ║
║  Template: Section 7                                     ║
╚══════════════════════════════════════════════════════════╝

STEP 5: PLAN UPDATE
  - Mark task DONE in docs/Plan.md
  - Note any follow-on items discovered
```

---

## Section 5 — Context Threshold Rule

**After approximately every 40 tool calls** (count tool-use blocks visible in your context):
1. Write a checkpoint immediately (do not finish the current task first)
2. State: "Context threshold reached — checkpoint written. Resume with `/deva:resume`."
3. Stop.

This rule overrides all other rules.

---

## Section 6 — Phase Gate

When all tasks in the current batch are complete:

```
Maintenance gate: [BUG-FIX | ENHANCEMENT] → [next phase]

Gate result: PASS | PASS_WITH_NOTES | BLOCKED

Tasks completed: [list with IDs]
Tasks remaining: [list with IDs, or NONE]
Checkpoint written: .claude/skills/state/[folder]/checkpoint.md

Next action:
  - If more P-phase tasks remain: invoke /deva:implement [next-task-ID]
  - If V&V needed: invoke /deva:verify
  - If done: invoke /deva:release or end session
```

**Do not chain phases without user approval.**

---

## Section 7 — Checkpoint Templates

### BUG-FIX checkpoint (`.claude/skills/state/maintenance/checkpoint.md`)

```markdown
# Maintenance Checkpoint
Updated: [ISO timestamp]
Sub-mode: BUG-FIX

## Completed
- [BUG-xxx] [description] — RESOLVED ([root cause in one sentence])

## In Progress
- [BUG-xxx] [description] — [what was done, what remains]

## Not Started
- [list remaining BUG-xxx items]

## Files Modified
- [file path] — [what changed]

## Resume Instructions
Load this checkpoint, read MAINTENANCE-LOG.md, continue with next bug.
```

### ENHANCEMENT checkpoint (`.claude/skills/state/implementation/checkpoint.md`)

```markdown
# Implementation Checkpoint (Enhancement Mode)
Updated: [ISO timestamp]
Sub-mode: ENHANCEMENT (routed from Maintenance skill)

## Completed
- [P-xxx] [description] — DONE
  - Files created: [list]
  - NFR-008 compliant: [yes/no/N/A]
  - Test stubs: [yes/no]

## In Progress
- [P-xxx] [description]
  - Completed: [what's done]
  - Remaining: [what's left]

## Not Started
- [list remaining P-xxx items]

## Resume Instructions
Load this checkpoint, read docs/Plan.md, continue with next P-xxx item.
```

---

## Section 8 — What This Skill Does NOT Handle

| Situation | Correct action |
|-----------|---------------|
| New feature not in plan.md | `/deva:feature [description]` |
| V&V / testing | `/deva:verify` |
| Release packaging | `/deva:release` |
| Design changes | `/deva:design` |
| Requirements changes | `/deva:requirements` |
