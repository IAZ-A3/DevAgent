# DevAgent Sub-skill: System Test Runner
**Parent:** V&V Orchestrator  
**Scope:** System-level test execution  
**Output:** System test results per feature

---

## Purpose

Execute system-level tests that validate end-to-end behavior of the implemented system. This sub-skill does NOT re-run unit or integration tests. It focuses on testing the system as a whole against user-facing requirements.

---

## Required Inputs

| Input | Source | Required |
|-------|--------|----------|
| PRD.md | docs/PRD.md | Yes |
| TechnologyStack.md | docs/design/TechnologyStack.md | Yes |
| SystemArchitecture.md | docs/design/SystemArchitecture.md | Yes |
| src/ | project source | Yes |
| tests/ | existing tests (reference only) | Yes |
| Integration report | state/implementation/ | Yes |

---

## 1. System Test Strategy

System tests validate end-to-end flows — from the system's entry point through to its outputs — corresponding to functional requirements. They treat the system as a black box where possible.

For each feature in the PRD:
- Identify the user-facing entry point and expected outcome
- Write and execute one system test per critical FR
- Verify actual output matches requirement specification
- Verify system state is correct after the operation

---

## 2. Test Environment Setup

Before running any tests:
1. Read `TechnologyStack.md` — identify test runner (e.g. pytest, jest, go test)
2. Verify test runner is available: run `{test_runner} --version`
3. If not available: halt and report to orchestrator with install instructions
4. Set up any required test fixtures, temp directories, or mock external services
5. Ensure test environment is isolated — tests must not affect production data

Setup script template (adapt to project language):
```bash
#!/usr/bin/env bash
# vv-setup.sh — test environment setup
set -e
echo "Setting up V&V test environment..."
# Create isolated test workspace
mkdir -p .vv-workspace
# Install dependencies if needed
# {language-specific install command from TechnologyStack.md}
echo "Setup complete."
```

---

## 3. System Test Execution

For each feature:
1. Write system test file to `.vv-workspace/system-tests/feat-XXX-system-test.{ext}`
2. Execute: `{test_runner} .vv-workspace/system-tests/feat-XXX-system-test.{ext}`
3. Capture: exit code, stdout, stderr, execution time
4. Record result: PASS | FAIL | ERROR | SKIP

**Execution rules:**
- Run each feature's system tests in isolation
- Set a timeout per test (default: 30 seconds, adjust per NFR if defined)
- Capture full output — do not truncate
- On test failure: capture the exact failure message and stack trace

---

## 4. Output

Write to `.claude/skills/state/vv/system-test-results.md`:

```markdown
# System Test Results
## Date: {date}
## Test Runner: {runner + version}

---

## Results by Feature

### FEAT-001: {Feature Name}
| Test | Requirement | Result | Duration | Notes |
|------|-------------|--------|----------|-------|
| test_feat001_happy_path | FEAT-001-FR-001 | PASS | 0.3s | |
| test_feat001_error_case | FEAT-001-FR-002 | FAIL | 0.1s | AssertionError: expected X got Y |

**Feature Result: PASS | FAIL**

---

## Summary
| Metric | Value |
|--------|-------|
| Total Tests Run | N |
| Passed | N |
| Failed | N |
| Errors | N |
| Skipped | N |
| Total Duration | Ns |

---

## Failed Test Details
### FAIL-001
**Test:** {test name}
**Feature:** FEAT-XXX
**Requirement:** {FR ID}
**Failure:** {exact error message}
**Stdout:** {captured output}
**Suggested cause:** {brief analysis}
```

---

## 5. Context Management

- Execute tests feature by feature — saves results after each feature
- Checkpoint after every 3 features
- If context runs low: save results so far, checkpoint, resume with remaining features
