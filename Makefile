SHELL := /bin/bash
GIT_ROOT := $(shell git rev-parse --show-toplevel 2>/dev/null)

help: ## show help.
	@gawk -f $(GIT_ROOT)/sh/makehelp.awk $(MAKEFILE_LIST)

.PHONY: sh
sh: ## run my shell
	@-bash --init-file $(GIT_ROOT)/sh/ell -i

push: ## save to cloud
	@read -p "Reason? " msg; git commit -am "$$msg"; git push; git status

mds: ## add all the headers to markdown files
	@$(GIT_ROOT)/sh/headers $(GIT_ROOT)

make enableRebase:
	git config pull.rebase false

