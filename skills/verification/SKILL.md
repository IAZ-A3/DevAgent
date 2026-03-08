# DevAgent Skill: Verification & Validation — Orchestrator
**Phase:** 5 of 7  
**Role:** Entry point and coordinator for all V&V sub-skills  
**Output:** `docs/VV-Report.md` + `docs/NFR-Checklist.md`  
**Imports:** `../_shared/context-manager.md`, `../_shared/subagent-patterns.md`, `../_shared/artifact-schema.md`

---

## Purpose

Verify that the implemented system satisfies all requirements at the system level, and validate that non-functional requirements meet their acceptance criteria. This phase does NOT re-run unit or integration tests — those were covered in Implementation. Focus is on system-level behavior, requirement coverage audit, and NFR validation.

Bugs found here are logged, minor ones fixed in place, structural ones handed off to the Maintenance skill input queue.

---

## 1. Input Discovery

### If inputs are explicitly provided:
Use them directly.

### If inputs are NOT explicitly provided (auto-discovery):
Scan in this order:
1. `docs/PRD.md` — requirements to validate against (required)
2. `docs/Plan.md` — confirm all tasks DONE before proceeding
3. `docs/design/DesignIndex.md` — design reference
4. `docs/design/TechnologyStack.md` — test runner definition (required for execution)
5. `src/` — source code to test
6. `tests/` — existing unit/integration tests (read only — not re-run)
7. `.claude/skills/state/implementation/integration-report.md` — integration status
8. `.claude/skills/state/vv/checkpoint.md` — resume from previous session

**If Plan.md has tasks not DONE:** halt and inform user. All implementation must be complete before V&V.
**If TechnologyStack.md has no test runner defined:** halt and ask user to specify.

---

## 2. Clarification Protocol

Before starting, resolve:
- Any implementation tasks not marked DONE or SKIPPED in Plan.md
- Test runner not defined in TechnologyStack.md
- Ambiguity about system test entry points or test environment setup

Single grouped list, suggested answers, [BLOCKING] / [OPTIONAL].

---

## 3. Orchestration Flow

```
Step 1: Load & validate all inputs
Step 2: Spawn sub-skills in parallel:
        → System Test Runner
        → NFR Validator
        → Requirement Coverage Auditor
Step 3: WAIT — all three complete
Step 3a: Classify each requirement by coverage tier (see below)
Step 4: Orchestrator consolidates results
Step 5: Bug triage (classify findings)
Step 6: Attempt minor bug fixes
Step 7: Hand off structural bugs to Maintenance queue
Step 8: Produce VV-Report.md and NFR-Checklist.md
Step 9: Update Plan.md
Step 10: Phase gate
```

**Parallelism note:** System Test Runner, NFR Validator, and Requirement Coverage Auditor run fully in parallel — they read the same artifacts but write to separate state files.

### Coverage Tier Definitions

Classify each requirement after Step 3:
- **Automated** — a running test asserts the behavior
- **Review-verified** — a named reviewer confirmed it and it is recorded in VV-Report.md
  (acceptable for: visual design, legal/compliance, subjective UX, deployment config)
- **Unverified** — no test, no review record → this fails the gate

PASS requires zero Unverified requirements.
Less than 100% automated is acceptable if review-verified entries cover the remainder.

---

## 4. Bug Triage Rules

When a bug is found during V&V:

| Severity | Definition | Action |
|----------|-----------|--------|
| MINOR | Localized, single function, clear fix, no design impact | Attempt fix in place, re-run affected test |
| STRUCTURAL | Affects component design, interface contract, or multiple components | Log BUG-XXX, write to Maintenance queue, do NOT attempt fix |
| BLOCKING | Prevents system from functioning at all | Escalate to user immediately |

**Minor fix protocol:**
1. Attempt fix in source file
2. Re-run the specific test that caught the bug
3. If fix resolves it: log as FIXED in report
4. If fix introduces new failures or doesn't resolve: reclassify as STRUCTURAL and hand off

**Maintenance handoff format:**
Append to `.claude/skills/state/maintenance/input-queue.md`:
```
## BUG-XXX: {title}
**Found by:** V&V Phase
**Severity:** STRUCTURAL
**Feature:** FEAT-XXX
**Requirement:** {FR or NFR ID}
**Description:** {what fails and how}
**Reproduction:** {steps or test case that reveals it}
**Suggested investigation:** {where to look}
```

---

## 5. Context Management (Phase-Specific)

Imports rules from `../_shared/context-manager.md`, plus:

- Checkpoint after Step 3 (all sub-skills complete)
- Checkpoint after Step 6 (bug fixes attempted)
- State folder: `.claude/skills/state/vv/`
- If context runs low during consolidation: save partial results, checkpoint, resume in fresh session

---

## 6. Output & Phase Gate

On completion:
1. Write `docs/VV-Report.md`
2. Write `docs/NFR-Checklist.md`
3. Write any bugs to `.claude/skills/state/maintenance/input-queue.md`
4. Update `docs/Plan.md`
5. Update `.claude/skills/state/artifact-registry.md`
6. Produce phase gate:

```
# Phase Gate — Verification & Validation
## Result: PASS | FAIL | PASS_WITH_BUGS
## System Tests: N passed / N failed
## NFRs Auto-Validated: N/N passed
## NFRs Pending Manual Check: N
## Requirements Coverage:
##   Automated:        N FRs / NFRs
##   Review-verified:  N (recorded in VV-Report.md)
##   Unverified:       N  ← must be 0 to PASS
## Bugs Found: N total (N minor fixed, N structural handed to Maintenance)
## Recommended Next Phase: release
## Blockers: {list or "None"}
```

7. Inform user: V&V complete. If PASS or PASS_WITH_BUGS, suggest **Release** skill next. If FAIL, structural bugs must be resolved first.
