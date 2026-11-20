---
id: K-85d0ea
title: Gates read raw exit codes, not filtered output
updated: 2026-11-20
---

## Gates read raw exit codes, not filtered output

The RTK hook rewrites shell commands and summarizes their output, so the text an agent sees can be wrong.
On 2026-11-05 a filtered pytest run said `No tests collected`, while the real run passed 3 tests with exit code 0.
On 2026-11-19 two `find` commands came back empty or cut short until they ran as `rtk proxy find`.
The source learning does not name the filter; RTK is the only output filter on this machine.

### Why

A gate that parses filtered text can pass broken work or block good work.

### How to apply

- A gate, check or script decides on the exit code of the raw command, never on its printed summary.
- When the exact output matters, run `rtk proxy <cmd>`.
- An empty or odd result from a search is a reason to rerun it with `rtk proxy` before drawing a conclusion.

Source: [gates-trust-exit-codes.md](https://github.com/islomar/corporate-hotel-booking-software-factory/blob/main/docs/knowledge/gates-trust-exit-codes.md)
in corporate-hotel-booking-software-factory.
