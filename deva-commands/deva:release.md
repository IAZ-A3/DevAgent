# /deva:release — Run the Release Phase

You are the DevAgent software development agent. The user wants to package and release the project.

## Instructions

1. Read `CLAUDE.md` and `PROJECT.md` (if present).
2. Verify `docs/VV-Report.md` exists and its gate result is PASS or PASS_WITH_BUGS — if not, stop and tell the user: "Release requires a passed V&V report. Run `/deva:verify` first."
3. If gate is PASS_WITH_BUGS: warn the user explicitly — list the known bugs being carried forward. Ask for confirmation before proceeding.
4. Load `.claude/skills/release/SKILL.md` and all its sub-skills.
5. Detect and load the active profile:
   - macOS profile: invoke `macos-release-builder` sub-skill (archive → sign → notarize → staple → DMG)
   - Web profile: invoke `cloudflare-deployer` sub-skill
   - No profile: follow base release skill
6. Determine the release version — ask the user if not specified in `$ARGUMENTS`:
   ```
   What version should this release be tagged as?
   Current VERSION file: {content or "not found"}
   Suggested: {next semantic version}
   ```
7. Follow the full Release skill procedure — generate changelog, release notes, and all release artifacts.
8. Present final release checklist before executing any git tag or deployment commands. Wait for explicit confirmation.
9. Never run `git tag`, `git push`, or deployment commands without explicit user approval — show the commands first.

## Version / context passed from user
$ARGUMENTS
