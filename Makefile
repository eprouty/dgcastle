init:
	pipenv install --dev

test:
	python3 -m unittest

.PHONY: init test
