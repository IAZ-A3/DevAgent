---
name: implementation
description: Implements features from an approved plan.md. Invoked by /deva:implement [task-ID] or when the user instructs the agent to implement a P-prefix task that exists in plan.md. Also handles enhancements routed from the Maintenance skill for P-prefix items. Writes artifacts to .claude/skills/state/implementation/. Do NOT use for bug fixes (use /deva:fix), new features not yet in plan.md (use /deva:feature), V&V (use /deva:verify), or release (use /deva:release).
---

# Implementation Skill — Orchestrator
**Phase:** 4 of 7
**Role:** Entry point and coordinator for all implementation sub-skills
**Output:** Completed source code + test cases + updated `docs/Plan.md`
**Imports:** `../_shared/context-manager.md`, `../_shared/subagent-patterns.md`, `../_shared/artifact-schema.md`

---

## Purpose

Coordinate the full implementation phase by reading the execution waves from Plan.md, spawning the appropriate sub-skills in the correct order, enforcing wave-complete gates, and keeping Plan.md current throughout. The orchestrator itself writes no code — it manages, sequences, and validates.

---

## Section 1 — Pre-Flight (MANDATORY)

Before writing any code:

1. **Identify the task:** Confirm the task ID (P1-xxx, P2-xxx, etc.) exists in `docs/Plan.md` and is `TODO`
2. **Read the PRD:** Open `docs/PRD.md` — read the feature requirement and any referenced NFRs
3. **Check NFR-008** if the task adds any content to the collapsed pill:
   - Pixel contribution declared in `NotchCoordinator.bindContentSources()`
   - `Defaults.Key<Bool>` toggle exists
   - Settings → Notch Display toggle wired
   - View content gated on that key
4. **Read design docs:** If plan.md notes reference a design doc, read it before coding
5. **Load prior checkpoint:** Read `.claude/skills/state/implementation/checkpoint.md` if resuming
6. **Confirm planning and design complete:** Scan `.claude/skills/state/artifact-registry.md` — both phases must be COMPLETED

If any pre-flight item is missing (no plan.md entry, no PRD section, NFR-008 gap), **stop and report** before writing code.

---

## Section 2 — Input Discovery

### If inputs are NOT explicitly provided (auto-discovery):
Scan in this order:
1. `docs/Plan.md` — primary input (required, must be COMPLETED status)
2. `docs/PRD.md` — for requirement context
3. `docs/design/DesignIndex.md` — entry point for all design artifacts
4. `.claude/skills/state/artifact-registry.md` — confirm Planning and Design phases COMPLETED
5. Coding standards: scan project root for `coding-standards.md`, `style-guide.md`, `.editorconfig`, `CONTRIBUTING.md`
6. `.claude/skills/state/implementation/checkpoint.md` — resume from previous session

**If Plan.md or DesignIndex.md not found:** halt and inform user. Implementation requires both Planning and Design phases to be completed.

---

## Section 3 — Orchestration Flow

```
Step 1: Load & validate all inputs (pre-flight)
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
             → All PASS: advance to Step 3g
             → Any FAIL: spawn Code Generator to fix findings, re-review
             → Blocking unresolved: escalate to user
    Step 3g: Update Plan.md — mark wave tasks as DONE

╔══════════════════════════════════════════════════════════╗
║  CHECKPOINT — MANDATORY AFTER EACH WAVE COMPLETES       ║
║  File: .claude/skills/state/implementation/checkpoint.md ║
║  Write BEFORE starting the next wave                     ║
║  Do not batch waves: one checkpoint per completed wave   ║
║  Template: Section 6                                     ║
╚══════════════════════════════════════════════════════════╝

Step 4: Spawn Integrator sub-skill (after all waves complete)
Step 5: Validate integration result
Step 6: Produce phase gate
```

**Do not start the next wave without writing the checkpoint first.**

---

## Section 4 — Sub-skill Invocation

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

## Section 5 — Context Threshold Rule

**After approximately every 40 tool calls** (count tool-use blocks visible in your context):
1. Write a checkpoint immediately (even mid-wave — note partial state)
2. State: "Context threshold reached — checkpoint written. Resume with `/deva:resume`."
3. Stop.

This rule overrides all other rules.

---

## Section 6 — Checkpoint Template

```markdown
# Implementation Checkpoint
Updated: [ISO timestamp]

## Completed Waves
- Wave [N]: [task list] — DONE

## Completed Tasks
- [P-xxx] [task name] — DONE
  - Files created: [list]
  - Files modified: [list]
  - NFR-008 compliant: [yes / no / N/A — reason]
  - Test stubs: [yes / no]
  - Notes: [any follow-on items or known gaps]

## In-Progress Wave/Task (if interrupted)
- Wave [N] / [P-xxx] [task name] — PARTIAL
  - Completed sub-steps: [list]
  - Remaining sub-steps: [list]
  - Files created so far: [list]

## Not Started
- Wave [N]: [task list]
- [P-xxx] [task name]

## Resume Instructions
1. Read this checkpoint
2. Read docs/Plan.md for remaining waves/tasks
3. Continue with the In-Progress wave/task (if any), then Not Started
4. Write a new checkpoint after each wave completes
```

---

## Section 7 — Wave Gate Rules

A wave is COMPLETE only when ALL of the following are true:
- [ ] All code generator sub-skills for the wave have completed successfully
- [ ] All test writer sub-skills for the wave have completed successfully
- [ ] All code reviewer sub-skills have returned PASS
- [ ] All review findings are resolved (no open FAIL items)
- [ ] Plan.md updated with DONE status for all wave tasks
- [ ] Checkpoint written for this wave

If any task in the wave is BLOCKED, pause the entire wave and escalate to user before proceeding.

---

## Section 8 — Phase Gate

On completion:
1. All source code written to project-appropriate structure
2. All test files written to project-appropriate structure
3. `docs/Plan.md` fully updated
4. Update `.claude/skills/state/artifact-registry.md`
5. Produce phase gate:

```
Implementation gate: [task list] → [next phase]

Gate result: PASS | PASS_WITH_NOTES | BLOCKED

Tasks completed: [list with IDs]
Tasks remaining in plan.md: [list, or NONE]
NFR-008 compliance: [verified / N/A per task]
Checkpoint written: .claude/skills/state/implementation/checkpoint.md

Artifacts produced:
  [file] — [what it does]

Next action:
  - If more tasks remain: /deva:implement [next-task-ID]
  - If phase complete and V&V needed: /deva:verify
  - If adding a new feature not in plan: /deva:feature [description]
```

**Do not chain to the next phase without user approval.**

---

## Section 9 — What This Skill Does NOT Handle

| Situation | Correct action |
|-----------|---------------|
| Bug fix / regression | `/deva:fix [BUG-ID]` |
| New feature not in plan.md | `/deva:feature [description]` |
| V&V / testing | `/deva:verify` |
| Release | `/deva:release` |
| Design changes needed | Stop, invoke `/deva:design` first |
