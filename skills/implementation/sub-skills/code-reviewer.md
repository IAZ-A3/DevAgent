# DevAgent Sub-skill: Code Reviewer
**Parent:** Implementation Orchestrator  
**Scope:** One feature task at a time  
**Output:** Review report with PASS | FAIL verdict  
**Runs:** After Code Generator AND Test Writer complete for the wave — blocks wave advancement

---

## Purpose

Review generated code and tests against requirements, design, and coding standards. The reviewer is the quality gate — no wave advances and no integration happens until all reviews pass. The reviewer does not fix code — it reports findings for the Code Generator to resolve.

---

## Required Inputs (passed by Orchestrator)

| Input | Source | Required |
|-------|--------|----------|
| Task ID | Plan.md | Yes |
| Generated source code file(s) | src/ | Yes |
| Generated test file(s) | tests/ | Yes |
| Code generation report | state/implementation/ | Yes |
| Test writing report | state/implementation/ | Yes |
| PRD.md feature section | docs/PRD.md | Yes |
| ComponentDesign.md | docs/design/ComponentDesign.md | Yes |
| InterfaceContracts.md | docs/design/InterfaceContracts.md | If exists |
| DataModel.md | docs/design/DataModel.md | If exists |
| SystemArchitecture.md | docs/design/SystemArchitecture.md | Yes |
| TechnologyStack.md | docs/design/TechnologyStack.md | Yes |
| Coding standards file | project root | If exists |

---

## 1. Review Dimensions

The reviewer checks all of the following dimensions. Each finding must be classified by severity.

### Dimension 1 — Requirements Compliance
- Every FR for this feature has corresponding implementation
- Every NFR acceptance criterion is addressed in code or tests
- No requirement is partially implemented without explicit note
- Inline requirement ID comments present at implementation points

### Dimension 2 — Design Compliance
- Code structure matches ComponentDesign.md (COMP-XXX)
- All public interfaces exactly match InterfaceContracts.md (INTF-XXX)
- Data structures match DataModel.md (DATA-XXX)
- Component boundaries respected — no direct access across undefined interfaces
- Interaction patterns match SystemArchitecture.md
- Technology used matches TechnologyStack.md exactly

### Dimension 3 — Code Quality
- Single responsibility per function/class/module
- No hardcoded values (use constants/config)
- No dead code or commented-out blocks
- Adequate error handling per ErrorHandling.md (if exists)
- Security rules applied per SecurityDesign.md (if exists)
- All public interfaces documented
- No obvious performance anti-patterns

### Dimension 4 — Test Quality
- Every FR has at least one positive and one negative test
- Tests are independent (no order dependency)
- Tests reference requirement IDs in comments
- Test names clearly describe what is tested and expected outcome
- No NFR test criterion left uncovered
- Contract tests present for all INTF-XXX the feature participates in

### Dimension 5 — Coding Standards
- All rules from coding standards file applied (if provided)
- Consistent naming conventions
- File structure matches project conventions

---

## 2. Finding Severity Classification

| Severity | Definition | Effect on Wave Gate |
|----------|-----------|-------------------|
| CRITICAL | Requirement not implemented, interface broken, security violation | Blocks wave — must fix |
| HIGH | Design not followed, missing test coverage for FR | Blocks wave — must fix |
| MEDIUM | Code quality issue, suboptimal pattern | Blocks wave — must fix |
| LOW | Style inconsistency, minor documentation gap | Does not block — log for future |
| INFO | Observation or suggestion | Does not block |

**Wave gate rule:** Any CRITICAL, HIGH, or MEDIUM finding = FAIL verdict. LOW and INFO findings = PASS with notes.

---

## 3. Review Report Format

Output to `.claude/skills/state/implementation/FEAT-XXX-TASK-YYY-review.md`:

```markdown
# Code Review Report
## Task: FEAT-XXX-TASK-YYY
## Reviewer: Code Reviewer Sub-skill
## Date: {date}
## Verdict: PASS | FAIL

---

## Summary
| Dimension | Status | Findings |
|-----------|--------|---------|
| Requirements Compliance | PASS/FAIL | N findings |
| Design Compliance | PASS/FAIL | N findings |
| Code Quality | PASS/FAIL | N findings |
| Test Quality | PASS/FAIL | N findings |
| Coding Standards | PASS/FAIL | N findings |

---

## Findings

### FINDING-001
**Severity:** CRITICAL | HIGH | MEDIUM | LOW | INFO  
**Dimension:** {dimension name}  
**Location:** {file:line or function name}  
**Issue:** {what is wrong}  
**Requirement/Design ref:** {ID}  
**Required fix:** {specific action needed}  

---

## Requirements Coverage Matrix
| FR/NFR ID | Implemented | Tested | Notes |
|-----------|-------------|--------|-------|
| FEAT-XXX-FR-001 | YES/NO | YES/NO | |

---

## LOW/INFO Notes (non-blocking)
{list}
```

---

## 4. Re-review Protocol

When Code Generator returns with fixes:
- Re-review ONLY the findings that were flagged — do not re-review passing dimensions
- Mark each finding as RESOLVED or STILL OPEN
- Issue new verdict based on remaining open findings

---

## 5. Context Management

- This sub-skill handles ONE task review — context is bounded
- For XL complexity tasks with many files: review one file at a time, accumulate findings, produce single unified report
- Checkpoint after each dimension is reviewed if context pressure builds
