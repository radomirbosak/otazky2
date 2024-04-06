.PHONY: test format

test:
	pytest
	ruff check .

format:
	 black otazky/ tests/ *.py
	 isort otazky/ tests/ *.py
