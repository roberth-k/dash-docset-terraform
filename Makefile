SHELL := /usr/bin/env bash
export PATH := $(shell pwd)/scripts:$(shell pwd)/.venv/bin:$(PATH)

DOCSET_VERSION := $(shell cat version/docset)

DOCSET := .build/$(DOCSET_VERSION)/Terraform.docset

STATIC_FILES := \
	$(DOCSET)/icon.png \
	$(DOCSET)/Contents/Info.plist \
	$(DOCSET)/Contents/Resources/Documents/style.css

###

.PHONY: venv clone html static docset
.DEFAULT_GOAL := docset

venv: .venv/bin/activate .build/.done-requirements
clone: .build/$(DOCSET_VERSION)/.done-cloning
html: .build/$(DOCSET_VERSION)/.done-make-html
static: $(STATIC_FILES)

docset:
	$(MAKE) venv
	$(MAKE) clone
	$(MAKE) static
	$(MAKE) html
	$(MAKE) tgz

###

.PHONY: clean clean/html

clean:
	rm -rf .build

clean/html:
	-rm .build/$(DOCSET_VERSION)/.done-make-html
	-rm .build/$(DOCSET_VERSION)/Makefile
	find $(DOCSET) -name '*.html' -delete
	-rm $(DOCSET)/Contents/Resources/docSet.dsidx
	-rm $(DOCSET)/Contents/Resources/optimizedIndex.dsidx

###

.venv/bin/activate:
	python3 -m venv .venv

.build/.done-requirements: .venv/bin/activate requirements.txt
	@mkdir -p $(dir $@)
	pip3 install -r requirements.txt
	@touch $@

.build/$(DOCSET_VERSION)/.done-cloning: scripts/clone.sh scripts/providers.py version/docset version/terraform
	@mkdir -p $(dir $@)
	./scripts/clone.sh $(shell cat version/terraform) $(dir $@)/src
	@touch $@

$(STATIC_FILES): $(DOCSET)/%:  static/%
	@mkdir -p $(dir $@)
	cp $< $@

.build/$(DOCSET_VERSION)/Makefile: scripts/makefile.sh
	@mkdir -p $(dir $@)
	./scripts/makefile.sh $(dir $@)/src $(DOCSET) > $@

.build/$(DOCSET_VERSION)/.done-make-html: .build/$(DOCSET_VERSION)/Makefile
	@mkdir -p $(dir $@)
	$(MAKE) -C $(dir $@) html
	@touch $@

.build/$(DOCSET_VERSION)/Terraform.tgz: .build/$(DOCSET_VERSION)/.done-make-html
	cd $(dir $@) \
	&& tar --exclude='.DS_Store' -czf $(notdir $@) $(patsubst %.tgz,%.docset,$(notdir $@))
