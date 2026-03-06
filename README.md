# DevAgent

A structured, 7-phase software development agent for Claude Code. DevAgent brings engineering discipline to AI-assisted development — requirements traceability, phase gates, checkpoints, and a consistent workflow from idea to release.

---

## What is DevAgent?

DevAgent is a configuration system for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that turns it into a disciplined software development agent. Instead of ad-hoc AI coding sessions, DevAgent gives you a repeatable process:

```
Requirements → Planning → Design → Implementation → V&V → Release → Maintenance
```

Every phase has defined inputs, outputs, and gate conditions. Nothing moves forward without your explicit approval. Every artifact is traceable — requirements link to design, design links to code, code links to tests.

---

## Key Features

- **7-phase pipeline** — structured workflow with gate conditions at every phase boundary
- **15 slash commands** — trigger any phase or action directly from Claude Code chat
- **Project onboarding** — bring an existing codebase under agent control with full reverse-engineering
- **Two profiles** — web (React, Next.js, Cloudflare deployment) and macOS (SwiftUI, code signing, notarization)
- **Context-aware checkpoints** — automatic saves at phase gates and context thresholds; resume cleanly across sessions
- **Change request flow** — new features go through PRD and Plan updates before any code is touched
- **Self-upgrading** — `/deva:upgrade` checks this repo for updates and applies them with your confirmation
- **No src/ assumption** — project detector identifies source locations for any language or framework

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — latest version
- For web projects: Node.js, Cloudflare account (optional)
- For macOS projects: Xcode, Apple Developer account, [XcodeBuildMCP](https://github.com/cameroncooke/XcodeBuildMCP)

---

## Installation

### New project (no existing code)

```bash
# 1. Clone DevAgent
git clone https://github.com/IAZ-A3/DevAgent.git

# 2. Copy into your project
cp DevAgent/CLAUDE.md your-project/
cp -r DevAgent/.claude your-project/

# 3. Open your project in Claude Code
cd your-project
claude

# 4. Start
/deva:new
```

### Existing project (code already written)

```bash
# 1. Clone DevAgent
git clone https://github.com/IAZ-A3/DevAgent.git

# 2. Copy into your project
cp DevAgent/CLAUDE.md your-project/
cp -r DevAgent/.claude your-project/

# 3. Open your project in Claude Code
cd your-project
claude

# 4. Onboard
/deva:onboard
```

### Global commands (available in all projects)

```bash
# Copy commands to Claude Code global config
cp DevAgent/.claude/commands/deva:* ~/.claude/commands/
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/deva:new` | Start a new project from scratch |
| `/deva:onboard` | Onboard an existing project with no paper trail |
| `/deva:resume` | Resume an interrupted session from checkpoint |
| `/deva:status` | Project status report — current phase, plan progress, open bugs |
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

Commands accept optional arguments. Examples:
```
/deva:implement TASK-005
/deva:fix login crashes on empty password
/deva:release v1.2.0
/deva:feature dark mode support
```

---

## Project Structure

After running `/deva:new` or `/deva:onboard`, your project will have this structure:

```
your-project/
├── CLAUDE.md                          ← DevAgent master config (do not edit)
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
    ├── registry.md                    ← Skill and MCP registry
    ├── commands/                      ← All /deva: commands
    ├── skills/                        ← Phase skills and profiles
    │   ├── _shared/                   ← Shared utilities
    │   ├── requirements/
    │   ├── planning/
    │   ├── design/
    │   ├── implementation/
    │   ├── verification/
    │   ├── release/
    │   ├── maintenance/
    │   ├── onboarding/
    │   ├── web-profile/               ← Web project extensions
    │   └── macos-profile/             ← macOS project extensions
    └── state/                         ← Runtime: checkpoints, artifact registry
```

---

## Profiles

DevAgent auto-detects your project type and loads the appropriate profile.

### Web Profile
Activates when PROJECT.md or prompt contains: `web`, `webapp`, `React`, `Vue`, `Next`, `frontend`, `fullstack`

Adds:
- Web-specific NFRs (Core Web Vitals, accessibility, SEO)
- Cloudflare Pages/Workers deployment pipeline
- Web-specific V&V (Lighthouse, cross-browser checks)
- Frontend design conventions

### macOS Profile
Activates when PROJECT.md or prompt contains: `macos`, `mac app`, `swift`, `swiftui`, `menubar`

Adds:
- SwiftUI component builder with MVVM conventions
- Entitlements and privacy manifest configurator
- 10-step release pipeline: archive → sign → notarize → staple → DMG
- XcodeBuildMCP integration
- macOS-specific NFRs (memory, launch time, VoiceOver, dark mode)

---

## How Phase Gates Work

Every phase ends with a gate. DevAgent stops and presents the gate result before proceeding:

```
Phase gate: Requirements → Planning

Gate result: PASS

Artifacts produced:
  ✓ docs/PRD.md — 12 features, 0 BLOCKING issues

Checkpoint saved: .claude/skills/state/requirements/checkpoint.md

Approve to continue to Planning, or end session here.
```

Gates can be `PASS`, `PASS_WITH_BUGS`, or `FAIL`. DevAgent never auto-chains phases — you approve each transition explicitly.

---

## Onboarding an Existing Project

`/deva:onboard` handles projects that were started without DevAgent:

1. **Project detection** — identifies language, framework, and source locations without assuming `src/`
2. **Artifact scan** — reads README, docs, git log, and branch history
3. **Code analysis** — reverse-engineers features from source with HIGH/MEDIUM/LOW confidence scoring
4. **Gap interview** — asks what's missing, what's planned, what debt exists
5. **PRD reconstruction** — produces a full PRD with AS-BUILT / PARTIAL / PLANNED status per feature
6. **Paper trail** — reconstructs Plan.md (DONE/TODO split) and design docs
7. **Re-entry decision** — you choose which phase to resume: Design, Implementation, V&V, or Maintenance

---

## Upgrading DevAgent

```
/deva:upgrade
```

The command:
1. Reads your local DevAgent version from CLAUDE.md
2. Fetches the latest version from this repo
3. Shows what changed (from CHANGELOG.md)
4. Lists which files differ
5. Asks you to confirm before updating anything
6. Creates `.backup` files before overwriting

Your project files (`docs/`, `PROJECT.md`, `.claude/skills/state/`) are never touched.

---

## Versioning

DevAgent uses semantic versioning: `MAJOR.MINOR.PATCH`

| Bump | When |
|------|------|
| MAJOR | Breaking changes — artifact format, phase redesign, ID convention changes |
| MINOR | New skills, commands, or profiles — fully backward compatible |
| PATCH | Bug fixes and clarifications — safe to apply without review |

Current version: **1.0.0**

---

## Repository Structure

```
devagent/
├── README.md
├── CHANGELOG.md
├── CLAUDE.md                          ← Copy to project root
├── PROJECT.md                         ← Base template
├── PROJECT-web-template.md
├── PROJECT-macos-template.md
└── .claude/
    ├── registry.md
    ├── commands/                      ← All 15 /deva: command files
    └── skills/
        ├── _shared/                   ← context-manager, artifact-schema,
        │                                 subagent-patterns, project-detector,
        │                                 upgrade-manifest
        ├── requirements/
        ├── planning/
        ├── design/
        ├── implementation/
        ├── verification/
        ├── release/
        ├── maintenance/
        ├── onboarding/
        ├── web-profile/
        └── macos-profile/
```

---

## License

MIT — use freely, modify as needed, contributions welcome.

---

## Contributing

Issues and pull requests are welcome. When proposing changes to skill files, please include:
- Which phase or command is affected
- What problem the change solves
- Whether it's a MAJOR / MINOR / PATCH change

---

*Built for Claude Code. Designed for engineers who want AI assistance with engineering discipline.*