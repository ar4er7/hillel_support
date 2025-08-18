.PHONY: run check format worker
run:
	python3 src/manage.py runserver

check:
	python -m ruff check . && python -m black --check . && python -m isort --check .

format:
	python -m ruff check . --fix && python -m isort . && python -m black .

worker:
	celery -A config worker -l INFO

.PHONY: redis-status redis-start redis-stop redis-restart redis-enable redis-disable

redis-status:
	@echo "🔍 Статус Redis:"
	sudo systemctl status redis-server | grep Active

redis-start:
	@echo "🚀 Запуск Redis..."
	sudo systemctl start redis-server

redis-stop:
	@echo "🛑 Остановка Redis..."
	sudo systemctl stop redis-server

redis-restart:
	@echo "🔄 Перезапуск Redis..."
	sudo systemctl restart redis-server

redis-enable:
	@echo "📌 Включение автозапуска Redis..."
	sudo systemctl enable redis-server

redis-disable:
	@echo "🚫 Отключение автозапуска Redis..."
	sudo systemctl disable redis-server
