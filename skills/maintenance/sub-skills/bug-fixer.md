# DevAgent Sub-skill: Bug Fixer
**Parent:** Maintenance Orchestrator  
**Scope:** One bug at a time  
**Output:** Fixed source code + impact assessment

---

## Purpose

Analyze a single bug, identify its root cause, apply a targeted fix, and assess whether the bug reveals a gap in requirements or design that needs upstream correction.

---

## Required Inputs

| Input | Source | Required |
|-------|--------|----------|
| BUG-XXX description | Maintenance queue or user | Yes |
| PRD.md | docs/PRD.md | Yes |
| DesignIndex.md | docs/design/DesignIndex.md | Yes |
| Relevant design documents | docs/design/ | Yes |
| Source files for affected feature | src/ | Yes |
| Relevant test files | tests/ | Yes |
| VV-Report.md | docs/VV-Report.md | If exists |

---

## 1. Root Cause Analysis

Before writing any fix:

**Step 1 — Reproduce:**
Identify the exact condition that triggers the bug. If a failing test exists, read it carefully. If not, construct a minimal reproduction case mentally from the bug description.

**Step 2 — Locate:**
Find the exact file(s) and function(s) responsible. Trace the execution path from trigger to failure.

**Step 3 — Classify root cause:**

| Root Cause Type | Description | Upstream Impact |
|----------------|-------------|----------------|
| Code defect | Logic error, off-by-one, null handling | None |
| Missing error handling | Edge case not handled | Possibly ErrorHandling.md |
| Wrong algorithm | Incorrect implementation of requirement | None (code only) |
| Requirement gap | Behavior not specified in PRD | PRD.md update needed |
| Design gap | Component interaction not specified | Design doc update needed |
| Requirement conflict | Two requirements contradict | PRD.md update needed |
| Dependency issue | External library behavior unexpected | TechnologyStack.md note |

**Step 4 — Confirm before fixing:**
Report root cause to orchestrator:
```
Bug Analysis: BUG-XXX
Root cause: {type} — {description}
Location: {file:function}
Upstream impact: {None | PRD.md | docs/design/ComponentDesign.md | ...}
Proposed fix: {brief description}
Risk: Low | Medium | High (could affect other components)
Proceed? [auto-proceed for Low/Medium, escalate High to user]
```
For HIGH risk fixes: wait for orchestrator to confirm with user before proceeding.

---

## 2. Fix Rules

- Fix the minimum code necessary — no opportunistic refactoring
- Preserve all existing behavior not related to the bug
- Add inline comment referencing the bug: `# Fix: BUG-XXX — {brief description}`
- If the fix changes a public interface: flag immediately — this is a design impact
- If the fix requires a new dependency: halt and report — do not introduce silently
- After fixing, re-read the requirement the code implements and verify the fix aligns

---

## 3. Fix Validation (pre-regression)

Before handing back to orchestrator:
- Re-read the fixed code against the relevant FR/NFR
- Confirm the fix does not introduce obvious new defects
- Identify which existing tests should now pass (list for Regression Runner)
- Identify if any new test should be written to prevent regression

---

## 4. Output

Write fix report to `.claude/skills/state/maintenance/BUG-XXX-fix.md`:

```markdown
# Bug Fix Report
## BUG-XXX: {title}
## Date: {date}
## Status: FIXED | PARTIAL | BLOCKED

### Root Cause
{detailed description}

### Root Cause Type
{type from classification table}

### Fix Applied
| File | Function/Line | Change Description |
|------|--------------|-------------------|
| src/feat1.py | handle_event():42 | Added null check before processing |

### Upstream Documents Requiring Update
{list with specific changes needed, or "None"}

### Tests That Should Now Pass
{list of test IDs or test names}

### New Test Recommended
{description of regression test to add, or "None"}

### Risk Assessment
Low | Medium | High — {reason}
```

---

## 5. Context Management

- Single bug scope — context is bounded
- For CRITICAL bugs with wide blast radius: analyze one component at a time, checkpoint between components
- Never attempt to fix multiple bugs in a single sub-skill invocation
