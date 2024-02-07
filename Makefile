all:
	black otazky/ tests/
	isort otazky/ tests/
	pytest
	pylint otazky/ tests/
