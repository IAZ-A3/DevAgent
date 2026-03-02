# DevAgent Skill: Implementation — Orchestrator
**Phase:** 4 of 7  
**Role:** Entry point and coordinator for all implementation sub-skills  
**Output:** Completed source code + test cases + updated `docs/Plan.md`  
**Imports:** `../_shared/context-manager.md`, `../_shared/subagent-patterns.md`, `../_shared/artifact-schema.md`

---

## Purpose

Coordinate the full implementation phase by reading the execution waves from Plan.md, spawning the appropriate sub-skills in the correct order, enforcing wave-complete gates, and keeping Plan.md current throughout. The orchestrator itself writes no code — it manages, sequences, and validates.

---

## 1. Input Discovery

### If inputs are explicitly provided:
Use them directly.

### If inputs are NOT explicitly provided (auto-discovery):
Scan in this order:
1. `docs/Plan.md` — primary input (required, must be COMPLETED status)
2. `docs/PRD.md` — for requirement context
3. `docs/design/DesignIndex.md` — entry point for all design artifacts
4. `.claude/skills/state/artifact-registry.md` — confirm Planning and Design phases COMPLETED
5. Coding standards: scan project root for `coding-standards.md`, `style-guide.md`, `.editorconfig`, `CONTRIBUTING.md` — pass to code-generating sub-skills if found
6. `.claude/skills/state/implementation/checkpoint.md` — resume from previous session

**If Plan.md or DesignIndex.md not found:** halt and inform user. Implementation requires both Planning and Design phases to be completed.

---

## 2. Clarification Protocol

Before starting, resolve:
- Any BLOCKED tasks in Plan.md that haven't been resolved
- Any OPEN design issues in DesignIndex.md marked as blockers
- Ambiguity about which coding standards to apply if multiple files found

Ask in single grouped list with suggested answers. Mark [BLOCKING] or [OPTIONAL].

---

## 3. Orchestration Flow

```
Step 1: Load & validate all inputs
Step 2: Read execution waves from Plan.md
Step 3: For each wave (sequential):
    Step 3a: Identify all tasks in this wave
    Step 3b: For each task in wave (PARALLEL):
             → Spawn Code Generator sub-skill
             → Spawn Test Writer sub-skill (parallel with code gen)
    Step 3c: WAIT — all code gen + test writing complete for this wave
    Step 3d: For each task in wave (PARALLEL):
             → Spawn Code Reviewer sub-skill
    Step 3e: WAIT — all reviews complete
    Step 3f: Evaluate review results:
             → All PASS: advance to next wave
             → Any FAIL: spawn Code Generator to fix findings, re-review
             → Blocking unresolved: escalate to user
    Step 3g: Update Plan.md — mark wave tasks as DONE
Step 4: Spawn Integrator sub-skill (after all waves complete)
Step 5: Validate integration result
Step 6: Produce phase gate
```

---

## 4. Sub-skill Invocation

When spawning a sub-skill, always pass:
- Task ID and feature ID
- Paths to: PRD.md, relevant design documents (from DesignIndex.md), Plan.md
- Path to coding standards file (if found)
- Output file path(s)
- Specific instructions for that task

Sub-skills to invoke (see sub-skills/ folder):
- `sub-skills/code-generator.md`
- `sub-skills/test-writer.md`
- `sub-skills/code-reviewer.md`
- `sub-skills/integrator.md`

---

## 5. Wave Gate Rules

A wave is COMPLETE only when ALL of the following are true:
- [ ] All code generator sub-skills for the wave have completed successfully
- [ ] All test writer sub-skills for the wave have completed successfully
- [ ] All code reviewer sub-skills have returned PASS
- [ ] All review findings are resolved (no open FAIL items)
- [ ] Plan.md updated with DONE status for all wave tasks

If any task in the wave is BLOCKED, pause the entire wave and escalate to user before proceeding.

---

## 6. Context Management (Phase-Specific)

Imports rules from `../_shared/context-manager.md`, plus:

- Save checkpoint after each wave completes
- Save checkpoint before spawning integrator
- State folder: `.claude/skills/state/implementation/`
- Checkpoint must record: completed waves, pending waves, any open findings
- If context runs low mid-wave: complete current sub-skill invocations, checkpoint with wave state, resume in fresh session

---

## 7. Output & Phase Gate

On completion:
1. All source code written to `src/` (or project-appropriate structure)
2. All test files written to `tests/` (or project-appropriate structure)
3. `docs/Plan.md` fully updated
4. Update `.claude/skills/state/artifact-registry.md`
5. Produce phase gate:

```
# Phase Gate — Implementation
## Result: PASS | NEEDS_REVIEW
## Waves Completed: N/N
## Tasks Completed: N/N
## Code Files Written: {list}
## Test Files Written: {list}
## Integration Status: PASS | FAIL
## Open Review Findings: {count}
## Recommended Next Phase: verification
## Blockers: {list or "None"}
```

6. Inform user: Implementation complete. Suggest running **Verification & Validation** skill next.
