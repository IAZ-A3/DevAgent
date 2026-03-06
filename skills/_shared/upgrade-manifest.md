# DevAgent Upgrade Manifest
# Version: 1.0.0
# This file is read by /deva:upgrade to determine which files belong to DevAgent.
# Update this file whenever files are added, removed, or renamed in a release.
# Format: {path} | {category} | {description}

---

## Core

CLAUDE.md | core | Master orchestrator configuration
.claude/registry.md | core | Skill and MCP server registry
.claude/skills/_shared/context-manager.md | core | Context window management rules
.claude/skills/_shared/artifact-schema.md | core | Artifact ID conventions and gate formats
.claude/skills/_shared/subagent-patterns.md | core | Parallel subagent patterns
.claude/skills/_shared/project-detector.md | core | Language and framework detection (shared)
.claude/skills/_shared/upgrade-manifest.md | core | This file — upgrade file list

---

## Commands

.claude/commands/deva:new.md | command | Start a new project from scratch
.claude/commands/deva:onboard.md | command | Onboard an existing project
.claude/commands/deva:resume.md | command | Resume an interrupted session
.claude/commands/deva:status.md | command | Project status report
.claude/commands/deva:requirements.md | command | Run the Requirements phase
.claude/commands/deva:plan.md | command | Run the Planning phase
.claude/commands/deva:design.md | command | Run the Design phase
.claude/commands/deva:implement.md | command | Run the Implementation phase
.claude/commands/deva:verify.md | command | Run the V&V phase
.claude/commands/deva:release.md | command | Run the Release phase
.claude/commands/deva:fix.md | command | Fix a bug or run maintenance
.claude/commands/deva:feature.md | command | Add a new feature via change request
.claude/commands/deva:audit.md | command | Project health and traceability audit
.claude/commands/deva:checkpoint.md | command | Save a manual checkpoint
.claude/commands/deva:upgrade.md | command | Upgrade DevAgent to latest version

---

## Base Skills

.claude/skills/requirements/SKILL.md | skill | Requirements phase orchestrator
.claude/skills/requirements/sub-skills/change-request-analyzer.md | skill | Change request impact analysis
.claude/skills/planning/SKILL.md | skill | Planning phase orchestrator
.claude/skills/design/SKILL.md | skill | Design phase orchestrator
.claude/skills/implementation/SKILL.md | skill | Implementation phase orchestrator
.claude/skills/implementation/sub-skills/code-generator.md | skill | Code generation
.claude/skills/implementation/sub-skills/code-reviewer.md | skill | Code review
.claude/skills/implementation/sub-skills/test-writer.md | skill | Test writing
.claude/skills/implementation/sub-skills/integrator.md | skill | Integration
.claude/skills/verification/SKILL.md | skill | V&V phase orchestrator
.claude/skills/verification/sub-skills/nfr-validator.md | skill | NFR validation
.claude/skills/verification/sub-skills/requirement-coverage-auditor.md | skill | Requirement coverage audit
.claude/skills/verification/sub-skills/system-test-runner.md | skill | System test runner
.claude/skills/release/SKILL.md | skill | Release phase orchestrator
.claude/skills/release/sub-skills/release-docs-generator.md | skill | Release documentation (changelog, notes, artifacts)
.claude/skills/maintenance/SKILL.md | skill | Maintenance phase orchestrator
.claude/skills/maintenance/sub-skills/bug-fixer.md | skill | Bug fixing
.claude/skills/maintenance/sub-skills/regression-runner.md | skill | Regression testing

---

## Onboarding

.claude/skills/onboarding/SKILL.md | skill | Project onboarding orchestrator
.claude/skills/onboarding/sub-skills/code-archaeologist.md | skill | Reverse-engineer features from code
.claude/skills/onboarding/sub-skills/paper-trail-builder.md | skill | Reconstruct Plan, design docs, maintenance queue

---

## Web Profile

.claude/skills/web-profile/SKILL.md | profile | Web project profile
.claude/skills/web-profile/sub-skills/cloudflare-deployer.md | profile | Cloudflare deployment
.claude/skills/web-profile/sub-skills/web-vv.md | profile | Web-specific V&V
.claude/skills/web-profile/scripts/check-dependencies.py | profile | Web dependency checker

---

## macOS Profile

.claude/skills/macos-profile/SKILL.md | profile | macOS project profile
.claude/skills/macos-profile/sub-skills/swiftui-component-builder.md | profile | SwiftUI component builder
.claude/skills/macos-profile/sub-skills/macos-release-builder.md | profile | macOS release pipeline
.claude/skills/macos-profile/sub-skills/entitlements-privacy-configurator.md | profile | Entitlements and privacy manifest
.claude/skills/macos-profile/scripts/check-macos-dependencies.py | profile | macOS dependency checker

---

## Project Templates (reference copies — not upgraded, project-specific)

# These files are NOT updated by /deva:upgrade — they belong to each project.
# Listed here for documentation only.
# PROJECT.md
# PROJECT-web-template.md
# PROJECT-macos-template.md
