"""
PDF-экспорт инструкций — три стиля с декоративными ветками и умной типографикой.
"""
import re
import math
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    HRFlowable, Table, TableStyle,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Шрифты ────────────────────────────────────────────────────────────────────

_WF = "C:/Windows/Fonts"

def _reg(name, fname):
    try:
        pdfmetrics.registerFont(TTFont(name, f"{_WF}/{fname}"))
    except Exception:
        pass

_reg("SansR",  "arial.ttf");   _reg("SansB",  "arialbd.ttf")
_reg("SansI",  "ariali.ttf");  _reg("SansBI", "arialbi.ttf")
_reg("SerifR", "times.ttf");   _reg("SerifB", "timesbd.ttf")
_reg("SerifI", "timesi.ttf");  _reg("SerifBI","timesbi.ttf")
_reg("CalR",   "calibri.ttf"); _reg("CalB",   "calibrib.ttf")
_reg("CalI",   "calibrii.ttf")

# ── Палитры стилей ────────────────────────────────────────────────────────────

STYLES = {
    "lavender": {
        "label":         "Лавандовый",
        # фон
        "page_bg":       colors.HexColor("#f2f3f9"),
        "page_bg2":      colors.HexColor("#e8eaf4"),   # нижняя полоса
        # ветки
        "branch_color":  colors.HexColor("#c0c8e0"),
        "branch_dot":    colors.HexColor("#a8b4d0"),
        # шапка
        "header_bg":     colors.HexColor("#5a6fa8"),
        "header_bg2":    colors.HexColor("#4a5c90"),
        "header_text":   colors.white,
        "header_sub":    colors.HexColor("#c8d0f0"),
        # акцент
        "accent":        colors.HexColor("#5060a0"),
        "accent2":       colors.HexColor("#8090c8"),
        # заголовок секции
        "title_bg":      colors.HexColor("#dde2f5"),
        "title_border":  colors.HexColor("#7888c0"),
        "title_color":   colors.HexColor("#2c3360"),
        # поля
        "field_bg":      colors.HexColor("#eaecf8"),
        "field_border":  colors.HexColor("#b8c0dc"),
        "field_label":   colors.HexColor("#4a5890"),
        "field_value":   colors.HexColor("#22284a"),
        # текст
        "body_color":    colors.HexColor("#30354a"),
        "italic_color":  colors.HexColor("#505898"),
        "bullet_color":  colors.HexColor("#6070b0"),
        "hr_color":      colors.HexColor("#b0b8d8"),
        # приоритет
        "p_high":   colors.HexColor("#c0392b"), "p_high_bg":   colors.HexColor("#fde8e8"),
        "p_med":    colors.HexColor("#d35400"), "p_med_bg":    colors.HexColor("#fef0e0"),
        "p_low":    colors.HexColor("#27ae60"), "p_low_bg":    colors.HexColor("#e8f8ee"),
        # шрифты
        "font_r": "SansR", "font_b": "SansB",
        "font_i": "SansI", "font_bi": "SansBI", "font_h": "SansB",
        "base_size": 16,
    },
    "pink": {
        "label":         "Розовый",
        "page_bg":       colors.HexColor("#fef6f9"),
        "page_bg2":      colors.HexColor("#fce8f0"),
        "branch_color":  colors.HexColor("#f0c0d0"),
        "branch_dot":    colors.HexColor("#e8a0b8"),
        "header_bg":     colors.HexColor("#d63670"),
        "header_bg2":    colors.HexColor("#b8205a"),
        "header_text":   colors.white,
        "header_sub":    colors.HexColor("#ffc8dc"),
        "accent":        colors.HexColor("#c2185b"),
        "accent2":       colors.HexColor("#e8609a"),
        "title_bg":      colors.HexColor("#fde0ec"),
        "title_border":  colors.HexColor("#e880aa"),
        "title_color":   colors.HexColor("#7b0a35"),
        "field_bg":      colors.HexColor("#fff0f5"),
        "field_border":  colors.HexColor("#f8c0d4"),
        "field_label":   colors.HexColor("#a01048"),
        "field_value":   colors.HexColor("#3a1020"),
        "body_color":    colors.HexColor("#3a1828"),
        "italic_color":  colors.HexColor("#b03060"),
        "bullet_color":  colors.HexColor("#d63670"),
        "hr_color":      colors.HexColor("#f0a0c0"),
        "p_high":   colors.HexColor("#b71c1c"), "p_high_bg":   colors.HexColor("#fde8e8"),
        "p_med":    colors.HexColor("#bf360c"), "p_med_bg":    colors.HexColor("#fbe9e7"),
        "p_low":    colors.HexColor("#1b5e20"), "p_low_bg":    colors.HexColor("#e8f5e9"),
        "font_r": "CalR", "font_b": "CalB",
        "font_i": "CalI", "font_bi": "CalB", "font_h": "CalB",
        "base_size": 16,
    },
    "editorial": {
        "label":         "Редакционный",
        "page_bg":       colors.HexColor("#f8f4ec"),
        "page_bg2":      colors.HexColor("#ede6d6"),
        "branch_color":  colors.HexColor("#d8c8a0"),
        "branch_dot":    colors.HexColor("#c0a870"),
        "header_bg":     colors.HexColor("#282420"),
        "header_bg2":    colors.HexColor("#1c1a16"),
        "header_text":   colors.HexColor("#f5f0e8"),
        "header_sub":    colors.HexColor("#9a8f6e"),
        "accent":        colors.HexColor("#b8872a"),
        "accent2":       colors.HexColor("#d4a84b"),
        "title_bg":      colors.HexColor("#282420"),
        "title_border":  colors.HexColor("#b8872a"),
        "title_color":   colors.white,
        "field_bg":      colors.HexColor("#ede8dc"),
        "field_border":  colors.HexColor("#c8b488"),
        "field_label":   colors.HexColor("#b8872a"),
        "field_value":   colors.HexColor("#1e1c18"),
        "body_color":    colors.HexColor("#282420"),
        "italic_color":  colors.HexColor("#8a6820"),
        "bullet_color":  colors.HexColor("#b8872a"),
        "hr_color":      colors.HexColor("#c8b088"),
        "p_high":   colors.HexColor("#8b0000"), "p_high_bg":   colors.HexColor("#fdf0e8"),
        "p_med":    colors.HexColor("#8b4500"), "p_med_bg":    colors.HexColor("#fdf5e8"),
        "p_low":    colors.HexColor("#1a4a20"), "p_low_bg":    colors.HexColor("#eef5ec"),
        "font_r": "SerifR", "font_b": "SerifB",
        "font_i": "SerifI", "font_bi": "SerifBI", "font_h": "SerifB",
        "base_size": 16,
    },
    "minimal": {
        "label":         "Минимальный (подложка)",
        "page_bg":       colors.white,
        "page_bg2":      colors.white,
        "branch_color":  colors.white,
        "branch_dot":    colors.white,
        "header_bg":     colors.white,
        "header_bg2":    colors.white,
        "header_text":   colors.HexColor("#2d2a22"),
        "header_sub":    colors.HexColor("#9a8f6e"),
        "accent":        colors.white,
        "accent2":       colors.white,
        "title_bg":      colors.white,
        "title_border":  colors.HexColor("#d4a64f"),
        "title_color":   colors.HexColor("#2d2a22"),
        "field_bg":      colors.HexColor("#faf8f4"),
        "field_border":  colors.HexColor("#e0d5c8"),
        "field_label":   colors.HexColor("#8a6820"),
        "field_value":   colors.HexColor("#3d3a34"),
        "body_color":    colors.HexColor("#2d2a22"),
        "italic_color":  colors.HexColor("#8a6820"),
        "bullet_color":  colors.HexColor("#b8872a"),
        "hr_color":      colors.HexColor("#d4a64f"),
        "p_high":   colors.HexColor("#8b0000"), "p_high_bg":   colors.HexColor("#fff5f5"),
        "p_med":    colors.HexColor("#8b4500"), "p_med_bg":    colors.HexColor("#fffaf0"),
        "p_low":    colors.HexColor("#1a4a20"), "p_low_bg":    colors.HexColor("#f5faf5"),
        "font_r": "SerifR", "font_b": "SerifB",
        "font_i": "SerifI", "font_bi": "SerifBI", "font_h": "SerifB",
        "base_size": 16,
        "use_background_image": True,
    },
}

STYLE_CHOICES = {v["label"]: k for k, v in STYLES.items()}

# ── Декоративные ветки ────────────────────────────────────────────────────────

def _branch(c, x, y, angle_deg, length, lw, depth, color, dot_color):
    """Рисует одну ветку с рекурсивными подветками через безье-кривые."""
    if depth <= 0 or length < 1.5:
        return
    a = math.radians(angle_deg)
    ex = x + length * math.cos(a)
    ey = y + length * math.sin(a)
    # Плавный изгиб через контрольные точки
    wobble = math.sin(x * 0.08 + y * 0.06) * length * 0.18
    cx1 = x + length * 0.35 * math.cos(math.radians(angle_deg + 12))
    cy1 = y + length * 0.35 * math.sin(math.radians(angle_deg + 12))
    cx2 = ex + wobble * math.cos(math.radians(angle_deg + 90))
    cy2 = ey + wobble * math.sin(math.radians(angle_deg + 90))
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    p = c.beginPath()
    p.moveTo(x, y)
    p.curveTo(cx1, cy1, cx2, cy2, ex, ey)
    c.drawPath(p, stroke=1, fill=0)
    # Бутон/листик на конце самых тонких веток
    if depth == 1:
        c.setFillColor(dot_color)
        c.circle(ex, ey, lw * 0.9, fill=1, stroke=0)
    # Подветки
    spread = 26 + depth * 2
    _branch(c, ex, ey, angle_deg + spread, length * 0.60, lw * 0.68, depth - 1, color, dot_color)
    _branch(c, ex, ey, angle_deg - spread * 0.8, length * 0.65, lw * 0.70, depth - 1, color, dot_color)
    if depth >= 3:
        mid_x = x + length * 0.55 * math.cos(a)
        mid_y = y + length * 0.55 * math.sin(a)
        _branch(c, mid_x, mid_y, angle_deg + 50, length * 0.38, lw * 0.50, depth - 2, color, dot_color)


def _draw_branches(c, W, H, st, style_key):
    """Рисует декоративные ветки по углам страницы."""
    col = st["branch_color"]
    dot = st["branch_dot"]
    c.saveState()

    if style_key == "lavender":
        # Снизу-слева — вверх-вправо
        _branch(c, 2*mm,  18*mm,  72, 28*mm, 1.1, 4, col, dot)
        _branch(c, 0,     8*mm,   82, 20*mm, 0.8, 3, col, dot)
        # Сверху-справа — вниз-влево
        c.saveState()
        c.translate(W, H)
        c.rotate(180)
        _branch(c, 2*mm,  18*mm,  72, 28*mm, 1.1, 4, col, dot)
        _branch(c, 0,     8*mm,   82, 20*mm, 0.8, 3, col, dot)
        c.restoreState()

    elif style_key == "pink":
        # Снизу-справа
        c.saveState()
        c.translate(W, 0)
        c.scale(-1, 1)
        _branch(c, 2*mm,  20*mm,  75, 32*mm, 1.1, 4, col, dot)
        _branch(c, 5*mm,  5*mm,   88, 22*mm, 0.8, 3, col, dot)
        c.restoreState()
        # Сверху-слева
        c.saveState()
        c.translate(0, H)
        c.scale(1, -1)
        _branch(c, 2*mm,  16*mm,  68, 26*mm, 0.9, 3, col, dot)
        c.restoreState()

    elif style_key == "editorial":
        # Оба нижних угла
        _branch(c, 2*mm,  15*mm,  70, 30*mm, 1.2, 4, col, dot)
        _branch(c, 0,     5*mm,   85, 18*mm, 0.7, 3, col, dot)
        c.saveState()
        c.translate(W, 0)
        c.scale(-1, 1)
        _branch(c, 2*mm,  15*mm,  70, 30*mm, 1.2, 4, col, dot)
        _branch(c, 0,     5*mm,   85, 18*mm, 0.7, 3, col, dot)
        c.restoreState()

    c.restoreState()

# ── Бейдж SUMMARA (правый нижний угол) ───────────────────────────────────────

_LOGO_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logo", "1232321.jpg")

def _draw_summara_badge(c, W, st, style_key):
    """Полупрозрачная подпись «Создано в SUMMARA» с логотипом, правый нижний угол."""
    from reportlab.lib.colors import Color

    c.saveState()

    # Позиция: правый нижний угол
    # Для minimal: чуть выше низа; для остальных: над колонтитулом
    if style_key == "minimal":
        y_base = 8 * mm
        text_color = Color(0.35, 0.25, 0.1, alpha=0.45)
    else:
        y_base = 11 * mm
        text_color = Color(1, 1, 1, alpha=0.55)

    logo_size = 7 * mm
    text = "Создано в SUMMARA"
    font_name = st.get("font_r", "Helvetica")
    font_size = 7

    # Ширина текста для выравнивания
    c.setFont(font_name, font_size)
    text_w = c.stringWidth(text, font_name, font_size)
    gap = 2 * mm
    total_w = logo_size + gap + text_w
    x_start = W - 14 * mm - total_w

    # Логотип
    if os.path.exists(_LOGO_PATH):
        try:
            c.setFillColor(Color(1, 1, 1, alpha=0.0))
            c.drawImage(_LOGO_PATH, x_start, y_base,
                        width=logo_size, height=logo_size,
                        mask="auto", preserveAspectRatio=True)
        except Exception:
            pass

    # Текст
    c.setFillColor(text_color)
    c.setFont(font_name, font_size)
    c.drawString(x_start + logo_size + gap, y_base + logo_size * 0.25, text)

    c.restoreState()


# ── Canvas с фоном ────────────────────────────────────────────────────────────

class _BgCanvas:
    def __init__(self, st: dict, style_key: str):
        self.st = st
        self.style_key = style_key

    def __call__(self, c, doc):
        st = self.st
        c.saveState()
        W, H = A4

        # Для минимального стиля — только подложка, без белого фона
        if self.style_key == "minimal":
            bg_img = "pdl/18f21238d58a2bf59c665d66374f2199.jpg"
            if os.path.exists(bg_img):
                try:
                    from reportlab.platypus import Image as RLImage
                    img = RLImage(bg_img, width=W, height=H)
                    img.drawOn(c, 0, 0)
                except Exception:
                    pass
        else:
            # 1. Основной фон для других стилей
            c.setFillColor(st["page_bg"])
            c.rect(0, 0, W, H, fill=1, stroke=0)

            # 2. Мягкий градиентный переход снизу (светло-серый оверлей)
            c.setFillColor(st["page_bg2"])
            c.rect(0, 0, W, 60 * mm, fill=1, stroke=0)

            # 3. Декоративные ветки
            _draw_branches(c, W, H, st, self.style_key)

        # Для минимального стиля не рисуем шапку и колонтитулы — только подложка
        if self.style_key != "minimal":
            # 4. Шапка с двухтоновым фоном
            header_h = 44 * mm
            c.setFillColor(st["header_bg2"])
            c.rect(0, H - header_h, W, header_h, fill=1, stroke=0)
            c.setFillColor(st["header_bg"])
            c.rect(0, H - header_h, W, header_h - 6 * mm, fill=1, stroke=0)

            # 5. Акцентная полоска под шапкой
            c.setFillColor(st["accent2"])
            c.rect(0, H - header_h - 1.5, W, 4, fill=1, stroke=0)
            c.setFillColor(st["accent"])
            c.rect(0, H - header_h - 1.5, W * 0.6, 4, fill=1, stroke=0)

            # 6. Нижний колонтитул
            c.setFillColor(st["header_bg"])
            c.rect(0, 0, W, 9 * mm, fill=1, stroke=0)
            c.setFillColor(st["accent"])
            c.rect(0, 9 * mm, W, 1, fill=1, stroke=0)

            # 7. Номер страницы
            c.setFillColor(st["header_text"])
            c.setFont(st["font_r"], 8)
            c.drawCentredString(W / 2, 3 * mm, f"— {doc.page} —")

        # 8. Подпись SUMMARA с логотипом — правый нижний угол, полупрозрачная
        _draw_summara_badge(c, W, st, self.style_key)

        c.restoreState()


class _FirstPageCanvas(_BgCanvas):
    def __init__(self, st: dict, style_key: str, title: str):
        super().__init__(st, style_key)
        self.title = title

    def __call__(self, c, doc):
        super().__call__(c, doc)
        st = self.st
        W, H = A4
        header_h = 44 * mm

        c.saveState()

        # Для минимального стиля не рисуем ничего — только подложка
        if self.style_key != "minimal":
            # Декоративная линия слева в шапке
            c.setStrokeColor(st["accent2"])
            c.setLineWidth(3)
            c.line(14 * mm, H - header_h + 8 * mm, 14 * mm, H - 8 * mm)

            # Фоновый блок для заголовка (чёрный прямоугольник для контраста)
            c.setFillColor(st["title_bg"])
            title_lines = _wrap_title(self.title, 50)
            box_h = 8 * mm + (len(title_lines) * 8.5 * mm)
            c.rect(18 * mm, H - 14 * mm - box_h, W - 36 * mm, box_h,
                   fill=1, stroke=0)

            # Заголовок — КРУПНЫЙ И ЖИРНЫЙ (28pt)
            c.setFillColor(st["header_text"])
            c.setFont(st["font_b"], 28)
            title_lines = _wrap_title(self.title, 45)
            y = H - 13 * mm - (len(title_lines) - 1) * 8.5 * mm
            for line in title_lines:
                c.drawString(20 * mm, y, line)
                y -= 8.5 * mm

            # Подпись
            # Логотип в шапке
            logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logo", "1232321.jpg")
            if os.path.exists(logo_path):
                try:
                    logo_size = 14 * mm
                    c.drawImage(logo_path, W - 20 * mm - logo_size,
                                H - header_h + (header_h - logo_size) / 2,
                                width=logo_size, height=logo_size,
                                mask="auto", preserveAspectRatio=True)
                except Exception:
                    pass

            c.setFillColor(st["header_sub"])
            c.setFont(st["font_i"], 8.5)
            c.drawString(20 * mm, H - header_h + 5 * mm, "Сгенерировано в SUMMARA")

        c.restoreState()


def _wrap_title(text: str, max_chars: int) -> list[str]:
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [text]

# ── Умное форматирование текста ───────────────────────────────────────────────

# Слова которые выделяем жирным по смыслу
_BOLD_WORDS = {
    "важно", "срочно", "обязательно", "критично", "внимание",
    "необходимо", "нельзя", "запрещено", "требуется", "должен",
    "должна", "обязан", "обязана", "ключевой", "главное",
}
# Слова → курсив (даты, состояния, технические термины)
_ITALIC_PATTERNS = [
    r'\b(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})\b',   # даты: 12.05.2025
    r'\b(\d{4}-\d{2}-\d{2})\b',                    # ISO даты
    r'\b(до конца \w+)\b',                          # "до конца недели/месяца"
    r'\b(v\d+\.\d+[\.\d]*)\b',                     # версии: v1.2.3
]


def _hex(color) -> str:
    return "#{:02x}{:02x}{:02x}".format(
        int(color.red * 255), int(color.green * 255), int(color.blue * 255)
    )


def _semantic_inline(text: str, st: dict) -> str:
    """
    Применяет форматирование:
    - **жирный** → жирный + цвет метки
    - *курсив* → курсив
    - Даты → курсив автоматически
    - Важные слова → жирный автоматически
    - high/critical/medium/low → цветные бейджи
    """
    # Сначала защищаем уже размеченные куски
    text = re.sub(
        r'\*\*(.+?)\*\*',
        lambda m: f'<font name="{st["font_b"]}" color="{_hex(st["field_label"])}">'
                  f'{m.group(1)}</font>',
        text,
    )
    text = re.sub(
        r'\*(.+?)\*',
        lambda m: f'<font name="{st["font_i"]}" color="{_hex(st["italic_color"])}">'
                  f'{m.group(1)}</font>',
        text,
    )

    # Автоматические даты → курсив
    for pat in _ITALIC_PATTERNS:
        text = re.sub(
            pat,
            lambda m: f'<font name="{st["font_i"]}" color="{_hex(st["italic_color"])}">'
                      f'{m.group(1)}</font>',
            text, flags=re.IGNORECASE,
        )

    # Приоритет — цветные теги
    def _priority_badge(m):
        word = m.group(0).lower()
        if word in ("high", "critical"):
            c, bg = _hex(st["p_high"]), _hex(st["p_high_bg"])
        elif word in ("medium",):
            c, bg = _hex(st["p_med"]), _hex(st["p_med_bg"])
        else:
            c, bg = _hex(st["p_low"]), _hex(st["p_low_bg"])
        return f'<font name="{st["font_b"]}" color="{c}"> {m.group(0).upper()} </font>'

    text = re.sub(r'\b(high|critical|medium|low)\b', _priority_badge, text, flags=re.IGNORECASE)

    # Важные слова → жирный
    def _bold_word(m):
        return f'<font name="{st["font_b"]}" color="{_hex(st["field_label"])}">{m.group(0)}</font>'

    for w in _BOLD_WORDS:
        text = re.sub(rf'\b({w})\b', _bold_word, text, flags=re.IGNORECASE)

    return text


def _format_field_value(value: str, label_lower: str, st: dict) -> str:
    """Умное форматирование значения поля в зависимости от типа."""
    if not value or value == "—":
        return f'<font name="{st["font_i"]}" color="{_hex(st["hr_color"])}">не указано</font>'

    v = _semantic_inline(value, st)

    # Имена людей (исполнитель, участники) → жирный курсив
    if any(k in label_lower for k in ("исполнитель", "assignee", "автор", "ответственный")):
        return f'<font name="{st["font_bi"]}" color="{_hex(st["field_value"])}">{value}</font>'

    # Даты/сроки → курсив
    if any(k in label_lower for k in ("срок", "дата", "deadline", "date")):
        return f'<font name="{st["font_i"]}" color="{_hex(st["italic_color"])}">{value}</font>'

    return v

# ── Стили параграфов ──────────────────────────────────────────────────────────

def _make_ps(st: dict, style_key: str = None) -> dict:
    bs = st["base_size"]   # 16pt

    # Для минимального стиля — заголовок 21pt, по центру, жирный, с цветом
    if style_key == "minimal":
        h2_style = ParagraphStyle("h2",
            fontName=st["font_b"], fontSize=21, leading=21 * 1.4,
            textColor=st["field_label"], spaceAfter=6, spaceBefore=4,
            alignment=TA_CENTER,
        )
    else:
        # Для других стилей — заголовок по умолчанию
        h2_style = ParagraphStyle("h2",
            fontName=st["font_b"], fontSize=bs + 4, leading=(bs + 4) * 1.4,
            textColor=st["title_color"], spaceAfter=3, spaceBefore=4,
        )

    return {
        # Заголовок секции
        "h2": h2_style,
        # Название поля — жирное, чуть меньше
        "fl": ParagraphStyle("fl",
            fontName=st["font_b"], fontSize=bs - 1, leading=bs * 1.5,
            textColor=st["field_label"], spaceAfter=0,
        ),
        # Значение поля
        "fv": ParagraphStyle("fv",
            fontName=st["font_r"], fontSize=bs, leading=bs * 1.5,
            textColor=st["field_value"], spaceAfter=0,
        ),
        # Основной текст абзаца
        "body": ParagraphStyle("body",
            fontName=st["font_r"], fontSize=bs, leading=bs * 1.6,
            textColor=st["body_color"], spaceAfter=6,
            alignment=TA_JUSTIFY, firstLineIndent=6,
        ),
        # Маркированный список
        "bullet": ParagraphStyle("bullet",
            fontName=st["font_r"], fontSize=bs, leading=bs * 1.5,
            textColor=st["body_color"], leftIndent=20, spaceAfter=4,
        ),
        # Нумерованный список
        "num": ParagraphStyle("num",
            fontName=st["font_r"], fontSize=bs, leading=bs * 1.5,
            textColor=st["body_color"], leftIndent=24, spaceAfter=4,
        ),
    }

# ── Markdown → Flowables ──────────────────────────────────────────────────────

def _md_to_flowables(text: str, st: dict, style_key: str = None) -> list:
    ps = _make_ps(st, style_key)
    out = []

    for raw in text.split("\n"):
        raw = raw.rstrip()

        if not raw:
            out.append(Spacer(1, 2.5 * mm))
            continue

        # ## Заголовок секции — жирный, крупный
        if raw.startswith("## "):
            title_text = raw[3:]
            # Явно указываем цвет, размер, шрифт и полужирное начертание в XML
            title_color_hex = _hex(st["title_color"]) if not st.get("use_background_image") else _hex(st["field_label"])
            title_size = ps["h2"].fontSize
            title_p = Paragraph(
                f'<b><font name="{st["font_b"]}" size="{title_size}" color="{title_color_hex}">{title_text}</font></b>',
                ps["h2"],
            )
            # Для минимального стиля — просто текст без фона
            if st.get("use_background_image"):
                out.append(title_p)
                out.append(Spacer(1, 4 * mm))
            else:
                # Для других стилей — стилизованный блок с фоном
                box = Table([[title_p]], colWidths=[170 * mm],
                    style=TableStyle([
                        ("BACKGROUND",   (0,0),(-1,-1), st["title_bg"]),
                        ("LEFTPADDING",  (0,0),(-1,-1), 12),
                        ("RIGHTPADDING", (0,0),(-1,-1), 12),
                        ("TOPPADDING",   (0,0),(-1,-1), 9),
                        ("BOTTOMPADDING",(0,0),(-1,-1), 9),
                        ("LINEBELOW",    (0,0),(-1,-1), 3, st["title_border"]),
                        ("LINEBEFORE",   (0,0),(-1,-1), 5, st["accent"]),
                        ("ROUNDEDCORNERS", [3]),
                    ]))
                out.append(box)
                out.append(Spacer(1, 4 * mm))
            continue

        # **Метка:** Значение — карточка поля (название метки жирное)
        m = re.match(r'^\*\*(.+?):\*\*\s*(.*)', raw)
        if m:
            label_raw = m.group(1)
            value_raw = m.group(2).strip()
            label_lower = label_raw.lower()

            # Жирное название поля
            label_p = Paragraph(
                f'<font name="{st["font_b"]}">{label_raw}:</font>',
                ps["fl"],
            )
            value_str = _format_field_value(value_raw, label_lower, st)
            value_p = Paragraph(value_str, ps["fv"])

            row = Table([[label_p, value_p]],
                colWidths=[58 * mm, 108 * mm],
                style=TableStyle([
                    ("BACKGROUND",   (0,0),(-1,-1), st["field_bg"]),
                    ("LEFTPADDING",  (0,0),(-1,-1), 10),
                    ("RIGHTPADDING", (0,0),(-1,-1), 10),
                    ("TOPPADDING",   (0,0),(-1,-1), 7),
                    ("BOTTOMPADDING",(0,0),(-1,-1), 7),
                    ("LINEBELOW",    (0,0),(-1,-1), 0.5, st["field_border"]),
                    ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
                ]))
            out.append(row)
            continue

        # - маркированный список
        if raw.startswith("- ") or raw.startswith("• "):
            item = _semantic_inline(raw[2:], st)
            bc = _hex(st["bullet_color"])
            out.append(Paragraph(
                f'<font name="{st["font_b"]}" color="{bc}">&#8226;</font>  {item}',
                ps["bullet"],
            ))
            continue

        # 1. нумерованный список
        nm = re.match(r'^(\d+)\.\s+(.*)', raw)
        if nm:
            num = nm.group(1)
            item = _semantic_inline(nm.group(2), st)
            nc = _hex(st["bullet_color"])
            out.append(Paragraph(
                f'<font name="{st["font_b"]}" color="{nc}">{num}.</font>  {item}',
                ps["num"],
            ))
            continue

        # --- горизонтальная черта
        if raw.strip() in ("---", "***", "___"):
            out.append(HRFlowable(
                width="100%", thickness=0.8, color=st["hr_color"],
                spaceBefore=3, spaceAfter=3,
            ))
            continue

        # Обычный абзац с умным форматированием
        out.append(Paragraph(_semantic_inline(raw, st), ps["body"]))

    return out

# ── Генерация PDF ─────────────────────────────────────────────────────────────

def generate_pdf(instruction: str, style_key: str, output_path: str) -> str:
    st = STYLES.get(style_key, STYLES["lavender"])

    title = "Инструкция"
    for line in instruction.splitlines():
        if line.startswith("## "):
            title = line[3:].strip()
            break

    # Разные поля для разных стилей
    if style_key == "minimal":
        # Поля для минимального стиля: 2см сверху, 6см снизу, 2см слева и справа
        top_margin = 20 * mm
        bottom_margin = 60 * mm
        left_margin = 20 * mm
        right_margin = 20 * mm
    else:
        # Стандартные поля для других стилей
        top_margin = 52 * mm
        bottom_margin = 18 * mm
        left_margin = 20 * mm
        right_margin = 20 * mm

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin,
    )

    story = _md_to_flowables(instruction, st, style_key)
    first_bg = _FirstPageCanvas(st, style_key, title)
    later_bg = _BgCanvas(st, style_key)
    doc.build(story, onFirstPage=first_bg, onLaterPages=later_bg)
    return output_path
