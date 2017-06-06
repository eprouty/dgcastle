init:
	python3 -m venv .venv

test:
	python3 -m unittest

.PHONY: init test
