# DevAgent Sub-skill: Code Generator
**Parent:** Implementation Orchestrator  
**Scope:** One feature task at a time  
**Output:** Source code file(s) for assigned task

---

## Purpose

Generate production-quality source code for a single assigned task, fully aligned with the design architecture, requirements, and project coding standards. This sub-skill has no awareness of other features being worked in parallel — it operates in isolation on its assigned task only.

---

## Required Inputs (passed by Orchestrator)

| Input | Source | Required |
|-------|--------|----------|
| Task ID | Plan.md | Yes |
| Feature ID | Plan.md | Yes |
| PRD.md | docs/PRD.md | Yes |
| Feature requirements section | PRD.md (FEAT-XXX section) | Yes |
| ComponentDesign.md | docs/design/ComponentDesign.md | Yes |
| DataModel.md | docs/design/DataModel.md | If exists |
| TechnologyStack.md | docs/design/TechnologyStack.md | Yes |
| InterfaceContracts.md | docs/design/InterfaceContracts.md | If exists |
| SystemArchitecture.md | docs/design/SystemArchitecture.md | Yes |
| Coding standards file | project root | If exists |
| Output path | Orchestrator | Yes |

---

## 1. Pre-Generation Checklist

Before writing any code:
- [ ] Read and internalize the feature's functional requirements (FR IDs)
- [ ] Read the assigned component(s) from ComponentDesign.md (COMP-XXX)
- [ ] Read relevant data entities from DataModel.md (DATA-XXX)
- [ ] Read relevant interface contracts (INTF-XXX)
- [ ] Read TechnologyStack.md — use only approved technologies
- [ ] Read SystemArchitecture.md — respect component boundaries and interaction patterns
- [ ] Read coding standards file if provided — apply all rules
- [ ] Identify all dependencies this code will have on other components

If any required input is missing or ambiguous: halt and report to orchestrator with specific question. Do not guess.

---

## 2. Code Generation Rules

### Structure
- Each generated file must start with a header comment block:
```
// Feature: FEAT-XXX — {Feature Name}
// Task: FEAT-XXX-TASK-YYY
// Implements: {FR IDs, NFR IDs}
// Component: COMP-XXX
// Design ref: ComponentDesign.md
```

### Quality Rules
- One responsibility per function/class/module
- No hardcoded values — use constants or configuration
- All public interfaces must match INTF-XXX contracts exactly
- All data structures must match DATA-XXX definitions exactly
- Error handling must follow ErrorHandling.md patterns (if exists)
- Security rules from SecurityDesign.md must be applied (if exists)
- No dead code, commented-out blocks, or TODO stubs in output
- Every function must have a descriptive docstring/comment

### Traceability
- Inline comments must reference requirement IDs at the point of implementation:
```python
# FEAT-001-FR-003: When file changes, notify all registered listeners
def notify_listeners(self, event: FileEvent) -> None:
```

### Technology Compliance
- Use only languages, frameworks, and libraries listed in TechnologyStack.md
- Use the exact versions specified
- If a required library is missing from TechnologyStack.md: halt and report to orchestrator — do not introduce new dependencies unilaterally

---

## 3. Clarification Protocol

If ambiguity is found during code generation:
- Do not guess or make assumptions silently
- Halt and produce a structured clarification request:
```
Code Generator — Clarification Needed
Task: FEAT-XXX-TASK-YYY
Issue: {specific ambiguity}
Options:
  A) {option with implication}
  B) {option with implication}
Suggested: A — because {reason}
```
- Pass this to orchestrator, which escalates to user

---

## 4. Output

- Write generated code to the path specified by orchestrator
- Write a brief generation report to `.claude/skills/state/implementation/FEAT-XXX-TASK-YYY-codegen.md`:
```
# Code Generation Report
## Task: FEAT-XXX-TASK-YYY
## Status: COMPLETE | BLOCKED
## Files Written: {list with line counts}
## Requirements Implemented: {FR IDs}
## Design Elements Used: {COMP, INTF, DATA IDs}
## Dependencies Introduced: {list}
## Notes: {any relevant observations for reviewer}
```

---

## 5. Context Management

- This sub-skill handles ONE task only — context load is bounded
- If the task is XL complexity and context pressure builds mid-generation:
  - Complete the current function/module
  - Save partial output with clear INCOMPLETE marker
  - Write checkpoint noting exact resume point
  - Report to orchestrator
