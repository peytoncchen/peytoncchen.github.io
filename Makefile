.PHONY: verify hooks
verify:
	python3 -m unittest discover -s tests
	python3 scripts/verify.py
hooks:
	git config core.hooksPath .githooks
