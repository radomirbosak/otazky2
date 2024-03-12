.PHONY: test format

test:
	pytest
	pylint otazky/ tests/ *.py

format:
	 black otazky/ tests/ *.py
	 isort otazky/ tests/ *.py
