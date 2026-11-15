.PHONY: setup check test records

setup:
	uv sync
	git config core.hooksPath .githooks

check: test records

test:
	uv run pytest -q

records:
	uv run ai-office check
