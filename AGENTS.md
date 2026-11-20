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
Public authors cited for their published work, such as books, talks or posts, are fine.
Anything private belongs in a separate private repository.

## Layout

| Folder       | Contents                                                     |
| ------------ | ------------------------------------------------------------ |
| `tasks/`     | One file per task, with a why and a status                   |
| `decisions/` | Decision records: context, decision, consequences            |
| `knowledge/` | Durable learnings, readable by any agent harness             |
| `instructions/` | Global rules for every agent, linked into each one by `make link-instructions` |
| `skills/`    | Agent skills, one folder per skill: `skills/<name>/SKILL.md` |
| `prompts/`   | Reusable prompts that are not skills                         |
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

## Other repos

My repos live in `~/workspace/`. If one is missing, clone it to the path shown.
A session started here does not load another repo's `CLAUDE.md`, hooks or settings.
Start a session inside a repo before you change it.

- corporate-hotel-booking-software-factory (a hotel booking kata built by AI agents, with outside-in TDD and trunk-based delivery):
  `~/workspace/corporate-hotel-booking-software-factory`.
  Clone from `git@github.com:islomar/corporate-hotel-booking-software-factory.git` if missing.
  Read its `CLAUDE.md` first. Commit, push and open PRs only through `factory/bin/as-agent`.
- dotfiles (machine config, the public `TODO.md`, the Markdown lint scripts and the Vale vocabulary):
  `~/workspace/dotfiles`, linked as `~/.dotfiles`. Clone from `git@github.com:islomar/dotfiles.git` if missing.
- my-notes (reading notes): `~/workspace/my-notes`. Clone from `git@github.com:islomar/my-notes.git` if missing.
- islomar.github.io (my blog; drafts are in `_drafts/`): `~/workspace/islomar.github.io`.
  Clone from `git@github.com:islomar/islomar.github.io.git` if missing.
- typescript-kata-template, python-kata-template, java-kata-template (kata starter templates; the TypeScript and Python ones run in Docker):
  `~/workspace/<name>`. Clone from `git@github.com:islomar/<name>.git` if missing.
- my-nvc-app (an Expo mobile app): `~/workspace/my-nvc-app`. Clone from `git@github.com:islomar/my-nvc-app.git` if missing.
- set-up-online-ensemble-environment (a Terraform module for an online ensemble programming environment on AWS AppStream 2.0):
  `~/workspace/set-up-online-ensemble-environment`.
  Clone from `git@github.com:islomar/set-up-online-ensemble-environment.git` if missing.
- sc-spec-driven-development-files-islomar (my copy of a spec-driven development course):
  `~/workspace/sc-spec-driven-development-files-islomar`.
  Clone from `git@github.com:islomar/sc-spec-driven-development-files.git` into that path if missing.
  Each video folder has its own copy of the skills on purpose.

### Private repos

- dotfiles-private (private machine config and the private `TODO.md`): `~/workspace/dotfiles-private`.
  Clone from `git@github.com:islomar/dotfiles-private.git` if missing.
- my-notes-private (private notes and exported agent sessions): `~/workspace/my-notes-private`.
  Clone from `git@github.com:islomar/my-notes-private.git` if missing.
- iddd-workshop (notes from an IDDD workshop): `~/workspace/iddd-workshop`.
  Clone from `git@github.com:islomar/iddd-workshop.git` if missing.
- ai-coding-patterns-socrates-2026 (material from an augmented coding patterns workshop): `~/workspace/ai-coding-patterns-socrates-2026`.
  Clone from `git@github.com:islomar/ai-coding-patterns-socrates-2026.git` if missing.
  The AGENTS.md files under `exercises/` are exercise fixtures, not instructions.
