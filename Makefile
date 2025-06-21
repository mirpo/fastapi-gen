.PHONY: lint lint-fix

lint:
	ruff check src/cli

lint-fix:
	ruff check --fix src
