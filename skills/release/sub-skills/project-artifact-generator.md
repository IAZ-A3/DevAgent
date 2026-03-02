# DevAgent Sub-skill: Project-Specific Artifact Generator
**Parent:** Release Orchestrator  
**Scope:** Project-type-dependent release artifacts  
**Output:** Variable — determined by project type analysis

---

## Purpose

Analyze the project type from TechnologyStack.md and PRD, determine which additional release artifacts are appropriate beyond the standard CHANGELOG and release notes, generate them, and report what was produced to the orchestrator.

---

## Required Inputs

| Input | Source | Required |
|-------|--------|----------|
| TechnologyStack.md | docs/design/TechnologyStack.md | Yes |
| PRD.md | docs/PRD.md | Yes |
| VV-Report.md | docs/VV-Report.md | Yes |
| src/ | project source | Yes |
| Version string | Orchestrator | Yes |

---

## 1. Project Type Detection

Read TechnologyStack.md and classify the project:

| Indicator | Project Type |
|-----------|-------------|
| Swift, SwiftUI, Xcode | macOS/iOS App |
| Python + setup.py/pyproject.toml | Python Package |
| package.json + node | Node.js Package |
| Cargo.toml | Rust Binary/Library |
| go.mod | Go Binary/Library |
| Dockerfile or docker-compose | Containerized Service |
| CLI flags/argparse/click/cobra | CLI Tool |
| REST/API endpoints | API/Service |
| No framework, scripts only | Script Collection |

Present detected type to orchestrator for confirmation before generating artifacts.

---

## 2. Artifact Decision Matrix

Based on project type, generate these additional artifacts:

### macOS/iOS App
- [ ] `docs/release/AppStoreDescription.md` — App Store release description draft
- [ ] `docs/release/PrivacyManifest-checklist.md` — privacy manifest review checklist
- [ ] Build instructions: `docs/release/BuildInstructions.md`

### Python Package
- [ ] Verify `pyproject.toml` or `setup.cfg` version is updated
- [ ] `docs/release/PyPI-checklist.md` — steps to publish to PyPI
- [ ] `requirements.txt` freshness check — warn if pinned deps are outdated

### Node.js Package
- [ ] Verify `package.json` version is updated
- [ ] `docs/release/npm-publish-checklist.md`
- [ ] `package-lock.json` or `yarn.lock` consistency check

### Rust Binary/Library
- [ ] Verify `Cargo.toml` version updated
- [ ] `docs/release/crates-publish-checklist.md`
- [ ] Binary size report

### Go Binary
- [ ] Build for target platforms defined in NFRs (cross-compile if specified)
- [ ] Binary size and hash report

### CLI Tool (any language)
- [ ] `docs/release/USAGE.md` — usage guide generated from help output if available
- [ ] Man page stub if project is Unix-targeted

### API/Service
- [ ] `docs/release/API-Changelog.md` — API-specific change log (endpoint additions/removals)
- [ ] `docs/release/MigrationGuide.md` if breaking API changes exist
- [ ] OpenAPI/Swagger spec update check if spec file exists

### Containerized Service
- [ ] `docs/release/DockerHub-checklist.md`
- [ ] Image tag instructions
- [ ] `docker-compose` version pin update check

### Script Collection / Generic
- [ ] `docs/release/InstallGuide.md` if not already present
- [ ] Dependency list freshness check

---

## 3. Artifact Generation Rules

- Each artifact is lightweight — checklists, guides, and summaries only
- Never generate artifacts that duplicate what CHANGELOG or RELEASE-NOTES already cover
- Every checklist item must have a clear pass/fail criterion
- If a required file (e.g. `pyproject.toml`) is missing: warn but don't block release

---

## 4. Output

Write all artifacts to `docs/release/` folder.
Write artifact manifest to `.claude/skills/state/release/project-artifacts.md`:
```markdown
# Project-Specific Release Artifacts
## Project Type Detected: {type}
## Version: v{version}
## Date: {date}

| Artifact | Path | Status |
|----------|------|--------|
| {name} | docs/release/{file} | GENERATED |
```
