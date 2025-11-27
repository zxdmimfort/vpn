# Persistence Layer

## Архитектура

Слой persistence реализован с использованием SQLAlchemy 2.0 (async) и SQLite.

### Структура

```
src/infrastructure/persistence/
├── __init__.py           # Экспорты модуля
├── models.py             # SQLAlchemy модели
├── database.py           # Database manager
└── repository.py         # Репозиторий для работы с данными
```

### Модели

#### ClientMetadata

Хранит метаданные о VPN клиентах, которые не хранятся в 3x-ui:

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer | Primary key (autoincrement) |
| `client_id` | String(255) | UUID VPN клиента (unique, indexed) |
| `owner_ref` | String(255) | User ID из биллинга (nullable, indexed) |
| `created_at` | DateTime | Дата создания записи |
| `updated_at` | DateTime | Дата последнего обновления |

### Database Manager

```python
from src.infrastructure.persistence import Database

db = Database(
    database_url="sqlite+aiosqlite:///./vpn.db",
    echo=False
)

# Создать таблицы
await db.create_tables()

# Получить сессию
async with db.session() as session:
    # Работа с БД
    ...
```

### Repository Pattern

```python
from src.infrastructure.persistence import ClientMetadataRepository

async with db.session() as session:
    repo = ClientMetadataRepository(session)
    
    # Создать запись
    metadata = await repo.create(
        client_id="uuid-123",
        owner_ref="user_456"
    )
    
    # Получить по client_id
    metadata = await repo.get_by_client_id("uuid-123")
    
    # Получить все клиенты пользователя
    clients = await repo.get_by_owner_ref("user_456")
    
    # Обновить owner_ref
    await repo.update_owner_ref("uuid-123", "user_789")
    
    # Удалить
    await repo.delete("uuid-123")
```

## Интеграция с Dishka

Dependency Injection настроен автоматически:

```python
@router.post("/clients")
async def add_client(
    metadata_repo: FromDishka[ClientMetadataRepository],
):
    # Repository автоматически инжектится с активной сессией
    metadata = await metadata_repo.create(...)
```

## Миграции

Пока используется `create_all()` для создания таблиц при старте приложения.

Для production рекомендуется использовать Alembic:

```bash
# Установить
pip install alembic

# Инициализировать
alembic init alembic

# Создать миграцию
alembic revision --autogenerate -m "Initial migration"

# Применить
alembic upgrade head
```

## База данных

### Разработка

```bash
# SQLite (по умолчанию)
DATABASE_URL=sqlite+aiosqlite:///./vpn.db
```

### Production

```bash
# PostgreSQL (рекомендуется)
DATABASE_URL=postgresql+asyncpg://user:password@localhost/vpn

# MySQL
DATABASE_URL=mysql+aiomysql://user:password@localhost/vpn
```

## Пример использования

### Создание клиента

```python
POST /inbounds/1/clients
{
  "limit_ip": 2,
  "total_gb": 100,
  "expired": 1735689600,
  "owner_ref": "user_123"  # ← Сохраняется в БД
}
```

### Получение клиента

```python
GET /inbounds/1/clients/uuid-123

Response:
{
  "id": "uuid-123",
  "email": "client-uuid123@vpn.local",
  "owner_ref": "user_123",  # ← Из БД
  "total_gb": 1024,         # ← Из 3x-ui
  ...
}
```

### Обновление owner_ref

```python
PUT /inbounds/1/clients/uuid-123
{
  "owner_ref": "user_456"  # ← Обновляется в БД
}
```

### Удаление клиента

```python
DELETE /inbounds/1/clients/uuid-123
# Удаляется и из 3x-ui, и из БД
```
