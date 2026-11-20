# Skills

One folder per skill: `skills/<name>/SKILL.md`, in the [Agent Skills](https://agentskills.io) format.
Scripts that a skill needs go in `tools/`, with tests, so the skill stays short.

A skill is a flow with phases and gates.
A gate is a point where the agent stops and waits for a human decision.

Install one skill in another project:

```bash
npx -y skills@1.8.1 add islomar/ai-office --skill <name> -a claude-code
```
