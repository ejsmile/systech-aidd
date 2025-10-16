# 📋 План разработки SP-2: Получение данных о пользователе

## 📊 Отчет о прогрессе

| № | Итерация | Статус | Тестирование | Дата завершения |
|---|----------|--------|--------------|-----------------|
| 1 | Анализ и проектирование | ✅ Завершено | - | 2025-10-16 |
| 2 | Модель User и миграция БД | ✅ Завершено | ✅ 100% coverage | 2025-10-16 |
| 3 | UserRepository | ⏳ Ожидает | - | - |
| 4 | Получение данных из Telegram | ⏳ Ожидает | - | - |
| 5 | Интеграция в handlers | ⏳ Ожидает | - | - |
| 6 | Покрытие тестами | ⏳ Ожидает | - | - |

**Легенда статусов:**
- ⏳ Ожидает
- 🔄 В работе
- ✅ Завершено
- ⚠️ Проблемы

---

## 🔍 Итерация 1: Анализ и проектирование

**Цель:** Изучить Telegram User API и спроектировать схему БД для хранения данных пользователей

### Задачи

**Анализ требований:**
- [x] Изучить документацию aiogram 3.x и Telegram Bot API для получения данных о пользователе
- [x] Определить какие поля доступны в `message.from_user`
- [x] Проанализировать существующий код handlers.py и определить точки интеграции
- [x] Документировать доступные поля пользователя и их типы
- [x] **Проанализировать существующие данные:**
  - Проверить таблицу `messages` - определить уникальных пользователей (chat_id + user_id)
  - Оценить количество существующих пользователей без записей в `users`
  - Спланировать стратегию миграции данных для существующих пользователей

**Проектирование схемы БД:**
- [x] Спроектировать таблицу `users` с полями:
  - `user_id` (BigInteger, PK) - ID пользователя в Telegram
  - `username` (String) - username (без @)
  - `first_name` (String) - имя
  - `last_name` (String, nullable) - фамилия
  - `bio` (Text, nullable) - описание профиля (если доступно)
  - `age` (Integer, nullable) - возраст (если потребуется сбор)
  - `created_at` (DateTime) - дата первого взаимодействия
  - `updated_at` (DateTime) - дата последнего обновления данных
- [x] Определить индексы для быстрого поиска
- [x] Создать ER-диаграмму (текстовую или графическую)
- [x] Определить связи с таблицей `messages` (foreign key на user_id)

**Документация:**
- [x] Создать документ с описанием структуры таблицы
- [x] Описать стратегию обновления данных (при каждом сообщении или периодически)

### Результат
- ✅ Документация по доступным полям Telegram User (`docs/database_schema.md`)
- ✅ ER-диаграмма базы данных (текстовая в документации)
- ✅ Спецификация таблицы `users` с индексами и стратегией миграции
- ✅ Анализ существующих данных: 4 уникальных пользователя, 30 сообщений

---

## 💾 Итерация 2: Модель User и миграция БД

**Цель:** Создать модель SQLAlchemy для пользователей и миграцию Alembic

### Задачи

**Создание модели (TDD):**
- [x] 🔴 RED: Написать тест для создания модели User
- [x] 🟢 GREEN: Создать класс `User` в `db_models.py` с полями:
  - `user_id`, `username`, `first_name`, `last_name`
  - `bio`, `age`, `created_at`, `updated_at`
- [x] 🔵 REFACTOR: Добавить type hints, docstring, индексы
- [x] Добавить метод `__repr__` для удобного отображения

**Создание миграции:**
- [x] Создать миграцию Alembic: `alembic revision --autogenerate -m "add users table"`
- [x] Проверить сгенерированный код миграции
- [x] Применить миграцию: `alembic upgrade head`
- [x] Убедиться что таблица создана в PostgreSQL

**Миграция существующих пользователей:**
- [x] Создать data-миграцию для извлечения user_id из таблицы `messages`
- [x] Заполнить таблицу `users` базовыми данными для существующих пользователей:
  - `user_id` из messages (уникальные значения)
  - `username`, `first_name`, `last_name` - NULL (будут заполнены при следующем взаимодействии)
  - `created_at` - MIN(created_at) из messages для каждого user_id
  - `updated_at` - текущее время
- [x] Проверить что все user_id из messages теперь есть в users

**Пример SQL для data-миграции:**
```sql
INSERT INTO users (user_id, username, first_name, last_name, created_at, updated_at)
SELECT DISTINCT 
    user_id,
    NULL as username,
    NULL as first_name, 
    NULL as last_name,
    MIN(created_at) as created_at,
    CURRENT_TIMESTAMP as updated_at
FROM messages
WHERE deleted_at IS NULL
GROUP BY user_id
ON CONFLICT (user_id) DO NOTHING;
```

**Seed данные (опционально):**
- [x] ~~Создать миграцию с тестовыми пользователями (для разработки)~~ Не требуется - используем реальные данные
- [x] ~~Добавить примеры пользователей с разными наборами данных~~ Не требуется

### Тест
```bash
# Создать миграцию
make db-migrate-create MESSAGE="add users table"

# Применить миграцию
make db-migrate

# Проверить в БД
docker exec -it systech-aidd-postgres psql -U postgres -d systech_aidd -c "\d users"

# Должна появиться таблица users со всеми полями

# Создать data-миграцию для существующих пользователей
make db-migrate-create MESSAGE="migrate existing users from messages"

# Применить data-миграцию
make db-migrate

# Проверить что пользователи мигрировали
docker exec -it systech-aidd-postgres psql -U postgres -d systech_aidd

# В psql выполнить:
SELECT COUNT(DISTINCT user_id) FROM messages WHERE deleted_at IS NULL;
SELECT COUNT(*) FROM users;
# Количество должно совпадать

# Проверить данные мигрированных пользователей
SELECT user_id, username, first_name, created_at FROM users LIMIT 5;
```

---

## 🗄️ Итерация 3: UserRepository

**Цель:** Реализовать слой доступа к данным для работы с пользователями

### Задачи

**Создание UserRepository (TDD):**

**Функциональность 1: Создание/обновление пользователя**
- [ ] 🔴 RED: Написать тест для `upsert_user()` - создание нового пользователя
- [ ] 🟢 GREEN: Реализовать метод `upsert_user()` для создания пользователя
- [ ] 🔴 RED: Написать тест для обновления существующего пользователя
- [ ] 🟢 GREEN: Реализовать логику обновления (upsert)
- [ ] 🔵 REFACTOR: Оптимизировать код, добавить логирование

**Функциональность 2: Получение пользователя по ID**
- [ ] 🔴 RED: Написать тест для `get_user_by_id()`
- [ ] 🟢 GREEN: Реализовать метод получения пользователя
- [ ] 🔵 REFACTOR: Добавить обработку случая когда пользователь не найден

**Функциональность 3: Получение статистики**
- [ ] 🔴 RED: Написать тест для `get_user_message_count()` - количество сообщений пользователя
- [ ] 🟢 GREEN: Реализовать метод подсчета сообщений
- [ ] 🔵 REFACTOR: Оптимизировать запрос

**Создание файла:**
- [ ] Создать `src/user_repository.py` с классом `UserRepository`
- [ ] Добавить type hints для всех методов
- [ ] Добавить docstrings с описанием параметров и возвращаемых значений

### Примеры методов
```python
class UserRepository:
    async def upsert_user(self, user_data: dict) -> User:
        """Создать или обновить данные пользователя"""
        
    async def get_user_by_id(self, user_id: int) -> User | None:
        """Получить пользователя по ID"""
        
    async def get_user_message_count(self, user_id: int) -> int:
        """Получить количество сообщений пользователя"""
```

### Тест
```bash
# Запустить тесты репозитория
make test tests/test_user_repository.py

# Все тесты должны пройти
```

---

## 📡 Итерация 4: Получение данных из Telegram

**Цель:** Реализовать извлечение данных пользователя из Telegram API

### Задачи

**Создание utility функций:**
- [ ] 🔴 RED: Написать тест для `extract_user_data()` - извлечение данных из `message.from_user`
- [ ] 🟢 GREEN: Реализовать функцию извлечения данных
- [ ] 🔵 REFACTOR: Обработать случаи когда поля отсутствуют

**Создание модели данных:**
- [ ] Создать dataclass `UserData` в `models.py` с полями:
  - `user_id`, `username`, `first_name`, `last_name`
- [ ] Добавить type hints и validation
- [ ] Добавить метод конвертации в dict для БД

**Обработка edge cases:**
- [ ] Обработать случай когда `username` отсутствует
- [ ] Обработать случай когда `last_name` отсутствует
- [ ] Логировать предупреждения при отсутствии данных

### Примеры
```python
@dataclass(frozen=True)
class UserData:
    """Данные пользователя из Telegram"""
    user_id: int
    username: str | None
    first_name: str
    last_name: str | None

def extract_user_data(telegram_user: TelegramUser) -> UserData:
    """Извлечь данные пользователя из Telegram объекта"""
```

### Тест
```bash
# Запустить тесты
make test tests/test_models.py

# Тесты должны покрывать:
# - Извлечение полных данных
# - Извлечение с отсутствующими optional полями
# - Конвертация в dict
```

---

## 🔗 Итерация 5: Интеграция в handlers

**Цель:** Интегрировать сохранение данных пользователя в обработчики команд

### Задачи

**Интеграция в handlers:**
- [ ] Добавить `UserRepository` в зависимости handlers
- [ ] В `handle_message()` добавить вызов `upsert_user()` перед обработкой сообщения
- [ ] **Реализовать логику upsert для двух сценариев:**
  - **Существующие пользователи** (из messages): обновить username, first_name, last_name, updated_at
  - **Новые пользователи**: создать запись со всеми данными из Telegram
- [ ] Обработать ошибки при сохранении данных (graceful degradation)
- [ ] Добавить логирование:
  - При первом сохранении пользователя (создание)
  - При обновлении данных существующего пользователя

**Интеграция в main.py:**
- [ ] Создать экземпляр `UserRepository` через DI
- [ ] Передать репозиторий в роутер через dependency injection

**Оптимизация:**
- [ ] Определить стратегию обновления: при каждом сообщении или кэшировать
- [ ] Реализовать кэширование если необходимо

### Изменения в handlers.py
```python
async def handle_message(
    message: Message,
    llm_client: LLMClient,
    conversation_manager: ConversationManager,
    user_repository: UserRepository,  # Новая зависимость
    system_prompt: str,
) -> None:
    """Обработка текстовых сообщений через LLM с историей"""
    if message.from_user is None or message.text is None:
        return
    
    # Сохранить/обновить данные пользователя
    try:
        user_data = extract_user_data(message.from_user)
        await user_repository.upsert_user(user_data)
    except Exception as e:
        logger.error(f"Failed to save user data: {e}")
        # Продолжаем работу даже если сохранение не удалось
    
    # ... остальная логика
```

### Тест
```bash
# Запустить бота
make run

# В Telegram отправить сообщения от разных пользователей
# Проверить в БД что данные сохранились

docker exec -it systech-aidd-postgres psql -U postgres -d systech_aidd -c "SELECT * FROM users;"

# Должны появиться записи пользователей
```

---

## ✅ Итерация 6: Покрытие тестами

**Цель:** Покрыть новую функциональность unit и интеграционными тестами

### Задачи

**Unit тесты:**
- [ ] `test_user_repository.py`:
  - Тест создания пользователя
  - Тест обновления пользователя (upsert)
  - Тест получения пользователя по ID
  - Тест получения статистики сообщений
- [ ] `test_models.py`:
  - Тест UserData dataclass
  - Тест extract_user_data()
  - Тест конвертации в dict
- [ ] `test_db_models.py`:
  - Тест модели User
  - Тест индексов и constraints

**Интеграционные тесты:**
- [ ] `test_user_integration.py`:
  - Тест полного цикла: получение данных из Telegram → сохранение в БД → получение из БД
  - Тест взаимодействия UserRepository + MessageRepository
  - Тест обработки пользователя в handlers
  - **Тест сценария миграции:**
    - Создать пользователя с минимальными данными (user_id, created_at)
    - Вызвать upsert с полными данными из Telegram
    - Проверить что данные обновились (username, first_name, last_name)
  - **Тест для нового пользователя:**
    - Вызвать upsert для несуществующего пользователя
    - Проверить что создалась новая запись со всеми данными

**Тестирование с testcontainers:**
- [ ] Убедиться что все тесты используют testcontainers
- [ ] Проверить что миграции применяются автоматически в тестах
- [ ] Тесты должны быть изолированы и независимы

**Coverage:**
- [ ] Запустить `make test-cov`
- [ ] Убедиться что покрытие новых модулей > 80%
- [ ] Добавить тесты для непокрытых веток кода

### Тест
```bash
# Запустить все тесты
make test

# Проверить покрытие
make test-cov

# Целевые метрики:
# - Все тесты проходят (зелёные)
# - Coverage для user_repository.py > 90%
# - Coverage для новых функций в models.py > 85%
# - Общий coverage проекта > 80%

# Проверка качества
make quality

# Все проверки должны пройти:
# - ruff format
# - ruff check
# - mypy (strict mode)
```

---

## 📝 Финальная проверка

**Чеклист перед завершением спринта:**

- [ ] Все миграции применены и работают
- [ ] Модель User создана с корректными типами и индексами
- [ ] UserRepository реализован и протестирован
- [ ] Данные пользователя извлекаются из Telegram
- [ ] Интеграция в handlers работает корректно
- [ ] Все unit тесты проходят (зелёные)
- [ ] Все интеграционные тесты проходят
- [ ] Coverage > 80% для всего проекта
- [ ] `make quality` проходит без ошибок
- [ ] Документация обновлена (если требуется)
- [ ] README.md обновлен при необходимости

**Ручное тестирование:**
```bash
# 1. Проверить миграцию существующих пользователей
docker exec -it systech-aidd-postgres psql -U postgres -d systech_aidd

# Выполнить SQL - должны быть мигрированные пользователи:
SELECT user_id, username, first_name, last_name, created_at 
FROM users 
WHERE username IS NULL;  -- Пользователи после data-миграции

# 2. Запустить бота
make run

# 3. В Telegram (от СУЩЕСТВУЮЩЕГО пользователя):
"Привет" → Отправить сообщение

# 4. Проверить что данные обновились
docker exec -it systech-aidd-postgres psql -U postgres -d systech_aidd

SELECT user_id, username, first_name, last_name, created_at, updated_at 
FROM users 
WHERE user_id = <ID_существующего_пользователя>;
# Теперь username, first_name, last_name должны быть заполнены

# 5. В Telegram (от НОВОГО пользователя):
/start → Отправить от нового пользователя
"Привет" → Отправить сообщение

# 6. Проверить что новый пользователь создан
SELECT user_id, username, first_name, last_name, created_at 
FROM users 
WHERE user_id = <ID_нового_пользователя>;
# Все поля должны быть заполнены сразу

# 7. Общая статистика
SELECT u.user_id, u.username, u.first_name, COUNT(m.id) as message_count
FROM users u
LEFT JOIN messages m ON u.user_id = m.user_id AND m.deleted_at IS NULL
GROUP BY u.user_id, u.username, u.first_name
ORDER BY message_count DESC;

# Должны быть:
# - Существующие пользователи с обновленными данными
# - Новые пользователи с полными данными
# - Количество сообщений для каждого
```

---

## 📚 Примечания

### Принципы разработки
- **KISS** - максимально простые решения
- **1 класс = 1 файл** - строгое правило
- **Type hints везде** - mypy strict mode
- **TDD цикл**: RED → GREEN → REFACTOR для каждой функциональности
- **Async/await** - все операции с БД асинхронные

### Технологический стек
- PostgreSQL 16 + SQLAlchemy 2.x (async)
- Alembic для миграций
- aiogram 3.x для Telegram Bot API
- pytest + testcontainers для тестирования
- Type hints + mypy для статической проверки типов

### Важные моменты

**Миграция данных:**
- **Два типа пользователей:**
  - **Существующие** - уже есть в таблице `messages`, но нет в `users` (нужна data-миграция)
  - **Новые** - будут подключаться после внедрения функционала
- Data-миграция создает записи с базовыми данными (user_id, created_at)
- Полные данные (username, first_name, last_name) заполняются при следующем взаимодействии через upsert

**Работа приложения:**
- Graceful degradation: если сохранение пользователя не удалось, бот продолжает работать
- Логирование всех важных операций (создание, обновление пользователей)
- Обработка edge cases: отсутствующие username, last_name и т.д.
- Использование upsert для атомарного создания/обновления

### Работа с документацией

**MCP Context7 (приоритет):**
- Используй `resolve-library-id` для поиска библиотеки
- Используй `get-library-docs` для получения актуальной документации
- Обязательно сверяйся с официальной документацией при:
  - Работе с aiogram 3.x (извлечение данных из `message.from_user`)
  - Использовании SQLAlchemy 2.x (модели, миграции)
  - Работе с pydantic (dataclasses, валидация)

**Примеры использования Context7:**
```bash
# Поиск библиотеки aiogram
resolve-library-id libraryName="aiogram"

# Получение документации по User type
get-library-docs context7CompatibleLibraryID="/aiogram/aiogram" topic="User type"

# Получение документации по SQLAlchemy async
get-library-docs context7CompatibleLibraryID="/sqlalchemy/sqlalchemy" topic="async session"
```

**Полезные ссылки:**
- [aiogram 3.x User type](https://docs.aiogram.dev/en/latest/api/types/user.html)
- [Telegram Bot API User](https://core.telegram.org/bots/api#user)
- [SQLAlchemy 2.x Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Alembic Migrations](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

---

## 🎯 Итоги спринта

После завершения спринта SP-2:
- ✅ Данные пользователей сохраняются в БД при каждом взаимодействии
- ✅ Реализован репозиторий для работы с пользователями
- ✅ Создана модель User с индексами
- ✅ **Выполнена миграция существующих пользователей из таблицы messages**
- ✅ **Работает upsert для обновления данных существующих и создания новых пользователей**
- ✅ Покрытие тестами > 80%
- ✅ Все проверки качества (ruff, mypy) проходят

**Состояние системы:**
- Все пользователи из messages теперь есть в users
- При взаимодействии данные пользователей автоматически обновляются
- Новые пользователи сразу сохраняются с полной информацией

Проект готов к следующему спринту.

