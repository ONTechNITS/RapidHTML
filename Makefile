.PHONY: lint test format github-checks docs_serve

lint:
	@echo "Running linter on src/"
	@ruff check src/
	@echo "Running linter on tests/"
	@ruff check tests/

test:
	@echo "Running tests"
	@pytest

format:
	@echo "Running formatter on src/"
	@ruff format src/
	@echo "Running formatter on tests/"
	@ruff format tests/

github-checks: test lint
	@echo "\nTests and linting passed"

docs_serve:
	@echo "Serving docs"
	@sphinx-autobuild --port 0 docs docs/_build