---
name: onboard-repo
description: Explore a code repository and explain what it is and how it works at a conceptual level. Use when the user asks for an overview of a repository, an onboarding guide, its architecture, or says /onboard-repo.
---

# Onboard a repository

Read only. Change no file until the gate in step 4.

## 1. Locate

Use the repository the user names, or the current one.
If it is listed under "Other repos" in `~/workspace/ai-office/AGENTS.md` and missing, clone it to the path shown.
Read its `AGENTS.md`, `CLAUDE.md` and `README.md` first.

## 2. Explore

Answer from the code. Cite files as `path:line`. Mark what you could not check.

1. Purpose: what the project does and the problem it solves.
2. Domain: the core concepts and the business area.
3. Components: the main modules and how they interact, by layer.
4. Stack: languages, frameworks and key dependencies.
5. Flow: the main user flow or data flow.
6. Tests: the strategy, the boundaries, the use of test doubles, and the unit, integration and acceptance tests.
7. Conventions: the code conventions in use.
8. Decisions: unusual architecture decisions, constraints and limits.
9. Development: how to install, run and test it.

## 3. Report

Start with a Mermaid architecture diagram. Then write one short section per question.

## 4. Gate

Stop and offer these next steps:

- Design review: where the core domain concept lives, which responsibilities are mixed, and where logic should move.
- Save the report in the repository as `docs/onboarding.md`.
- Go deeper into one component.

Wait for the user's choice.
