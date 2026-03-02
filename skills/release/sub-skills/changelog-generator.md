# DevAgent Sub-skill: Changelog Generator
**Parent:** Release Orchestrator  
**Scope:** CHANGELOG.md generation/update  
**Output:** Updated `CHANGELOG.md`

---

## Purpose

Generate or update CHANGELOG.md following the Keep a Changelog format. Derive entries from PRD features, Plan tasks, and the V&V report. Every change must be traceable to a requirement or bug ID.

---

## Required Inputs

| Input | Source | Required |
|-------|--------|----------|
| PRD.md | docs/PRD.md | Yes |
| Plan.md | docs/Plan.md | Yes |
| VV-Report.md | docs/VV-Report.md | Yes |
| Maintenance input queue | state/maintenance/input-queue.md | If exists |
| Current CHANGELOG.md | project root | If exists (append) |
| New version string | Orchestrator | Yes |

---

## 1. Changelog Entry Categories

Follow Keep a Changelog categories:

| Category | What goes here |
|----------|---------------|
| Added | New features (new FEAT-XXX implemented) |
| Changed | Modified behavior of existing features |
| Deprecated | Features marked for future removal |
| Removed | Features removed in this release |
| Fixed | Bugs fixed (BUG-XXX resolved) |
| Security | Security fixes or improvements |

---

## 2. Entry Generation Rules

- One entry per completed FEAT-XXX task group (not per individual task)
- One entry per resolved BUG-XXX
- Each entry references its ID: `[FEAT-001]`, `[BUG-003]`
- Language: past tense, imperative mood ("Added file watching capability" not "Adds...")
- No implementation details — user-facing behavior only
- Sort entries: Added first, then Changed, Fixed, Security, Removed, Deprecated

---

## 3. CHANGELOG.md Format

```markdown
# Changelog
All notable changes to this project will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [v{version}] — {YYYY-MM-DD}

### Added
- [FEAT-001] {user-facing description of new feature}
- [FEAT-002] {user-facing description of new feature}

### Fixed
- [BUG-001] {description of what was fixed}

### Security
- [NFR-002] {description of security improvement}

---

## [v{previous}] — {date}
{previous entries preserved exactly}
```

---

## 4. Output

Write to `CHANGELOG.md` in project root.
If file already exists: prepend new release section, preserve all previous content exactly.
