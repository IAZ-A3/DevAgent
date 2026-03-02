# DevAgent Sub-skill: Requirement Coverage Auditor
**Parent:** V&V Orchestrator  
**Scope:** Full PRD vs implementation  
**Output:** Coverage audit report per feature

---

## Purpose

Perform a systematic audit verifying that every requirement in the PRD is implemented in source code and covered by at least one test. This is a static analysis task — no test execution. It complements the System Test Runner by catching requirements that were never tested at all.

---

## Required Inputs

| Input | Source | Required |
|-------|--------|----------|
| PRD.md | docs/PRD.md | Yes |
| src/ | project source | Yes |
| tests/ | test files | Yes |
| All code generation reports | state/implementation/ | Yes |
| All test writing reports | state/implementation/ | Yes |

---

## 1. Audit Method

For each FR and NFR in the PRD:

**Step 1 — Implementation check:**
Search all source files for the requirement ID in comments.
- Found → IMPLEMENTED
- Not found → scan for functional evidence (function names, logic patterns matching requirement)
  - Evidence found → IMPLEMENTED (inferred) — note the file and line
  - No evidence → NOT_IMPLEMENTED → error

**Step 2 — Test coverage check:**
Search all test files for the requirement ID in comments.
- Found → TESTED
- Not found → scan test names and assertions for coverage
  - Evidence found → TESTED (inferred)
  - No evidence → NOT_TESTED → warning

**Step 3 — Cross-check with implementation reports:**
Compare findings against code generation reports from Implementation phase.
Flag any discrepancy between what was reported as implemented and what is found in code.

---

## 2. Coverage Classification

| Status | Meaning | Severity |
|--------|---------|---------|
| IMPLEMENTED + TESTED | Full coverage | None |
| IMPLEMENTED + NOT_TESTED | Code exists, no test | Warning |
| NOT_IMPLEMENTED + TESTED | Test exists for missing code | Error |
| NOT_IMPLEMENTED + NOT_TESTED | Completely missing | Error |
| IMPLEMENTED (inferred) | ID comment missing but code found | Warning |

---

## 3. Output

Write to `.claude/skills/state/vv/coverage-audit.md`:

```markdown
# Requirement Coverage Audit
## Date: {date}

---

## Coverage Summary
| Metric | Count |
|--------|-------|
| Total FRs | N |
| Fully covered (impl + tested) | N |
| Implemented, not tested | N |
| Not implemented | N |
| Total NFRs | N |
| Auto-validated | N |
| Pending manual | N |

---

## Coverage by Feature

### FEAT-001: {Feature Name}
| Req ID | Implemented | Tested | Status | Location |
|--------|-------------|--------|--------|---------|
| FEAT-001-FR-001 | YES | YES | FULL | src/feat1.py:42 |
| FEAT-001-FR-002 | YES (inferred) | NO | WARN | src/feat1.py:67 |
| FEAT-001-NFR-001 | YES | AUTO | FULL | NFR auto-validated |

**Feature Coverage: FULL | PARTIAL | MISSING**

---

## Errors (must resolve before release)
| Req ID | Issue | Suggested Action |
|--------|-------|-----------------|
| FEAT-002-FR-003 | NOT_IMPLEMENTED + NOT_TESTED | Implement and add test |

---

## Warnings (should resolve)
| Req ID | Issue | Suggested Action |
|--------|-------|-----------------|
| FEAT-001-FR-002 | ID comment missing in source | Add traceability comment |
```

---

## 5. Context Management

- Process one feature at a time
- Save audit results after each feature
- Checkpoint after every 3 features
- For large projects: spawn one subagent per feature (parallel coverage audit)
