.DEFAULT_GOAL := help

.PHONY: help setup check test records tasks new-task new-decision new-knowledge skills link-skills link-instructions install-plan write-workflow lint-md

help: ## List targets
	@grep -E '^[a-zA-Z0-9_-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-18s %s\n", $$1, $$2}'

setup: ## Install Python dependencies with uv and turn on the pre-commit hook
	uv sync
	git config core.hooksPath .githooks

check: test records ## Run the tests and check every record (the pre-commit gate)

test: ## Run the tests of tools/
	uv run pytest -q

records: ## Check every record and instruction file
	uv run ai-office check

tasks: ## List the tasks that still need work, in progress first
	@uv run ai-office list-tasks

new-task: ## Create a task: make new-task TITLE="Short imperative title"
	@test -n "$(TITLE)" || { echo 'Usage: make new-task TITLE="..."'; exit 1; }
	uv run ai-office new task "$(TITLE)"

new-decision: ## Create a decision record: make new-decision TITLE="..."
	@test -n "$(TITLE)" || { echo 'Usage: make new-decision TITLE="..."'; exit 1; }
	uv run ai-office new decision "$(TITLE)"

new-knowledge: ## Create a knowledge record: make new-knowledge TITLE="..."
	@test -n "$(TITLE)" || { echo 'Usage: make new-knowledge TITLE="..."'; exit 1; }
	uv run ai-office new knowledge "$(TITLE)"

skills: ## List the skills in skills/, marking those installed in REPO (default: here)
	@uv run --project "$(CURDIR)" ai-office list-skills --repo "$(or $(REPO),$(CURDIR))"

# Make every skill in skills/ available to Claude Code in all repositories on this machine.
link-skills: ## Link every skill in skills/ into ~/.claude/skills
	mkdir -p "$(HOME)/.claude/skills"
	for dir in "$(CURDIR)"/skills/*/; do \
		[ -d "$$dir" ] || continue; \
		ln -sfn "$${dir%/}" "$(HOME)/.claude/skills/$$(basename "$$dir")"; \
		echo "linked $$(basename "$$dir")"; \
	done

# Point every agent's global instructions file at instructions/.
# Claude Code reads CLAUDE.md, which imports AGENTS.md and RTK.md (linked next to it).
# The other agents cannot import files, so they read AGENTS.md directly.
# A regular file in the way is kept as <file>.bak-<date>.
INSTRUCTIONS := $(CURDIR)/instructions
INSTRUCTION_LINKS := \
	.claude/CLAUDE.md:CLAUDE.md \
	.claude/AGENTS.md:AGENTS.md \
	.claude/RTK.md:RTK.md \
	.codex/AGENTS.md:AGENTS.md \
	.config/opencode/AGENTS.md:AGENTS.md \
	.pi/agent/AGENTS.md:AGENTS.md \
	.copilot/copilot-instructions.md:AGENTS.md \
	.gemini/GEMINI.md:AGENTS.md

link-instructions: ## Point every agent's global rules file at instructions/
	@for pair in $(INSTRUCTION_LINKS); do \
		target="$(HOME)/$${pair%%:*}"; source="$(INSTRUCTIONS)/$${pair##*:}"; \
		mkdir -p "$$(dirname "$$target")"; \
		if [ -f "$$target" ] && [ ! -L "$$target" ]; then \
			mv "$$target" "$$target.bak-$$(date +%Y%m%d)"; echo "backed up $$target"; \
		fi; \
		ln -sfn "$$source" "$$target"; echo "linked $$target -> $$source"; \
	done

# Both run in the target repository: the commands read and write the current directory.
install-plan: ## Check a skill can be installed in a repo: make install-plan SKILL=<name> REPO=<path> [AGENTS="claude-code opencode"]
	@test -n "$(SKILL)" -a -n "$(REPO)" || { echo 'Usage: make install-plan SKILL=<name> REPO=<path>'; exit 1; }
	cd "$(REPO)" && uv run --project "$(CURDIR)" ai-office install-plan "$(SKILL)" $(foreach agent,$(AGENTS),--agent $(agent))

write-workflow: ## Write the skills update workflow into a repo: make write-workflow REPO=<path>
	@test -n "$(REPO)" || { echo 'Usage: make write-workflow REPO=<path>'; exit 1; }
	cd "$(REPO)" && uv run --project "$(CURDIR)" ai-office write-workflow

# Lints only changed files: Vale on the whole repository can pass the 2-minute command limit.
lint-md: ## Lint the changed and new Markdown files (or FILES="a.md b.md")
	@files="$(FILES)"; \
	[ -n "$$files" ] || files=$$( { git diff --name-only HEAD -- '*.md'; git ls-files --others --exclude-standard -- '*.md'; } | sort -u); \
	if [ -z "$$files" ]; then echo "No changed Markdown files."; else ~/.dotfiles/scripts/check-markdown.sh $$files; fi
