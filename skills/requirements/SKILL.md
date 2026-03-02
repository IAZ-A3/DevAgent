# DevAgent Skill: Requirements
**Phase:** 1 of 7  
**Output:** `docs/PRD.md`, `PROJECT.md`  
**Imports:** `../_shared/context-manager.md`, `../_shared/subagent-patterns.md`, `../_shared/artifact-schema.md`

---

## Purpose

Produce a complete, unambiguous, traceable Product Requirements Document (PRD) that will serve as the single source of truth for all subsequent development phases. Quality here directly determines quality across the entire project.

---

## 1. Input Discovery

### If inputs are explicitly provided:
Use them directly. Accepted forms:
- Project description in the prompt
- Existing notes, brief, or idea file
- Partial or draft PRD
- Existing codebase (reverse-engineer requirements from code)
- Any combination of the above

### If inputs are NOT explicitly provided (auto-discovery):
Scan the project root in this order:
1. `.claude/skills/state/checkpoint.md` — resume from previous session (highest priority)
2. `docs/PRD.md` or `docs/requirements*.md` — existing PRD draft
3. `README.md` — project description
4. `BRIEF.md`, `IDEA.md`, `NOTES.md` — informal project notes
5. Source code — see detection procedure below

If nothing is found: ask the user for a project description before proceeding.

### Source code detection (do not assume `src/`)

If source code is detected but no PRD exists, this is an existing project without a paper trail.
**Do not attempt inline reverse-engineering here.** Instead:

> Invoke the **Onboarding skill** (`.claude/skills/onboarding/SKILL.md`) which handles
> language detection, code analysis, user gap interview, and full paper trail reconstruction.
> Requirements skill resumes after onboarding completes with a confirmed PRD.

To detect whether source code exists, invoke the project-detector sub-skill:
`.claude/skills/_shared/project-detector.md`

Detection output will confirm: language, framework, source locations.
If source code is found with no PRD → hand off to Onboarding skill immediately.

---

## 2. Clarification Protocol

**Before writing any requirements**, the skill MUST resolve ambiguities.

### Mandatory clarification triggers:
- Project purpose or target user is unclear
- Scope boundaries are undefined (what is IN vs OUT of scope)
- A requirement could be interpreted in more than one way
- Performance, security, or reliability targets are not specified
- A proposed feature conflicts with another

### How to ask:
- Group all clarification questions into a **single structured list** — never ask one at a time across multiple turns.
- Number each question.
- For each question, provide a suggested answer based on best analysis so the user can confirm or correct rather than answer from scratch.
- Mark questions as [BLOCKING] if the PRD cannot proceed without the answer, or [OPTIONAL] if a reasonable default can be assumed.

### Example format:
```
Before I proceed, I need to clarify a few points:

1. [BLOCKING] What is the primary target platform? (Suggested: macOS 13+)
2. [BLOCKING] Should offline mode be supported? (Suggested: No, requires internet)
3. [OPTIONAL] What is the expected maximum response time for UI interactions? (Suggested: <200ms)

Please confirm, correct, or skip optional items.
```

---

## 3. Internal Sub-Phases

The skill decomposes internally into these sub-phases, using parallel subagents where indicated:

```
Sub-phase A: Project Analysis          [sequential — needs user input]
Sub-phase B: Feature Identification    [sequential — user validates]
Sub-phase C: Requirements Elaboration  [PARALLEL per feature]
Sub-phase D: NFR Definition            [PARALLEL: global NFRs + per-feature NFRs]
Sub-phase E: Quality Review            [sequential — orchestrator merges + validates]
Sub-phase F: PRD Assembly              [sequential — final document]
Sub-phase G: PROJECT.md Generation    [sequential — after PRD confirmed]
```

### Sub-phase A — Project Analysis
Analyze all available inputs. Produce an internal summary:
- Project name and purpose
- Target users
- Core problem being solved
- Known constraints
- Identified ambiguities → trigger clarification protocol if needed

### Sub-phase B — Feature Identification
1. List features explicitly mentioned by the user.
2. Analyze project description and propose **additional features** that are logically implied or would significantly improve completeness.
3. Present the combined feature list to the user:
   - Clearly distinguish user-defined vs agent-proposed features
   - Ask user to confirm, reject, or modify the proposed additions
4. Assign `FEAT-XXX` IDs to all confirmed features.

**Do not proceed to Sub-phase C until feature list is confirmed by user.**

### Sub-phase C — Requirements Elaboration (Parallel per feature)
Spawn one subagent per feature. Each subagent:
- Writes functional requirements for its assigned feature
- Applies EARS notation (see Section 4) for precision
- Assigns scoped IDs: `FEAT-XXX-FR-YYY`
- Flags any ambiguity found and adds to open questions list
- Writes output to: `skills/state/requirements/feat-XXX-functional.md`

### Sub-phase D — NFR Definition (Parallel)
Run two subagents simultaneously:

**Subagent D1 — Global NFRs:**
Define NFRs that apply across the entire system. Categories to cover:
- Performance (`NFR-001`)
- Security (`NFR-002`)
- Reliability / Availability (`NFR-003`)
- Maintainability (`NFR-004`)
- Portability / Compatibility (`NFR-005`)
- Usability (`NFR-006`)
- Scalability (`NFR-007`)
Output: `skills/state/requirements/global-nfr.md`

**Subagent D2 — Feature-scoped NFRs:**
For each feature, identify if it has specific NFRs beyond the global ones.
Assign IDs: `FEAT-XXX-NFR-YYY`
Output: `skills/state/requirements/feat-scoped-nfr.md`

### Sub-phase E — Quality Review
Orchestrator merges all sub-phase outputs and applies quality validation:

For every requirement, verify:
- [ ] **Unambiguous** — only one possible interpretation
- [ ] **Verifiable** — can be tested or measured
- [ ] **Traceable** — has a unique ID
- [ ] **Complete** — no missing information
- [ ] **Consistent** — does not conflict with other requirements
- [ ] **Feasible** — realistic to implement
- [ ] **Necessary** — serves a real project need

Flag any requirement that fails a check. Resolve or escalate to user before proceeding.

### Sub-phase F — PRD Assembly
Assemble the final `docs/PRD.md` using the structure defined in Section 5.


### Sub-phase G — PROJECT.md Generation

After PRD.md is assembled and before the phase gate closes:

1. Detect project type from PRD.md (platform, technology stack, distribution) to select the correct template:
   - macOS app detected → copy `.claude/PROJECT-macos-template.md`
   - Web project detected → copy `.claude/PROJECT-web-template.md`
   - Neither → copy `.claude/PROJECT-base-template.md` 

2. Fill in every field using answers already collected during the Requirements interview:

   | PROJECT.md Field | Source |
   |-----------------|--------|
   | Name | Sub-phase A — project name |
   | Type | Sub-phase A — platform/type |
   | One-liner | Sub-phase A — project purpose |
   | Target platform | Sub-phase A — constraints |
   | Target users | Sub-phase A — target users |
   | Distribution | Sub-phase A — deployment/distribution |
   | Design references | Sub-phase A — any references provided |
   | Git conventions | Clarification protocol answers |
   | Quality gates | NFR definitions from Sub-phase D |
   | Claude Code preferences | Use safe defaults (all "yes") |
   | Out of scope | PRD.md Section 1.3 — Non-Goals |
   | Notes | PRD.md Section 1.6 — Assumptions + Constraints |

   For macOS template, also fill: Xcode project fields left blank (user fills post-setup),
   Apple Developer Account fields left blank, App Capabilities from NFR/API questions.

   For web template, also fill: subtype, stack, accessibility standard, performance budget
   from NFR definitions.

3. Leave fields blank (with comment) only if the information was genuinely not discussed
   during Requirements. Never invent values.

4. Present the filled PROJECT.md to the user:
   ```
   I've generated PROJECT.md from the Requirements interview.
   Please review and confirm — or edit any fields before we proceed.
   Fields marked with comments need your input before the next session.
   ```

5. Wait for user confirmation. Apply any corrections the user requests.

6. Write confirmed PROJECT.md to project root.

**PROJECT.md is a phase gate artifact — the gate does not PASS until the user confirms it.**

---
---

## 4. Requirement Writing Rules (EARS-based)

Use EARS (Easy Approach to Requirements Syntax) patterns for all functional requirements:

| Pattern | Template | Use when |
|---------|----------|----------|
| Ubiquitous | The system shall `<action>` | Always-true requirement |
| Event-driven | When `<trigger>`, the system shall `<action>` | Triggered behavior |
| State-driven | While `<state>`, the system shall `<action>` | Ongoing condition |
| Conditional | If `<condition>`, then the system shall `<action>` | Optional feature |
| Optional | Where `<feature included>`, the system shall `<action>` | Optional feature |

**Rules:**
- Use "shall" for mandatory requirements, "should" for desirable, "may" for optional.
- One requirement = one testable statement. No "and" combining two requirements in one.
- Avoid vague terms: never use "fast", "user-friendly", "robust", "easy", "simple" without measurable criteria.
- Every NFR must include a measurable acceptance criterion (e.g., "response time < 200ms at P95").

---

## 5. PRD Structure

```markdown
# Product Requirements Document
## Project: {name}
## Version: 1.0
## Date: {date}
## Status: DRAFT | REVIEWED | BASELINED

---

## 1. Project Overview
### 1.1 Purpose
### 1.2 Goals
### 1.3 Non-Goals (explicit out-of-scope)
### 1.4 Target Users
### 1.5 Constraints
### 1.6 Assumptions

---

## 2. Global Non-Functional Requirements
| ID | Category | Requirement | Acceptance Criterion |
|----|----------|-------------|----------------------|
| NFR-001 | Performance | ... | ... |

---

## 3. Features & Requirements

### FEAT-001: {Feature Name}
**Description:** ...
**Priority:** Critical | High | Medium | Low
**Dependencies:** {FEAT-XXX or None}

#### Functional Requirements
| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FEAT-001-FR-001 | ... | shall | ... |

#### Feature-Scoped Non-Functional Requirements
| ID | Category | Requirement | Acceptance Criterion |
|----|----------|-------------|----------------------|
| FEAT-001-NFR-001 | ... | ... | ... |

---

## 4. Risks
| ID | Description | Impact | Likelihood | Mitigation |
|----|-------------|--------|------------|------------|
| RISK-001 | ... | High | Medium | ... |

---

## 5. Open Questions
| ID | Question | Owner | Status |
|----|----------|-------|--------|
| OQ-001 | ... | User | OPEN |

---

## 6. Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | {date} | AI Agent | Initial draft |
```

---

## 6. Context Management (Phase-Specific)

Imports rules from `../_shared/context-manager.md`, plus:

- After Sub-phase B (feature list confirmed): save checkpoint.
- After Sub-phase C completes: save checkpoint with all feature requirement files listed.
- After Sub-phase E (quality review): save checkpoint before final assembly.
- State folder: `.claude/skills/state/requirements/`
- If context is running low mid Sub-phase C: complete current feature subagents, checkpoint, resume in fresh session.

---

## 7. Output & Phase Gate

On completion:
1. Write final `docs/PRD.md`
2. Write confirmed `PROJECT.md` to project root
3. Update `.claude/skills/state/artifact-registry.md`
4. Produce phase gate summary:

```
# Phase Gate — Requirements
## Result: PASS | NEEDS_REVIEW
## Artifacts: docs/PRD.md, PROJECT.md
## Open Issues: {count} open questions remaining
## Recommended Next Phase: planning
## Blockers: {list or "None"}
```

5. Inform user: PRD and PROJECT.md are ready. Suggest running the **Planning** skill next.

---

## 8. Quality Checklist (Self-Assessment before delivery)

Before delivering the PRD, the agent must confirm:
- [ ] All features have confirmed IDs
- [ ] Every functional requirement uses EARS notation
- [ ] Every NFR has a measurable acceptance criterion
- [ ] No vague language remains (fast, simple, robust, etc.)
- [ ] No conflicting requirements exist
- [ ] All BLOCKING open questions are resolved
- [ ] Traceability IDs are consistent and unique
- [ ] PRD compiles cleanly as a readable Markdown document
- [ ] PROJECT.md generated, all available fields filled, user confirmed