# VPN Management Microservice

# VPN Management Service

Микросервис на FastAPI для управления VPN серверами через API 3x-ui панели.

## Технологии

- **FastAPI** - REST API
- **Pydantic v2** - валидация данных
- **Dishka** - dependency injection
- **httpx** - HTTP клиент для 3x-ui API
- **uv** - супер быстрый менеджер пакетов

## Быстрый старт

```bash
# 1. Установка (автоматически установит uv)
./setup.sh

# 2. Настройка
cp .env.example .env
# Отредактируйте X_UI_BASE_URL, X_UI_USERNAME, X_UI_PASSWORD

# 3. Запуск
./run.sh
# или: uv run python main.py
```

Откройте: http://localhost:8000/docs

## Структура проекта (гексагональная архитектура)

```
src/
├── domain/              # Бизнес-логика (entities, ports)
├── application/         # Use cases (services)
├── infrastructure/      # Адаптеры (3x-ui, DI)
└── presentation/        # API endpoints
```

## API Endpoints

- `GET /api/v1/inbounds` - список inbounds
- `POST /api/v1/inbounds` - создать inbound
- `PUT /api/v1/inbounds/{id}` - обновить
- `DELETE /api/v1/inbounds/{id}` - удалить
- `POST /api/v1/inbounds/{id}/clients` - добавить клиента
- `GET /api/v1/stats/traffic` - статистика трафика
- `GET /api/v1/stats/server` - статистика сервера

## Разработка

```bash
# Основные команды
make run          # Запуск
make dev-run      # С hot-reload
make test         # Тесты
make lint         # Проверка кода
make format       # Форматирование

# Управление пакетами (uv)
uv add package    # Добавить
uv remove package # Удалить
uv sync           # Синхронизировать
```

## Docker

```bash
make docker-build  # Собрать образ
make docker-run    # Запустить
```

## Конфигурация (.env)

```env
X_UI_BASE_URL=http://your-server:2053
X_UI_USERNAME=admin
X_UI_PASSWORD=password
API_KEY=secret  # опционально
```

## Примеры использования

### Создать inbound

```bash
curl -X POST "http://localhost:8000/api/v1/inbounds" \
  -H "Content-Type: application/json" \
  -d '{
    "remark": "VPN Server",
    "port": 443,
    "protocol": "vless",
    "enable": true
  }'
```

### Добавить клиента

```bash
curl -X POST "http://localhost:8000/api/v1/inbounds/1/clients" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "uuid-here",
    "email": "user@example.com",
    "enable": true
  }'
```

## Лицензия

MIT

## 🏗️ Архитектура

Проект построен с использованием **гексагональной (портов и ад## 🧪 Тестирование

```bash
# Запуск всех тестов
make test
# или
uv run pytest

# С покрытием кода
make test-cov
# или
uv run pytest --cov=src --cov-report=html
```тектуры**:

```
src/
├── domain/              # Доменный слой (бизнес-логика)
│   ├── entities.py      # Доменные сущности (Inbound, Client, ServerStats)
│   ├── exceptions.py    # Доменные исключения
│   └── ports.py         # Интерфейсы (порты) для адаптеров
├── application/         # Слой приложения (use cases)
│   └── services.py      # Сервисы приложения (VPNManagementService)
├── infrastructure/      # Инфраструктурный слой (адаптеры)
│   ├── x_ui_adapter.py  # Адаптер для 3x-ui API
│   └── di.py            # Dependency Injection (Dishka)
├── presentation/        # Слой представления (API)
│   ├── api/
│   │   ├── inbounds.py  # Эндпоинты для управления inbounds
│   │   ├── clients.py   # Эндпоинты для управления клиентами
│   │   ├── stats.py     # Эндпоинты для статистики
│   │   └── schemas.py   # Pydantic схемы запросов/ответов
│   ├── middleware.py    # Middleware (API key authentication)
│   └── app.py           # Фабрика FastAPI приложения
└── config.py            # Конфигурация приложения
```

### Принципы архитектуры

- **Независимость от фреймворков**: Доменная логика не зависит от FastAPI или других библиотек
- **Инверсия зависимостей**: Инфраструктурный слой зависит от доменного через интерфейсы
- **Тестируемость**: Легко заменить реальные адаптеры на моки в тестах
- **Расширяемость**: Легко добавить адаптер для другой VPN панели, реализовав `VPNServerPort`

## 🚀 Технологии

- **FastAPI** - современный веб-фреймворк для Python
- **Pydantic v2** - валидация данных и настройки приложения
- **Dishka** - dependency injection контейнер
- **httpx** - асинхронный HTTP клиент для работы с 3x-ui API
- **Uvicorn** - ASGI сервер

## 📦 Установка

> 💡 **Проект использует [uv](https://github.com/astral-sh/uv)** - сверхбыстрый менеджер пакетов для Python (в 10-100 раз быстрее pip!)

### Быстрая установка (рекомендуется)

```bash
# Скрипт автоматически установит uv и все зависимости
./setup.sh
```

### Ручная установка с uv

1. Установите uv (если еще не установлен):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Синхронизируйте зависимости:
```bash
# Production + dev зависимости
uv sync

# Только production
uv sync --no-dev
```

### Альтернатива: установка с pip

1. Создайте виртуальное окружение:
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
```

2. Установите зависимости:
```bash
pip install -e .
pip install -e ".[dev]"  # для разработки
```

> 📖 Подробнее об использовании uv см. [UV_GUIDE.md](UV_GUIDE.md)

## ⚙️ Настройка

1. Скопируйте файл с примером конфигурации:
```bash
cp .env.example .env
```

2. Отредактируйте `.env` файл:
```env
# 3x-ui API settings (обязательные)
X_UI_BASE_URL=http://your-3x-ui-panel.com:2053
X_UI_USERNAME=admin
X_UI_PASSWORD=your_password

# Security (опционально - для защиты API ключом)
API_KEY=your_secret_api_key

# Server settings (опционально)
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

## 🏃 Запуск

### Локальный запуск

```bash
# Простой запуск (с uv)
uv run python main.py

# Или используя скрипт
./run.sh

# Разработка с hot-reload
make dev-run
# или
uv run uvicorn src.presentation.app:create_app --factory --reload
```

### Docker запуск

```bash
# Собрать образ
make docker-build
# или
docker build -t vpn-manager:latest .

# Запустить с docker-compose
make docker-run
# или
docker-compose up -d

# Посмотреть логи
make docker-logs
```

Сервер будет доступен по адресу: **http://localhost:8000**

API документация (Swagger UI): **http://localhost:8000/docs**

## 📚 API Endpoints

### Health Check

- `GET /health` - Проверка здоровья сервиса

### Inbounds Management

- `GET /api/v1/inbounds` - Получить список всех inbounds
- `GET /api/v1/inbounds/{id}` - Получить inbound по ID
- `POST /api/v1/inbounds` - Создать новый inbound
- `PUT /api/v1/inbounds/{id}` - Обновить inbound
- `DELETE /api/v1/inbounds/{id}` - Удалить inbound

### Client Management

- `POST /api/v1/inbounds/{inbound_id}/clients` - Добавить клиента к inbound
- `PUT /api/v1/inbounds/{inbound_id}/clients/{client_id}` - Обновить клиента
- `DELETE /api/v1/inbounds/{inbound_id}/clients/{client_id}` - Удалить клиента

### Statistics

- `GET /api/v1/stats/traffic` - Получить статистику трафика для всех inbounds
- `GET /api/v1/stats/server` - Получить статистику сервера (CPU, память, диск)

## 🔒 Аутентификация

Если установлен `API_KEY` в `.env`, все запросы к API должны содержать заголовок:

```bash
X-API-Key: your_secret_api_key
```

## 📝 Примеры использования

### Создание inbound

```bash
curl -X POST "http://localhost:8000/api/v1/inbounds" \
  -H "X-API-Key: your_secret_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "remark": "My VPN Server",
    "enable": true,
    "port": 443,
    "protocol": "vless",
    "settings": {
      "clients": [],
      "decryption": "none"
    },
    "stream_settings": {
      "network": "tcp",
      "security": "tls"
    },
    "sniffing": {
      "enabled": true,
      "destOverride": ["http", "tls"]
    }
  }'
```

### Добавление клиента

```bash
curl -X POST "http://localhost:8000/api/v1/inbounds/1/clients" \
  -H "X-API-Key: your_secret_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "enable": true,
    "flow": "",
    "limit_ip": 2,
    "total_gb": 10737418240,
    "expire_time": 1735689600
  }'
```

### Получение статистики

```bash
# Статистика трафика
curl -X GET "http://localhost:8000/api/v1/stats/traffic" \
  -H "X-API-Key: your_secret_api_key"

# Статистика сервера
curl -X GET "http://localhost:8000/api/v1/stats/server" \
  -H "X-API-Key: your_secret_api_key"
```

### Python пример

См. файл `examples/api_usage.py`:

```bash
python examples/api_usage.py
```

## � Тестирование

```bash
# Запуск всех тестов
make test
# или
pytest

# С покрытием кода
make test-cov
# или
pytest --cov=src --cov-report=html
```

## 🔧 Разработка

### Проверка кода

```bash
# Линтинг
make lint

# Форматирование
make format

# Проверка типов
make type-check

# Все проверки
make all
```

### Добавление нового адаптера

Чтобы добавить поддержку другой VPN панели:

1. Создайте новый адаптер, реализующий интерфейс `VPNServerPort` из `src/domain/ports.py`
2. См. пример в `examples/custom_adapter.py`
3. Зарегистрируйте адаптер в `src/infrastructure/di.py`

Пример:

```python
from src.domain.ports import VPNServerPort

class MyVPNAdapter(VPNServerPort):
    async def authenticate(self) -> bool:
        # Ваша реализация
        pass
    
    async def get_inbounds(self) -> list[Inbound]:
        # Ваша реализация
        pass
    
    # ... остальные методы
```

## 📊 Структура проекта

```
.
├── examples/              # Примеры использования
├── src/                   # Исходный код
│   ├── application/       # Бизнес-логика
│   ├── domain/           # Доменная модель
│   ├── infrastructure/   # Адаптеры и DI
│   └── presentation/     # API endpoints
├── tests/                # Тесты
├── .env.example          # Пример конфигурации
├── docker-compose.yml    # Docker Compose конфигурация
├── Dockerfile            # Docker образ
├── Makefile              # Команды для разработки
├── pyproject.toml        # Зависимости проекта
└── README.md             # Этот файл
```

## 🤝 Вклад в проект

См. [CONTRIBUTING.md](CONTRIBUTING.md) для деталей.

## 📄 Changelog

См. [CHANGELOG.md](CHANGELOG.md) для истории изменений.

## 📄 Лицензия

MIT License

## 🙋 Поддержка

Если у вас возникли вопросы или проблемы:

1. Проверьте существующие Issues
2. Создайте новый Issue с подробным описанием
3. Предоставьте логи и конфигурацию (без секретов!)

## 🎯 Планы развития

- [ ] JWT аутентификация
- [ ] Rate limiting
- [ ] Prometheus метрики
- [ ] Structured logging
- [ ] Кеширование данных (Redis)
- [ ] Миграции базы данных
- [ ] Webhook уведомления
- [ ] Админ панель (web UI)
- [ ] Мультитенантность

## 📖 Документация

- 📘 [README.md](README.md) - основная документация (вы здесь)
- 🚀 [QUICKSTART.md](QUICKSTART.md) - быстрый старт за 3 минуты
- 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md) - подробное описание архитектуры
- 📋 [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - обзор всего проекта
- 🤝 [CONTRIBUTING.md](CONTRIBUTING.md) - руководство для разработчиков
- 📝 [CHANGELOG.md](CHANGELOG.md) - история изменений
- ⚡ [UV_GUIDE.md](UV_GUIDE.md) - подробное руководство по uv
- 🔄 [MIGRATION_UV.md](MIGRATION_UV.md) - миграция на uv
- 📄 [UV_CHEATSHEET.md](UV_CHEATSHEET.md) - шпаргалка по uv
