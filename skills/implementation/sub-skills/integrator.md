# DevAgent Sub-skill: Integrator
**Parent:** Implementation Orchestrator  
**Scope:** Full codebase — runs after ALL waves complete  
**Output:** Integration report + glue code (if needed)

---

## Purpose

Verify that all independently developed components work together correctly according to the system architecture and interface contracts. Write minimal glue code where components need adapters, bridges, or wiring. The integrator's primary reference is the architecture and interface contracts — not the individual component implementations.

---

## Required Inputs (passed by Orchestrator)

| Input | Source | Required |
|-------|--------|----------|
| All generated source files | src/ | Yes |
| All generated test files | tests/ | Yes |
| SystemArchitecture.md | docs/design/SystemArchitecture.md | Yes |
| InterfaceContracts.md | docs/design/InterfaceContracts.md | Yes |
| ComponentDesign.md | docs/design/ComponentDesign.md | Yes |
| DataModel.md | docs/design/DataModel.md | If exists |
| TechnologyStack.md | docs/design/TechnologyStack.md | Yes |
| All code generation reports | state/implementation/ | Yes |
| All review reports | state/implementation/ | Yes |
| Coding standards file | project root | If exists |

---

## 1. Integration Analysis Sub-Phases

```
Step 1: Interface Verification      [PARALLEL per interface]
Step 2: Data Flow Verification      [sequential]
Step 3: Gap Analysis                [sequential]
Step 4: Glue Code Generation        [sequential — only if gaps found]
Step 5: Integration Test Writing    [sequential]
Step 6: Integration Report          [sequential]
```

### Step 1 — Interface Verification (Parallel per INTF)
Spawn one subagent per interface contract defined in InterfaceContracts.md. Each subagent:
- Reads the INTF-XXX contract definition
- Reads the producer component's code (the component that implements the interface)
- Reads the consumer component's code (the component that calls the interface)
- Verifies: method signatures match, data types match, error cases handled on both sides
- Output: `.claude/skills/state/implementation/intf-XXX-verify.md` with PASS | FAIL

### Step 2 — Data Flow Verification
Following the component interaction diagram from SystemArchitecture.md:
- Trace each data flow end-to-end through the actual code
- Verify data is transformed correctly at each hop
- Verify DATA-XXX entity structures are consistent across component boundaries
- Flag any data loss, corruption risk, or type mismatch

### Step 3 — Gap Analysis
Identify integration gaps requiring glue code:
- **Adapter needed:** component A produces type X, component B expects type Y
- **Bridge needed:** components use different protocols or calling conventions
- **Wiring needed:** components are implemented but not connected in the entry point
- **Configuration needed:** component requires setup/initialization not present

For each gap, classify:
- Can be resolved by glue code (proceed)
- Requires change to component design (escalate to user — this is a design issue)

### Step 4 — Glue Code Generation (only if gaps found)
For each identified gap:
- Write the minimum code needed to bridge the gap
- File header must include:
```
// Glue Code: {gap description}
// Bridges: COMP-XXX → COMP-YYY
// Resolves: Integration gap found by Integrator sub-skill
// Implements: {INTF-XXX or architecture requirement}
```
- Glue code must not contain business logic — only adaptation/wiring
- If glue code requires a new dependency not in TechnologyStack.md: halt and report

### Step 5 — Integration Test Writing
Write integration tests that exercise component interactions end-to-end:
- At least one integration test per component interaction defined in SystemArchitecture.md
- Tests must use real component instances (not mocks) where practical
- Label all integration tests: `[INTEGRATION]`
- Reference architecture interaction: `# Tests: COMP-001 → COMP-002 via INTF-001`
- Write to `tests/integration/`

### Step 6 — Integration Report
Produce final integration report.

---

## 2. Integration Report Format

Output to `.claude/skills/state/implementation/integration-report.md`:

```markdown
# Integration Report
## Date: {date}
## Status: PASS | FAIL | PASS_WITH_GLUE

---

## Interface Verification Summary
| Interface | Producer | Consumer | Status | Issues |
|-----------|----------|----------|--------|--------|
| INTF-001 | COMP-001 | COMP-002 | PASS | None |

---

## Data Flow Verification
| Flow | Status | Issues |
|------|--------|--------|
| COMP-001 → COMP-002 → COMP-003 | PASS | None |

---

## Gaps Found & Resolved
| Gap ID | Description | Resolution | Glue File |
|--------|-------------|-----------|-----------|
| GAP-001 | Type mismatch at INTF-002 | Adapter written | src/adapters/intf002-adapter.py |

---

## Escalated Issues (require user input)
| Issue | Component | Reason | Suggested Action |
|-------|-----------|--------|-----------------|

---

## Integration Tests Written
| Test File | Tests | Components Covered |
|-----------|-------|-------------------|

---

## Final Verdict
PASS: All components integrate correctly.
PASS_WITH_GLUE: Integration complete with N glue files written.
FAIL: N unresolved issues — see escalated issues above.
```

---

## 3. Context Management

- Integration is the heaviest sub-skill — many files in scope simultaneously
- Process one interface at a time in Step 1 (parallel subagents help here)
- In Step 2, trace one data flow at a time and save findings before moving to next
- Checkpoint after Step 2 and after Step 4
- If context pressure mid-Step 1: complete current interface verification, checkpoint remaining interfaces, resume in fresh session
