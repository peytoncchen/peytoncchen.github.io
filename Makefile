.PHONY: verify check smoke smoke-live smoke-setup hooks

# Use the same browser revision for the checked-out site and the Pages smoke.
BROWSER := uv run --no-project --with playwright==1.64.1

verify: check smoke

check:
	python3 -m unittest discover -s tests
	python3 scripts/verify.py

smoke:
	$(BROWSER) python scripts/smoke.py

smoke-live:
	$(BROWSER) python scripts/smoke.py --live

smoke-setup:
	$(BROWSER) playwright install chromium

hooks:
	git config core.hooksPath .githooks
