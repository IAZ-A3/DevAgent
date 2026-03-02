# DevAgent Sub-skill: Test Writer
**Parent:** Implementation Orchestrator  
**Scope:** One feature task at a time  
**Output:** Test file(s) for assigned task  
**Runs:** In parallel with Code Generator — reads requirements and design ONLY, never generated code

---

## Purpose

Write comprehensive test cases for a single assigned task based purely on requirements and interface contracts. Tests are written independently from the code to ensure they validate requirements, not implementation details. Tests serve as executable specifications.

---

## Required Inputs (passed by Orchestrator)

| Input | Source | Required |
|-------|--------|----------|
| Task ID | Plan.md | Yes |
| Feature ID | Plan.md | Yes |
| PRD.md | docs/PRD.md | Yes |
| Feature requirements section | PRD.md (FEAT-XXX section) | Yes |
| InterfaceContracts.md | docs/design/InterfaceContracts.md | If exists |
| DataModel.md | docs/design/DataModel.md | If exists |
| TechnologyStack.md | docs/design/TechnologyStack.md | Yes |
| ComponentDesign.md | docs/design/ComponentDesign.md | Yes |
| Global NFRs | PRD.md Section 2 | Yes |
| Coding standards file | project root | If exists |
| Output path | Orchestrator | Yes |

**Strict rule:** Do NOT read generated source code files. Tests must be derived from requirements and contracts only.

---

## 1. Test Strategy Per Requirement

For every functional requirement (FR) of the assigned feature:
- Write at least one positive test (happy path — requirement satisfied)
- Write at least one negative test (requirement boundary or failure case)
- Write edge case tests where the requirement implies boundary conditions

For every feature-scoped NFR:
- Write at least one performance/security/reliability test that validates the acceptance criterion

For every interface contract (INTF-XXX) the feature participates in:
- Write contract tests validating inputs, outputs, preconditions, and error cases

---

## 2. Test File Structure

Each test file must start with a header:
```
// Test Suite: FEAT-XXX — {Feature Name}
// Task: FEAT-XXX-TASK-YYY
// Validates: {FR IDs, NFR IDs}
// Contracts tested: {INTF IDs}
// Test framework: {from TechnologyStack.md}
```

Each individual test must:
- Have a descriptive name that states what is being tested and expected outcome
- Reference the requirement ID it validates in a comment:
```python
# Tests: FEAT-001-FR-003 — When file changes, listeners must be notified
def test_file_change_notifies_all_registered_listeners():
```
- Be independent — no test shall depend on execution order or shared mutable state
- Clean up after itself (setup/teardown)

---

## 3. Test Coverage Requirements

| Requirement Type | Minimum Tests |
|-----------------|---------------|
| Each FR (happy path) | 1 positive |
| Each FR (boundaries) | 1 negative |
| Each NFR with measurable criterion | 1 validation test |
| Each INTF contract | 1 per error case + 1 happy path |
| Each DATA entity lifecycle | 1 create, 1 read, 1 update, 1 delete (where applicable) |

---

## 4. Test Categories

Label every test with one of:
- `[UNIT]` — tests a single component in isolation (mock dependencies)
- `[CONTRACT]` — tests interface boundary between components
- `[NFR]` — tests non-functional acceptance criterion
- `[EDGE]` — tests boundary or unusual input condition

---

## 5. Clarification Protocol

If a requirement is ambiguous and cannot be tested without interpretation:
- Do not silently pick an interpretation
- Halt and produce:
```
Test Writer — Clarification Needed
Task: FEAT-XXX-TASK-YYY
Requirement: FEAT-XXX-FR-YYY
Ambiguity: {what is unclear}
Interpretation A: {implies these test cases}
Interpretation B: {implies these test cases}
Suggested: A — because {reason from PRD context}
```
- Pass to orchestrator

---

## 6. Output

- Write test file(s) to path specified by orchestrator (typically `tests/`)
- Write test report to `.claude/skills/state/implementation/FEAT-XXX-TASK-YYY-tests.md`:
```
# Test Writing Report
## Task: FEAT-XXX-TASK-YYY
## Status: COMPLETE | BLOCKED
## Test Files Written: {list}
## Total Tests Written: N
## Requirements Covered: {FR IDs}
## NFRs Covered: {NFR IDs}
## Contracts Covered: {INTF IDs}
## Uncovered Requirements: {list — should be empty}
## Notes: {observations for reviewer}
```

---

## 5. Context Management

- This sub-skill handles ONE task only — context is bounded
- If task has many requirements and context pressure builds:
  - Complete tests for current requirement group
  - Save partial output with INCOMPLETE marker
  - Checkpoint with list of remaining requirements to test
  - Report to orchestrator
