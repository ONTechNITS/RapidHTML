# Assume `poetry` exists within PATH by default
POETRY_BIN ?= poetry

# Used in `format` and `link`. If True, check if changes are needed.
CHECK ?= false

# Indicate if the current build is a DEV environment. True by default.
DEV ?= true

.PHONY:help
help:
	@echo "Available targets:"
	@echo "  install    Install dependencies"
	@echo "  format     Format all code within src/quickhtml"
	@echo "  lint       Link all code within src/quickhtml"
	@echo "  lock       Update the poetry lock file"

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

.PHONY:test
test:
	@$(POETRY_BIN) run pytest