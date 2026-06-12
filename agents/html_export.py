"""
HTML-экспорт инструкций — 6 стилей оформления «лэндинг».

Готовая Markdown-инструкция (та же, что идёт в PDF) парсится в структуру
блоков и рендерится через Jinja2 в самодостаточную HTML-страницу
(весь CSS и логотип встроены инлайн — файл открывается оффлайн).

Контракт структуры (то, что получают шаблоны через Jinja2-контекст):

    {
      "title":   str,             # текст первого "## " (заголовок документа)
      "doc_type": str,            # "task" | "meeting" | "bug_report"
      "logo_b64": str,            # base64 JPEG для <img src="data:image/jpeg;base64,...">
      "blocks": [
         {"type": "field",  "label": str, "value": str},
         {"type": "group",  "label": str|None, "ordered": bool, "items": [str, ...]},
         {"type": "heading","text": str},
         {"type": "para",   "text": str},
         {"type": "divider"},
      ],
    }

Inline-разметка внутри значений/пунктов (**жирный**, *курсив*) преобразуется
в <strong>/<em> функцией `inline_md` (доступна в шаблонах как фильтр `md`).
"""
import re
import base64
from pathlib import Path
from jinja2 import Environment

from .html_templates import HTML_STYLES  # noqa: E402  (определяется субагентами)

# ── Логотип ─────────────────────────────────────────────────────────────────

_LOGO_PATH = Path(__file__).parent.parent / "logo" / "1232321.jpg"


def _logo_b64() -> str:
    try:
        return base64.b64encode(_LOGO_PATH.read_bytes()).decode()
    except Exception:
        return ""


# ── Inline-разметка ───────────────────────────────────────────────────────────

def _escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
    )


def inline_md(text: str) -> str:
    """**жирный** / *курсив* / сноски [1] → HTML. Экранирует остальное."""
    text = _escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    # Сноски-маркеры вида [1] → надстрочные
    text = re.sub(r"\[(\d+)\]", r"<sup>[\1]</sup>", text)
    return text


# ── Парсер Markdown → блоки ────────────────────────────────────────────────────

_FIELD_RE = re.compile(r"^\*\*(.+?):\*\*\s*(.*)$")
_NUM_RE = re.compile(r"^(\d+)\.\s+(.*)$")


def parse_markdown(instruction: str, doc_type: str = "") -> dict:
    """Разбирает готовую Markdown-инструкцию в структуру блоков (см. модульный docstring)."""
    title = "Инструкция"
    blocks: list[dict] = []
    current_group: dict | None = None

    def flush_group():
        nonlocal current_group
        if current_group is not None:
            blocks.append(current_group)
            current_group = None

    title_set = False
    for raw in instruction.splitlines():
        line = raw.rstrip()

        if not line.strip():
            flush_group()
            continue

        # ## Заголовок
        if line.startswith("## "):
            heading = line[3:].strip()
            flush_group()
            if not title_set:
                title = heading
                title_set = True
            else:
                blocks.append({"type": "heading", "text": heading})
            continue

        # **Метка:** значение
        m = _FIELD_RE.match(line)
        if m:
            flush_group()
            label, value = m.group(1).strip(), m.group(2).strip()
            if value:
                blocks.append({"type": "field", "label": label, "value": value})
            else:
                # Метка-заголовок для следующего списка
                current_group = {"type": "group", "label": label, "ordered": False, "items": []}
            continue

        # - маркер
        if line.startswith("- ") or line.startswith("• "):
            item = line[2:].strip()
            if current_group is None:
                current_group = {"type": "group", "label": None, "ordered": False, "items": []}
            current_group["items"].append(item)
            continue

        # N. нумерованный
        nm = _NUM_RE.match(line)
        if nm:
            item = nm.group(2).strip()
            if current_group is None:
                current_group = {"type": "group", "label": None, "ordered": True, "items": []}
            current_group["ordered"] = True
            current_group["items"].append(item)
            continue

        # --- разделитель
        if line.strip() in ("---", "***", "___"):
            flush_group()
            blocks.append({"type": "divider"})
            continue

        # обычный абзац
        flush_group()
        blocks.append({"type": "para", "text": line.strip()})

    flush_group()
    return {"title": title, "doc_type": doc_type, "blocks": blocks}


# ── Рендер ──────────────────────────────────────────────────────────────────

_env = Environment(autoescape=False)
_env.filters["md"] = inline_md


def generate_html(instruction: str, style_key: str, output_path: str, doc_type: str = "") -> str:
    """Рендерит инструкцию в HTML выбранного стиля и сохраняет в output_path."""
    style = HTML_STYLES.get(style_key) or next(iter(HTML_STYLES.values()))
    ctx = parse_markdown(instruction, doc_type)
    ctx["logo_b64"] = _logo_b64()
    template = _env.from_string(style["template"])
    html = template.render(**ctx)
    Path(output_path).write_text(html, encoding="utf-8")
    return output_path


# Карта {человекочитаемая метка: ключ} — для UI
HTML_STYLE_CHOICES = {meta["label"]: key for key, meta in HTML_STYLES.items()}
