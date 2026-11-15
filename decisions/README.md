# Decisions

One decision record per file: `DR-<6 hex>-<slug>.md`.
Create one with `uv run ai-office new decision "Title"`.
IDs use a random suffix, not a sequence, so two sessions never pick the same number.

## Front matter

```yaml
id: DR-a1b2c3
title: Short statement of the decision
status: proposed
date: 2026-11-15
```

Statuses: `proposed`, `accepted`, `superseded`, `rejected`.
A superseded record links to the one that replaces it.

## Body

Three sections: **Context**, **Decision**, **Consequences**.
