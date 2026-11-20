---
id: DR-03274c
title: Make ai-office the Home Repo that points at my other repos
status: accepted
date: 2026-11-20
---

## Make ai-office the Home Repo that points at my other repos

### Context

Matt Pocock's Home Repo pattern: one repository holds the shared skills, instructions and docs, and points at the other repositories.
DR-48d815 already made `ai-office` the workspace, but no agent could find my other repositories from here.
An inventory on 2026-11-19 found 81 git repositories under my home folder.
15 are mine with a commit in the last 3 months.
The rest are clones of other people's repositories and tool installs.
Shared material outside `ai-office` was one skill (`spec-polish`) and a prompt library, both in `my-notes`.

### Decision

- `ai-office` is the Home Repo. Sessions that span several repositories start here.
- The root `AGENTS.md` has an "Other repos" section.
  Each pointer gives the name, what it is, the local path, the clone remote, and hints when needed.
- A repository of mine gets a pointer when it has a commit in the last 3 months.
  Clones of other people's repositories and tool installs get none.
- Private repositories are listed by name under their own heading.
  The name of a repository I own is not private material.
  Descriptions name no other people, employers or clients.
- The pointers stay in `AGENTS.md` until about 20 repositories, then move to one file per area.
- Shared skills live in `skills/` and reach every repository through `make link-skills`.
  Repository-specific skills, decision records and docs stay in their repository.
  Skills installed from published repositories stay installed.
- Reusable prompts live in `prompts/`.
  A prompt becomes a skill only when it is a flow with phases and gates.
- Material that moves out of another repository is removed there with a commit on `main`, with no branch.
  Pushing waits for my go.
- Later changes to these rules get a new decision record that links to or supersedes this one.

### Consequences

- The pointers go stale unless I update them when I create or abandon a repository.
  T-9eab99 proposes a check for this.
- A session started here does not load another repository's `CLAUDE.md`, hooks or settings.
  The pointers say so, and the hotel booking factory pointer repeats its commit rule.
- The hotel booking factory keeps its own copy of the writing-style rule: its agents may run without my global instructions.
- The prompts lost the names of their authors and of a project, to respect the public rule.
