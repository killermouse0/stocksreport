.PHONY: tests run

run:
	/home/pi/gitRepos/stocks/.venv/bin/python /home/pi/gitRepos/stocks/main.py

tests:
	pytest --cov-report=html --cov=provider --cov=portfolio tests/
