---
id: T-1c574c
title: Add a make help target to my other repositories
status: open
created: 2026-11-20
---

## Add a make help target to my other repositories

### Why

The global rule says the Makefile lists everything a repository can run.
Repositories whose Makefile has no `help` target and no `##` descriptions break that rule.

### Steps

In each repository below, make `help` the default target, as in `ai-office/Makefile`, and add a `##` description to every target.
Do one repository per session, or a batch when asked.

- [ ] dotfiles
- [ ] my-notes
- [ ] typescript-kata-template
- [ ] python-kata-template
- [ ] java-kata-template
- [ ] my-nvc-app
- [ ] islomar.github.io
- [ ] poc-postgresql

corporate-hotel-booking-software-factory already has it.
Repositories without a Makefile get one only when they first need a command.

### Log

- 2026-11-20: created when `ai-office` got `make help` (Round 7 of the Home Repo setup).
