UV=uv
UV_RUN=$(UV) run
FIX=1
COVERAGE=0
VERSION=$(shell $(UV_RUN) dunamai from git |sed 's/+/_/g')
IMAGE=docker.io/library/jinja-tree
LINT_MYPY=1

default: help

.PHONY: sync
sync: ## Sync the venv
	$(UV) sync

.PHONY: install
install: sync ## Install the venv

.PHONY: lint
lint: ## Lint the code
ifeq ($(FIX), 1)
	$(UV_RUN) ruff check --fix jinja_tree tests
	$(UV_RUN) ruff format jinja_tree tests
else
	$(UV_RUN) ruff check jinja_tree tests
	$(UV_RUN) ruff format --check jinja_tree tests
endif
ifeq ($(LINT_MYPY), 1)
	$(UV_RUN) mypy --check-untyped-defs jinja_tree
endif

.PHONY: test
test: ## Test the code
ifeq ($(COVERAGE), 1)
	$(UV_RUN) pytest --cov=jinja_tree --cov-report=html --cov-report=term tests
else
	$(UV_RUN) pytest tests
endif

.PHONY: doc
doc: ## Generate documentation
	$(UV_RUN) python jinja_tree/infra/controllers/cli_tree.py .

.PHONY: docker
docker: ## Build docker image
	docker build --progress plain -t $(IMAGE) .

.PHONY: no-dirty
no-dirty: ## Check that the repository is clean
	if test -n "$$(git status --porcelain)"; then \
		echo "***** git status *****"; \
		git status; \
		echo "***** git diff *****"; \
		git diff; \
		echo "ERROR: the repository is dirty"; \
		exit 1; \
	fi

.PHONY: clean
clean: ## Clean the repository
	rm -Rf .venv .*_cache build dist htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -Rf {} \; 2>/dev/null || true

.PHONY: mrproper
mrproper: clean ## Clean the repository (including downloaded tools)

.PHONY: build
build: ## Build the package
	$(UV) build

.PHONY: publish
publish: build ## Publish the package (to pypi)
	if [ "$${UV_PUBLISH_TOKEN:-}" = "" ]; then \
		echo "UV_PUBLISH_TOKEN is not set"; \
		exit 1; \
	fi
	$(UV) publish

.PHONY: help
help:
	@# See https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
