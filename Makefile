.PHONY: lint lint-fix

lint:
	ruff check src

lint-fix:
	ruff --fix src
