SHELL := /usr/bin/env bash
export PATH := .venv/bin:$(PATH)

###

.PHONY: venv

venv: .venv/bin/activate .build/.done-requirements

###

.venv/bin/activate:
	python3 -m venv .venv

.build/.done-requirements: .venv/bin/activate requirements.txt
	@mkdir -p $(dir $@)
	pip3 install -r requirements.txt
	@touch $@
