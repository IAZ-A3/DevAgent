# /deva:upgrade — Upgrade DevAgent Skills to Latest Version

You are the DevAgent software development agent. The user wants to check for and apply updates to the DevAgent skill files in this project.

## Reference Repository
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/IAZ-A3/DevAgent/develop"
GITHUB_REPO_URL = "https://github.com/IAZ-A3/DevAgent"

Replace {YOUR_GITHUB_USERNAME} with the actual GitHub username once the repo is created.

---

## Instructions

### Step 1 — Read local version
Read the first 6 lines of `CLAUDE.md` in the project root.
Extract the version from the line: `# DevAgent version: X.Y.Z  |  Released: {date}`
If no version line is found: local version = "unknown".

### Step 2 — Fetch remote version
Fetch: `{GITHUB_RAW_BASE}/CLAUDE.md`
Extract the version line from the first 6 lines.
If fetch fails: stop and report:
```
Could not reach the DevAgent repository.
Check your internet connection or visit: {GITHUB_REPO_URL}
```

### Step 3 — Compare versions
Parse both versions as MAJOR.MINOR.PATCH integers and compare.

If local == remote:
```
✓ DevAgent is up to date (version {version})
  No upgrade needed.
```
Stop here.

If local > remote (should not happen — flag it):
```
⚠ Local version ({local}) is ahead of the repository ({remote}).
  This may mean you have local customizations. No changes will be made.
```
Stop here.

If local < remote: proceed to Step 4.

### Step 4 — Fetch remote CHANGELOG.md
Fetch: `{GITHUB_RAW_BASE}/CHANGELOG.md`
Extract all entries between the remote version and the local version.
Present to the user:
```
DevAgent upgrade available: {local} → {remote}

Changes since your version:
{changelog entries between local and remote versions}

Repository: {GITHUB_REPO_URL}
```

### Step 5 — Build file manifest
Fetch: `{GITHUB_RAW_BASE}/.claude/skills/_shared/upgrade-manifest.md`

This file lists every DevAgent file with its path and a short description.
If the manifest cannot be fetched: build the manifest manually from the known file list below.

Known DevAgent files (fallback manifest):
```
CLAUDE.md
.claude/registry.md
.claude/commands/deva:new.md
.claude/commands/deva:onboard.md
.claude/commands/deva:resume.md
.claude/commands/deva:status.md
.claude/commands/deva:requirements.md
.claude/commands/deva:plan.md
.claude/commands/deva:design.md
.claude/commands/deva:implement.md
.claude/commands/deva:verify.md
.claude/commands/deva:release.md
.claude/commands/deva:fix.md
.claude/commands/deva:feature.md
.claude/commands/deva:audit.md
.claude/commands/deva:checkpoint.md
.claude/commands/deva:upgrade.md
.claude/skills/_shared/context-manager.md
.claude/skills/_shared/artifact-schema.md
.claude/skills/_shared/subagent-patterns.md
.claude/skills/_shared/project-detector.md
.claude/skills/requirements/SKILL.md
.claude/skills/requirements/sub-skills/change-request-analyzer.md
.claude/skills/planning/SKILL.md
.claude/skills/design/SKILL.md
.claude/skills/implementation/SKILL.md
.claude/skills/implementation/sub-skills/code-generator.md
.claude/skills/implementation/sub-skills/code-reviewer.md
.claude/skills/implementation/sub-skills/test-writer.md
.claude/skills/implementation/sub-skills/integrator.md
.claude/skills/verification/SKILL.md
.claude/skills/verification/sub-skills/nfr-validator.md
.claude/skills/verification/sub-skills/requirement-coverage-auditor.md
.claude/skills/verification/sub-skills/system-test-runner.md
.claude/skills/release/SKILL.md
.claude/skills/release/sub-skills/release-docs-generator.md
.claude/skills/maintenance/SKILL.md
.claude/skills/maintenance/sub-skills/bug-fixer.md
.claude/skills/maintenance/sub-skills/regression-runner.md
.claude/skills/onboarding/SKILL.md
.claude/skills/onboarding/sub-skills/code-archaeologist.md
.claude/skills/onboarding/sub-skills/paper-trail-builder.md
.claude/skills/web-profile/SKILL.md
.claude/skills/web-profile/sub-skills/cloudflare-deployer.md
.claude/skills/web-profile/sub-skills/web-vv.md
.claude/skills/macos-profile/SKILL.md
.claude/skills/macos-profile/sub-skills/swiftui-component-builder.md
.claude/skills/macos-profile/sub-skills/macos-release-builder.md
.claude/skills/macos-profile/sub-skills/entitlements-privacy-configurator.md
```

### Step 6 — Check which files have changed
For each file in the manifest:
1. Fetch remote version from `{GITHUB_RAW_BASE}/{file_path}`
2. Read local version from disk
3. Compare — flag as CHANGED if different, SAME if identical, NEW if not present locally

Group results:
```
Files to update ({X} changed, {Y} new):
  CHANGED  CLAUDE.md
  CHANGED  .claude/skills/requirements/SKILL.md
  NEW      .claude/skills/requirements/sub-skills/change-request-analyzer.md
  ...

Files unchanged ({Z} files):
  SAME     .claude/skills/planning/SKILL.md
  ...
```

### Step 7 — Ask for confirmation
Present upgrade options:
```
How would you like to proceed?
A) Update all changed/new files
B) Select files to update individually
C) Cancel — I'll update manually from {GITHUB_REPO_URL}
```

Wait for user choice.

**If A:** proceed to Step 8 for all CHANGED and NEW files.
**If B:** list each file, ask "Update this file? (yes/no)" — proceed to Step 8 only for confirmed files.
**If C:** stop. Provide the repo URL and remind them they can download a ZIP from any tagged release.

### Step 8 — Apply updates (confirmed files only)

For each confirmed file:
1. If file exists locally: back it up first → `{original_path}.backup`
2. Write the fetched remote content to the local path
3. Confirm: `✓ Updated: {file_path}`

After all files updated:
```
✓ DevAgent upgraded to version {remote_version}

Backup files created with .backup extension — delete them once you've verified the upgrade.

If anything broke, restore a file with:
  cp {file_path}.backup {file_path}
```

### Step 9 — Post-upgrade check
Run `/deva:status` automatically to verify the project state is still valid after the upgrade.
If any artifact format has changed (MAJOR version bump): warn the user:
```
⚠ This was a MAJOR version upgrade. Artifact formats may have changed.
  Run /deva:audit to check for any compatibility issues with existing project files.
```

---

## Safety Rules

- NEVER overwrite a file without creating a .backup first
- NEVER update `.claude/skills/state/` files — these are project-specific runtime data
- NEVER update `PROJECT.md` or `docs/` — these belong to the project, not DevAgent
- NEVER auto-proceed past Step 7 without explicit user confirmation
- If any fetch fails mid-upgrade: stop, report which file failed, leave already-updated files in place (do not roll back automatically — ask the user)

## Context passed from user
$ARGUMENTS
