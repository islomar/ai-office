---
name: list-my-skills
description: List the skills kept in ~/workspace/ai-office/skills and show which ones the current repository already has. Use when the user says /list-my-skills, asks which of their skills exist, or before /install-my-skill.
---

# List my skills

Run from the current repository:

```bash
make -s -C ~/workspace/ai-office skills REPO="$PWD"
```

Show the output as a table: name, description, installed here (yes or no).
Do not install or change anything.
To install one, the user runs `/install-my-skill <name>`.
