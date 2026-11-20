---
id: T-259c62
title: Fix install-plan with npm 12 view output
status: open
created: 2026-11-20
---

## Fix install-plan with npm 12 view output

### Why

`make install-plan` and the `install-my-skill` skill crash with `AttributeError: 'list' object has no attribute 'items'`.
With npm 12.2.3, `npm view skills time --json` returns a list that holds one object, not the object.
`fetch_release_times` in `tools/ai_office/skills.py` passes that list to `update_notice`.

### Steps

1. Add a test with the list-wrapped output.
2. Accept both shapes in `fetch_release_times`.
3. Run `make install-plan SKILL=spec-polish REPO=~/workspace/my-notes` and confirm it prints a `COMMAND:` line.

### Log

- 2026-11-20: found while smoke-testing the new `install-plan` target. The bug predates the target.
