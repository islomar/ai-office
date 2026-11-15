.PHONY: setup check test records link-skills skills link-instructions

setup:
	uv sync
	git config core.hooksPath .githooks

check: test records

test:
	uv run pytest -q

records:
	uv run ai-office check

# Make every skill in skills/ available to Claude Code in all repositories on this machine.
link-skills:
	mkdir -p "$(HOME)/.claude/skills"
	for dir in "$(CURDIR)"/skills/*/; do \
		[ -d "$$dir" ] || continue; \
		ln -sfn "$${dir%/}" "$(HOME)/.claude/skills/$$(basename "$$dir")"; \
		echo "linked $$(basename "$$dir")"; \
	done

skills:
	uv run ai-office list-skills

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

link-instructions:
	@for pair in $(INSTRUCTION_LINKS); do \
		target="$(HOME)/$${pair%%:*}"; source="$(INSTRUCTIONS)/$${pair##*:}"; \
		mkdir -p "$$(dirname "$$target")"; \
		if [ -f "$$target" ] && [ ! -L "$$target" ]; then \
			mv "$$target" "$$target.bak-$$(date +%Y%m%d)"; echo "backed up $$target"; \
		fi; \
		ln -sfn "$$source" "$$target"; echo "linked $$target -> $$source"; \
	done
