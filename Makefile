SHELL := /usr/bin/env bash
export PATH := .venv/bin:$(PATH)

DOCSET_VERSION := $(shell cat version/docset)

###

.PHONY: venv clone docset
.DEFAULT_GOAL := docset

venv: .venv/bin/activate .build/.done-requirements
clone: .build/$(DOCSET_VERSION)/.done-cloning
docset:
	$(MAKE) venv
	$(MAKE) clone

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
