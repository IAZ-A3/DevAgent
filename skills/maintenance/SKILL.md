# DevAgent Skill: Maintenance — Orchestrator
**Phase:** 7 of 7  
**Role:** Entry point and coordinator for reactive bug fixing  
**Output:** Fixed code, updated docs (if needed), updated `docs/Plan.md`, optional patch release  
**Imports:** `../_shared/context-manager.md`, `../_shared/subagent-patterns.md`, `../_shared/artifact-schema.md`

---

## Purpose

Handle bugs reactively — from the V&V maintenance queue or directly reported by the user. For each bug: analyze, fix, re-run affected tests, and ask the user whether to release a patch. If a bug reveals a requirements or design gap, update the relevant upstream documents. Change requests (new features) are out of scope — redirect to Requirements skill.

---

## 1. Input Discovery

### If inputs are explicitly provided:
Use them directly. Accepted forms:
- Bug description in the prompt
- BUG-XXX ID referencing the maintenance queue
- Error message, stack trace, or test failure output

### If inputs are NOT explicitly provided (auto-discovery):
Scan in this order:
1. `.claude/skills/state/maintenance/input-queue.md` — bugs handed off from V&V
2. `docs/VV-Report.md` — failed tests reference
3. `docs/PRD.md` — requirements reference
4. `docs/design/DesignIndex.md` — design reference
5. `docs/Plan.md` — task and feature reference
6. `docs/design/TechnologyStack.md` — test runner
7. `.claude/skills/state/maintenance/checkpoint.md` — resume from previous session

**If no bugs found in queue and none provided:** inform user the maintenance queue is empty and ask if they want to report a new bug.

---

## 2. Change Request Detection

Apply these steps in order before processing any maintenance item:

**Step 1 — Find the feature**
Search PRD.md for a FEAT-XXX whose description covers the reported behavior.
→ No matching feature → Change Request (missing spec). Redirect to Requirements skill.

**Step 2 — Find the requirement**
In that feature section, find the FR or NFR governing the reported behavior.
→ No matching requirement → Change Request (unspecified behavior). Redirect.

**Step 3 — Check implementation intent**
- Code crashes, throws exception, or causes data loss → Bug (always, regardless of coverage)
- Code produces wrong output for behavior the FR explicitly defines → Bug
- Performance is below the NFR acceptance criterion → Bug
- Code correctly implements the FR but user wants different behavior → Change Request
- User wants something the FR does not mention → Change Request

**Step 4 — If still ambiguous:**
Ask: "Is the code failing to do what the PRD says it should do (Bug)?
Or do you want behavior that differs from what was specified (Change Request)?"

**If Change Request detected:**
```
This describes behavior not covered by the current PRD. It is classified as a
Change Request, not a bug.

Run /deva:requirements to update the PRD first.
I can help you start that process if you'd like.
```

---

## 3. Bug Intake & Prioritization

For each bug in the queue or provided by user:

**Assign/confirm BUG-XXX ID** (from artifact-schema.md conventions).

**Classify severity:**
| Severity | Definition |
|----------|-----------|
| CRITICAL | System crash, data loss, security vulnerability, complete feature failure |
| HIGH | Feature partially broken, NFR acceptance criterion violated |
| MEDIUM | Incorrect behavior in edge case, minor functional issue |
| LOW | Cosmetic issue, minor inconsistency |

**Process order:** CRITICAL first, then HIGH, MEDIUM, LOW.
**One bug at a time** — complete full fix + test cycle before starting next bug.

---

## 4. Orchestration Flow (per bug)

```
Step 1: Classify bug (CR check + severity)
Step 2: Spawn Bug Fixer sub-skill
Step 3: WAIT — Bug Fixer produces fix + impact assessment
Step 4: If upstream docs need update → apply updates
Step 5: Spawn Regression Runner sub-skill
Step 6: WAIT — Regression Runner produces test results
Step 7: Evaluate results:
        → All previously failing tests now PASS: proceed to Step 8
        → Some tests still failing: back to Step 2 (re-fix)
        → New failures introduced: back to Step 2 (fix regression)
Step 8: Update Plan.md and maintenance log
Step 9: Ask user: release patch or continue to next bug?
Step 10: If release → invoke Release skill (PATCH bump)
         If continue → process next bug from queue
```

---

## 5. Upstream Document Update Rules

The Bug Fixer assesses whether upstream documents need updating. The orchestrator applies the updates:

| Bug Type | Document to Update | Update Action |
|----------|-------------------|---------------|
| Requirement was wrong/missing | `docs/PRD.md` | Add/correct the requirement, assign new ID if needed |
| Design was wrong/missing | relevant `docs/design/*.md` | Correct the design element, note the change |
| Both requirement and design wrong | Both | Update both, maintain traceability |
| Pure code defect | None | No upstream update needed |

All upstream updates must be logged in the maintenance log with the BUG-XXX reference.

---

## 6. Maintenance Log

Append to `docs/MAINTENANCE-LOG.md` after each bug resolution:

```markdown
## BUG-XXX: {title}
**Date:** {date}  
**Severity:** CRITICAL | HIGH | MEDIUM | LOW  
**Reported by:** V&V Phase | User  
**Feature:** FEAT-XXX  
**Requirement:** {FR/NFR ID or "None — code defect"}  
**Root cause:** {brief description}  
**Fix applied:** {files changed, what was changed}  
**Upstream updates:** {PRD.md | design doc | None}  
**Tests re-run:** {list of test IDs}  
**Test result:** PASS | FAIL  
**Released in:** v{version} | Pending  
```

---

## 7. Context Management (Phase-Specific)

Imports rules from `../_shared/context-manager.md`, plus:

- Checkpoint after each bug is resolved (before starting next)
- Checkpoint before invoking Release skill
- State folder: `.claude/skills/state/maintenance/`
- If context runs low mid-fix: complete current function fix, save partial state, checkpoint with exact resume point

---

## 8. Output & Maintenance Cycle Summary

After all bugs in the current session are processed:
1. Updated source files
2. Updated upstream docs (if needed)
3. `docs/MAINTENANCE-LOG.md` updated
4. `docs/Plan.md` updated
5. Update `.claude/skills/state/artifact-registry.md`
6. Produce session summary:

```
# Maintenance Session Summary
## Date: {date}
## Bugs Processed: N
## Fixed: N
## Pending (deferred): N
## Upstream Updates: {list or "None"}
## Patch Released: v{version} | No release this session
## Remaining Queue: N bugs
```
