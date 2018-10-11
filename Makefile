.PHONY: test

test:
	pytest --flake8

coverage:
	pytest --cov
