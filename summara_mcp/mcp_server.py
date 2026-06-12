"""
SUMMARA MCP-сервер.
Инструменты для Claude Desktop и других MCP-клиентов.
"""
import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# Добавляем корень проекта в путь (папка выше summara_mcp/)
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from config import BASE_DIR
from pipeline import run
from agents.pdf_export import generate_pdf, STYLES
from agents.html_export import generate_html, HTML_STYLES

EXPORTS_DIR = BASE_DIR / "exports"
EXPORTS_DIR.mkdir(exist_ok=True)

app = Server("summara")


# ── Инструменты ───────────────────────────────────────────────────────────────

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="generate_instruction",
            description=(
                "Принимает текст задачи/поручения и генерирует структурированную инструкцию. "
                "Определяет тип (задача, встреча, баг-репорт), извлекает исполнителя, срок, "
                "приоритет и возвращает готовый Markdown-документ."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Текст поручения или задачи в свободной форме"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="generate_instruction_with_pdfs",
            description=(
                "Принимает текст задачи, генерирует структурированную инструкцию и автоматически "
                "создаёт все 4 варианта PDF (Лавандовый, Розовый, Редакционный, Минимальный) "
                "в папку exports/. Возвращает инструкцию и пути к созданным файлам."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Текст поручения или задачи в свободной форме"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="export_pdfs",
            description=(
                "Создаёт все 4 варианта PDF из готового Markdown-текста инструкции "
                "и сохраняет их в папку exports/. "
                "Используйте если инструкция уже готова."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "instruction": {
                        "type": "string",
                        "description": "Готовый Markdown-текст инструкции"
                    }
                },
                "required": ["instruction"]
            }
        ),
        Tool(
            name="generate_landing",
            description=(
                "Принимает текст задачи, генерирует структурированную инструкцию и создаёт "
                "красивые HTML-страницы ВО ВСЕХ доступных стилях оформления "
                "в папку exports/, чтобы можно было выбрать понравившийся. "
                "Опционально обогащает текст (живее, примеры, пояснения, сноски)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Текст поручения или задачи в свободной форме"
                    },
                    "enrich": {
                        "type": "boolean",
                        "description": "Сделать текст живее: примеры, пояснения, сноски, эмоции (по умолчанию false)"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="transcribe_audio",
            description=(
                "Транскрибирует аудиофайл в текст с помощью Whisper. "
                "Принимает путь к файлу на локальном компьютере."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Абсолютный путь к аудиофайлу (mp3, wav, m4a, ogg и др.)"
                    }
                },
                "required": ["file_path"]
            }
        ),
    ]


# ── Обработчики ───────────────────────────────────────────────────────────────

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:

    if name == "generate_instruction":
        return await _handle_generate(arguments["text"], with_pdfs=False)

    elif name == "generate_instruction_with_pdfs":
        return await _handle_generate(arguments["text"], with_pdfs=True)

    elif name == "export_pdfs":
        paths = _export_all_pdfs(arguments["instruction"])
        lines = ["**Созданы PDF-файлы (4 стиля):**\n"]
        for style_label, path in paths.items():
            lines.append(f"- **{style_label}**: `{path}`")
        return [TextContent(type="text", text="\n".join(lines))]

    elif name == "generate_landing":
        return await _handle_landing(arguments["text"], enrich=bool(arguments.get("enrich", False)))

    elif name == "transcribe_audio":
        return await _handle_transcribe(arguments["file_path"])

    return [TextContent(type="text", text=f"Неизвестный инструмент: {name}")]


async def _handle_generate(text: str, with_pdfs: bool) -> list[TextContent]:
    try:
        result = await asyncio.get_event_loop().run_in_executor(None, run, text)
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Ошибка генерации: {e}")]

    instruction = result["rendered"]
    template = result["template"]
    validation = result["validation"]

    lines = [
        f"**Шаблон:** {template}",
        f"**Оценка качества:** {validation['score']}/10",
        "",
        "---",
        "",
        instruction,
    ]

    if with_pdfs:
        lines += ["", "---", "", "**Создаю PDF-файлы...**"]
        try:
            paths = _export_all_pdfs(instruction)
            lines.append("\n**Готовы 4 варианта PDF:**")
            for style_label, path in paths.items():
                lines.append(f"- **{style_label}**: `{path}`")
        except Exception as e:
            lines.append(f"\n❌ Ошибка создания PDF: {e}")

    return [TextContent(type="text", text="\n".join(lines))]


async def _handle_transcribe(file_path: str) -> list[TextContent]:
    if not os.path.exists(file_path):
        return [TextContent(type="text", text=f"❌ Файл не найден: {file_path}")]
    try:
        from agents.transcription import transcribe
        text = await asyncio.get_event_loop().run_in_executor(None, transcribe, file_path)
        return [TextContent(type="text", text=f"**Транскрипция:**\n\n{text}")]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Ошибка транскрипции: {e}")]


def _export_all_pdfs(instruction: str) -> dict[str, str]:
    """Создаёт все 4 стиля PDF и возвращает словарь {название: путь}."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    paths = {}
    for style_key, style_meta in STYLES.items():
        filename = EXPORTS_DIR / f"instruction_{ts}_{style_key}.pdf"
        generate_pdf(instruction, style_key, str(filename))
        paths[style_meta["label"]] = str(filename)
    return paths


def _export_all_landings(instruction: str, doc_type: str) -> dict[str, str]:
    """Создаёт HTML-страницы во ВСЕХ доступных стилях. {название: путь}."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    paths = {}
    for key, meta in HTML_STYLES.items():
        filename = EXPORTS_DIR / f"landing_{ts}_{key}.html"
        generate_html(instruction, key, str(filename), doc_type=doc_type or "")
        paths[meta.get("label", key)] = str(filename)
    return paths


async def _handle_landing(text: str, enrich: bool) -> list[TextContent]:
    try:
        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: run(text=text, enrich=enrich)
        )
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Ошибка генерации: {e}")]

    instruction = result["rendered"]
    template = result["template"]
    validation = result["validation"]

    lines = [
        f"**Шаблон:** {template}",
        f"**Оценка качества:** {validation['score']}/10",
        f"**Обогащение текста:** {'включено' if enrich else 'выключено'}",
        "",
        "---",
        "",
        instruction,
        "",
        "---",
        "",
        "**Создаю HTML-страницы во всех стилях...**",
    ]
    try:
        paths = _export_all_landings(instruction, template)
        lines.append(f"\n**Готовы веб-страницы ({len(paths)} стилей):**")
        for label, path in paths.items():
            lines.append(f"- **{label}**: `{path}`")
    except Exception as e:
        lines.append(f"\n❌ Ошибка создания лэндингов: {e}")

    return [TextContent(type="text", text="\n".join(lines))]


# ── Запуск ────────────────────────────────────────────────────────────────────

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
