# AGENTS.md

This repository is a personal AI-native workspace.
It holds tasks, decisions, knowledge and the skills that agents use to work on my personal projects and side projects.
Code repositories are not stored here: clone them on demand when a task needs them.

## Rule zero

If it is not in this repository, it does not exist.
When you learn something that a future session needs, write it into `knowledge/` or `decisions/`.
Never write it into per-user harness memory, and never point an instruction file at that memory: `make check` fails if one does.

## This repository is public

Write nothing private: no credentials, hostnames, machine state, names of other people, employers or clients.
Anything private belongs in a separate private repository.

## Layout

| Folder       | Contents                                                     |
| ------------ | ------------------------------------------------------------ |
| `tasks/`     | One file per task, with a why and a status                   |
| `decisions/` | Decision records: context, decision, consequences            |
| `knowledge/` | Durable learnings, readable by any agent harness             |
| `instructions/` | Global rules for every agent, linked into each one by `make link-instructions` |
| `skills/`    | Agent skills, one folder per skill: `skills/<name>/SKILL.md` |
| `templates/` | Files that tools copy into other repositories                |
| `tools/`     | Deterministic Python tools that skills call                  |
| `tests/`     | Tests for `tools/`                                           |

Each folder has a README with its front-matter schema.

## Working rules

- Create records with the tool, never by hand: `uv run ai-office new task|decision|knowledge "Title"`.
  It assigns a random-suffix ID, so parallel sessions never collide.
- Run `make check` before every commit. The pre-commit hook runs it too.
- Work in small, safe steps on `main`.
- Skills stop at gates and wait for a human decision before pushing, publishing or contacting anyone.
- A merged change is not done: move the task to `validating` until it is checked where it runs.
- When a rule keeps being broken, turn it into a check or a tool instead of adding more prose here.
