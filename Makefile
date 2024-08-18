.PHONY: lint lint-fix

lint:
	ruff check src

lint-fix:
	ruff check --fix src
