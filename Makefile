SHELL := /usr/bin/env bash
export PATH := .venv/bin:$(PATH)

DOCSET_VERSION := $(shell cat version/docset)

DOCSET := .build/$(DOCSET_VERSION)/Terraform.docset

STATIC_FILES := \
	$(DOCSET)/icon.png \
	$(DOCSET)/Contents/Info.plist \
	$(DOCSET)/Contents/Resources/Documents/style.css

###

.PHONY: venv clone static docset
.DEFAULT_GOAL := docset

venv: .venv/bin/activate .build/.done-requirements
clone: .build/$(DOCSET_VERSION)/.done-cloning
static: $(STATIC_FILES)

docset:
	$(MAKE) venv
	$(MAKE) clone
	$(MAKE) static

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
