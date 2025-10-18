<!-- fb86f462-79b7-4c28-8b62-e23e1cc32a6b 5e24665a-8062-4f6c-8169-8e117bdf9264 -->
# Реализация веб-чата (Подспринт 4)

## Обзор

Реализация полнофункционального веб-чата для общения с ИИ-ботом через браузер, с последующим добавлением администраторского режима Text2SQL для запросов к базе данных. Включает как unit тесты для бизнес-логики, так и API интеграционные тесты.

## Итерация 4.1: API для веб-чата

### 1. Расширение моделей API для чата

**Файл:** `src/api/models.py`

Добавить новые Pydantic модели для работы с чатом:

```python
class ChatMessageRequest(BaseModel):
    """Запрос на отправку сообщения в чат."""
    user_id: str = Field(description="ID веб-пользователя (например, 'web-user-1')")
    message: str = Field(min_length=1, max_length=4000, description="Текст сообщения")

class ChatMessageResponse(BaseModel):
    """Ответ на сообщение в чате."""
    response: str = Field(description="Ответ бота")
    message_id: int = Field(description="ID сохраненного сообщения")

class ChatHistoryItem(BaseModel):
    """Элемент истории чата."""
    role: Literal["system", "user", "assistant"]
    content: str
    created_at: datetime

class ChatHistoryResponse(BaseModel):
    """История чата пользователя."""
    messages: list[ChatHistoryItem]

class ClearHistoryResponse(BaseModel):
    """Результат очистки истории."""
    success: bool
    deleted_count: int
```

### 2. Создание обработчика чата

**Новый файл:** `src/api/chat_handler.py`

Реализовать класс `WebChatHandler` с методами:

```python
class WebChatHandler:
    """Обработчик веб-чата (аналог Telegram handlers)."""
    
    def __init__(
        self,
        llm_client: LLMClient,
        conversation_manager: ConversationManager,
        system_prompt: str
    ) -> None:
        ...
    
    async def send_message(self, user_id: str, message: str) -> tuple[str, int]:
        """Отправить сообщение и получить ответ."""
        # 1. Создать ConversationKey из user_id (chat_id = user_id для веб-чата)
        # 2. Добавить сообщение пользователя в историю
        # 3. Получить историю с system prompt
        # 4. Получить ответ от LLM
        # 5. Сохранить ответ в историю
        # 6. Вернуть (ответ, message_id)
        
    async def get_history(self, user_id: str) -> list[ChatHistoryItem]:
        """Получить историю чата."""
        
    async def clear_history(self, user_id: str) -> int:
        """Очистить историю чата."""
```

**Ключевые моменты:**

- Для веб-пользователей `chat_id = user_id` (упрощение)
- User ID должен быть преобразован в int (hash строки или использовать отрицательные числа)
- Graceful error handling с понятными сообщениями

### 3. Добавление endpoints в FastAPI

**Файл:** `src/api/app.py`

Добавить три новых endpoint:

```python
@app.post("/api/v1/chat/message", response_model=ChatMessageResponse)
async def send_chat_message(request: ChatMessageRequest) -> ChatMessageResponse:
    """Отправить сообщение в чат и получить ответ от бота."""
    
@app.get("/api/v1/chat/history/{user_id}", response_model=ChatHistoryResponse)
async def get_chat_history(user_id: str) -> ChatHistoryResponse:
    """Получить историю чата пользователя."""
    
@app.delete("/api/v1/chat/history/{user_id}", response_model=ClearHistoryResponse)
async def clear_chat_history(user_id: str) -> ClearHistoryResponse:
    """Очистить историю чата пользователя."""
```

**Интеграция:**

- Создать экземпляр `WebChatHandler` при старте приложения
- Использовать существующие `LLMClient` и `ConversationManager`
- Инициализировать `Database` и `session_factory` в app.py
- Обработка ошибок через FastAPI exception handlers

### 4. Unit тесты для WebChatHandler

**Новый файл:** `tests/test_web_chat_handler.py`

Написать изолированные unit тесты для логики:

- `send_message()` - проверка обработки сообщения
- `get_history()` - проверка получения истории
- `clear_history()` - проверка очистки
- Преобразование `user_id` (str) в `ConversationKey` (int)
- Обработка ошибок LLM (mock LLMClient для graceful degradation)
- Сохранение user и assistant сообщений в БД

### 5. API интеграционные тесты

**Новый файл:** `tests/test_chat_api.py`

Написать интеграционные тесты для HTTP endpoints:

- POST `/api/v1/chat/message` - отправка и получение ответа
- GET `/api/v1/chat/history/{user_id}` - загрузка истории
- DELETE `/api/v1/chat/history/{user_id}` - очистка истории
- Валидация Pydantic моделей (пустое сообщение, слишком длинное)
- HTTP статус коды (200, 400, 422, 500)
- CORS headers
- OpenAPI schema

**Ручное тестирование:**

```bash
# Запустить API
make run-api

# Отправить сообщение
curl -X POST http://localhost:8000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{"user_id": "web-user-1", "message": "Привет!"}'

# Получить историю
curl http://localhost:8000/api/v1/chat/history/web-user-1

# Очистить историю
curl -X DELETE http://localhost:8000/api/v1/chat/history/web-user-1
```

---

## Итерация 4.2: UI веб-чата

### 1. Создание TypeScript типов

**Новый файл:** `frontend/src/types/chat.ts`

```typescript
export interface ChatMessage {
  role: 'system' | 'user' | 'assistant'
  content: string
  created_at: string
}

export interface SendMessageRequest {
  user_id: string
  message: string
}

export interface SendMessageResponse {
  response: string
  message_id: number
}

export interface ChatHistoryResponse {
  messages: ChatMessage[]
}

export interface ClearHistoryResponse {
  success: boolean
  deleted_count: number
}
```

### 2. Создание API методов для чата

**Новый файл:** `frontend/src/api/chat.ts`

```typescript
import { get, post, del } from './client'
import type { 
  SendMessageRequest, 
  SendMessageResponse, 
  ChatHistoryResponse,
  ClearHistoryResponse 
} from '@/types/chat'

export async function sendMessage(data: SendMessageRequest): Promise<SendMessageResponse> {
  return post<SendMessageResponse, SendMessageRequest>('/chat/message', data)
}

export async function getChatHistory(userId: string): Promise<ChatHistoryResponse> {
  return get<ChatHistoryResponse>(`/chat/history/${userId}`)
}

export async function clearChatHistory(userId: string): Promise<ClearHistoryResponse> {
  return del<ClearHistoryResponse>(`/chat/history/${userId}`)
}
```

### 3. Создание компонента ChatMessage

**Новый файл:** `frontend/src/components/ChatMessage.tsx`

Компонент для отображения одного сообщения:

- Разный стиль для user/assistant сообщений
- User сообщения справа (синий фон)
- Assistant сообщения слева (серый фон)
- Timestamp (опционально)
- Поддержка многострочного текста
```typescript
interface ChatMessageProps {
  role: 'user' | 'assistant'
  content: string
  timestamp?: string
}
```


### 4. Создание компонента ChatInput

**Новый файл:** `frontend/src/components/ChatInput.tsx`

Компонент для ввода сообщений:

- Textarea для ввода (с автоувеличением высоты)
- Кнопка отправки
- Disabled состояние при загрузке
- Обработка Enter (отправка) и Shift+Enter (новая строка)
- Валидация (непустое сообщение)
```typescript
interface ChatInputProps {
  onSendMessage: (message: string) => void
  disabled: boolean
}
```


### 5. Реализация страницы Chat

**Файл:** `frontend/src/pages/Chat.tsx`

Основная логика чата:

```typescript
export default function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const userId = 'web-user-1' // TODO: заменить на реальную аутентификацию
  
  // Загрузка истории при монтировании
  useEffect(() => {
    loadHistory()
  }, [])
  
  // Auto-scroll к последнему сообщению
  const messagesEndRef = useRef<HTMLDivElement>(null)
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])
  
  async function loadHistory() { ... }
  async function handleSendMessage(message: string) { ... }
  async function handleClearHistory() { ... }
  
  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b p-4">
        <h1>Chat with AI Assistant</h1>
        <Button onClick={handleClearHistory}>Clear History</Button>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((msg, idx) => (
          <ChatMessage key={idx} {...msg} />
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="border-t p-4">
        <ChatInput 
          onSendMessage={handleSendMessage}
          disabled={isLoading}
        />
      </div>
    </div>
  )
}
```

**Функционал:**

- Загрузка истории при открытии страницы
- Отправка сообщения и получение ответа
- Индикатор загрузки ("Assistant is typing...")
- Обработка ошибок (показать Alert)
- Очистка истории с подтверждением
- Auto-scroll к новым сообщениям

### 6. Тестирование UI

**Ручная проверка:**

- Отправка нескольких сообщений подряд
- Проверка сохранения истории (перезагрузить страницу)
- Очистка истории
- Обработка ошибок (остановить API)
- Responsive дизайн на mobile/tablet

---

## Итерация 4.3: Админ-чат с Text2SQL

### 1. Создание Text2SQL промпта

**Новый файл:** `prompts/text2sql.txt`

Системный промпт для Text2SQL режима:

```
Ты SQL ассистент. Твоя задача - преобразовывать вопросы пользователя в SQL запросы к PostgreSQL базе данных.

Доступные таблицы:
- users (id, telegram_id, username, first_name, last_name, created_at)
- messages (id, chat_id, user_id, role, content, created_at, deleted_at)

Правила:
1. Используй ТОЛЬКО SELECT запросы (read-only)
2. Всегда учитывай deleted_at IS NULL для messages
3. Форматируй результаты в понятном виде
4. Если вопрос не относится к БД, вежливо откажись

Формат ответа:
1. SQL запрос
2. Результат выполнения
3. Интерпретация результата
```

### 2. Создание обработчика Text2SQL

**Новый файл:** `src/api/text2sql_handler.py`

```python
class Text2SQLHandler:
    """Обработчик Text2SQL запросов для администратора."""
    
    def __init__(
        self,
        llm_client: LLMClient,
        session_factory: Callable[[], AsyncGenerator[AsyncSession, None]],
        text2sql_prompt: str
    ) -> None:
        ...
    
    async def process_query(self, user_query: str) -> Text2SQLResponse:
        """
        Обработать Text2SQL запрос.
        
        1. Отправить вопрос в LLM с Text2SQL промптом
        2. Извлечь SQL из ответа
        3. Валидировать SQL (только SELECT, whitelist таблиц)
        4. Выполнить SQL (read-only)
        5. Отправить результаты обратно в LLM
        6. Получить финальный ответ
        """
        
    def validate_sql(self, sql: str) -> bool:
        """Валидация SQL: только SELECT, whitelist таблиц."""
        
    async def execute_sql(self, sql: str) -> list[dict]:
        """Выполнить SQL запрос (read-only)."""
```

**Безопасность:**

- Regex проверка на SELECT only: `^SELECT\s+.*FROM\s+(users|messages)`
- Запрет на: INSERT, UPDATE, DELETE, DROP, ALTER, CREATE
- Whitelist таблиц: только users и messages
- Timeout для SQL запросов (5 секунд)
- Rate limiting (опционально)

### 3. Добавление API endpoint и моделей

**Файл:** `src/api/models.py`

Добавить модели:

```python
class Text2SQLRequest(BaseModel):
    query: str = Field(description="Вопрос на естественном языке")
    
class Text2SQLResponse(BaseModel):
    sql: str = Field(description="Сгенерированный SQL запрос")
    result: list[dict] = Field(description="Результат выполнения")
    interpretation: str = Field(description="Интерпретация результата")
```

**Файл:** `src/api/app.py`

```python
@app.post("/api/v1/admin/query", response_model=Text2SQLResponse)
async def execute_text2sql(request: Text2SQLRequest) -> Text2SQLResponse:
    """
    Выполнить Text2SQL запрос (только для администраторов).
    
    TODO: Добавить аутентификацию администратора
    """
```

### 4. Unit тесты для Text2SQLHandler

**Новый файл:** `tests/test_text2sql_handler.py`

Написать unit тесты для:

- `validate_sql()` - проверка валидации (только SELECT)
- Блокировка опасных запросов (DELETE, UPDATE, DROP и т.д.)
- Whitelist таблиц (только users, messages)
- `execute_sql()` - выполнение безопасных запросов
- Обработка SQL ошибок (синтаксические ошибки)
- Timeout для долгих запросов

### 5. API интеграционные тесты для Text2SQL

**Файл:** `tests/test_chat_api.py` (расширить)

Добавить тесты для:

- POST `/api/v1/admin/query` - успешное выполнение
- Валидация Pydantic модели Text2SQLRequest
- Блокировка опасных SQL через API
- HTTP 400 для невалидного SQL
- HTTP 200 для валидного запроса

### 6. Добавление админ-режима в UI

**Файл:** `frontend/src/pages/Chat.tsx`

Добавить переключатель режима:

```typescript
const [isAdminMode, setIsAdminMode] = useState(false)

// В header:
<div className="flex items-center gap-4">
  <Switch 
    checked={isAdminMode}
    onCheckedChange={setIsAdminMode}
  />
  <Label>Admin Mode (Text2SQL)</Label>
</div>
```

**Логика:**

- Если `isAdminMode === true`, использовать `/admin/query` endpoint
- Показывать SQL запрос в отдельном блоке (code block)
- Показывать результаты в таблице
- Показывать интерпретацию LLM

### 7. Компонент для отображения SQL результатов

**Новый файл:** `frontend/src/components/SQLResultDisplay.tsx`

```typescript
interface SQLResultDisplayProps {
  sql: string
  result: Array<Record<string, unknown>>
  interpretation: string
}
```

Отображает:

- SQL запрос (syntax highlighted)
- Таблица с результатами (использовать shadcn Table)
- Текстовая интерпретация

### 8. Ручное тестирование Text2SQL

**Примеры вопросов:**

```bash
# Должны работать
- "Сколько всего пользователей?"
- "Покажи топ 5 пользователей по количеству сообщений"
- "Какой процент пользователей активен?"
- "Сколько сообщений отправлено за последнюю неделю?"
```

**Проверка безопасности (должны быть заблокированы):**

```bash
- "DELETE FROM users"
- "UPDATE messages SET content = 'hack'"
- "DROP TABLE messages"
```

---

## Финальная проверка

### Чеклист функционала

#### Итерация 4.1 - API

- [ ] Модели ChatMessageRequest/Response созданы
- [ ] WebChatHandler реализован
- [ ] Endpoints /chat/message, /chat/history, /chat/history DELETE работают
- [ ] Unit тесты для WebChatHandler (tests/test_web_chat_handler.py)
- [ ] API тесты для endpoints (tests/test_chat_api.py)
- [ ] Интеграция с LLMClient и ConversationManager
- [ ] OpenAPI документация обновлена

#### Итерация 4.2 - UI

- [ ] Компонент ChatMessage отображает сообщения
- [ ] Компонент ChatInput принимает ввод
- [ ] Страница Chat загружает историю
- [ ] Отправка сообщений и получение ответов работает
- [ ] Очистка истории работает
- [ ] Loading states отображаются корректно
- [ ] Error handling работает
- [ ] Auto-scroll к новым сообщениям
- [ ] Responsive дизайн

#### Итерация 4.3 - Text2SQL

- [ ] Text2SQL промпт создан
- [ ] Text2SQLHandler реализован
- [ ] Unit тесты для Text2SQLHandler (tests/test_text2sql_handler.py)
- [ ] API тесты для /admin/query endpoint
- [ ] SQL валидация работает (только SELECT)
- [ ] Endpoint /admin/query работает
- [ ] UI переключатель админ-режима
- [ ] SQLResultDisplay компонент создан
- [ ] Безопасность: опасные запросы блокируются
- [ ] Coverage > 70% для новых модулей

### Команды для проверки

```bash
# Backend тестирование
make test              # Запустить все тесты (unit + API)
make test-cov          # Тесты с coverage
make quality           # Проверить качество кода
make run-api           # Запустить API сервер

# Frontend тестирование
cd frontend && npm run dev     # Dev сервер
cd frontend && npm run lint    # Линтер

# Интеграционное тестирование
# 1. Запустить API: make run-api
# 2. Запустить Frontend: cd frontend && npm run dev
# 3. Открыть http://localhost:5173/chat
# 4. Проверить отправку сообщений
# 5. Включить Admin Mode и протестировать Text2SQL
```

### Обновление документации

После завершения обновить в `docs/tasklists/tasklist-sp3.md`:

- Итерация 4.1: ✅ Завершено
- Итерация 4.2: ✅ Завершено
- Итерация 4.3: ✅ Завершено

### Известные ограничения

1. **Аутентификация:** Пока используется захардкоженный `user_id = "web-user-1"`, в будущем нужно добавить настоящую аутентификацию
2. **Admin Mode:** Нет проверки прав администратора, любой может включить режим (TODO для следующих спринтов)
3. **Rate limiting:** Нет ограничения частоты запросов к LLM
4. **Streaming:** Ответы приходят целиком, нет потоковой передачи (SSE)

Эти ограничения приемлемы для текущего спринта и могут быть реализованы позже.

### To-dos

- [ ] Расширить src/api/models.py моделями для чата (ChatMessageRequest, ChatMessageResponse, ChatHistoryItem и др.)
- [ ] Создать src/api/chat_handler.py с классом WebChatHandler для обработки веб-чата
- [ ] Добавить endpoints в src/api/app.py: POST /chat/message, GET /chat/history/{user_id}, DELETE /chat/history/{user_id}
- [ ] Написать тесты для chat API в tests/test_chat_api.py
- [ ] Создать frontend/src/types/chat.ts с TypeScript типами для чата
- [ ] Создать frontend/src/api/chat.ts с методами sendMessage, getChatHistory, clearChatHistory
- [ ] Создать frontend/src/components/ChatMessage.tsx для отображения сообщений
- [ ] Создать frontend/src/components/ChatInput.tsx для ввода сообщений
- [ ] Реализовать frontend/src/pages/Chat.tsx с полным функционалом чата
- [ ] Создать prompts/text2sql.txt с системным промптом для Text2SQL
- [ ] Создать src/api/text2sql_handler.py с классом Text2SQLHandler и валидацией SQL
- [ ] Добавить endpoint POST /admin/query в src/api/app.py для Text2SQL
- [ ] Добавить переключатель админ-режима в frontend/src/pages/Chat.tsx
- [ ] Создать frontend/src/components/SQLResultDisplay.tsx для отображения SQL результатов
- [ ] Финальное тестирование всех функций, проверка безопасности Text2SQL, обновление tasklist-sp3.md