init:
	python3 -m venv .venv

test:
	python3 -m unittest

coverage:
	coverage run --source dgcastle -m unittest

server:
	python3 server.py

.PHONY: init test coverage server
