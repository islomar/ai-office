# AI Office aka Home Repo

My AI-native workspace.
It holds what I and my coding agents need across all my projects: skills, decisions, knowledge and tasks.
The code of each project stays in its own repository.

This repository is public, to show what I am doing, testing and learning.
Anything private goes to a separate private repository.

## Origins of the idea

- Eduardo Ferro's blog post
[Turning up the dial: seeing the forest while working on any tree](https://www.eferro.net/2026/10/turning-up-dial-seeing-forest-while.html).
- Matt Pocock's Home Repo
  - [The Home Repo: The effortless multi-repo agent setup](https://www.youtube.com/watch?v=hWe-j78vNpc)
  - [The Home Repo Pattern](https://www.aihero.dev/the-home-repo-pattern)
  - [Home Repo](https://www.aihero.dev/ai-coding-dictionary/home-repo)

## The idea in three rules

This repository follows
[Turning up the dial: seeing the forest while working on any tree](https://www.eferro.net/2026/10/turning-up-dial-seeing-forest-while.html).

1. **If it is not in this repository, it does not exist.**
   A learning that only lives in an agent's memory or in my head is lost.
   Write it here.
2. **Delegate to agents only as far as the safety net allows.**
   The safety net is small steps, tests, checks and validation where the code runs.
3. **A rule that keeps being broken becomes a tool or a check, not more text.**
   For example, `make check` fails when a record has a wrong ID, so nobody has to remember the ID format.

## Back after months away? Start here

1. The repository must be at `~/workspace/ai-office`.
   Skills and scripts use that path.
2. Run the setup once per machine:

   ```bash
   cd ~/workspace/ai-office
   make setup         # installs Python dependencies with uv, turns on the pre-commit hook
   make link-skills   # makes every skill here available to Claude Code in all repositories
   make link-instructions   # points every agent's global rules file at instructions/
   make check         # runs the tests and checks every record: it must say "ok"
   ```

3. See what exists:

   ```bash
   make skills        # the skills, one line each
   ls decisions/      # what was decided, and why
   ls knowledge/      # what was learned
   ls tasks/          # what is pending
   ```

4. Read [AGENTS.md](AGENTS.md): it holds the rules that agents follow here.

Requirements: [uv](https://docs.astral.sh/uv/), `make`, `git`, the `gh` CLI logged in, and Node.js 22.20 or later for the skills CLI.

## What goes in each folder

| Folder | What goes in it | Example | How to add one |
| --- | --- | --- | --- |
| `instructions/` | My global rules for every coding agent: how I want them to work in any project | `AGENTS.md`: ask before risky operations, verify before claiming | Edit `AGENTS.md`; it applies at once in every agent |
| `skills/` | Agent skills: a flow an agent follows, one folder per skill with a `SKILL.md` | `skills/ship/SKILL.md`: lint, commit and push | Create `skills/<name>/SKILL.md`, then `make link-skills` |
| `decisions/` | Decision records: what I decided, why, and what it costs | `DR-48d815`: one public repository, skills installable one by one | `uv run ai-office new decision "Title"` |
| `knowledge/` | Durable learnings any agent can read, instead of per-user agent memory | How a tool behaves, a pitfall, a working setup | `uv run ai-office new knowledge "Title"` |
| `tasks/` | Pending work for this repository, one file per task, with a why and a status | Move a skill here from another repository | `uv run ai-office new task "Title"` |
| `templates/` | Files that tools copy into other repositories | `skills-update.yml`: the weekly skill update workflow | Add the file and the tool that copies it |
| `tools/` | Python code behind the `ai-office` command | `skills.py`: list and install skills | Add code with tests in `tests/` |
| `tests/` | Tests for `tools/` and `templates/` | `test_skills.py` | `make test` runs them |
| `.githooks/` | The pre-commit hook: runs `make check` before every commit | | `make setup` turns it on |

Each of `tasks/`, `decisions/` and `knowledge/` has a README with its required front matter and statuses.
Create records with `uv run ai-office new`, never by hand: it adds a random ID (for example `DR-48d815`), so two sessions never pick the same number.

## Two kinds of skills

| Kind | Where it runs | How it gets there | Examples |
| --- | --- | --- | --- |
| **Personal** | In every repository on my machine, only for me | A link in `~/.claude/skills/`, made by `make link-skills` | `ship`, `list-my-skills`, `install-my-skill` |
| **Project** | In one repository, for anyone and any CI agent working on it | A committed copy in that repository, made by `/install-my-skill` | A review checklist for one project's tickets |

A personal skill may depend on my machine: `ship` uses scripts from my dotfiles.
A project skill must work on any machine that clones the repository.

## How to

### Change my global rules for agents

Edit `instructions/AGENTS.md`.
Every agent reads it through a link, so the change applies at the next session start:

| Agent | Its global rules file, linked by `make link-instructions` |
| --- | --- |
| Claude Code | `~/.claude/CLAUDE.md` → `instructions/CLAUDE.md`, which imports `AGENTS.md` and `RTK.md` |
| Codex | `~/.codex/AGENTS.md` → `instructions/AGENTS.md` |
| OpenCode | `~/.config/opencode/AGENTS.md` → `instructions/AGENTS.md` |
| Pi | `~/.pi/agent/AGENTS.md` → `instructions/AGENTS.md` |
| GitHub Copilot CLI | `~/.copilot/copilot-instructions.md` → `instructions/AGENTS.md` |
| Gemini CLI and Antigravity CLI (`agy`) | `~/.gemini/GEMINI.md` → `instructions/AGENTS.md`. Both read this file. Do not add `~/.gemini/AGENTS.md`: `agy` also reads that name, and would load the rules twice |

Hermes has no global rules file, and Cursor keeps global rules only in its settings screen.
Only Claude Code, Copilot and Gemini understand `@file` imports, so `AGENTS.md` must never contain one: a test checks it.
A new agent: add its path to `INSTRUCTION_LINKS` in the `Makefile` and to the test in `tests/test_instructions.py`.

### Use a skill

In Claude Code, type `/<skill-name>`, for example `/ship`.
Skills in `skills/` work in every repository after `make link-skills`.

### Create a new skill

1. Create `skills/<name>/SKILL.md` with front matter `name` and `description`.
   The description says when to use it: agents read it to decide.
2. Put any script the skill needs in `tools/`, with tests.
3. Run `make link-skills`, then try `/<name>` in a new Claude Code session.
4. Commit and push with `/ship`.

### Change a skill

Edit `skills/<name>/SKILL.md`.
On this machine the change applies at once, because `~/.claude/skills/<name>` is a link to this folder.
Push it with `/ship`.
Repositories that hold a copy get a pull request with the change the next Monday (see below).

### List my skills

`/list-my-skills` in Claude Code, or `make skills` here.
Run in another repository, it also marks the skills installed there.

### Install a skill into another repository

In that repository, run `/install-my-skill <name>`.
It checks the skill is pushed, shows what it will do and waits for my yes. Then it:

1. installs the skill with the skills CLI into `.agents/skills/<name>`, with a link in `.claude/skills/<name>`, and records it in `skills-lock.json`;
2. adds the workflow `.github/workflows/skills-update.yml`;
3. allows GitHub Actions to open pull requests in that repository, if it was not allowed.

It does not commit: review the files, then `/ship` or commit by hand.

Without Claude Code, the same steps by hand:

```bash
uv run --project ~/workspace/ai-office ai-office install-plan <name>   # checks and prints the command
npx -y skills@1.7.6 add islomar/ai-office --skill <name> -a claude-code -a opencode -y
uv run --project ~/workspace/ai-office ai-office write-workflow
```

### Keep installed skills up to date

Nothing to do.
Every Monday at 06:00 UTC, `skills-update.yml` checks each repository's skills against this repository.
When a skill changed, it opens a pull request "Update skills from ai-office". Review it and merge it.
To run it now: the repository's Actions tab, "Update skills", "Run workflow".

Pull requests opened by that workflow do not start the repository's other workflows, so CI does not run on them.

### Update the skills CLI version

The skills CLI is pinned to one version (now 1.7.6), so a new and possibly compromised npm release never runs unnoticed.
`/install-my-skill` says `UPDATE AVAILABLE` when a newer release has been public for at least 7 days.
Then:

1. Read the release notes of the new version.
2. Change the version in three places:
   - `SKILLS_CLI_PINNED` in `tools/ai_office/skills.py`
   - `SKILLS_CLI` in `templates/skills-update.yml`
   - the allow rule `Bash(npx -y skills@<version> *)` in `~/.claude/settings.json`
3. Run `make check`: a test fails if the first two disagree.
4. Run `/install-my-skill` in each repository that has the workflow: it reports the workflow as outdated and rewrites it.

### Record a decision, a learning or a task

```bash
uv run ai-office new decision "Use X instead of Y"
uv run ai-office new knowledge "How X behaves when Y"
uv run ai-office new task "Do X"
```

Each command prints the new file. Open it and fill the sections its folder README describes.

## Rules

- Nothing private: no credentials, hostnames, machine state, names of other people, employers or clients.
- Run `make check` before committing. The pre-commit hook runs it too.
- Commit on `main`, in small steps.
- Knowledge goes in `knowledge/`, never in per-user agent memory.
  `make check` fails if an instruction file points to that memory.

## When something does not work

| Symptom | Fix |
| --- | --- |
| A skill does not appear in Claude Code | Run `make link-skills`, then start a new session |
| `/install-my-skill` says `BLOCKED: ... not pushed` | Commit and push this repository first: the skills CLI installs from GitHub |
| `npx -y skills@...` asks for permission | The allow rule in `~/.claude/settings.json` does not match the pinned version |
| `make check` fails | Read the file and line it prints. Records need the front matter their folder README lists |
| The update workflow never opens a pull request | In the repository: Settings, Actions, General, allow GitHub Actions to create pull requests. `install-plan` prints the command |

## License

[MIT](LICENSE)
