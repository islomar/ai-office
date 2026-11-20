---
id: T-5c680c
title: Turn the factory memory and secret hooks into hooks for every repo
status: open
created: 2026-11-20
---

## Turn the factory memory and secret hooks into hooks for every repo

### Why

Hypothesis: rule zero bans harness memory, but `make check` only checks instruction files.
A hook that blocks memory writes and secret reads in every repo enforces the rule where it is broken.

### Steps

1. Read `factory/hooks/deny_agent_memory_writes.py` and `factory/hooks/deny_secret_reads.py` in corporate-hotel-booking-software-factory.
2. Remove their imports of factory helpers.
3. Decide where they live: `ai-office/tools/` with tests, linked into user-level settings by a `make` target.
4. Keep the factory copies until the factory can use the shared ones.

### Log

- 2026-11-20: created during the review of my other repos (DR-03274c).
