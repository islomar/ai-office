---
id: T-35e30a
title: Build a session analysis tool and skill
status: open
created: 2026-11-16
---

## Build a session analysis tool and skill

### Why

Hypothesis: a factual list of what ran in a session makes it easier to see why a skill did not fire or a hook misbehaved.
The list covers skills, hooks, subagents and MCP calls.
Paired with a retrospective, that list turns into concrete fixes to skills, hooks and instructions.

No existing skill does both parts.
Candidates reviewed on 2026-11-16:

- `session-transcript-analyzer` (agent-studio repository): no hook names or exit codes, no suggestions, tied to its repository layout.
- `transcript-analysis` (kaizen plugin): source repository deleted; depends on a custom MCP server whose code went with the repository.
- `diagnosing-superpowers` (Superpowers): scoped to Superpowers failures, proposes no fixes, does not cover hooks.
- `retro` (`mattpocock-skills` plugin): ranks environment improvements, but does not list which skills or hooks ran.

### Plan

1. Add a deterministic tool in `tools/` that reads one transcript JSONL and prints a report:
   - `Skill` tool calls and the skill names they loaded.
   - Hook runs from `attachment` records (`hook_success` and error variants): `hookName`, `hookEvent`, `exitCode`.
   - `stop_hook_summary` system records.
   - `Agent` calls with `subagent_type`.
   - MCP tool calls (`mcp__<server>__<tool>`).
2. Add tests in `tests/` with small fixture transcripts.
3. Add a skill that runs the tool, then follows the `retro` categories to propose improvements.
4. Optional: compare against OpenTelemetry events (`claude_code.skill_activated`, `claude_code.hook_execution_complete`) as a more stable source.

### Risks

- The transcript format is internal to Claude Code and can change between versions.
  The tool must fail loudly on unknown record shapes, and the tests must pin the shapes it relies on.
- Hook stderr is only in the `--debug` log, not in the transcript.
- Error-variant hook attachments are not yet confirmed; check a session with a failing hook.

### Log

- 2026-11-16: Task created after reviewing existing skills.
- 2026-11-20: `~/workspace/dotfiles/scripts/claude-session-export` already turns a transcript into Markdown. Reuse it or build on it.
