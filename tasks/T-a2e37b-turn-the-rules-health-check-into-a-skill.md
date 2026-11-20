---
id: T-a2e37b
title: Turn the rules health check into a skill
status: open
created: 2026-11-20
---

## Turn the rules health check into a skill

### Why

Hypothesis: the instructions, decisions and knowledge here will drift like the factory's rules did.
A skill that finds duplicates, stale names and contradictions keeps them consistent.

### Steps

1. Read `docs/process/rules-health.md` and `factory/rules_health.py` in corporate-hotel-booking-software-factory.
2. Drop the Jira and factory parts. Keep the three checks.
3. Write `skills/rules-health/SKILL.md`, with any deterministic part in `tools/`.

### Log

- 2026-11-20: created during the review of my other repos (DR-03274c).
