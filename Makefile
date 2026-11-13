test:
	pytest

unit_test:
	pytest -m "not perf"

perf_test:
	pytest -m perf -s

coverage:
	pytest -m "not perf" --cov=src --cov-report=term-missing --cov-report=html

lint:
	ruff check src tests

doc:
	cd src/ && pdoc3 --html --force -o ../docs .
