---
id: DR-48d815
title: Keep the workspace in one public repository with skills installable one by one
status: accepted
date: 2026-11-15
---

## Keep the workspace in one public repository with skills installable one by one

### Context

My skills, agent notes and learnings are spread across several repositories and per-user harness memory.
No agent can find them all, and other people cannot see them.
I want to try several harnesses: Claude Code, OpenCode, GitHub Copilot, Pi, Hermes Agent and others.

### Decision

- One public repository, `ai-office`, holds tasks, decisions, knowledge and skills.
  Private material goes to a separate private repository when it is needed.
- Code repositories stay outside and are cloned on demand.
- Skills use the `skills/<name>/SKILL.md` layout, so the skills CLI can install one skill into many harnesses:
  `npx skills add islomar/ai-office --skill <name>`.
- `AGENTS.md` is the source of truth for agent instructions. `CLAUDE.md` only imports it.
- Records get random-suffix IDs from `uv run ai-office new`, and `make check` validates them in the pre-commit hook.
- A Claude Code plugin marketplace is postponed until a skill needs hooks or agents bundled with it.

### Consequences

- Nothing private can be written here, which limits what tasks and knowledge can say.
- Installing through the skills CLI needs Node.js 22.20 or later on the target machine.
- A Claude Code plugin would namespace skills as `/<plugin>:<skill>`, so adding one later changes how skills are invoked.
