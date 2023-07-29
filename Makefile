.PHONY: lint lint-fix

lint:
	black --check src
	ruff check src

lint-fix:
	black src
	ruff --fix src