# Artifact Schema — Shared Module
> Defines standard handoff formats between skills/phases.

---

## ID Conventions (used across all skills)

| Entity | Global ID | Scoped ID (to feature) |
|--------|-----------|------------------------|
| Feature | `FEAT-001` | — |
| Functional Requirement | `FR-001` (global) | `FEAT-001-FR-001` (feature-scoped) |
| Non-Functional Requirement | `NFR-001` (global) | `FEAT-001-NFR-001` (feature-scoped) |
| Task / Work Item | `TASK-001` | — |
| Test Case | `TC-001` | `FEAT-001-TC-001` |
| Risk | `RISK-001` | — |
| Decision | `DEC-001` | — |
| Bug | `BUG-001` | — |

---

## Artifact Registry

Each skill must update `.claude/skills/state/artifact-registry.md` upon completion:

```
# Artifact Registry
| Skill       | Artifact File          | Status    | Timestamp  |
|-------------|------------------------|-----------|------------|
| requirements| docs/PRD.md            | COMPLETED | 2025-01-01 |
| planning    | docs/Plan.md           | COMPLETED | 2025-01-01 |
```

---

## Phase Gate Format

At the end of each skill execution, produce a phase gate summary:
```
# Phase Gate — {Skill Name}
## Result: PASS | FAIL | NEEDS_REVIEW
## Artifacts: [list of output files]
## Open Issues: [list]
## Recommended Next Phase: {skill name}
## Blockers: [list or "None"]
```
