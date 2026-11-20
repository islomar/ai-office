# Tasks

One Markdown file per task: `T-<6 hex>-<slug>.md`.
Create one with `make new-task TITLE="Title"`.

## Front matter

```yaml
id: T-a1b2c3
title: Short imperative title
status: open
created: 2026-11-15
```

Statuses: `open`, `doing`, `validating`, `done`, `discarded`.

- `validating`: the change is merged, but not yet checked where it runs.
- `discarded`: a reasoned decision not to do it. Write the reason in the body.

## Body

Start with **Why**: the outcome the task is for, framed as a hypothesis when possible.
End with a short log of what happened.
