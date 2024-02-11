.PHONY: build
build:: ## Build the Docker image
	docker build -t myapp .

.PHONY: help
help::
	@# See https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@cat $(MAKEFILE_LIST) >"$(TMPDIR)/makefile_help.txt"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' "$(TMPDIR)/makefile_help.txt" | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@rm -f "$(TMPDIR)/makefile_help.txt"