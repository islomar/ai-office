---
id: K-e86eb5
title: Dependency release age applies at lock time
updated: 2026-11-20
---

## Dependency release age applies at lock time

A dependency cooldown (`min-release-age` in npm, `exclude-newer` in uv) filters versions when the lockfile is written.
Installing from an existing lockfile ignores it: `npm ci`, `uv sync --locked` and `uv sync --frozen` install what the lockfile says,
even a version published one day earlier.

### Why

A cooldown set only in the install config gives no protection against a lockfile that already holds a fresh release.

### How to apply

- Check every lockfile change in CI against the cooldown window, with a script that reads the publish dates.
- npm reads `min-release-age` in whole days: `7`, not `7d`. npm before 11.10 ignores it.
- With uv, `exclude-newer` also blocks `uv lock --upgrade-package` for a security fix younger than the window.
  Dependabot uses that command, so it cannot open such a PR.

Source: [release-age-applies-at-lock-time.md](https://github.com/islomar/corporate-hotel-booking-software-factory/blob/main/docs/knowledge/release-age-applies-at-lock-time.md)
in corporate-hotel-booking-software-factory, checked on 2026-11-06 and 2026-11-10.
