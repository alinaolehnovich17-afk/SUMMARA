# SUMMARA MCP — Инструкция для Claude Desktop

Эта папка содержит MCP-сервер для подключения SUMMARA к Claude Desktop.

---

## Требования

- Python 3.10 или новее
- Claude Desktop: https://claude.ai/download
- Полная папка проекта SUMMARA (эта папка `summara_mcp/` должна лежать внутри неё)

---

## Установка (один раз)

**1. Установить зависимости** (из корневой папки SUMMARA):

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**2. Создать файл `.env`** в корне SUMMARA:

```
ANTHROPIC_API_KEY=ваш_ключ_здесь
```

Ключ получить на: https://console.anthropic.com

**3. Настроить Claude Desktop**

Открыть файл конфигурации:
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

Вставить (заменить пути на реальные):

```json
{
  "mcpServers": {
    "summara": {
      "command": "C:/путь/к/summara/.venv/Scripts/python.exe",
      "args": ["C:/путь/к/summara/summara_mcp/mcp_server.py"]
    }
  }
}
```

Пример для macOS:
```json
{
  "mcpServers": {
    "summara": {
      "command": "/Users/имя/summara/.venv/bin/python",
      "args": ["/Users/имя/summara/summara_mcp/mcp_server.py"]
    }
  }
}
```

**4. Перезапустить Claude Desktop**

---

## Использование

Открыть Claude Desktop и написать в чат:

> *«Создай инструкцию: поручить Марине редизайн главной страницы до пятницы»*

> *«Сгенерируй задачу для Ивана — разработать модуль авторизации, срочно, и сделай PDF»*

> *«Транскрибируй файл C:/recordings/meeting.mp3»*

---

## Доступные инструменты

| Инструмент | Что делает |
|---|---|
| `generate_instruction` | Текст → структурированная инструкция |
| `generate_instruction_with_pdfs` | Текст → инструкция + **4 PDF сразу** в папку `exports/` |
| `export_pdfs` | Готовый текст → 4 PDF в папку `exports/` |
| `transcribe_audio` | Аудиофайл → текст (Whisper) |

---

## Результаты

PDF-файлы сохраняются в папку `exports/` рядом с проектом:

```
exports/
  instruction_20260603_143022_lavender.pdf    ← Лавандовый
  instruction_20260603_143022_pink.pdf        ← Розовый
  instruction_20260603_143022_editorial.pdf   ← Редакционный
  instruction_20260603_143022_minimal.pdf     ← Минимальный (подложка)
```
