# DevAgent Skill: Planning
**Phase:** 2 of 7  
**Output:** `docs/Plan.md`  
**Imports:** `../_shared/context-manager.md`, `../_shared/subagent-patterns.md`, `../_shared/artifact-schema.md`

---

## Purpose

Produce a structured, living project plan (`Plan.md`) derived from the PRD. The plan breaks down each feature into prioritized, sequenced tasks with complexity scores and explicit parallel execution opportunities. The plan stays current throughout the project — other skills update it directly as work progresses.

---

## 1. Input Discovery

### If inputs are explicitly provided:
Use them directly. Accepted forms:
- Path to `docs/PRD.md`
- Prompt describing scope/constraints directly

### If inputs are NOT explicitly provided (auto-discovery):
Scan in this order:
1. `docs/PRD.md` — primary input (required)
2. `.claude/skills/state/artifact-registry.md` — confirm PRD is COMPLETED
3. `.claude/skills/state/planning/checkpoint.md` — resume from previous session

**If PRD is not found or not baselined:** halt and inform the user. The Planning skill requires a completed PRD. Suggest running the Requirements skill first.

---

## 2. Clarification Protocol

Before generating the plan, resolve any ambiguities.

### Mandatory clarification triggers:
- PRD contains OPEN blocking questions (OQ marked BLOCKING)
- Feature priorities are not clear from the PRD
- Dependencies between features are ambiguous or circular
- Scope of a feature is too vague to estimate complexity

### How to ask:
- Group all questions into a **single structured list**
- Provide a suggested answer for each
- Mark [BLOCKING] or [OPTIONAL]
- Example:
```
Before I generate the plan, I need to clarify:

1. [BLOCKING] FEAT-002 and FEAT-003 appear to have a circular dependency. 
   Should FEAT-003 be split? (Suggested: yes, extract shared component as FEAT-003a)
2. [OPTIONAL] No priority is specified for FEAT-004. 
   (Suggested: Medium, based on PRD description)
```

---

## 3. Internal Sub-Phases

```
Sub-phase A: PRD Analysis              [sequential]
Sub-phase B: Task Generation           [PARALLEL per feature]
Sub-phase C: Dependency Mapping        [sequential — orchestrator]
Sub-phase D: Complexity Scoring        [PARALLEL per feature]
Sub-phase E: Sequencing & Parallelism  [sequential — orchestrator]
Sub-phase F: Plan Assembly             [sequential]
```

### Sub-phase A — PRD Analysis
Read and internalize the full PRD. Produce an internal summary:
- List of all confirmed features with IDs and priorities
- Global NFRs that will influence task planning
- Known constraints and risks
- Any open questions that need resolution (trigger clarification protocol)

### Sub-phase B — Task Generation (Parallel per feature)
Spawn one subagent per feature. Each subagent:
- Reads its assigned feature section from the PRD
- Generates the task list for that feature (one task per logical unit of work at feature level)
- Assigns task IDs: `FEAT-XXX-TASK-YYY`
- Assigns priority: Critical / High / Medium / Low (inherited or inferred from PRD)
- Identifies any intra-feature dependencies
- Output: `.claude/skills/state/planning/feat-XXX-tasks.md`

### Sub-phase C — Dependency Mapping
Orchestrator reads all feature task files and:
- Builds a global dependency graph across all features
- Identifies inter-feature dependencies
- Detects and flags circular dependencies (escalate to user if found)
- Tags each task: `DEPENDS_ON: [TASK-IDs or None]`

### Sub-phase D — Complexity Scoring (Parallel per feature)
Spawn one subagent per feature. Each subagent:
- Scores each task using the complexity scale (see Section 4)
- Considers: number of requirements covered, dependencies, technical risk
- Output: updates `.claude/skills/state/planning/feat-XXX-tasks.md` with scores

### Sub-phase E — Sequencing & Parallelism
Orchestrator analyzes the full dependency graph and complexity scores:
- Determines execution order respecting all dependencies
- Identifies tasks that can run **in parallel** (no shared dependencies)
- Groups tasks into execution waves:
  - **Wave 1:** tasks with no dependencies (full parallel)
  - **Wave 2:** tasks depending only on Wave 1 outputs
  - etc.
- Flags any task with complexity XL as a candidate for further breakdown

### Sub-phase F — Plan Assembly
Assemble final `docs/Plan.md` using structure defined in Section 5.

---

## 4. Complexity Scoring Scale

| Score | Label | Description |
|-------|-------|-------------|
| 1 | XS | Trivial — straightforward, no unknowns, <1h equivalent |
| 2 | S | Simple — clear path, minimal risk |
| 3 | M | Medium — some complexity or unknowns |
| 5 | L | Large — significant complexity, multiple components |
| 8 | XL | Very large — should be considered for breakdown |
| 13 | XXL | Excessive — must be broken down before implementation |

**Rule:** No task shall remain at XXL in the final plan. The agent must propose a breakdown and confirm with the user.

---

## 5. Plan.md Structure

```markdown
# Project Plan
## Project: {name}
## Generated from: docs/PRD.md v{version}
## Date: {date}
## Last Updated: {date} by {skill}

---

## Plan Summary
| Metric | Value |
|--------|-------|
| Total Features | N |
| Total Tasks | N |
| Critical Tasks | N |
| Total Complexity Points | N |
| Parallel Execution Waves | N |

---

## Execution Waves

### Wave 1 — Parallel (no dependencies)
| Task ID | Feature | Task Description | Priority | Complexity | Status | Depends On |
|---------|---------|-----------------|----------|------------|--------|------------|
| FEAT-001-TASK-001 | FEAT-001 | ... | Critical | M(3) | TODO | None |

### Wave 2 — Parallel (depends on Wave 1)
| Task ID | Feature | Task Description | Priority | Complexity | Status | Depends On |
|---------|---------|-----------------|----------|------------|--------|------------|
| FEAT-002-TASK-001 | FEAT-002 | ... | High | L(5) | TODO | FEAT-001-TASK-001 |

### Wave N — ...

---

## Feature Progress

### FEAT-001: {Feature Name}
**Priority:** Critical | High | Medium | Low  
**Overall Status:** TODO | IN_PROGRESS | DONE | BLOCKED  
**Complexity Total:** N points  

| Task ID | Description | Priority | Complexity | Status | Notes |
|---------|-------------|----------|------------|--------|-------|
| FEAT-001-TASK-001 | ... | Critical | M(3) | TODO | |

---

## Blocked Items
| Task ID | Reason | Blocker | Reported By |
|---------|--------|---------|-------------|
| — | — | — | — |

---

## Change Log
| Date | Changed By | Change Description |
|------|------------|-------------------|
| {date} | Planning Skill | Initial plan generated from PRD v1.0 |
```

---

## 6. Plan Update Protocol (for other skills)

When any skill updates Plan.md (e.g. Implementation marks a task DONE):

1. Read current `docs/Plan.md`
2. Update ONLY the relevant task row(s): change Status field
3. Update `Last Updated` header
4. Append an entry to the Change Log section
5. Recalculate Feature Progress `Overall Status`:
   - All tasks TODO → TODO
   - Any task IN_PROGRESS → IN_PROGRESS
   - All tasks DONE → DONE
   - Any task BLOCKED → BLOCKED
6. Write the updated file back
7. Do NOT restructure or reformat the rest of the plan

**Valid status values:** `TODO` | `IN_PROGRESS` | `DONE` | `BLOCKED` | `SKIPPED`

---

## 7. Context Management (Phase-Specific)

Imports rules from `../_shared/context-manager.md`, plus:

- After Sub-phase A (PRD analyzed): save checkpoint
- After Sub-phase C (dependency map built): save checkpoint
- After Sub-phase E (waves defined): save checkpoint before assembly
- State folder: `.claude/skills/state/planning/`
- If context runs low mid Sub-phase B: complete current feature subagents, checkpoint, resume in fresh session loading checkpoint and remaining feature list

---

## 8. Output & Phase Gate

On completion:
1. Write final `docs/Plan.md`
2. Update `.claude/skills/state/artifact-registry.md`
3. Produce phase gate summary:

```
# Phase Gate — Planning
## Result: PASS | NEEDS_REVIEW
## Artifacts: docs/Plan.md
## Total Tasks: N
## Total Complexity Points: N
## Execution Waves: N
## Open Issues: {list or "None"}
## Recommended Next Phase: design
## Blockers: {list or "None"}
```

4. Inform user: Plan is ready for review. Suggest running the **Design & Architecture** skill next.

---

## 9. Quality Checklist (Self-Assessment before delivery)

- [ ] Every feature from PRD has at least one task
- [ ] Every task has a unique ID, priority, and complexity score
- [ ] No task remains at XXL complexity
- [ ] All inter-feature dependencies are mapped
- [ ] Parallel waves are correctly identified (no false parallelism)
- [ ] No circular dependencies exist
- [ ] Plan.md Change Log initialized
- [ ] Plan summary metrics are accurate
- [ ] All BLOCKING open questions resolved before plan generation
