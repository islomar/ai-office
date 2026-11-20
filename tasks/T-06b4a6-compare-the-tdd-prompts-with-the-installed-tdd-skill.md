---
id: T-06b4a6
title: Compare the TDD prompts with the installed tdd skill
status: open
created: 2026-11-20
---

## Compare the TDD prompts with the installed tdd skill

### Why

Hypothesis: the prompts in `prompts/tdd/` have gates that the installed `mattpocock-skills:tdd` skill lacks,
such as "name the next test, do not write it" and "list refactors, write nothing".
Keeping only those gates would give one TDD flow instead of two.

### Steps

1. Read the installed `tdd` skill and the five prompts.
2. List the behaviour the prompts add.
3. Decide: a small skill in `skills/`, a note in `knowledge/`, or discard the prompts.

### Log

- 2026-11-20: created during the Home Repo setup (DR-03274c).
