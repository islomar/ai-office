---
name: install-my-skill
description: Install one skill from ~/workspace/ai-office into the current repository, committed with a lock file, through the skills CLI at a pinned version, plus a weekly workflow that opens a pull request when the skill changes. Use when the user says /install-my-skill <name> or asks to add one of their skills to this repository.
argument-hint: "<skill-name> [agent ...]"
---

# Install my skill

Input: a skill name, and optionally agents (default `claude-code` and `opencode`).
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
- `WORKFLOW:` whether `.github/workflows/skills-update.yml` is missing, outdated or current.
- `SETTING:` whether GitHub Actions may open pull requests in this repository.

## 2. Gate

Show the user, in one list:

- the repository, the skill, the agents and the `COMMAND:` line;
- the workflow action: write it, rewrite an outdated one, or nothing;
- the setting change, with its `gh api` command, when Actions cannot open pull requests.

Wait for an explicit yes. The user may accept the install and refuse the workflow or the setting.

## 3. Install

1. Run the `COMMAND:` line exactly as printed, from the repository root.
2. If accepted, run `uv run --project ~/workspace/ai-office ai-office write-workflow`.
3. If accepted, run the `gh api` command from the `SETTING:` line.
   Then rerun `install-plan` and confirm the line says Actions can open pull requests.

## 4. Report

- Run `git status --short` and list the new files: `.agents/skills/<name>`, the link in `.claude/skills/<name>`, `skills-lock.json` and the workflow.
- Say that pull requests opened by the workflow do not trigger other workflows, so CI does not run on them on its own.
- Do not commit. The user commits with `/ship` or by hand.
