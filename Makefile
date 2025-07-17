.PHONY: run
run:
	python3 src/manage.py runserver

.PHONY: check
check:
	python -m ruff check . && python -m black --check . && python -m isort --check .

.PHONY: format
format:
	python -m ruff check . --fix && python -m isort . && python -m black .
