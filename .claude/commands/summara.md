---
description: "SUMMARA — голосовые/текстовые сообщения в структурированные инструкции"
allowed-tools: Bash, PowerShell, Read, Write, Edit, Glob, Grep
argument-hint: "[setup | run | generate <текст> | status | help]"
---

Ты помогаешь пользователю работать с проектом **SUMMARA**.

**Что такое SUMMARA:**
Веб-приложение + MCP-сервер. Принимает голосовые или текстовые сообщения и преобразует их в структурированные рабочие инструкции (Markdown, TXT, JSON, PDF) через Whisper + Claude API.

**Стек:** Python 3.11, Gradio 6.x, faster-whisper (base, CPU), Anthropic SDK (claude-sonnet-4-6), ReportLab, MCP.

**Аргументы пользователя:** $ARGUMENTS

---

## Логика обработки аргументов

### Нет аргументов или "help"
Выведи это:
```
SUMMARA — доступные команды:
  /summara setup          — установка зависимостей и настройка .env
  /summara run            — запустить веб-интерфейс (localhost:7860)
  /summara status         — проверить что всё установлено и работает
  /summara generate <txt> — сгенерировать инструкцию из текста напрямую
  /summara help           — эта справка
```

---

### "setup"
Выполни установку пошагово:

1. **Определи ОС** — Windows (PowerShell) или Linux/macOS (Bash)

2. **Проверь Python:**
   - Windows: `python --version` или `py --version`
   - Linux/macOS: `python3 --version`
   - Нужен 3.11+. Если нет — сообщи пользователю установить.

3. **Создай виртуальное окружение** (если нет папки `.venv`):
   - Windows: `python -m venv .venv`
   - Linux/macOS: `python3 -m venv .venv`

4. **Установи зависимости:**
   - Windows: `.venv\Scripts\pip install -r requirements.txt`
   - Linux/macOS: `.venv/bin/pip install -r requirements.txt`

5. **Проверь .env:**
   - Если файл `.env` отсутствует — скопируй из `.env.example` и попроси пользователя вставить `ANTHROPIC_API_KEY`
   - Если `.env` есть — проверь что там есть строка `ANTHROPIC_API_KEY=`

6. **Сообщи результат:** что установлено, что готово к запуску.

**Важно для Linux/macOS:** шрифты Arial, Calibri, Times New Roman нужно установить отдельно — иначе PDF будут с fallback-шрифтом. Модель Whisper (~150 МБ) скачивается при первом запуске автоматически.

---

### "run"
Запусти приложение:
- Windows: `.venv\Scripts\python app.py`
- Linux/macOS: `.venv/bin/python app.py`

Сообщи пользователю что интерфейс откроется на `http://localhost:7860`.

---

### "status"
Проверь по порядку:
1. Существует ли `.venv/`
2. Установлены ли зависимости — создай файл `_check.py` с содержимым:
   ```python
   import gradio, anthropic, faster_whisper, reportlab; print('OK')
   ```
   Запусти: Windows — `.venv\Scripts\python _check.py`, Linux/macOS — `.venv/bin/python _check.py`.
   Удали файл после проверки.
3. Есть ли `.env` с `ANTHROPIC_API_KEY`
4. Существуют ли ключевые файлы: `app.py`, `pipeline.py`, `agents/`, `templates/`

Выведи таблицу результатов.

---

### "generate <текст>"
Сгенерируй инструкцию и 4 PDF-файла прямо из Claude Code, без запуска Gradio.

**Шаг 1 — создай временный скрипт через Write tool:**

Запиши файл `_summara_run.py` в корень проекта со следующим содержимым,
подставив текст пользователя в переменную `text`:

```python
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, '.')
from pipeline import run
from agents.pdf_export import generate_pdf
from pathlib import Path
import time

text = '<текст пользователя>'
result = run(text=text)
instruction = result['rendered']
ts = int(time.time())
exports = Path('exports')
exports.mkdir(exist_ok=True)

for style in ['lavender', 'pink', 'editorial', 'minimal']:
    out = str(exports / f'instruction_{ts}_{style}.pdf')
    generate_pdf(instruction, style, out)
    print(f'PDF [{style}]: {out}')

print('---')
print(f"Шаблон: {result['template']}")
print(f"Оценка: {result['validation']['score']}/10")
print()
print(instruction)
```

**Шаг 2 — запусти скрипт и перенаправь вывод в файл:**

- Windows:
  ```
  .venv\Scripts\python _summara_run.py 2>&1 | Out-File -FilePath _summara_out.txt -Encoding utf8
  Get-Content _summara_out.txt
  ```
- Linux/macOS:
  ```
  .venv/bin/python _summara_run.py 2>&1 | tee _summara_out.txt
  ```

**Шаг 3 — удали временные файлы:**

- Windows: `Remove-Item _summara_run.py, _summara_out.txt -Force`
- Linux/macOS: `rm _summara_run.py _summara_out.txt`

**Шаг 4 — выведи пользователю:**
- Путь к папке `exports/` с 4 PDF-файлами
- Определённый шаблон (task / meeting / bug_report)
- Оценку качества (score/10)
- Саму инструкцию в Markdown

---

## Структура проекта

```
summara/
├── app.py              — Gradio UI
├── pipeline.py         — оркестрация (classifier → extractor → validator → render)
├── config.py           — пути, API-ключ, настройки
├── requirements.txt    — зависимости
├── .env                — ANTHROPIC_API_KEY (не в git)
├── .env.example        — шаблон
├── agents/
│   ├── transcription.py — Whisper транскрипция
│   ├── classifier.py    — тип сообщения
│   ├── extractor.py     — извлечение полей
│   ├── validator.py     — оценка качества
│   └── pdf_export.py    — 4 стиля PDF
├── templates/           — task.yaml, meeting.yaml, bug_report.yaml
├── models/schemas.py    — Pydantic-схемы
├── summara_mcp/
│   ├── mcp_server.py    — MCP-сервер для Claude Desktop
│   └── README.md        — инструкция по подключению
├── logo/                — логотип SUMMARA
├── pdl/                 — подложка для PDF-стиля "Минимальный"
└── exports/             — сгенерированные файлы
```

---

## Технические правила (соблюдай при редактировании кода)

- **Gradio 6.x:** `theme` передаётся в `demo.launch()`, НЕ в `gr.Blocks()`
- **Queue:** `demo.queue()` обязателен для generator-функций
- **Кириллица на Windows:** `print()` падает с cp1251; использовать `sys.stdout.buffer.write("текст\n".encode('utf-8'))`
- **ReportLab XML:** цвет и шрифт указывать явно через `<font name=... size=... color=...>`, иначе ParagraphStyle перекрывается
- **clear_all()** возвращает ровно 10 значений: audio_input, text_box, instruction_box, json_box, template_label, val_status_box, val_details_box, audio_status, confirm_status, export_file
- **PDF minimal:** поля top=20mm, bottom=60mm; заголовок 21pt, по центру, цвет #8a6820

## MCP-сервер (для Claude Desktop)

Конфиг в `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "summara": {
      "command": "/абсолютный/путь/к/.venv/Scripts/python.exe",
      "args": ["/абсолютный/путь/к/summara_mcp/mcp_server.py"]
    }
  }
}
```

Инструменты MCP:
- `generate_instruction` — текст → инструкция
- `generate_instruction_with_pdfs` — текст → инструкция + 4 PDF
- `export_pdfs` — готовый текст → 4 PDF
- `transcribe_audio` — путь к аудио → текст
