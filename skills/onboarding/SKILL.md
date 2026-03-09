---
name: onboarding
description: Reverse-engineers an existing codebase that has no DevAgent paper trail. Run via /deva:onboard. Produces PRD.md, Plan.md, and design docs. At the end, emits an explicit skill handoff command — do not leave re-entry decision as prose. Also creates change-request stubs for all P-prefix plan.md items so they have traceability records.
---

# DevAgent Skill: Project Onboarding
**Phase:** 0 — Pre-phase (runs before normal phase sequence)
**Output:** `docs/PRD.md`, `PROJECT.md`, `docs/Plan.md`, `docs/design/DesignIndex.md`, `docs/change-requests/`, re-entry decision
**Imports:** `../_shared/context-manager.md`, `../_shared/artifact-schema.md`
**Sub-skills:**
- `sub-skills/code-archaeologist.md` — reverse-engineer features from source code
- `sub-skills/paper-trail-builder.md` — reconstruct PRD, Plan, design docs

---

## Purpose

Enable DevAgent to take over an existing project that was started without it.
Produces a complete, confirmed paper trail (PRD, PROJECT.md, Plan, design docs) that
accurately reflects the as-built state plus the user's intended remaining work.
Hands off cleanly to the normal phase sequence at the correct re-entry point.

---

## 1. Trigger Detection

CLAUDE.md activates this skill when the user says anything like:
- "Take over my existing project"
- "I have code already written / already started"
- "Continue this project with DevAgent"
- "Reverse-engineer requirements from my codebase"
- "Onboard this project"
- "I started without DevAgent"

Also activates when artifact scan finds `src/` or detectable source files
**but no** `docs/PRD.md` — indicating a project in flight with no paper trail.

---

## 2. Internal Sub-Phases

```
Sub-phase A: Project Detection         [sequential — reads filesystem + config files]
Sub-phase B: Existing Artifacts Scan   [sequential — reads any docs/notes that exist]
Sub-phase C: Source Code Analysis      [PARALLEL — one subagent per detected component]
Sub-phase D: User Gap Interview        [sequential — user fills in what code can't tell us]
Sub-phase E: PRD Reconstruction        [sequential — as-built + planned combined]
Sub-phase F: Paper Trail Reconstruction [PARALLEL — Plan.md + DesignIndex.md]
Sub-phase G: PROJECT.md Generation     [sequential — same as Requirements Sub-phase G]
Sub-phase H: Re-entry Decision         [sequential — confirm which phase to resume]
```

---

## 3. Sub-phase A — Project Detection

**Invoke sub-skill:** `_shared/project-detector.md`

Detect language, framework, and source locations. Do NOT assume `src/`.
Detection is driven by config files and file extensions, not folder names.

Output written to: `.claude/skills/state/onboarding/detection-report.md`

---

## 4. Sub-phase B — Existing Artifacts Scan

Before touching source code, read everything the user may already have.
Scan in this order — read every file found, never skip:

| Priority | File/Location | What to extract |
|----------|--------------|-----------------|
| 1 | `README.md` | Project purpose, features described, setup instructions |
| 2 | `docs/` (any .md files) | Any requirements, design notes, ADRs, API docs |
| 3 | `CHANGELOG.md` | What has been released/built already |
| 4 | `*.md` at project root | Any notes, briefs, ideas |
| 5 | Issue tracker export (if provided) | Feature requests, bug reports |
| 6 | Git log | `git log --oneline -50` — commit history as feature signal |
| 7 | Branch names | `git branch -a` — work in progress signals |

**Git log procedure:**
```bash
git log --oneline -50          # last 50 commits — feature and fix history
git branch -a                  # all branches — WIP signals
git status                     # uncommitted changes
```

If no git repo: note as "no version control detected" — flag to user in Sub-phase D.

**Do not overwrite any existing file found here.** Read only. Flag any file that would
conflict with agent conventions (e.g. existing partial PRD.md) — ask user before replacing.

Output written to: `.claude/skills/state/onboarding/existing-artifacts.md`

---

## 5. Sub-phase C — Source Code Analysis (Parallel)

**Invoke sub-skill:** `sub-skills/code-archaeologist.md`

Using the source locations from Sub-phase A, spawn one subagent per detected component:

| Component type | What to analyze |
|---------------|----------------|
| UI / Views | Screens, components, user flows visible in UI code |
| Business logic | Core domain logic, rules, calculations |
| Data layer | Models, schemas, persistence, API calls |
| API routes | Endpoints, methods, request/response shapes |
| Tests (if any) | What's tested — use as ground truth for implemented behavior |
| Config / Entitlements | Capabilities, permissions, integrations declared |

Each subagent produces a feature map:
```markdown
# Component Analysis — {component name}
## Detected Features:
- {feature description} — confidence: HIGH | MEDIUM | LOW
  - Evidence: {file:line or pattern}
  - Behavior: {what it does}
  - Completeness: COMPLETE | PARTIAL | STUB
## Detected Patterns:
- Architecture: {e.g. MVVM, MVC, flat}
- State management: {e.g. @StateObject, Redux, Zustand}
- Error handling: PRESENT | PARTIAL | ABSENT
- Test coverage: {percentage or NONE}
## Quality Observations:
- {any hardcoded values, missing error handling, inconsistent patterns}
```

Output per subagent: `.claude/skills/state/onboarding/analysis-{component}.md`

**Confidence rules:**
- HIGH — behavior is explicit in code and matches a named UI element or test
- MEDIUM — behavior inferred from code logic but not explicitly named
- LOW — behavior guessed from file/function names only

Flag all LOW confidence items for user confirmation in Sub-phase D.

---

## 6. Sub-phase D — User Gap Interview

This is the most important sub-phase. Code tells us what exists — the user tells us what's intended.

Present findings first, then ask questions in one grouped message:

```
Here's what I found in your codebase:

DETECTED FEATURES ({count} total):
  ✓ {feature} — COMPLETE
  ◑ {feature} — PARTIAL ({what's missing})
  ? {feature} — LOW CONFIDENCE (need your confirmation)

EXISTING DOCS FOUND: {list or "None"}
TEST COVERAGE: {summary or "No tests found"}
ARCHITECTURE: {detected pattern}
QUALITY OBSERVATIONS: {list of flags}

Before I reconstruct the full paper trail, I need your input:

[REQUIRED]
1. Do the detected features above accurately represent what you've built?
   Any missing, misread, or incorrectly described features?

2. What features or requirements are still PENDING — not yet in the code?
   (This will become the TODO section of your plan)

3. Are there any known bugs or technical debt I should carry forward?
   (These will go into the maintenance queue)

[OPTIONAL]
4. Do you have any existing design documents, wireframes, architecture notes,
   or external references I should read before reconstructing design docs?
   (Suggested: No additional docs)

5. Are there constraints or decisions already made that should be locked in
   the PRD? (e.g. "we are committed to Supabase", "no third-party UI libs")
   (Suggested: None beyond what's detectable)

6. Is there anything in the existing code you want to override or change
   going forward? (Suggested: No — preserve existing patterns)
```

Wait for complete user response before proceeding.
Do not proceed to Sub-phase E with unresolved [REQUIRED] questions.

Output written to: `.claude/skills/state/onboarding/user-interview.md`

---

## 7. Sub-phase E — PRD Reconstruction

**Invoke sub-skill:** `sub-skills/code-archaeologist.md` (assembly mode)

Merge all inputs into a single PRD.md:

| PRD Section | Source |
|-------------|--------|
| Project Overview | README.md + user interview |
| Target Users | README.md + user interview |
| Constraints | Detected stack + user interview |
| Assumptions | Git history + user interview |
| **As-built features** (COMPLETE) | Code analysis — marked `[AS-BUILT]` |
| **Partial features** (PARTIAL) | Code analysis + user interview — marked `[PARTIAL]` |
| **Planned features** (TODO) | User interview only — marked `[PLANNED]` |
| Global NFRs | Detected patterns + profile NFRs (web/macOS if applicable) |
| Risks | Quality observations + missing tests + user interview |
| Open Questions | LOW confidence items + unresolved user answers |

**Critical distinction — mark every feature clearly:**
```markdown
### FEAT-001: {Feature Name}
**Status:** AS-BUILT | PARTIAL | PLANNED
**Completeness:** {what exists} / {what's missing if PARTIAL}
```

Apply full EARS notation and quality checklist from Requirements SKILL.md Section 4 and 8.
All requirements must pass the same quality bar as a greenfield PRD.

Present reconstructed PRD to user for review before writing to disk.
Incorporate feedback. Write final `docs/PRD.md` only after user confirms.

---

## 8. Sub-phase F — Paper Trail Reconstruction (Parallel)

Run two subagents simultaneously:

**Subagent F1 — Plan.md Reconstruction:**
- Generate Plan.md following Planning SKILL.md structure
- AS-BUILT features → all tasks marked `DONE`
- PARTIAL features → completed tasks `DONE`, remaining tasks `TODO`
- PLANNED features → all tasks `TODO`
- Preserve detected architecture decisions as planning constraints
- Write to: `docs/Plan.md`

**Subagent F2 — Design Index Reconstruction:**
- Generate `docs/design/DesignIndex.md` listing all design documents
- For each standard design doc (SystemArchitecture, TechnologyStack, etc.):
  - If enough information exists to write it → write it, mark `[RECONSTRUCTED]`
  - If information is insufficient → create stub with `[NEEDS DETAIL]` marker
- Write `docs/design/TechnologyStack.md` always — detected stack is reliable
- Write `docs/design/SystemArchitecture.md` from detected patterns
- Profile-specific docs (SwiftUIDesign.md, UIDesign.md) → stubs only, mark `[NEEDS DETAIL]`
- Write to: `docs/design/`

**Maintenance queue:**
If quality observations or known bugs were reported in user interview:
- Write each to `.claude/skills/state/maintenance/input-queue.md`
- Format per Maintenance skill BUG-XXX convention

---

## 9. Sub-phase G — Change Request Stubs (MANDATORY)

After Plan.md is written, for every P-prefix task (P1-xxx, P2-xxx, P3-xxx, P4-xxx) in Plan.md:

```
Create one file per P-xxx task:
File: docs/change-requests/CR-[task-ID].md

Template:
---
# Change Request: [task name]
ID: CR-[task-ID]
Plan task: [task-ID]
Status: APPROVED (pre-approved via onboarding)
Source: Onboarding gap interview
PRD section: [section number]
Description: [from plan.md notes]
NFR impact: [list affected NFRs, especially NFR-008 if pill content]
Design doc required: [yes/no — if yes, path in DesignIndex.md]
---
```

**Rationale:** P-prefix tasks produced by Onboarding bypass the `/deva:feature` change-request flow. These stubs create the traceability records that `/deva:feature` would normally produce, so `/deva:audit` can verify them.

If Plan.md has no P-prefix tasks, skip this sub-phase and note "No CR stubs needed" in the checkpoint.

---

## 10. Sub-phase G — PROJECT.md Generation

Follow the identical procedure as Requirements SKILL.md Sub-phase G:
- Detect project type → select correct template
- Fill fields from detection report + user interview
- Present to user for confirmation
- Write confirmed `PROJECT.md` to project root

---

## 11. Sub-phase I — Re-entry Decision and Skill Handoff (CRITICAL)

Present a summary and ask the user where to resume:

```
Onboarding complete.

Artifacts produced:
  ✓ docs/PRD.md — {X} features ({a} complete, {b} partial, {c} planned)
  ✓ docs/Plan.md — Phase 0: {N} bugs, Phase 1: {N} enhancements
  ✓ docs/design/ — {X} written, {Y} stubs needing detail
  ✓ PROJECT.md — confirmed
  ✓ docs/change-requests/ — {N} CR stubs (or "None")
  ✓ Maintenance queue — {X} items (or "None")

Re-entry options:
  A) Phase 0 — Bug fixes (BUG-xxx items)
     → I will invoke: /deva:fix
  B) Phase 1 — Enhancements (P1-xxx items)
     → I will invoke: /deva:implement
  C) Design — Flesh out NEEDS DETAIL design doc stubs
     → I will invoke: /deva:design
  D) V&V — The code is complete, run full verification
     → I will invoke: /deva:verify
  E) Planning — Rebuild or refine the task plan first
     → I will invoke: /deva:plan
  F) Maintenance — No planned work; monitor and fix as needed
     → I will invoke: /deva:fix when issues arise

Which option? (A / B / C / D / E / F)
```

**When the user selects an option, emit the exact command and immediately begin the target skill flow. Do NOT describe what you will do in prose and then wait.**

| Selection | Output | Action |
|-----------|--------|--------|
| A | `→ Invoking /deva:fix` | Begin Maintenance skill BUG-FIX flow immediately |
| B | `→ Invoking /deva:implement [first P1-xxx task ID]` | Begin Implementation skill flow immediately |
| C | `→ Invoking /deva:design` | Begin Design skill flow immediately |
| D | `→ Invoking /deva:verify` | Begin Verification skill flow immediately |
| E | `→ Invoking /deva:plan` | Begin Planning skill flow immediately |
| F | `→ No active skill. Use /deva:fix when a bug is reported.` | End session |

> **Why this matters:** Leaving the handoff as prose allows the AI to stay in the wrong skill context (e.g., continuing in Maintenance after Phase 0 when Phase 1 needs Implementation). The explicit command forces a clean skill switch.

Write final onboarding checkpoint before invoking the target skill:
```
# Checkpoint — Onboarding — {timestamp}
## Status: COMPLETED
## Phase just completed: Onboarding

## Artifacts Produced
  - docs/PRD.md
  - docs/Plan.md
  - docs/design/DesignIndex.md + {list of design docs}
  - PROJECT.md
  - docs/change-requests/ ({N} CR stubs, or "None")
  - .claude/skills/state/maintenance/input-queue.md (if applicable)

## Re-Entry Decision
Selected: {option letter}
Next skill: {skill name}
Next command: {exact command}

## Known Gaps
- {any NEEDS DETAIL items, unanswered questions}

## Resume Instructions
Load skills/{phase}/SKILL.md, read docs/PRD.md and docs/Plan.md, proceed with first TODO task.
```

---

## 12. What This Skill Must Never Do

- Never overwrite an existing file without reading it first and asking the user
- Never mark a feature AS-BUILT without evidence in the code
- Never mark a feature PLANNED without the user explicitly confirming it
- Never skip the user gap interview — code alone is never sufficient
- Never assume test absence means feature absence — some features have no tests
- Never proceed to Sub-phase E with LOW confidence items unresolved
