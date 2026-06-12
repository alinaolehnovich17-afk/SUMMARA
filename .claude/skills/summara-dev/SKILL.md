---
name: summara-dev
description: >-
  Use when working on the SUMMARA repository itself — understanding its structure,
  running the Gradio app or MCP server, making code changes, adding templates or HTML
  styles, updating docs/README, checking for errors, or preparing the project for
  public GitHub release (including secret-leak checks). Triggers on tasks about
  "this project", "SUMMARA repo", running/fixing/extending the app, or publishing.
---

# SUMMARA — рабочий скилл разработчика

Помогает Claude Code эффективно работать с репозиторием SUMMARA: понимать структуру,
запускать сервис, вносить изменения, обновлять документацию, проверять ошибки и
готовить проект к публикации.

## 0. Сначала прочитай контекст
- `CLAUDE.md` — карта кода, подводные камни, контракт Markdown.
- `JOURNAL.md` — текущие идеи/бэклог пользователя и журнал работ.
- `AUDIT.md` — известные проблемы и их приоритет.
Этого достаточно, чтобы войти в курс дела без повторного сканирования.

## 1. Запуск и проверка
```bash
# веб-приложение → http://localhost:7860
.venv/Scripts/python.exe app.py          # Windows (фоном/в отдельном процессе)
.venv/bin/python app.py                   # macOS/Linux

# MCP-сервер
.venv/Scripts/python.exe summara_mcp/mcp_server.py
```
- После правок **синтаксис-чек**: `ast.parse` изменённых файлов.
- **Экспорт** проверять рендером всех стилей через `agents/html_export.generate_html`.
- **UI** проверять Playwright-скриншотом (`.venv/Scripts/playwright`) страницы `localhost:7860`.
- **При правке `_tpl_*.py` или шаблонов — перезапускать `app.py`** (грузятся в память при импорте).

## 2. Подводные камни (критично)
1. **cp1251-консоль Windows:** в `print()` только ASCII-стрелки `->`, без `→`/эмодзи —
   иначе `UnicodeEncodeError` глушится `try/except` и тихо ломает логику.
2. **Gradio 6.x:** `css`/`theme` → в `demo.launch()`, не в `gr.Blocks()`.
3. **Jinja:** `b['items']`, не `b.items`.
4. **Контракт Markdown** (`## Заголовок`, `**Метка:** значение`, списки) обязан сохраняться
   при любой обработке текста — иначе PDF/HTML-парсеры ломаются. Парсер: `html_export.parse_markdown`.

## 3. Типовые изменения
- **Новый тип документа:** `templates/<name>.yaml` + схема в `models/schemas.py` (`SCHEMA_MAP`)
  + метка в `app.py` (`TEMPLATE_LABELS`).
- **Новый HTML-стиль:** Jinja2-шаблон в `agents/_tpl_*.py` + запись в `HTML_STYLES`
  (`agents/html_templates.py`). Следуй контракту блоков из docstring `agents/html_export.py`.
- **Промпты обработки:** дефолты в `settings.py`; пользователь правит их в UI («Настройки»).

## 4. Обновление документации
После функциональных изменений синхронизируй: `README.md`, `CLAUDE.md`, `CONTEXT.md`,
`CHANGELOG.md` и перенеси сделанное в `JOURNAL.md` (раздел «✅ Сделано», с датой).
README держи «крутым», но точным — не описывай несуществующих возможностей.

## 5. Подготовка к публикации на GitHub (проверка утечек)
Выполнять ПЕРЕД `git add`/`commit`/`push`:
```bash
# 1. Реальный ключ должен быть ТОЛЬКО в .env (он в .gitignore)
rg -l --hidden --glob '!.venv' 'sk-ant-' .          # ждём: .env, .env.example(placeholder), README(placeholder)
# 2. .env реально игнорируется git-ом
git check-ignore .env user_settings.json            # обе строки должны вернуться
# 3. В staged-файлах нет .env
git add -A && git status                            # .env НЕ должен быть в списке
```
- `.env.example` — только placeholder `sk-ant-xxxx...`, без настоящего ключа.
- `.gitignore` обязан содержать `.env`, `user_settings.json`, `.venv/`, `exports/*`, `models/*`.
- **Публикация в публичный репозиторий — действие необратимое:** не пушить без явного
  подтверждения пользователя. Предложи команды (`gh repo create SUMMARA --public ...`), но
  выполняй push только по запросу.

## 6. Что улучшать дальше
Смотри бэклог в `JOURNAL.md` и приоритеты в `AUDIT.md` (тесты, безопасный логгер для cp1251,
очистка `exports/`, профили настроек и т.д.).
