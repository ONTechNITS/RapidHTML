# Assume `poetry` exists within PATH by default
POETRY_BIN ?= poetry

# Used in `format` and `link`. If True, check if changes are needed.
CHECK ?= false

# Indicate if the current build is a DEV environment. True by default.
DEV ?= true

.PHONY:help
help:
	@echo "Available targets:"
	@echo "  install    	Install dependencies"
	@echo "  test 	 		Run tests"
	@echo "  format     	Format all code within src/rapidhtml"
	@echo "  lint       	Link all code within src/rapidhtml"
	@echo "  lock       	Update the poetry lock file"
	@echo "  docs-serve     Serve the documentation for editing purposes"
	@echo "  docs-build     Build the documentation"

.PHONY:install-dev
install-dev:
ifeq ($(DEV),true)
	@$(POETRY_BIN) install --only dev
endif

.PHONY:install
install:install-dev
	@$(POETRY_BIN) install

.PHONY:lock
lock:
ifeq ($(CHECK),true)
	@$(POETRY_BIN) check --lock
else
	@$(POETRY_BIN) lock
endif

.PHONY:format
format:
ifeq ($(CHECK),true)
	@$(POETRY_BIN) run ruff format --check
else
	@$(POETRY_BIN) run ruff format
endif

.PHONY:lint
lint:
	@$(POETRY_BIN) run ruff check

.PHONY:docs-serve
docs-serve:
	@echo "Serving docs"
	@$(POETRY_BIN) run mkdocs serve

.PHONY:docs-build
docs-build:
	@echo "Building docs"
	@$(POETRY_BIN) run mkdocs build
	
.PHONY:test
test:
	@$(POETRY_BIN) run pytest
