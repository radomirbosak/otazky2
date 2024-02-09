all:
	black otazky/ tests/ *.py
	isort otazky/ tests/ *.py
	pytest
	pylint otazky/ tests/ *.py
