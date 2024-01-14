SHELL:=/bin/bash
FIX=1
COVERAGE=0
RUFF=ruff
MYPY=mypy
PYTEST=pytest
PYTHON=python3
VERSION=0.0.0
PYPI_TOKEN=

default: help

.PHONY: lint
lint: ## Lint the code (FIX=0 to disable autofix)
ifeq ($(FIX), 0)
	$(RUFF) format --check .
	$(RUFF) .
else
	$(RUFF) format .
	$(RUFF) --fix .
endif
	$(MYPY) --check-untyped-defs .

.PHONY: test
test: ## Test the code
ifeq ($(COVERAGE), 0)
	$(PYTEST) tests
else
	$(PYTEST) --no-cov-on-fail --cov=jinja_tree --cov-report=term --cov-report=html --cov-report=xml tests
endif

.PHONY: doc
doc: ## Generate documentation
	$(PYTHON) jinja_tree/infra/controllers/cli_tree.py .

.PHONY: clean
clean: ## Clean generated files
	rm -Rf .*_cache build
	find . -type d -name __pycache__ -exec rm -Rf {} \; 2>/dev/null || true

.PHONY: publish
publish: ## Publish to PyPI
	@if test "${VERSION}" = "0.0.0"; then echo "ERROR: Cannot publish a dev version"; exit 1; fi
	@if test "${PYPI_TOKEN}" = ""; then echo "ERROR: PYPI_TOKEN is not set"; exit 1; fi
	cp -f pyproject.toml pyproject.toml.dev 
	poetry version "$(VERSION)"
	poetry config pypi-token.pypi "$(PYPI_TOKEN)"
	poetry build
	poetry publish

.PHONY: help
help::
	@# See https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@cat $(MAKEFILE_LIST) >"$(TMPDIR)/makefile_help.txt"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' "$(TMPDIR)/makefile_help.txt" | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@rm -f "$(TMPDIR)/makefile_help.txt"