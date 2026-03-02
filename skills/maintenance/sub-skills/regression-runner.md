# DevAgent Sub-skill: Regression Runner
**Parent:** Maintenance Orchestrator  
**Scope:** Re-run previously failing tests after a bug fix  
**Output:** Test results — PASS | FAIL per test

---

## Purpose

After a bug fix is applied, re-run the specific tests that were previously failing plus any tests that cover the modified code. Confirm the fix resolves the failure without introducing new failures. Do NOT run the full test suite — targeted regression only.

---

## Required Inputs

| Input | Source | Required |
|-------|--------|----------|
| BUG-XXX fix report | state/maintenance/ | Yes |
| List of tests to re-run | Fix report: "Tests That Should Now Pass" | Yes |
| TechnologyStack.md | docs/design/TechnologyStack.md | Yes |
| VV-Report.md | docs/VV-Report.md | If exists |
| tests/ | project test files | Yes |

---

## 1. Test Selection Strategy

Run tests in this order:

**Group 1 — Previously failing tests:**
Tests listed in the fix report under "Tests That Should Now Pass".
These MUST pass for the fix to be considered successful.

**Group 2 — Tests covering modified files:**
Identify which test files cover the source files that were changed.
Run these to catch any regression introduced by the fix.

**Group 3 — New regression test (if recommended):**
If the fix report recommended a new test, write it first, then run it.
New test must PASS to confirm fix correctness.

**Do NOT run:**
- Unrelated test suites
- Full system test suite (that is V&V scope)
- Performance tests (unless the bug was a performance NFR violation)

---

## 2. Test Execution

Read test runner from `TechnologyStack.md`.

For each test group:
1. Execute targeted test run:
   ```bash
   {test_runner} {specific_test_file_or_test_id} -v
   ```
2. Capture: exit code, output, duration
3. Record: PASS | FAIL | ERROR per test

**Timeout:** 60 seconds per test (or NFR-defined timeout if applicable).

---

## 3. Result Evaluation

After all groups run:

| Outcome | Condition | Action |
|---------|-----------|--------|
| FULL PASS | All Group 1 + 2 + 3 tests pass | Report SUCCESS to orchestrator |
| PARTIAL | Some Group 1 tests still fail | Report STILL_FAILING — back to Bug Fixer |
| REGRESSION | Group 2 tests newly failing | Report REGRESSION_INTRODUCED — back to Bug Fixer |
| NEW TEST FAIL | Group 3 new test fails | Report FIX_INCOMPLETE — back to Bug Fixer |

---

## 4. Output

Write to `.claude/skills/state/maintenance/BUG-XXX-regression.md`:

```markdown
# Regression Test Report
## BUG-XXX: {title}
## Date: {date}
## Test Runner: {runner + version}
## Overall Result: FULL_PASS | STILL_FAILING | REGRESSION_INTRODUCED | FIX_INCOMPLETE

---

## Group 1 — Previously Failing Tests
| Test | Result | Duration | Notes |
|------|--------|----------|-------|
| test_feat001_file_change | PASS | 0.2s | Previously FAIL |
| test_feat001_error_case | PASS | 0.1s | Previously FAIL |

**Group 1 Result: PASS | FAIL**

---

## Group 2 — Regression Check (modified files)
| Test | Result | Duration | Notes |
|------|--------|----------|-------|
| test_feat001_happy_path | PASS | 0.3s | No regression |

**Group 2 Result: PASS | FAIL**

---

## Group 3 — New Regression Test
| Test | Result | Duration | Notes |
|------|--------|----------|-------|
| test_feat001_null_input_handled | PASS | 0.1s | New test |

**Group 3 Result: PASS | FAIL | SKIPPED (none recommended)**

---

## Summary
| Metric | Value |
|--------|-------|
| Total Tests Run | N |
| Passed | N |
| Failed | N |
| Duration | Ns |

## Verdict
{FULL_PASS: Fix verified — ready for release decision}
{STILL_FAILING: N tests still failing — return to Bug Fixer}
{REGRESSION_INTRODUCED: Fix broke N previously passing tests — return to Bug Fixer}
{FIX_INCOMPLETE: New regression test failed — return to Bug Fixer}
```

---

## 5. Context Management

- Targeted and lightweight — context load is minimal
- Save results immediately after each test group
- Checkpoint if running more than 20 tests (large blast radius fix)
