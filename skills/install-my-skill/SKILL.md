---
name: install-my-skill
description: Install one skill from ~/workspace/ai-office into the current repository, committed with a lock file, through the skills CLI at a pinned version. Use when the user says /install-my-skill <name> or asks to add one of their skills to this repository.
argument-hint: "<skill-name> [agent ...]"
---

# Install my skill

Input: a skill name, and optionally agents (default `claude-code`).
Without a name, run `/list-my-skills` and ask which one.

## 1. Plan

Run from the root of the current repository:

```bash
uv run --project ~/workspace/ai-office ai-office install-plan <name> [--agent <agent> ...]
```

- `BLOCKED:` stop and report the reason. An unpublished skill must be shipped from `~/workspace/ai-office` first.
- `UPDATE AVAILABLE:` show the message to the user word for word, then continue with the pinned version.
  Never change the pin yourself.
- `NOTE:` the permission rule is missing; the command will ask for approval.

## 2. Gate

Show the user the repository, the skill, the agents and the `COMMAND:` line.
Wait for an explicit yes.

## 3. Install

Run the `COMMAND:` line exactly as printed, from the repository root.

## 4. Report

- Run `git status --short` and list the new files: the skill folder and `skills-lock.json`.
- Do not commit. The user commits with `/ship` or by hand.
