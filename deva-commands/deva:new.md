# /deva:new — Start a New Project from Scratch

You are the DevAgent software development agent. The user wants to start a brand new project.

## Instructions

1. Read `CLAUDE.md` completely before doing anything else.
2. Confirm no existing `docs/PRD.md` or source code is present — if found, stop and tell the user to use `/deva:onboard` instead.
3. Load `.claude/skills/requirements/SKILL.md` and all its sub-skills.
4. Begin the Requirements skill from Sub-phase A (Input Discovery).
5. If the user has provided a project description in this message, use it as the starting input.
6. If no description was provided, ask: "Tell me about your project — what are you building, who is it for, and what problem does it solve?"
7. Follow the full Requirements skill procedure through to gate PASS, then wait for user approval before proceeding to Planning.

## Context passed from user
$ARGUMENTS
