# DevAgent Sub-skill: Code Archaeologist
**Parent:** Onboarding — Sub-phase C (analysis mode) and Sub-phase E (assembly mode)
**Output:**
- Analysis mode: `.claude/skills/state/onboarding/analysis-{component}.md` per component
- Assembly mode: `docs/PRD.md` (reconstructed)

---

## Purpose

Reverse-engineer features, behaviors, and requirements from existing source code.
Operates in two modes: **analysis** (per-component feature extraction) and
**assembly** (merge all analysis + user interview into a complete PRD).

---

## Mode 1: Analysis (Sub-phase C)

One subagent instance per component. Receives:
- Component name and type
- Source file paths to analyze
- Detection report (for architecture context)

### Analysis procedure

**Step 1 — File inventory**
List all files in the component. Group by type:
- Entry points (main files, app delegates, index files)
- Feature files (named after domain concepts)
- Support files (utilities, extensions, helpers)
- Test files

**Step 2 — Feature extraction**

For each feature file or logical group:

```
For each file:
  1. Read the file completely
  2. Identify: what user-visible behavior does this enable?
  3. Assign confidence: HIGH / MEDIUM / LOW (see rules below)
  4. Assess completeness: COMPLETE / PARTIAL / STUB
  5. Note evidence: file name + key function/class names
```

**Confidence rules:**
- **HIGH** — behavior is explicit: UI element named after it, test covering it, or it's a complete end-to-end flow
- **MEDIUM** — behavior inferred from business logic but no UI or test confirms it
- **LOW** — behavior guessed from file/function name only, or code is commented out / TODO

**Completeness rules:**
- **COMPLETE** — happy path + error handling present, no obvious TODOs
- **PARTIAL** — core logic present but: error handling missing, TODOs in code, UI exists without backend or vice versa, hardcoded stubs
- **STUB** — placeholder only: empty function body, `// TODO`, `fatalError("not implemented")`, hardcoded return values

**Step 3 — Quality observations**

Flag any of the following — these go to the maintenance queue:
- Force unwraps (`!`) in Swift production code
- `TODO`, `FIXME`, `HACK` comments
- Hardcoded values (URLs, credentials, magic numbers)
- Missing error handling (empty catch blocks, unhandled promises)
- Inconsistent patterns (mix of async styles, mix of state management)
- Dead code (unreachable blocks, unused imports)
- No tests for critical paths

**Step 4 — Dependency mapping**

For each detected feature, note:
- Which other features does it depend on? (calls to other modules)
- Which external APIs or services does it use?
- Which entitlements or permissions does it require?

### Analysis output format

```markdown
# Component Analysis — {component name}
## Type: UI | Business Logic | Data Layer | API Routes | Config | Tests
## Files analyzed: {count}

## Detected Features:

### {Feature name}
- **Confidence:** HIGH | MEDIUM | LOW
- **Completeness:** COMPLETE | PARTIAL | STUB
- **Evidence:** {file(s) and key identifiers}
- **Behavior:** {one sentence — what the user can do}
- **Dependencies:** {other features or external services}
- **Partial detail:** {what's missing, if PARTIAL}

(repeat per feature)

## Architecture observations:
- Pattern: {detected}
- State management: {detected}
- Error handling: PRESENT | PARTIAL | ABSENT
- Async style: {e.g. async/await, callbacks, Combine}

## Quality flags:
- {flag description} — {file:approximate location}

## Test coverage:
- {what's tested, or "No tests found for this component"}
```

---

## Mode 2: Assembly (Sub-phase E)

Receives all component analysis files + user interview output.
Produces the final reconstructed `docs/PRD.md`.

### Assembly procedure

**Step 1 — Feature consolidation**

Merge features across all component analyses:
- Deduplicate features that appear in multiple components
- Resolve conflicts (same feature with different confidence levels — use highest)
- Add PLANNED features from user interview
- Assign `FEAT-XXX` IDs in order: AS-BUILT first, PARTIAL second, PLANNED last

**Step 2 — Status classification**

| Feature status | Criteria |
|---------------|---------|
| `AS-BUILT` | All components COMPLETE, HIGH or MEDIUM confidence |
| `PARTIAL` | Any component PARTIAL, or MEDIUM/LOW confidence with user confirmation |
| `PLANNED` | From user interview only — no code evidence |

**Step 3 — Requirements elaboration**

For each feature, write functional requirements using EARS notation
(same rules as Requirements SKILL.md Section 4):
- AS-BUILT: requirements describe what the code demonstrably does
- PARTIAL: requirements describe both what exists and what's missing
- PLANNED: requirements describe intended behavior from user interview

**Step 4 — NFR definition**

- Import profile-specific NFRs if web-profile or macos-profile is active
- Add any NFRs implied by detected stack (e.g. if Cloudflare detected → edge performance NFRs)
- Add NFRs from user interview (locked-in constraints)
- Flag NFRs that the existing code may already violate (from quality observations)

**Step 5 — PRD assembly**

Use the standard PRD structure from Requirements SKILL.md Section 5, with additions:

```markdown
## 0. Onboarding Context
**Onboarding date:** {date}
**As-built baseline:** {X} features reconstructed from codebase
**Partial features:** {X} features requiring completion
**Planned features:** {X} features from user interview
**Known quality debt:** {X} items (see Maintenance Queue)
**Design docs status:** {X} written, {Y} stubs requiring detail
```

Every feature entry includes its status badge:
```markdown
### FEAT-001: {Feature Name}
**Status:** `AS-BUILT` | `PARTIAL` | `PLANNED`
**Completeness:** {for PARTIAL: what exists / what's missing}
```

**Step 6 — User review**

Present PRD summary to user before writing to disk:
```
I've reconstructed your PRD. Here's a summary before I write it:

AS-BUILT features ({count}): {list}
PARTIAL features ({count}): {list with what's missing}
PLANNED features ({count}): {list}
Quality debt items: {count} (queued for maintenance)

Does this accurately represent your project?
Any corrections before I write docs/PRD.md?
```

Wait for confirmation. Apply corrections. Then write `docs/PRD.md`.
