# CLAUDE.md

Гайд для Claude Code по работе с этим репозиторием. Коротко и по делу.

## Что это

**SUMMARA** — превращает голосовое/текстовое сообщение в структурированный документ
(инструкция, регламент, пояснение…) и красиво оформляет его: **8 стилей HTML** и
**4 стиля PDF**. Два режима: веб-приложение Gradio и MCP-сервер для Claude Desktop.

## Запуск

```bash
# Веб-приложение (http://localhost:7860)
.venv/Scripts/python.exe app.py          # Windows
.venv/bin/python app.py                   # macOS/Linux

# MCP-сервер
.venv/Scripts/python.exe summara_mcp/mcp_server.py
```

Зависимости: `.venv/Scripts/python.exe -m pip install -r requirements.txt`.
Нужен `.env` с `ANTHROPIC_API_KEY` (шаблон — `.env.example`).

## Архитектура

Пайплайн (`pipeline.py`): `transcribe → classify → extract → render(Jinja2) → [enrich] → validate`.

| Файл | Роль |
|---|---|
| `app.py` | Gradio UI и все обработчики событий |
| `pipeline.py` | Оркестратор; `run(text, audio_path, enrich)` |
| `config.py` | Модель Claude, ключ API, параметры Whisper |
| `settings.py` + `user_settings.json` | Редактируемые промпты + «вид документа» |
| `agents/transcription.py` | faster-whisper |
| `agents/classifier.py` | Claude: тип документа (task/meeting/bug_report) |
| `agents/extractor.py` | Claude tool-use: извлечение полей по схеме |
| `agents/validator.py` | Claude: оценка качества 1–10 |
| `agents/enricher.py` | Claude: «оживляет»/переоформляет текст (промпты из settings) |
| `agents/pdf_export.py` | ReportLab: 4 стиля PDF |
| `agents/html_export.py` | парсер Markdown → блоки → HTML; `generate_html` |
| `agents/html_templates.py` | реестр `HTML_STYLES` (8 стилей) |
| `agents/_tpl_a/b/c.py` | Jinja2-шаблоны стилей (a: primer 1-3, b: 4-6, c: neon/juicy) |
| `agents/selector.py` | подбор стиля по контексту — **сейчас не используется** |
| `templates/*.yaml` | структура документов + Jinja2 |
| `models/schemas.py` | Pydantic-схемы полей |
| `summara_mcp/mcp_server.py` | **канонический** MCP-сервер |
| `mcp_server.py` (корень) | редирект на канонический (для старых конфигов) |

Документы: `CONTEXT.md` (полный контекст), `JOURNAL.md` (журнал/идеи), `AUDIT.md` (аудит),
`GUIDE.md` (для пользователя), `CHANGELOG.md`.

## Контракт Markdown (ВАЖНО)

Готовая инструкция в Markdown — общий промежуточный формат. И PDF, и HTML парсят его
по правилам: `## Заголовок`, строки `**Метка:** значение`, списки `- ` и `1. `, `---`.
**Любая правка текста (включая enricher) обязана сохранять этот скелет**, иначе
экспорт в PDF/HTML сломается. Парсер — `agents/html_export.parse_markdown`.

## Подводные камни (не наступать повторно)

1. **cp1251-консоль Windows:** в `print()` НЕ использовать не-cp1251 символы (`→`, эмодзи) —
   только `->`. Иначе `UnicodeEncodeError` глушится `try/except` и тихо ломает логику.
2. **Gradio 6.x:** `css` и `theme` передаются в `demo.launch()`, НЕ в `gr.Blocks()`.
3. **После правки HTML-шаблонов** (`_tpl_*.py`) — перезапустить `app.py`
   (шаблоны грузятся в память при импорте).
4. **В Jinja используем `b['items']`**, не `b.items` (конфликт с методом dict).
5. Форматы экспорта в `app.py` — константы `FMT_HTML/FMT_TXT/FMT_JSON/FMT_PDF`.

## Как расширять

- **Новый тип документа:** `templates/<name>.yaml` + схема в `models/schemas.py` (`SCHEMA_MAP`)
  + метка в `app.py` (`TEMPLATE_LABELS`).
- **Новый HTML-стиль:** Jinja2-шаблон в `_tpl_*.py` + запись в `HTML_STYLES` (`html_templates.py`).
- **Промпты обработки текста:** правятся в UI («Настройки») или в `settings.py` (дефолты).

## Безопасность

- `.env` и `user_settings.json` — в `.gitignore`, НЕ коммитить.
- `.env.example` — только placeholder, без реальных ключей.
- Перед коммитом/публикацией проверять: `git status` не должен показывать `.env`;
  `rg --hidden 'sk-ant-' --glob '!.venv'` — реальный ключ только в `.env`.

## Проверка изменений

Нет автотестов. Минимальная проверка: `ast.parse` всех правленых файлов; для экспорта —
отрендерить все стили через `agents/html_export.generate_html`; UI-проверка через Playwright
(`.venv/Scripts/playwright`) скриншотом `http://localhost:7860`.
