# DevAgent Skill: Release — Orchestrator
**Phase:** 6 of 7  
**Role:** Entry point and coordinator for all release sub-skills  
**Output:** `CHANGELOG.md`, `RELEASE-NOTES.md`, versioned code package, git tag, project-specific artifacts  
**Imports:** `../_shared/context-manager.md`, `../_shared/subagent-patterns.md`, `../_shared/artifact-schema.md`

---

## Purpose

Prepare and execute a complete, traceable release of the project. Determine the correct semantic version, produce all required artifacts, package and distribute the code per project type, and create a git tag. Enforce V&V gate before proceeding. Infer project-specific packaging steps from TechnologyStack.md.

---

## 1. Input Discovery

### If inputs are explicitly provided:
Use them directly.

### If inputs are NOT explicitly provided (auto-discovery):
Scan in this order:
1. `docs/VV-Report.md` — V&V gate result (required)
2. `docs/PRD.md` — feature and requirement reference
3. `docs/Plan.md` — completed tasks reference
4. `docs/design/TechnologyStack.md` — infer packaging/distribution steps
5. `CHANGELOG.md` — existing changelog (append to if present)
6. `VERSION` or `version.txt` or `pyproject.toml` or `package.json` — current version
7. `.claude/skills/state/maintenance/input-queue.md` — open bugs (warning check)
8. `.git/` — confirm git repository exists for tagging
9. `.claude/skills/state/release/checkpoint.md` — resume from previous session

---

## 2. Release Gate Enforcement

**Before any release work begins**, check V&V gate:

1. Read `docs/VV-Report.md`
2. Extract Overall Result field
3. Apply gate rules:

| V&V Result | Release Action |
|------------|---------------|
| PASS | Proceed |
| PASS_WITH_BUGS | Proceed with warning — list open bugs in release notes |
| FAIL | HALT — inform user, list failing items, do not proceed |
| Not found | HALT — V&V must be completed first |

4. Check Maintenance input queue for STRUCTURAL bugs:
   - If open structural bugs exist: warn user, list them, ask for explicit confirmation to proceed
   - User must confirm before release continues

**Clarification format for structural bugs:**
```
⚠ WARNING: The following structural bugs are in the Maintenance queue:
  - BUG-001: {description}
  - BUG-002: {description}

These were not fixed during V&V. Do you want to:
A) Proceed with release and document bugs as known issues (Suggested)
B) Halt release until bugs are resolved

Please confirm your choice before I continue.
```

---

## 3. Version Determination

Read current version from project files (in order):
1. `VERSION` or `version.txt`
2. `package.json` → `version` field
3. `pyproject.toml` → `[project] version` field
4. `Cargo.toml` → `version` field
5. Git tags → latest tag matching `v*.*.*`
6. If none found: start at `0.1.0`

**Determine version bump from PRD and Plan.md:**

| Condition | Bump |
|-----------|------|
| Any breaking change (interface removed/changed, incompatible behavior) | MAJOR |
| New features added (new FEAT-XXX implemented) | MINOR |
| Bug fixes only, no new features | PATCH |
| First release | 0.1.0 (regardless of features) |

**Present version to user for confirmation:**
```
Proposed version: {current} → {new}
Reason: {N new features implemented: FEAT-001, FEAT-002}
Confirm or provide alternative version:
```
Wait for confirmation before proceeding.

---

## 4. Orchestration Flow

```
Step 1: Release gate check            [sequential — blocks if FAIL]
Step 2: Version determination         [sequential — user confirms]
Step 3: Spawn parallel sub-skills:
        → Changelog Generator
        → Release Notes Generator
        → Project-Specific Artifact Generator
Step 4: WAIT — all sub-skills complete
Step 5: Package & distribute          [sequential]
Step 6: Git tag & commit              [sequential — explicit permission]
Step 7: Final release manifest        [sequential]
Step 8: Update Plan.md + artifact registry
Step 9: Phase gate
```

---

## 5. Packaging & Distribution (inferred from TechnologyStack.md)

Read TechnologyStack.md and apply the matching packaging strategy:

| Technology | Packaging Action |
|-----------|-----------------|
| Python | `python -m build` → produces `.whl` and `.tar.gz` in `dist/` |
| Node.js / npm | `npm pack` → produces `.tgz` in project root |
| Rust / Cargo | `cargo build --release` → binary in `target/release/` |
| Go | `go build -o dist/` → binary in `dist/` |
| macOS App (Swift) | `xcodebuild archive` → `.xcarchive`, then export `.app` or `.pkg` |
| Generic / Script | Create zip archive of `src/` + docs + README |
| Unknown | Create zip archive of project root (excluding `.git`, `node_modules`, `.venv`) |

**Package naming convention:**
`{project-name}-v{version}-{YYYYMMDD}.{ext}`

---

## 6. Git Operations

Requires explicit user permission before execution (see security rules).

Steps:
1. Verify git repository: `git status`
2. Stage release artifacts: `git add CHANGELOG.md RELEASE-NOTES.md VERSION {other release files}`
3. Commit: `git commit -m "release: v{version} — {brief summary}"`
4. Tag: `git tag -a v{version} -m "Release v{version}"`
5. Inform user: tag created locally. Provide command to push: `git push && git push --tags`
   - Do NOT push automatically — user decides when to push

---

## 7. Context Management (Phase-Specific)

Imports rules from `../_shared/context-manager.md`, plus:

- Checkpoint after version confirmation
- Checkpoint after sub-skills complete (Step 4)
- Checkpoint after packaging (Step 5)
- State folder: `.claude/skills/state/release/`

---

## 8. Output & Phase Gate

On completion:
1. `CHANGELOG.md` — updated
2. `RELEASE-NOTES.md` — created for this release
3. `VERSION` — updated to new version
4. Release package in `dist/` or `release/`
5. Project-specific artifacts (see sub-skill)
6. Git tag created locally
7. Update `.claude/skills/state/artifact-registry.md`
8. Produce phase gate:

```
# Phase Gate — Release
## Result: PASS
## Version: v{version}
## Artifacts: {list}
## Git Tag: v{version} (local — push with: git push && git push --tags)
## Known Issues: {list from maintenance queue or "None"}
## Recommended Next Phase: maintenance
## Notes: {any warnings}
```

9. Inform user: Release v{version} is ready. Provide git push command.
