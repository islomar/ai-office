---
id: T-ca083c
title: Review which installed skills overlap
status: open
created: 2026-11-20
---

## Review which installed skills overlap

### Why

Hypothesis: several installed skills cover the same ground, for example `grilling`, `grill-me` and `grill-with-docs`,
and the plugin copies under `mattpocock-skills:`. Overlaps make the wrong skill fire.

### Steps

1. List every skill in `~/.agents/skills`, `~/.claude/skills` and the enabled plugins.
2. Group them by purpose and mark overlaps.
3. Propose which to uninstall. Uninstall only after my yes.

### Log

- 2026-11-20: created during the review of my other repos (DR-03274c).
