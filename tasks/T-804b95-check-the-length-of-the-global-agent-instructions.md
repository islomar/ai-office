---
id: T-804b95
title: Check the length of the global agent instructions
status: open
created: 2026-11-20
---

## Check the length of the global agent instructions

### Why

Hypothesis: long global instructions get followed less.
`instructions/AGENTS.md` has 116 lines on 2026-11-20, plus `RTK.md`, and both load in every session.

### Steps

1. Find the documented guidance on instruction file length for Claude Code, and cite it.
2. Measure the files that load at session start.
3. Propose cuts or moves to skills if needed.

### Log

- 2026-11-20: created during the review of my other repos (DR-03274c).
