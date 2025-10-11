# 📋 План разработки systech-aidd

## 📊 Отчет о прогрессе

| № | Итерация | Статус | Тестирование | Дата завершения |
|---|----------|--------|--------------|-----------------|
| 1 | Базовая инфраструктура + Echo bot | ✅ Завершено | ✅ Passed | 2025-10-10 |
| 2 | LLM клиент | ✅ Завершено | ✅ Passed | 2025-10-10 |
| 3 | Интеграция Telegram + LLM | ✅ Завершено | ✅ Passed | 2025-10-10 |
| 4 | История диалогов | ✅ Завершено | ✅ Passed | 2025-10-10 |
| 5 | Финальная интеграция | ✅ Завершено | ✅ Passed | 2025-10-10 |
| 6 | Команда /role и системный промпт из файла | ✅ Завершено | ✅ Passed | 2025-10-11 |

**Легенда статусов:**
- ⏳ Ожидает
- 🔄 В работе
- ✅ Завершено
- ⚠️ Проблемы

---

## 🚀 Итерация 1: Базовая инфраструктура + Echo bot

**Цель:** Создать основу проекта и простой эхо-бот, который повторяет сообщения пользователя

### Задачи
- [x] Создать структуру директорий `src/`
- [x] Реализовать `config.py` с pydantic-settings
- [x] Создать `.env.example` с примером конфигурации
- [x] Настроить логирование в `main.py`
- [x] Создать `pyproject.toml` с зависимостями
- [x] Создать `Makefile` с базовыми командами
- [x] Создать `bot.py` с инициализацией aiogram
- [x] Реализовать `handlers.py` с командами `/start`, `/help` и обработкой текстовых сообщений (echo)
- [x] Запустить polling

### Тест
```bash
# Запустить бота
make run

# В Telegram:
/start  → "Привет! Я LLM-ассистент..." (или подобное приветствие)
/help   → "Доступные команды..."
"Привет!" → "Привет!" (эхо)
"Тест" → "Тест" (эхо)
```

---

## 🧠 Итерация 2: LLM клиент

**Цель:** Создать клиент для работы с OpenRouter API

### Задачи
- [x] Создать `models.py` с базовыми моделями данных (Message)
- [x] Создать `llm_client.py` с LLMClient классом
- [x] Настроить openai клиент с base_url на OpenRouter
- [x] Реализовать метод `get_response()` для получения ответа
- [x] Добавить обработку ошибок и таймаутов
- [x] Создать отдельный скрипт `dev_test_llm.py` для тестирования LLM клиента

### Тест
```bash
# Запустить тест LLM клиента
python dev_test_llm.py

# Должен выполнить тестовый запрос к OpenRouter и получить ответ
# Пример: отправить "Привет!" и получить ответ от LLM

# После успешного теста файл dev_test_llm.py можно удалить
```

---

## 🔗 Итерация 3: Интеграция Telegram + LLM

**Цель:** Бот отвечает через LLM вместо эха

### Задачи
- [x] Интегрировать LLMClient в handlers
- [x] Изменить обработку текстовых сообщений: вместо эха отправлять запрос в LLM
- [x] Добавить команду `/clear` (подготовка к истории диалогов)
- [x] Обработка ошибок LLM API в handlers
- [x] Тестирование интеграции

### Тест
```bash
# Запустить бота
make run

# В Telegram отправить сообщения:
"Привет!" → Получить ответ от LLM
"Как дела?" → Получить ответ от LLM (пока без контекста предыдущих сообщений)
/clear → "История диалога очищена" (пока просто команда без функционала)
```

---

## 💬 Итерация 4: История диалогов

**Цель:** Бот хранит историю и отправляет контекст в LLM

### Задачи
- [x] Создать `conversation.py` с ConversationManager
- [x] Реализовать хранение истории в памяти (dict)
- [x] Добавить ограничение на количество сообщений
- [x] Интегрировать ConversationManager в handlers
- [x] Реализовать очистку истории по `/clear`

### Тест
```bash
# Запустить бота
make run

# В Telegram вести диалог:
"Меня зовут Павел"
"Как меня зовут?"  → Должен ответить "Павел"
/clear             → "История очищена"
"Как меня зовут?"  → Не должен помнить имя
```

---

## ✨ Итерация 5: Финальная интеграция

**Цель:** Полировка, документация, готовый к использованию бот

### Задачи
- [x] Добавить игнорирование неподдерживаемых типов сообщений
- [x] Протестировать все команды
- [x] Обновить README.md с инструкциями по запуску
- [x] Добавить .gitignore (если отсутствует)
- [x] Проверить работу в DEBUG и INFO режимах логирования
- [x] Финальное тестирование всех сценариев

### Тест
```bash
# Полный цикл тестирования:
1. make install  → Установка зависимостей
2. make run      → Запуск бота
3. Тест /start, /help, /clear
4. Тест обычного диалога с историей
5. Отправить фото/стикер → Игнорируется
6. Проверить логи (INFO режим)
7. Проверить логи (DEBUG режим)
```

---

## 🎭 Итерация 6: Команда /role и системный промпт из файла

**Цель:** Реализовать команду `/role` для отображения роли ассистента и загрузку системного промпта из файла

### Задачи

**Подготовка (без TDD):**
- [ ] Создать директорию `prompts/`
- [ ] Создать файл `prompts/system.txt` с дефолтным промптом
- [ ] Обновить `.env.example` с переменной `SYSTEM_PROMPT_FILE`

**Реализация по TDD (RED → GREEN → REFACTOR):**

**Функциональность 1: Загрузка системного промпта из файла**
- [ ] 🔴 RED: Написать тест для загрузки промпта из существующего файла
- [ ] 🟢 GREEN: Реализовать функцию загрузки промпта из файла
- [ ] 🔵 REFACTOR: Улучшить код загрузки промпта

**Функциональность 2: Fallback на дефолтный промпт**
- [ ] 🔴 RED: Написать тест для fallback на дефолт если файл не найден
- [ ] 🟢 GREEN: Реализовать fallback логику с warning в логе
- [ ] 🔵 REFACTOR: Упростить логику обработки ошибок

**Функциональность 3: Добавить `system_prompt_file` в Config**
- [ ] 🔴 RED: Написать тест для нового поля в Config
- [ ] 🟢 GREEN: Добавить поле `system_prompt_file` в Config с дефолтным значением
- [ ] 🔵 REFACTOR: Убедиться в корректной валидации

**Функциональность 4: Команда /role**
- [ ] 🔴 RED: Написать тест для обработчика команды `/role`
- [ ] 🟢 GREEN: Реализовать обработчик команды `/role` в handlers
- [ ] 🔵 REFACTOR: Оптимизировать код обработчика

**Функциональность 5: Обновить /help**
- [ ] 🔴 RED: Написать тест для обновленного `/help` (включает `/role`)
- [ ] 🟢 GREEN: Добавить `/role` в список команд
- [ ] 🔵 REFACTOR: Улучшить форматирование справки

**Функциональность 6: Интеграция в main.py**
- [ ] 🔴 RED: Написать интеграционный тест для загрузки промпта при старте
- [ ] 🟢 GREEN: Интегрировать загрузку промпта в main.py
- [ ] 🔵 REFACTOR: Упростить инициализацию

**Финальная проверка:**
- [ ] Запустить `make quality` - все проверки должны пройти
- [ ] Запустить `make test-cov` - покрытие минимум 70%
- [ ] Все тесты должны быть зелеными

### TDD План

#### Функциональность 1: Загрузка системного промпта из файла

**🔴 RED - Тест:**
```python
# tests/test_config.py
def test_load_system_prompt_from_file(tmp_path):
    """Тест загрузки системного промпта из файла."""
    # Создать временный файл с промптом
    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text("Ты тестовый ассистент.", encoding="utf-8")
    
    # Загрузить промпт
    prompt = load_system_prompt(str(prompt_file))
    
    # Проверить
    assert prompt == "Ты тестовый ассистент."
```

**🟢 GREEN - Минимальный код:**
```python
# src/config.py или src/main.py
def load_system_prompt(file_path: str) -> str:
    """Загрузить системный промпт из файла."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()
```

**🔵 REFACTOR - Улучшения:**
- Добавить type hints
- Добавить docstring
- Убедиться в корректной обработке encoding

#### Функциональность 2: Fallback на дефолтный промпт

**🔴 RED - Тест:**
```python
# tests/test_config.py
def test_load_system_prompt_fallback_on_missing_file():
    """Тест fallback на дефолтный промпт при отсутствии файла."""
    # Попытаться загрузить несуществующий файл
    prompt = load_system_prompt_with_fallback("nonexistent.txt")
    
    # Проверить дефолтное значение
    assert prompt == "Ты полезный ассистент."
```

**🟢 GREEN - Минимальный код:**
```python
# src/config.py или src/main.py
def load_system_prompt_with_fallback(file_path: str) -> str:
    """Загрузить системный промпт с fallback на дефолт."""
    try:
        return load_system_prompt(file_path)
    except FileNotFoundError:
        logger.warning(f"Файл промпта не найден: {file_path}, используется дефолтный")
        return "Ты полезный ассистент."
```

**🔵 REFACTOR - Улучшения:**
- Вынести дефолтный промпт в константу
- Улучшить сообщение в логе
- Добавить type hints и docstring

#### Функциональность 3: Добавить `system_prompt_file` в Config

**🔴 RED - Тест:**
```python
# tests/test_config.py
def test_config_system_prompt_file_default():
    """Тест дефолтного значения system_prompt_file в конфиге."""
    config = Config(
        telegram_token="test_token",
        openrouter_api_key="test_key"
    )
    assert config.system_prompt_file == "prompts/system.txt"
```

**🟢 GREEN - Минимальный код:**
```python
# src/config.py
class Config(BaseSettings):
    # ... существующие поля ...
    system_prompt_file: str = "prompts/system.txt"
```

**🔵 REFACTOR - Улучшения:**
- Добавить комментарий к полю
- Убедиться в корректности type hints

#### Функциональность 4: Команда /role

**🔴 RED - Тест:**
```python
# tests/test_handlers.py
async def test_role_command():
    """Тест команды /role."""
    # Arrange
    message = MockMessage(text="/role", chat_id=1, user_id=1)
    handler = MessageHandler(bot, llm_client, conv_manager, system_prompt="Ты тестовый бот.")
    
    # Act
    await handler.handle_role(message)
    
    # Assert
    assert message.answer_called
    assert "Ты тестовый бот." in message.last_answer
```

**🟢 GREEN - Минимальный код:**
```python
# src/handlers.py
async def handle_role(self, message: Message) -> None:
    """Обработчик команды /role."""
    await message.answer(f"Моя роль:\n\n{self.system_prompt}")
```

**🔵 REFACTOR - Улучшения:**
- Улучшить форматирование ответа
- Добавить эмодзи для наглядности (опционально)
- Добавить type hints и docstring

#### Функциональность 5: Обновить /help

**🔴 RED - Тест:**
```python
# tests/test_handlers.py
async def test_help_command_includes_role():
    """Тест что /help включает команду /role."""
    # Arrange
    message = MockMessage(text="/help", chat_id=1, user_id=1)
    handler = MessageHandler(bot, llm_client, conv_manager, system_prompt="test")
    
    # Act
    await handler.handle_help(message)
    
    # Assert
    assert "/role" in message.last_answer
```

**🟢 GREEN - Минимальный код:**
```python
# src/handlers.py
async def handle_help(self, message: Message) -> None:
    """Обработчик команды /help."""
    help_text = """
Доступные команды:
/start - начать работу с ботом
/help - показать справку
/clear - очистить историю диалога
/role - показать роль ассистента
"""
    await message.answer(help_text)
```

**🔵 REFACTOR - Улучшения:**
- Улучшить форматирование
- Убедиться в консистентности стиля

### Тест

#### Автоматизированное тестирование
```bash
# TDD цикл для каждой функциональности
make test        # После каждого RED/GREEN шага
make quality     # В REFACTOR фазе
make test-cov    # Финальная проверка покрытия
```

#### Ручное тестирование
```bash
# Создать prompts/system.txt с кастомным промптом
mkdir -p prompts
echo "Ты специализированный ассистент для технической поддержки." > prompts/system.txt

# Запустить бота
make run

# В Telegram:
/start              → Приветствие
/role               → "Моя роль:\n\nТы специализированный ассистент..."
/help               → Список команд (включая /role)
"Привет"            → Ответ в рамках роли
/clear              → "История очищена"
"Как меня зовут?"   → Не должен помнить (история очищена)

# Тест fallback на дефолт
rm prompts/system.txt
make run            → В логах: WARNING "Файл промпта не найден, используется дефолтный"
/role               → "Моя роль:\n\nТы полезный ассистент."
```

#### Проверка логирования
```bash
# В логах при старте должно быть:
# - INFO: "Bot started successfully"
# - Если файла нет: WARNING: "Файл промпта не найден..."

# Убедиться что бот работает в обоих случаях:
# 1. С файлом prompts/system.txt
# 2. Без файла (fallback на дефолт)
```

---

## 📝 Примечания

- Каждая итерация должна быть завершена и протестирована перед переходом к следующей
- После завершения итерации обновить таблицу прогресса
- Следовать принципу KISS - простые решения
- Правило: **1 класс = 1 файл**
- Все асинхронно через `async/await`
- **TDD цикл**: RED → GREEN → REFACTOR для каждой функциональности


