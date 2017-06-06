init:
	python3 -m venv .venv

test:
	python3 -m unittest

coverage:
	coverage run --source dgcastle -m unittest

.PHONY: init test coverage
