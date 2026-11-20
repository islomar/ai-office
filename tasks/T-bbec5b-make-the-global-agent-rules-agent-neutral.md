---
id: T-bbec5b
title: Make the global agent rules agent-neutral
status: open
created: 2026-11-20
---

## Make the global agent rules agent-neutral

### Why

Every agent reads `instructions/AGENTS.md`, but some lines apply only to Claude Code:
the `PostToolUse` hook, the `/ship` skill and RTK. Other agents follow instructions they cannot carry out.

### Steps

Mark those lines as Claude Code only, or move them to a Claude-only file that `instructions/CLAUDE.md` imports.

### Log

- 2026-11-20: moved here from `dotfiles/TODO.md` (DR-03274c).
