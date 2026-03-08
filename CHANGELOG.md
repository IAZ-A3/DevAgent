# DevAgent Changelog

All notable changes to DevAgent are documented here.
Format: version, date, category, description.
Categories: Added | Changed | Fixed | Removed

---

## [1.0.1] — 2026-03-08

### Fixed
- **context-manager.md**: Removed undetectable token-budget % thresholds (30/40/50%); replaced with event-based-only checkpointing. Agents cannot measure context window percentage — this approach was misleading.
- **CLAUDE.md**: Updated Section 2 context discipline note to reference event-based approach only; removed threshold mention.
- **CLAUDE.md**: Fixed `src/` hardcoding in Section 7 project structure — replaced with `{source}/` placeholder and note to use project-detector, consistent with the no-`src/`-assumption rule.
- **CLAUDE.md**: Added phase rollback reference line in Section 8 pointing to new rollback-protocol.md.
- **onboarding/SKILL.md**: Added Planning as a re-entry option in Sub-phase H; the previous omission left no path back to planning from an onboarded project. Added step-by-step resume instructions for each option.
- **design/SKILL.md**: Added Conflict Escalation Protocol to Sub-phase F — agent now halts and presents conflicts to user rather than silently proceeding with inconsistent design documents.
- **verification/SKILL.md**: Added tiered coverage model (Automated / Review-verified / Unverified) with PASS requiring zero Unverified items. Prevents false PASS results from untestable or untested requirements.
- **maintenance/SKILL.md**: Replaced ambiguous CR classification table with a 4-step procedure (find feature → find requirement → check implementation intent → ask if ambiguous). Eliminates subjective guessing on bug vs. change-request classification.
- **deva:upgrade.md**: Added Step 0 to check for in-progress phases before upgrading — prevents mid-phase upgrade inconsistencies. Replaced per-file `.backup` naming with dated folder backup strategy for atomic rollback.
- **web-profile/SKILL.md**: Added PROJECT.md override block for NFR defaults — projects can now set custom accessibility, performance, and browser targets in PROJECT.md rather than being locked to global defaults.
- **planning/SKILL.md**: Added Example Task column to complexity scoring table — each score level now has a concrete example to reduce scoring inconsistency.
- **planning/SKILL.md**: Added Task ID column to Change Log table; tightened Section 6 step 4 to require exact change format (`Status: {old} → {new}` or `Added FEAT-XXX-TASK-YYY`).

### Added
- **rollback-protocol.md** (new shared skill): Defines a 4-step protocol for rolling back to an earlier phase — assess invalidated artifacts, archive to `.claude/archive/rollback-{date}/`, mark ARCHIVED in registry, load target phase skill.

---

## [1.0.0] — 2026-03-02

### Added
- 7-phase development pipeline: Requirements → Planning → Design → Implementation → V&V → Release → Maintenance
- CLAUDE.md master orchestrator (195 lines)
- 14 slash commands: /deva:new, /deva:onboard, /deva:resume, /deva:status, /deva:requirements, /deva:plan, /deva:design, /deva:implement, /deva:verify, /deva:release, /deva:fix, /deva:feature, /deva:audit, /deva:checkpoint
- /deva:upgrade command with GitHub-based version checking
- Onboarding skill with 5-layer project detection (no src/ assumption)
- Code Archaeologist sub-skill: reverse-engineer features with HIGH/MEDIUM/LOW confidence
- Paper Trail Builder sub-skill: reconstruct Plan.md and design docs from existing code
- Web profile: Cloudflare deployment, web-specific V&V
- macOS profile: SwiftUI component builder, code signing, notarization pipeline, entitlements configurator
- Shared project-detector sub-skill: language/framework detection across all skills
- Context manager: 50/75/90% threshold checkpoints + mandatory event-based checkpoints at phase gates
- Artifact schema: FEAT-XXX / TASK-XXX / BUG-XXX ID conventions
- Upgrade manifest: machine-readable file list for /deva:upgrade
- DevAgent version header in CLAUDE.md

---

## Versioning Policy

MAJOR — Breaking changes: artifact format changes, phase redesign, ID convention changes.
         Existing projects may need /deva:audit after upgrading.

MINOR — New capabilities: new skills, new commands, new profiles, new sub-skills.
         Fully backward compatible.

PATCH — Fixes and clarifications: wording improvements, bug fixes in skill logic, 
         typo corrections. Safe to apply without review.
