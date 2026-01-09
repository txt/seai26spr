SHELL := /bin/bash
GIT_ROOT := $(shell git rev-parse --show-toplevel 2>/dev/null)

help: ## show help.
	@gawk -f $(GIT_ROOT)/sh/makehelp.awk $(MAKEFILE_LIST)


push: ## save to cloud
	@read -p "Reason? " msg; git commit -am "$$msg"; git push; git status


ONE=cat $< | gawk 'BEGIN {FS="\n";RS=""} {print $$0 ; exit}'
TWOPLUS=cat $@ | gawk 'BEGIN {FS="\n";RS=""} NR==1 { print("\n\n"); next} {print $$0 "\n\n"}'

all: ## save all to Github
	cd $(GIT_ROOT); $(MAKE) -B ../LICENSE.md ;
	cd $(GIT_ROOT)/dpcs; $(MAKE) -B *.md ;
	$(MAKE) push

../LICENSE.md: $(GIT_ROOT)/README.md ## update license
	@echo "$@ ... " ; ($(ONE);  $(TWOPLUS)) > .tmp; mv .tmp $@

*.md: $(GIT_ROOT)/README.md  ## add standard header to *md files
	echo "$@ ... "
	@($(ONE);  $(TWOPLUS)) > .tmp; mv .tmp $@

