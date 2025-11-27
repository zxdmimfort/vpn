# Архитектурные решения

## Маппинг между Domain Entities и API Schemas

### Проблема
Domain entities используют **camelCase** (как в 3x-ui API), а API schemas используют **snake_case** (Python convention).

### Рассмотренные варианты

#### 1. Адаптеры в Presentation Layer ✅ ВЫБРАНО

**Реализация:** `src/presentation/api/adapters.py`

```python
def client_to_response(client: Client) -> ClientResponse:
    return ClientResponse(
        id=client.id,
        limit_ip=client.limitIp,  # camelCase -> snake_case
        expire_time=client.expireTime,
        # ...
    )
```

**Плюсы:**
- ✅ Чистая архитектура: domain layer не знает о presentation
- ✅ Entity остаётся чистой доменной моделью
- ✅ Schemas остаются чистыми API контрактами
- ✅ Легко менять API без изменения domain
- ✅ Явная конвертация - легко отлаживать
- ✅ Соответствует принципу единственной ответственности (SRP)
- ✅ Переиспользуемость адаптеров

**Минусы:**
- ⚠️ Немного больше кода (но он изолирован)

#### 2. Field(alias=...) в Schemas

```python
class ClientResponse(BaseModel):
    limit_ip: int = Field(alias="limitIp")
```

**Плюсы:**
- Меньше кода
- Pydantic автоматически конвертирует

**Минусы:**
- ❌ Schemas становятся зависимыми от структуры Entity
- ❌ Нарушается принцип разделения слоёв
- ❌ API контракт связан с внутренней моделью

#### 3. Field(serialization_alias=...) в Entities

```python
class Client(BaseModel):
    limitIp: int = Field(serialization_alias="limit_ip")
```

**Минусы:**
- ❌ **ПЛОХО**: Domain знает о presentation
- ❌ Нарушает чистую архитектуру
- ❌ Entity должна отражать структуру VPN сервера, а не API
- ❌ Смешивание ответственностей

### Решение

**Выбран вариант 1**: адаптеры в presentation layer (`adapters.py`)

**Обоснование:**
1. Соответствует Clean Architecture
2. Domain layer остаётся независимым
3. Легко тестировать каждый слой отдельно
4. Легко поддерживать и расширять
5. Явное преобразование лучше неявного (Zen of Python)

### Структура слоёв

```
┌─────────────────────────────────────┐
│     Presentation Layer              │
│  ┌─────────────────────────────┐   │
│  │ API Endpoints (clients.py)  │   │
│  │ ┌─────────────────────────┐ │   │
│  │ │ Adapters (adapters.py)  │ │   │
│  │ │ - client_to_response()  │ │   │
│  │ │ - inbound_to_response() │ │   │
│  │ └─────────────────────────┘ │   │
│  │ Schemas (snake_case)        │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│     Application Layer               │
│  - VPNManagementService             │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│     Domain Layer                    │
│  - Entities (camelCase)             │
│  - Ports (interfaces)               │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│     Infrastructure Layer            │
│  - XUIAdapter (camelCase ↔ 3x-ui)  │
└─────────────────────────────────────┘
```

### Преимущества текущего подхода

1. **Независимость domain**: можно менять API без изменения бизнес-логики
2. **Тестируемость**: легко mock'ить адаптеры
3. **Переиспользование**: адаптеры используются в clients.py и inbounds.py
4. **Явность**: видно где и как происходит конвертация
5. **Соответствие стандартам**: domain → 3x-ui camelCase, API → Python snake_case
