---
id: T-9eab99
title: Check that every repo of mine is listed in Other repos
status: open
created: 2026-11-20
---

## Check that every repo of mine is listed in Other repos

### Why

Hypothesis: a check catches stale pointers in the "Other repos" section of `AGENTS.md`
before an agent goes looking for a repository that is not listed.

### Steps

1. Add a tool command that lists the git repositories under `~/workspace` whose remote is mine.
2. Compare them with the pointers in `AGENTS.md`, honouring the 3-month rule in DR-03274c.
3. Decide whether it runs in `make check` (it reads the machine, so the pre-commit hook may be the wrong place) or on demand.

### Log

- 2026-11-20: created during the Home Repo setup (DR-03274c).
