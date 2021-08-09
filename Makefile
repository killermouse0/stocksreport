PYTEST := /home/pi/gitRepos/stocks/.venv/bin/pytest
PYTHON := /home/pi/gitRepos/stocks/.venv/bin/python

.PHONY: tests run

run:
	./run.sh

tests:
	$(PYTEST) --cov-report=html --cov=provider --cov=portfolio tests/
