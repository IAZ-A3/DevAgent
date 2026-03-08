# DevAgent

A structured, 7-phase software development agent for Claude Code. DevAgent brings engineering discipline to AI-assisted development — requirements traceability, phase gates, checkpoints, and a consistent workflow from idea to release.

> Built for Claude Code. Designed for engineers who want AI assistance with engineering discipline.

---

## What is DevAgent?

DevAgent is a configuration system for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that turns it into a disciplined software development agent. Instead of ad-hoc AI coding sessions, DevAgent gives you a repeatable, traceable process:

```
Requirements → Planning → Design → Implementation → V&V → Release → Maintenance
```

Every phase has defined inputs, outputs, and gate conditions. Nothing moves forward without your explicit approval. Every artifact is traceable — requirements link to design, design links to code, code links to tests.

---

## Key Features

- **7-phase pipeline** — structured workflow with gate conditions at every phase boundary
- **15 slash commands** — trigger any phase or action directly from Claude Code chat
- **Project onboarding** — bring an existing codebase under agent control with full reverse-engineering
- **Two profiles** — web (React, Next.js, Cloudflare) and macOS (SwiftUI, code signing, notarization)
- **Context-aware checkpoints** — automatic saves at phase gates; resume cleanly across sessions
- **Change request flow** — new features update PRD and Plan before any code is touched
- **Self-upgrading** — `/deva:upgrade` checks this repo for updates and applies them with your confirmation
- **No `src/` assumption** — project detector identifies source locations for any language or framework

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — latest version
- Node.js 18+ — required for the installer
- For web projects: Cloudflare account (optional)
- For macOS projects: Xcode, Apple Developer account, [XcodeBuildMCP](https://github.com/cameroncooke/XcodeBuildMCP)

---

## Installation

DevAgent installs in one command. It copies all skills, commands, and config files to the right locations automatically.

```bash
npx devagent-cc@latest
```

The installer will ask:

```
Where would you like to install DevAgent?

  1) Global — available in ALL projects  (~/.claude/)  [recommended]
  2) Local  — this project only          (./.claude/)
```

**Choose Global** if you want `/deva:` commands available in every project without reinstalling.
**Choose Local** if you want DevAgent scoped to a single project only.

### Non-interactive install

```bash
npx devagent-cc@latest --global   # install globally, no prompts
npx devagent-cc@latest --local    # install locally, no prompts
```

### Alternative — shell installer (no Node.js required)

```bash
curl -fsSL https://raw.githubusercontent.com/IAZ-A3/DevAgent/develop/install.sh | bash
```

### Updating

```bash
npx devagent-cc@latest
```

Same command — the installer detects your current version and offers to update.

### Uninstalling

```bash
npx devagent-cc@latest --global --uninstall
```

---

## Getting Started

Once installed, open any project in Claude Code and type:

**New project — starting from scratch:**
```
/deva:new
```

**Existing project — code already written, no paper trail:**
```
/deva:onboard
```

**Not sure where you are?**
```
/deva:status
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/deva:new` | Start a new project from scratch |
| `/deva:onboard` | Onboard an existing project with no paper trail |
| `/deva:resume` | Resume an interrupted session from checkpoint |
| `/deva:status` | Project status — current phase, plan progress, open bugs |
| `/deva:requirements` | Run or update the Requirements phase |
| `/deva:plan` | Run or update the Planning phase |
| `/deva:design` | Run or update the Design phase |
| `/deva:implement [task]` | Implement features — optionally pass a task ID |
| `/deva:verify` | Run Verification & Validation against the PRD |
| `/deva:release [version]` | Package and release — optionally pass a version number |
| `/deva:fix [BUG-ID]` | Fix a bug — optionally pass a bug ID or description |
| `/deva:feature [description]` | Add a new feature via change request flow |
| `/deva:audit` | Full health check — traceability, coverage, plan consistency |
| `/deva:checkpoint` | Save a manual checkpoint before ending your session |
| `/deva:upgrade` | Check for and apply DevAgent updates from this repo |

Commands accept optional arguments:
```
/deva:implement TASK-005
/deva:fix login crashes on empty password
/deva:release v1.2.0
/deva:feature dark mode support
```

---

## How Phase Gates Work

Every phase ends with a gate. DevAgent stops and presents the result — you decide whether to continue:

```
Phase gate: Requirements → Planning

Gate result: PASS

Artifacts produced:
  ✓ docs/PRD.md — 12 features, 0 BLOCKING issues

Checkpoint saved: .claude/skills/state/requirements/checkpoint.md

Approve to continue to Planning, or end session here.
```

Gates can be `PASS`, `PASS_WITH_BUGS`, or `FAIL`. DevAgent never auto-chains phases.

---

## Profiles

DevAgent auto-detects your project type from `PROJECT.md` and loads the appropriate profile.

### Web Profile
**Activates on:** `web`, `webapp`, `React`, `Vue`, `Next`, `frontend`, `fullstack`

Adds web-specific NFRs (Core Web Vitals, accessibility, SEO), Cloudflare Pages/Workers deployment pipeline, and web-specific V&V checks.

### macOS Profile
**Activates on:** `macos`, `mac app`, `swift`, `swiftui`, `menubar`

Adds SwiftUI component builder with MVVM conventions, entitlements and privacy manifest configurator, and a 10-step release pipeline: archive → sign → notarize → staple → DMG.

---

## Onboarding an Existing Project

`/deva:onboard` handles projects started without DevAgent:

1. **Project detection** — identifies language, framework, source locations (no `src/` assumption)
2. **Artifact scan** — reads README, docs, git log, branch history
3. **Code analysis** — reverse-engineers features with HIGH/MEDIUM/LOW confidence scoring
4. **Gap interview** — asks what's missing, what's planned, what debt exists
5. **PRD reconstruction** — full PRD with `AS-BUILT` / `PARTIAL` / `PLANNED` status per feature
6. **Paper trail** — reconstructs `Plan.md` (DONE/TODO split) and design docs
7. **Re-entry decision** — you choose which phase to resume

---

## Project Structure

After running `/deva:new` or `/deva:onboard`, your project will look like:

```
your-project/
├── CLAUDE.md                          ← DevAgent master config
├── PROJECT.md                         ← Your project identity and conventions
├── VERSION
├── CHANGELOG.md
├── docs/
│   ├── PRD.md                         ← Requirements (source of truth)
│   ├── Plan.md                        ← Task plan with DONE/TODO status
│   ├── VV-Report.md                   ← Verification report
│   ├── MAINTENANCE-LOG.md
│   └── design/
│       ├── DesignIndex.md
│       ├── SystemArchitecture.md
│       ├── TechnologyStack.md
│       └── ...
└── .claude/
    ├── commands/                      ← All /deva: commands
    └── skills/
        ├── deva/                      ← DevAgent skills
        │   ├── _shared/
        │   ├── requirements/
        │   ├── planning/
        │   ├── design/
        │   ├── implementation/
        │   ├── verification/
        │   ├── release/
        │   ├── maintenance/
        │   ├── onboarding/
        │   ├── web-profile/
        │   └── macos-profile/
        └── state/                     ← Runtime: checkpoints, artifact registry
```

---

## Versioning

DevAgent uses semantic versioning: `MAJOR.MINOR.PATCH`

| Bump | When |
|------|------|
| MAJOR | Breaking changes — artifact format, phase redesign, ID convention changes |
| MINOR | New skills, commands, or profiles — fully backward compatible |
| PATCH | Bug fixes and clarifications — safe to apply without review |

Current version: **1.1.0**

---

## License

[Apache 2.0](./LICENSE) — use freely, modify as needed, contributions welcome.

---

## Contributing

Issues and pull requests are welcome. When proposing changes to skill files, please include:
- Which phase or command is affected
- What problem the change solves
- Whether it is a MAJOR / MINOR / PATCH change