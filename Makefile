.PHONY: setup check test records link-skills skills

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
