.PHONY: tests

tests:
	pytest --cov-report=html --cov=provider tests/
