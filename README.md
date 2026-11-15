# ai-office

My AI-native workspace: the hub for the skills, agents, workflows, decisions and knowledge I use with coding agents.
It is public on purpose, to show what I am doing, testing and learning.

It follows the approach described in
[Turning up the dial: seeing the forest while working on any tree](https://www.eferro.net/2026/10/turning-up-dial-seeing-forest-while.html):

- If it is not in the repository, it does not exist.
- Delegation to agents can only go as far as the engineering practices behind it: small safe steps, tests, trunk-based development, validation in the running system.
- Rules written as prose get ignored. Rules turned into tools and checks get followed.

## Layout

See [AGENTS.md](AGENTS.md) for the layout and the working rules that agents follow.

## Install a skill in another project

Skills live in `skills/<name>/SKILL.md`, the layout read by the [skills CLI](https://github.com/vercel-labs/skills).
It installs one skill into Claude Code, OpenCode, GitHub Copilot, Codex, Pi, Hermes Agent and other agents:

```bash
npx -y skills@1.7.6 add islomar/ai-office --list
npx -y skills@1.7.6 add islomar/ai-office --skill <name> -a claude-code -a opencode
```

The CLI version is pinned. `uv run ai-office install-plan <name>` prints the install command and says when a newer release has been public for at least 7 days.
In Claude Code, `/list-my-skills` and `/install-my-skill <name>` wrap these commands.

## Development

Requires [uv](https://docs.astral.sh/uv/) and `make`.

```bash
make setup   # install dependencies and enable the pre-commit hook
make check   # run the tests and check every record
uv run ai-office new task "Title"
```

## License

[MIT](LICENSE)
