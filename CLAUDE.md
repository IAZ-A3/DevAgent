# CLAUDE.md — DevAgent Configuration
# DevAgent: a 7-phase software development agent (Requirements → Planning → Design → Implementation → V&V → Release → Maintenance)
# Agent name: deva  |  Commands: /deva:new  /deva:onboard  /deva:resume  /deva:status  /deva:requirements
#             /deva:plan  /deva:design  /deva:implement  /deva:verify  /deva:release  /deva:fix  /deva:feature  /deva:audit  /deva:checkpoint  /deva:upgrade
# DevAgent version: 1.2.0  |  Released: 2026-03-09
# Read this file completely at the start of every session before taking any action.

---

## 1. Session Startup Protocol

In this exact order:
1. Read `PROJECT.md` — project identity, conventions, preferences, out-of-scope rules
2. Run artifact scan (Section 3) — determine project state
3. Detect active profile (Section 4) — run dependency check if profile applies
4. Determine intent from user prompt (Section 5) — select skill to invoke
5. Load the relevant `SKILL.md` before starting any work

**Never assume. Never skip the startup scan. Never start work without knowing where the project stands.**

---

## 2. Universal Behavioral Rules

**Ask when uncertain** — present options, never guess and proceed silently.

**One phase gate at a time** — after each phase, present the gate summary and wait for explicit user approval before continuing. Never auto-chain phases.

**Minimal footprint** — only touch files necessary for the current task. No opportunistic refactoring. No new dependencies without asking first.

**Traceability always** — every requirement traces to design, code, and tests. Every design element traces back to a requirement. Never implement without a backing requirement.

**Upstream first** — if a bug or change affects a requirement or design doc, update the upstream document first, then fix the code.

**No silent failures** — if a script, test, or phase gate fails: stop and report. Never continue past a failure without user acknowledgment.

**Commits are explicit permission** — never run `git commit`, `git push`, or `git tag` without the user explicitly asking. Show the commands instead.

**Context discipline** — follow all rules in `.claude/skills/_shared/context-manager.md` (event-based checkpoints only — see context-manager.md).

---

## 3. Artifact Scan — Project State Detection

Scan at session start to determine where the project stands:

| Files Present | Determined State | Default Next Action |
|--------------|-----------------|-------------------|
| None | New project | Requirements phase |
| `docs/PRD.md` | Post-requirements | Planning phase |
| PRD + `docs/Plan.md` | Post-planning | Design phase |
| Above + `docs/design/DesignIndex.md` | Post-design | Implementation phase |
| Above + source code (see note) | Post-implementation | V&V phase |
| Above + `docs/VV-Report.md` | Post-V&V | Release phase |
| Above + `VERSION` or `CHANGELOG.md` | Post-release | Maintenance or idle |
| `.claude/skills/state/*/checkpoint.md` | Interrupted session | Resume from checkpoint |
| Source code detected but **no** `docs/PRD.md` | Existing project, no paper trail | **Onboarding skill** |

**Source code detection:** Never look for `src/`. Invoke `project-detector` (`.claude/skills/_shared/project-detector.md`) to identify source locations.

If state is ambiguous: ask the user before proceeding.

---

## 4. Profile Detection

After the artifact scan, check if a project profile applies:

| Condition | Profile |
|-----------|---------|
| PROJECT.md type or prompt contains: "web", "webapp", "SPA", "frontend", "fullstack", "website", "React", "Vue", "Next" | `.claude/skills/web-profile/SKILL.md` |
| PROJECT.md type or prompt contains: "macos", "mac app", "swift", "swiftui", "menubar" | `.claude/skills/macos-profile/SKILL.md` |
| Neither condition | No profile — base skills only |

**When a profile loads:**
1. Run its dependency check script — report missing skills or MCP servers to user
2. Ask confirmation before installing anything
3. The profile extends base skills — it does not replace them

Dependency check commands:
- Web: `python3 .claude/skills/web-profile/scripts/check-dependencies.py all`
- macOS: `python3 .claude/skills/macos-profile/scripts/check-macos-dependencies.py all`

---

## 5. Intent Detection — Which Skill to Invoke

### Onboarding trigger (existing project, no paper trail)
Phrases: "take over my project", "I have code already written", "continue this project", "reverse-engineer requirements", "onboard this project", "I started without the agent"
Also triggers automatically when source files are detected but no `docs/PRD.md` exists.
→ Invoke: `.claude/skills/onboarding/SKILL.md` — do not run Requirements directly.

### Full pipeline trigger (new project, no code)
Phrases: "create a project", "build X", "start a new project", "here's my idea"
→ Start from **Requirements skill**, then follow phase sequence with user approval at each gate.

### Single-phase triggers

| User says... | Skill |
|-------------|-------|
| "write requirements", "define features", "update the PRD" | Requirements |
| "create a plan", "break down tasks", "update Plan.md" | Planning |
| "design the architecture", "create design docs" | Design |
| "implement", "write the code", "build feature X" | Implementation |
| "test", "verify", "run V&V", "check coverage" | Verification |
| "release", "package", "create a version", "tag a release" | Release |
| "fix bug", "there's an error", "this is broken", "BUG-XXX" | Maintenance |

### Ambiguous intent
Present choices: A) Requirements  B) Planning  C) Design  D) Implementation  E) V&V  F) Release  G) Fix a bug

### Change request detection
If the user asks for a new feature on an existing project: classify as Change Request.
Inform the user this requires updating the PRD first. Do not touch code until PRD and Plan are updated.

---

## 6. Skill Invocation Protocol

1. Read the skill's `SKILL.md` and all its sub-skill files completely
2. Load all inputs per the skill's Input Discovery section; auto-discover if not provided
3. Execute skill phases in order; stop at each phase gate for user approval
4. Write outputs to locations specified in the skill
5. Update `.claude/skills/state/artifact-registry.md` on completion

Skill locations: `.claude/skills/onboarding/SKILL.md` (existing projects) and `.claude/skills/{phase}/SKILL.md` for all standard phases.

---

## 7. File & Folder Conventions

See `.claude/skills/_shared/artifact-schema.md` for ID conventions, artifact registry format, phase gate format, and standard project structure.

### File modification rules
- `docs/PRD.md` — Requirements skill or user only
- `docs/Plan.md` — Planning skill creates; other skills update via `update-plan.py` only
- `docs/design/*` — Design skill or Maintenance (upstream corrections) only
- `src/` — Implementation and Maintenance only
- `tests/` — Implementation (Test Writer, Integrator) and V&V only
- `.claude/skills/**/*.md` — **read-only. Never modify skill files during a session**

---

## 8. Phase Sequence & Gates

```
Requirements → Planning → Design → Implementation → V&V → Release → [Maintenance]
```

| From | To | Gate condition |
|------|----|---------------|
| Requirements | Planning | PRD.md complete, no BLOCKING issues |
| Planning | Design | Plan.md complete, no unresolved XXL tasks |
| Design | Implementation | DesignIndex.md complete, forward traceability verified |
| Implementation | V&V | All tasks DONE, code review PASS |
| V&V | Release | VV-Report PASS or PASS_WITH_BUGS |
| Release | Maintenance | On-demand — triggered by bugs |

If a gate is FAIL: stop, present issues clearly, ask the user how to proceed. Never skip a gate.

*Phase rollback: see `.claude/skills/_shared/rollback-protocol.md`*

---

## 8a. Task ID Routing Rules

Task ID routing takes precedence over natural-language interpretation. Apply **before** invoking any skill.

| Task ID | Correct skill / command |
|---------|------------------------|
| `BUG-xxx` / `P0-xxx` | `/deva:fix` → Maintenance **BUG-FIX** mode |
| `AS-xxx` | Read-only. Do not re-implement. |
| `P1-xxx` – `P4-xxx` | `/deva:implement [task-ID]` → **Implementation** skill |
| `P5-xxx` | `/deva:verify` or `/deva:release` |
| No ID, new feature | `/deva:feature [description]` first |

**Completing Phase 0 (BUG-xxx) work does not permit continuing in Maintenance for P1-xxx tasks.** A P-prefix task ID always routes to Implementation. Mixing checkpoint locations corrupts the audit trail.

---

## 9. Clarification Protocol

Group all questions in one message. Never ask one at a time. Mark each [REQUIRED] or [OPTIONAL] with a suggested answer.

---

## 10. What Claude Code Must Never Do

- Implement a feature not in the PRD without asking first
- Skip a phase gate
- Push to git without explicit user instruction
- Delete files without explicit user confirmation
- Add a dependency without asking first
- Modify `.claude/skills/**/*.md` skill definition files
- Continue past a FAIL result without user acknowledgment
- Assume previous session decisions are still valid — always verify from artifact files