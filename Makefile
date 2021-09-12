PYTEST := /home/pi/gitRepos/stocks/.venv/bin/pytest
PYTHON := /home/pi/gitRepos/stocks/.venv/bin/python
MYPY := /home/pi/gitRepos/stocks/.venv/bin/mypy
FLAKE8 := /home/pi/gitRepos/stocks/.venv/bin/flake8

.PHONY: tests run

all: lint tests run

run:
	./run.sh

lint:
	$(FLAKE8) portfolio/ provider/ helpers/ main.py
	$(MYPY) main.py

tests:
	$(PYTEST) --cov-report=html --cov=provider --cov=portfolio tests/

upload:
	aws s3 cp webfront/index.html s3://sakana-stockpick-www
