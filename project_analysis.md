# Анализ проекта MyLangSmith

## Суть проекта

**MyLangSmith** - это демонстрационный проект, который показывает различные способы организации взаимодействия между агентами (агентами искусственного интеллекта) с использованием LangChain и OpenAI API. Проект демонстрирует:

1. **Простые LangChain цепочки** - базовый пример использования LLM
2. **FIPA ACL протокол** - стандартизированный протокол для коммуникации между агентами
3. **WebSocket коммуникация** - система агентов Commander/Executor с real-time взаимодействием
4. **Прямая коммуникация** - альтернативная реализация без WebSocket

## Архитектура проекта

### Основные компоненты

```
MyLangSmith/
├── agents/                   # Агенты ИИ
│   ├── base/                # Базовые классы агентов
│   ├── websocket/           # WebSocket агенты
│   └── workers/             # Рабочие агенты (Commander/Executor)
├── buses/                   # Системы передачи сообщений
│   ├── base/               # Базовые классы шин
│   └── websocket/          # WebSocket шина
├── messages/               # Структуры сообщений
└── scripts/                # Точки входа
```

### Иерархия классов

```
FIPAAgent (базовый класс)
├── AsyncFIPAAgent (асинхронная версия)
│   ├── Supervisor (командующий агент)
│   └── Doer (исполнитель)
└── WebSocketFIPAAgent (WebSocket версия)
```

## Точка входа: commander_executor.py

### Что делает скрипт

`commander_executor.py` - это главная точка входа для демонстрации системы Commander/Executor через WebSocket. Система состоит из:

1. **WebSocket сервера** (`WebBus`) - центральный хаб для обмена сообщениями
2. **Commander (Supervisor)** - агент, принимающий команды от пользователя
3. **Executor (Doer)** - агент, выполняющий shell-команды

### Пошаговый разбор работы

#### 1. Инициализация системы
```python
async def main() -> None:
    # Создаем WebSocket шину
    bus = WebBus()
    server_task = asyncio.create_task(bus.start())
    await asyncio.sleep(0.5)  # Даем серверу время подняться
```

#### 2. Создание и подключение агентов
```python
    # Создаем исполнителя
    executor = Doer("Doer", "ws://localhost:8765")
    await executor.connect()

    # Создаем командующего
    commander = Supervisor("Supervisor", "ws://localhost:8765")
    await commander.run()
```

#### 3. Завершение работы
```python
    await commander.websocket.close()
    await executor.websocket.close()
    server_task.cancel()
```

### Как работает WebBus

**WebBus** - это простой WebSocket сервер, который:
- Принимает регистрацию клиентов
- Пересылает сообщения между подключенными агентами
- Логирует все сообщения в формате `отправитель --> получатель: содержание`

### Как работает Supervisor (Commander)

**Supervisor** - это интеллектуальный агент, который:

1. **Принимает команды от пользователя** через консольный ввод
2. **Анализирует запрос** с помощью OpenAI API:
   - Декомпозирует задачу на подзадачи
   - Определяет, нужны ли shell-команды (`NEEDS_SHELL: yes/no`)
3. **Формулирует поручение** для Doer-а человеческим языком
4. **Отправляет FIPA сообщение** типа `request` через WebSocket
5. **Ждет ответа** от Doer-а и обрабатывает результат

#### Пример взаимодействия Supervisor:
```
Пользователь: "Покажи список файлов"
↓
OpenAI анализ: "NEEDS_SHELL: yes DECOMPOSITION: • Выполнить команду ls"
↓
Формулировка для Doer: "Пожалуйста, покажи список файлов в текущей директории"
↓
Отправка FIPA сообщения: request → Doer
```

### Как работает Doer (Executor)

**Doer** - это агент-исполнитель, который:

1. **Получает FIPA сообщение** типа `request` от Supervisor
2. **Преобразует запрос в shell-команду** через OpenAI API
3. **Выполняет команду** с помощью `asyncio.create_subprocess_shell`
4. **Обрабатывает результат** через OpenAI API для создания человеко-читаемого ответа
5. **Отправляет результат** обратно Supervisor через FIPA сообщение типа `inform`

#### Пример работы Doer:
```
Получен запрос: "Покажи список файлов в текущей директории"
↓
OpenAI генерирует: "ls -la"
↓
Выполнение команды: subprocess.run("ls -la")
↓
Результат: "total 48\ndrwxr-xr-x 2 user..."
↓
OpenAI обрабатывает: "Вот список файлов в текущей директории: ..."
↓
Отправка ответа: inform → Supervisor
```

## Протокол FIPA ACL

Проект использует упрощенную версию FIPA ACL (Foundation for Intelligent Physical Agents Agent Communication Language):

### Структура сообщения
```python
@dataclass
class FIPAMessage:
    performative: str      # Тип сообщения (request, inform, etc.)
    sender: str           # Отправитель
    receiver: str         # Получатель
    content: str          # Содержимое
    conversation_id: str  # Уникальный ID беседы
```

### Типы сообщений
- **request** - запрос на выполнение действия
- **inform** - информирование о результате

## Особенности реализации

### Безопасность
- Функция `clean_input()` очищает ввод от некорректных Unicode символов
- Обработка ошибок в критических местах

### Асинхронность
- Полностью асинхронная архитектура с использованием `asyncio`
- Неблокирующий ввод пользователя через `asyncio.to_thread`

### Интеграция с OpenAI
- Использование модели `gpt-3.5-turbo` для всех задач
- Структурированные промпты для надежного парсинга ответов
- Обработка ответов на русском языке

## Запуск и использование

### Требования
```bash
pip install langchain openai websockets
export OPENAI_API_KEY="your-api-key"
```

### Запуск
```bash
python scripts/commander_executor.py
```

### Интерфейс пользователя
```
You --> Supervisor: покажи список файлов
Supervisor --> OpenAI: [запрос на анализ]
OpenAI --> Supervisor: NEEDS_SHELL: yes DECOMPOSITION: ...
Supervisor --> Doer: [запрос через WebSocket]
Doer --> Supervisor: [результат выполнения]
Supervisor --> You: Вот список файлов в текущей директории: ...
```

## Альтернативные реализации

Проект также содержит:
- **`direct_commander_executor.py`** - версия без WebSocket, с прямой коммуникацией через in-memory bus
- **`fipa_demo.py`** - демонстрация базового FIPA ACL протокола
- **`main.py`** - простой пример LangChain цепочки

Это позволяет сравнить различные подходы к организации многоагентных систем.