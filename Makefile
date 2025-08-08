.PHONY: test format

test:
	pytest
	ruff check .

format:
	 black --line-length 100 otazky/ tests/ *.py
	 isort --profile black otazky/ tests/ *.py
