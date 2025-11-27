"""Makefile для управления проектом."""

.PHONY: help install dev-install run test lint format type-check clean docker-build docker-run

help:  ## Показать эту справку
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Установить зависимости (с uv)
	uv sync --no-dev

dev-install:  ## Установить зависимости для разработки (с uv)
	uv sync

run:  ## Запустить приложение
	uv run python main.py

dev-run:  ## Запустить приложение в режиме разработки с hot-reload
	uv run uvicorn src.presentation.app:create_app --factory --reload --host 0.0.0.0 --port 8000

test:  ## Запустить тесты
	uv run pytest

test-cov:  ## Запустить тесты с покрытием кода
	uv run pytest --cov=src --cov-report=html --cov-report=term

lint:  ## Проверить код с помощью ruff
	uv run ruff check src/ tests/

format:  ## Отформатировать код с помощью ruff
	uv run ruff format src/ tests/
	uv run ruff check --fix src/ tests/

type-check:  ## Проверить типы с помощью mypy
	uv run mypy src/

clean:  ## Очистить кеш и временные файлы
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf htmlcov/ .coverage

docker-build:  ## Собрать Docker образ
	docker build -t vpn-manager:latest .

docker-run:  ## Запустить в Docker
	docker-compose up -d

docker-stop:  ## Остановить Docker контейнеры
	docker-compose down

docker-logs:  ## Показать логи Docker
	docker-compose logs -f

all: clean install dev-install test lint type-check  ## Выполнить все проверки
