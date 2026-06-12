import json
from datetime import datetime
from pathlib import Path
import gradio as gr
from agents.transcription import transcribe
from agents.pdf_export import generate_pdf, STYLE_CHOICES
from agents.html_export import generate_html, HTML_STYLES
from pipeline import run
from config import BASE_DIR
import settings as user_settings

EXPORTS_DIR = BASE_DIR / "exports"
EXPORTS_DIR.mkdir(exist_ok=True)

TEMPLATE_LABELS = {
    "task": "Задача",
    "meeting": "Встреча",
    "bug_report": "Баг-репорт",
}


def handle_audio(audio_path: str | None) -> tuple[str, str]:
    if audio_path is None:
        return "", "Загрузите файл или запишите голос."
    try:
        text = transcribe(audio_path)
        return text, f"Транскрипция готова — {len(text)} символов"
    except Exception as e:
        return "", f"Ошибка транскрипции: {e}"


def handle_pipeline(text: str, enrich: bool) -> tuple:
    text = text.strip()
    if not text:
        return "", "", "", "Введите или транскрибируйте текст.", "", "", ""

    try:
        result = run(text=text, enrich=bool(enrich))
        v = result["validation"]

        template_name = result["template"]
        template_lbl = TEMPLATE_LABELS.get(template_name, template_name)

        if v["ok"]:
            val_status = f"Оценка {v['score']}/10"
        else:
            val_status = f"Оценка {v['score']}/10 — проблем: {len(v['issues'])}"

        parts = []
        if v["issues"]:
            parts.append("**Проблемы:**\n" + "\n".join(f"- {i}" for i in v["issues"]))
        if v["suggestions"]:
            parts.append("**Рекомендации:**\n" + "\n".join(f"- {s}" for s in v["suggestions"]))
        val_details = "\n\n".join(parts) if parts else "Всё в порядке."

        json_str = json.dumps(result["data"], ensure_ascii=False, indent=2)

        # confirm_status сбрасываем — новая инструкция требует нового подтверждения
        # последнее значение — doc_type (для подбора HTML-лэндингов)
        return result["rendered"], json_str, template_lbl, val_status, val_details, "", template_name

    except Exception as e:
        return "", "", "", f"Ошибка: {e}", "", "", ""


FMT_HTML = "Веб-страница (HTML)"
FMT_TXT = "Текстовый файл (.txt)"
FMT_JSON = "Данные (JSON)"
FMT_PDF = "Документ (PDF)"


def handle_export(instruction: str, json_data: str, fmt: str, pdf_style: str) -> str | None:
    """Сохраняет инструкцию в одиночный файл (TXT/JSON/PDF) и возвращает путь."""
    if not instruction.strip():
        return None

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    if fmt == FMT_TXT:
        filepath = EXPORTS_DIR / f"instruction_{ts}.txt"
        filepath.write_text(instruction, encoding="utf-8")
    elif fmt == FMT_JSON:
        filepath = EXPORTS_DIR / f"instruction_{ts}.json"
        filepath.write_text(json_data or "{}", encoding="utf-8")
    elif fmt == FMT_PDF:
        filepath = EXPORTS_DIR / f"instruction_{ts}.pdf"
        style_key = STYLE_CHOICES.get(pdf_style, "lavender")
        generate_pdf(instruction, style_key, str(filepath))
    else:
        return None

    return str(filepath)


def _iframe_srcdoc(html: str) -> str:
    """Экранирует HTML для безопасной вставки в атрибут srcdoc."""
    return (
        html.replace("&", "&amp;")
            .replace('"', "&quot;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )


def _build_previews(items: list[tuple[str, str, str]]) -> str:
    """items: [(label, style_key, html), ...] → HTML с превью в iframe."""
    cards = []
    for label, _key, html in items:
        srcdoc = _iframe_srcdoc(html)
        cards.append(
            f'<div style="margin-bottom:18px;">'
            f'<div style="font-weight:600;color:#4f46e5;margin-bottom:6px;font-size:0.95rem;">'
            f'🎨 {label}</div>'
            f'<iframe srcdoc="{srcdoc}" '
            f'style="width:100%;height:620px;border:1px solid #ddd6fe;border-radius:10px;'
            f'background:#fff;"></iframe>'
            f'</div>'
        )
    return "<div>" + "".join(cards) + "</div>"


def handle_landing(instruction: str, doc_type: str):
    """Генерит ВСЕ доступные стили HTML-страниц, возвращает (файлы, превью, статус)."""
    if not instruction.strip():
        return None, "", "⚠️ Сначала сгенерируйте инструкцию."

    keys = list(HTML_STYLES.keys())
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    files: list[str] = []
    previews: list[tuple[str, str, str]] = []

    for key in keys:
        meta = HTML_STYLES.get(key, {})
        label = meta.get("label", key)
        filepath = EXPORTS_DIR / f"landing_{ts}_{key}.html"
        try:
            generate_html(instruction, key, str(filepath), doc_type=doc_type or "")
            html = filepath.read_text(encoding="utf-8")
            files.append(str(filepath))
            previews.append((label, key, html))
        except Exception as e:
            print(f"[Landing] Ошибка стиля {key}: {e}")

    if not files:
        return None, "", "❌ Не удалось создать лэндинги."

    status = (
        f"✅ Готово вариантов оформления: {len(files)} — "
        f"листайте превью ниже и выбирайте, файлы для скачивания выше."
    )
    return files, _build_previews(previews), status


def handle_export_dispatch(instruction: str, json_data: str, fmt: str, pdf_style: str, doc_type: str):
    """Единый обработчик кнопки экспорта. Возвращает (export_file, landing_files, landing_previews, landing_status)."""
    if fmt == FMT_HTML:
        files, previews, status = handle_landing(instruction, doc_type)
        return None, files, previews, status

    if fmt == FMT_PDF:
        if not pdf_style:
            return None, None, "", ""  # PDF создаётся при выборе стиля ниже
        path = handle_export(instruction, json_data, fmt, pdf_style)
        return path, None, "", ""

    # TXT / JSON
    path = handle_export(instruction, json_data, fmt, pdf_style)
    return path, None, "", ""


def confirm_instruction(text: str) -> str:
    if not text.strip():
        return "⚠️ Инструкция пустая — нечего подтверждать"
    return f"✅ Инструкция подтверждена ({len(text)} симв.) — переходите к экспорту"


def toggle_format(fmt: str):
    """Показывает/скрывает контролы под выбранный формат."""
    is_pdf = fmt == FMT_PDF
    is_html = fmt == FMT_HTML
    is_single = fmt in (FMT_TXT, FMT_JSON, FMT_PDF)
    return (
        gr.update(visible=is_pdf, value=None),     # pdf_style_selector
        gr.update(visible=is_pdf, value=""),       # pdf_status
        gr.update(visible=is_single),              # export_file (одиночный)
        gr.update(visible=is_html, value=None),    # landing_files
        gr.update(visible=is_html, value=""),      # landing_previews
        gr.update(visible=is_html, value=""),      # landing_status
    )


def auto_generate_pdf(instruction: str, json_data: str, fmt: str, pdf_style: str):
    """Генератор: показывает статус и ожидаемое время, потом возвращает файл."""
    import time

    if fmt != FMT_PDF:
        yield None, ""
        return
    if not pdf_style:
        yield None, "👆 Выберите стиль выше — PDF создастся автоматически"
        return
    if not instruction.strip():
        yield None, "⚠️ Сначала сгенерируйте инструкцию."
        return

    # Показываем статус до начала генерации
    yield None, f"⏳ Создаётся PDF «{pdf_style}»..."

    t0 = time.perf_counter()
    path = handle_export(instruction, json_data, fmt, pdf_style)
    elapsed = time.perf_counter() - t0

    if path:
        yield path, f"✅ «{pdf_style}» готов за {elapsed:.2f} сек — можно скачать"
    else:
        yield None, "❌ Ошибка при создании PDF"


def clear_all() -> tuple:
    # audio_input, text_box, instruction_box, json_box, template_label,
    # val_status_box, val_details_box, audio_status, confirm_status,
    # export_file, doc_type_state, landing_files, landing_previews, landing_status
    return (None, "", "", "", "", "", "", "", "", None, "", None, "", "")


# ── CSS ───────────────────────────────────────────────────────────────────────

CSS = """
/* Шапка */
.app-header {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    border-radius: 14px;
    padding: 16px 28px 16px;
    margin-bottom: 4px;
    display: flex !important;
    align-items: center !important;
    gap: 20px !important;
}
.app-header img.logo {
    width: 72px !important;
    height: 72px !important;
    border-radius: 16px !important;
    flex-shrink: 0 !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.25) !important;
}
.app-header-text { flex: 1 !important; }
.app-header h1 {
    color: #ffffff !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    margin: 0 0 4px !important;
    letter-spacing: 2px !important;
}
.app-header p {
    color: rgba(255,255,255,0.82) !important;
    font-size: 0.95rem !important;
    margin: 0 !important;
}

/* Панели ввода и результата */
.panel-input, .panel-result {
    background: #fafaff;
    border: 1px solid #e5e7ff;
    border-radius: 12px;
    padding: 18px 16px 12px !important;
}

/* Заголовки секций */
.section-title { margin-bottom: 6px !important; }
.section-title h3 {
    color: #4f46e5 !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    margin: 0 !important;
}

/* Кнопка «Сгенерировать» */
.btn-generate button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.35) !important;
    transition: box-shadow 0.2s, transform 0.15s !important;
    font-weight: 600 !important;
}
.btn-generate button:hover {
    box-shadow: 0 6px 20px rgba(99,102,241,0.5) !important;
    transform: translateY(-1px) !important;
}

/* Кнопка «Транскрибировать» */
.btn-transcribe button {
    border: 1.5px solid #6366f1 !important;
    color: #6366f1 !important;
    font-weight: 500 !important;
    transition: background 0.15s !important;
}
.btn-transcribe button:hover {
    background: #f0f0ff !important;
}

/* Секция экспорта */
.export-card {
    background: #f5f3ff;
    border: 1px solid #ddd6fe;
    border-radius: 10px;
    padding: 14px 16px 10px !important;
    margin-top: 4px;
}

/* Поле статуса */
.status-box textarea {
    font-size: 0.85rem !important;
    color: #6b7280 !important;
    background: #f9fafb !important;
}

/* Поле инструкции — редактируемое */
.instruction-box textarea {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88rem !important;
    line-height: 1.6 !important;
    border: 1.5px dashed #8090c8 !important;
    background: #fafbff !important;
    transition: border-color 0.2s !important;
}
.instruction-box textarea:focus {
    border-color: #5060a0 !important;
    background: #f5f6ff !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}

/* Кнопка подтверждения */
.btn-confirm button {
    border: 1.5px solid #22c55e !important;
    color: #16a34a !important;
    font-weight: 600 !important;
    background: #f0fdf4 !important;
    transition: all 0.15s !important;
}
.btn-confirm button:hover {
    background: #dcfce7 !important;
    border-color: #16a34a !important;
}

/* Статус подтверждения */
.confirm-status textarea {
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    border: none !important;
    background: transparent !important;
    padding: 2px 0 !important;
}

/* Выбор стиля PDF */
.pdf-style-radio {
    background: #eef0ff;
    border-radius: 8px;
    padding: 10px 12px !important;
    border: 1.5px dashed #a0a8e0;
}

/* Статус PDF */
.pdf-status textarea {
    background: transparent !important;
    border: none !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 4px 0 !important;
}
"""

# ── UI ────────────────────────────────────────────────────────────────────────

_LOGO_PATH = str(Path(__file__).parent / "logo" / "1232321.jpg")
import base64 as _b64
with open(_LOGO_PATH, "rb") as _f:
    _LOGO_B64 = _b64.b64encode(_f.read()).decode()

with gr.Blocks(title="SUMMARA") as demo:
    # Тип шаблона текущей инструкции (task/meeting/bug_report) — для подбора лэндингов
    doc_type_state = gr.State("")

    gr.HTML(f"""
        <div class="app-header">
            <img class="logo" src="data:image/jpeg;base64,{_LOGO_B64}" alt="SUMMARA logo">
            <div class="app-header-text">
                <h1>SUMMARA</h1>
                <p>Преобразователь голосовых и текстовых сообщений в структурированные инструкции</p>
            </div>
        </div>
    """)

    # ── Настройки: редактируемые промпты обработки готового текста ────────────
    _cfg0 = user_settings.load_settings()
    with gr.Accordion("⚙️ Настройки обработки текста", open=False):
        gr.Markdown(
            "Здесь можно изменить **вид итогового документа** и **промпты**, по которым "
            "обрабатывается готовый текст (когда включён режим «✨ Сделать текст живее»). "
            "Например, поменяйте «инструкция» на «регламент» или «пояснение». "
            "Изменения применяются при следующей генерации.",
        )
        set_kind = gr.Textbox(
            value=_cfg0["output_kind"],
            label=user_settings.FIELD_LABELS["output_kind"],
            info="Одним словом: инструкция / регламент / пояснение / памятка / чек-лист …",
            max_lines=1,
        )
        set_system = gr.Textbox(
            value=_cfg0["enrich_system"],
            label=user_settings.FIELD_LABELS["enrich_system"],
            lines=2,
        )
        set_rules = gr.Textbox(
            value=_cfg0["enrich_rules"],
            label=user_settings.FIELD_LABELS["enrich_rules"],
            lines=12,
        )
        with gr.Row():
            settings_save_btn = gr.Button("💾 Сохранить настройки", variant="primary", scale=2)
            settings_reset_btn = gr.Button("↩️ Сбросить к стандартным", variant="secondary", scale=1)
        settings_status = gr.Textbox(show_label=False, interactive=False, max_lines=1)

    with gr.Row():
        # ── Левая колонка: ввод ──────────────────────────────────────────────
        with gr.Column(scale=1, elem_classes="panel-input"):
            gr.Markdown("### Ввод", elem_classes="section-title")

            with gr.Tabs():
                with gr.Tab("🎙 Голос"):
                    audio_input = gr.Audio(
                        sources=["microphone", "upload"],
                        type="filepath",
                        label="Запись с микрофона или загрузка файла",
                    )
                    audio_btn = gr.Button(
                        "Транскрибировать",
                        variant="secondary",
                        elem_classes="btn-transcribe",
                    )

                with gr.Tab("✏️ Текст"):
                    gr.Markdown("Введите текст напрямую в поле **«Текст сообщения»** ниже.")

            text_box = gr.Textbox(
                lines=7,
                placeholder="Текст появится после транскрипции, или введите вручную...",
                label="Текст сообщения",
            )

            enrich_toggle = gr.Checkbox(
                value=False,
                label="✨ Сделать текст живее (примеры, пояснения, сноски, эмоции)",
            )

            with gr.Row():
                run_btn = gr.Button(
                    "⚡ Сгенерировать инструкцию",
                    variant="primary",
                    scale=3,
                    elem_classes="btn-generate",
                )
                clear_btn = gr.Button("Очистить", variant="stop", scale=1)

            audio_status = gr.Textbox(
                label="Статус обработки",
                interactive=False,
                max_lines=1,
                elem_classes="status-box",
            )

        # ── Правая колонка: результат ────────────────────────────────────────
        with gr.Column(scale=1, elem_classes="panel-result"):
            gr.Markdown("### Результат", elem_classes="section-title")

            with gr.Row():
                template_label = gr.Textbox(
                    label="Тип инструкции", interactive=False, scale=1, max_lines=1
                )
                val_status_box = gr.Textbox(
                    label="Оценка качества", interactive=False, scale=2, max_lines=1
                )

            instruction_box = gr.Textbox(
                lines=10,
                label="Готовая инструкция (можно редактировать)",
                interactive=True,
                elem_classes="instruction-box",
                placeholder="Инструкция появится здесь. Вы можете отредактировать её перед сохранением.",
            )

            with gr.Row():
                confirm_btn = gr.Button(
                    "✓ Подтвердить инструкцию",
                    variant="secondary",
                    scale=2,
                    elem_classes="btn-confirm",
                )
            confirm_status = gr.Textbox(
                show_label=False,
                interactive=False,
                max_lines=1,
                elem_classes="confirm-status",
                placeholder="",
            )

            with gr.Accordion("📋 Подробнее об оценке", open=False):
                val_details_box = gr.Markdown()

            with gr.Accordion("🗂 Технические данные (JSON)", open=False):
                json_box = gr.Code(language="json", label="")

            # ── Экспорт ──────────────────────────────────────────────────────
            with gr.Group(elem_classes="export-card"):
                gr.Markdown("### Сохранение результата", elem_classes="section-title")
                with gr.Row():
                    fmt_selector = gr.Radio(
                        choices=[FMT_HTML, FMT_TXT, FMT_JSON, FMT_PDF],
                        value=FMT_HTML,
                        label="Шаг 1 — В каком виде сохранить",
                        scale=2,
                    )
                    export_btn = gr.Button("⬇ Создать и скачать", variant="secondary", scale=1)

                pdf_style_selector = gr.Radio(
                    choices=list(STYLE_CHOICES.keys()),
                    value=None,
                    label="Шаг 2 — Выберите оформление PDF",
                    visible=False,
                    elem_classes="pdf-style-radio",
                )

                pdf_status = gr.Textbox(
                    show_label=False,
                    interactive=False,
                    max_lines=1,
                    visible=False,
                    elem_classes="pdf-status",
                )

                # Одиночный файл (TXT / JSON / PDF) — по умолчанию скрыт, т.к. дефолт = HTML
                export_file = gr.File(
                    label="Файл для скачивания", interactive=False, visible=False
                )

                # ── HTML-лэндинги: 3 подобранных варианта ──────────────────────
                landing_status = gr.Textbox(
                    show_label=False,
                    interactive=False,
                    max_lines=2,
                    elem_classes="pdf-status",
                )
                landing_files = gr.Files(
                    label="Готовые веб-страницы для скачивания (.html)", interactive=False
                )
                landing_previews = gr.HTML()

    # ── Обработчики ──────────────────────────────────────────────────────────
    audio_btn.click(
        handle_audio,
        inputs=audio_input,
        outputs=[text_box, audio_status],
    )

    audio_input.stop_recording(
        handle_audio,
        inputs=audio_input,
        outputs=[text_box, audio_status],
    )

    audio_input.upload(
        handle_audio,
        inputs=audio_input,
        outputs=[text_box, audio_status],
    )

    run_btn.click(
        handle_pipeline,
        inputs=[text_box, enrich_toggle],
        outputs=[instruction_box, json_box, template_label, val_status_box, val_details_box,
                 confirm_status, doc_type_state],
    )

    confirm_btn.click(
        confirm_instruction,
        inputs=instruction_box,
        outputs=confirm_status,
    )

    fmt_selector.change(
        toggle_format,
        inputs=fmt_selector,
        outputs=[pdf_style_selector, pdf_status, export_file,
                 landing_files, landing_previews, landing_status],
    )

    # Шаг 2 для PDF: выбрали стиль → запускается генерация
    pdf_style_selector.change(
        auto_generate_pdf,
        inputs=[instruction_box, json_box, fmt_selector, pdf_style_selector],
        outputs=[export_file, pdf_status],
    )

    # Кнопка экспорта: HTML-лэндинги (3 варианта) / TXT / JSON / PDF
    export_btn.click(
        handle_export_dispatch,
        inputs=[instruction_box, json_box, fmt_selector, pdf_style_selector, doc_type_state],
        outputs=[export_file, landing_files, landing_previews, landing_status],
    )

    clear_btn.click(
        clear_all,
        inputs=[],
        outputs=[audio_input, text_box, instruction_box, json_box,
                 template_label, val_status_box, val_details_box, audio_status,
                 confirm_status, export_file, doc_type_state,
                 landing_files, landing_previews, landing_status],
    )

    # ── Настройки ────────────────────────────────────────────────────────────
    settings_save_btn.click(
        user_settings.save_settings,
        inputs=[set_kind, set_system, set_rules],
        outputs=settings_status,
    )
    settings_reset_btn.click(
        user_settings.reset_settings,
        inputs=[],
        outputs=[set_kind, set_system, set_rules, settings_status],
    )


demo.queue()

if __name__ == "__main__":
    theme = gr.themes.Soft(
        primary_hue=gr.themes.colors.violet,
        secondary_hue=gr.themes.colors.indigo,
        neutral_hue=gr.themes.colors.slate,
        font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "sans-serif"],
        font_mono=[gr.themes.GoogleFont("JetBrains Mono"), "ui-monospace", "monospace"],
    ).set(
        button_primary_background_fill="linear-gradient(135deg, #6366f1, #8b5cf6)",
        button_primary_background_fill_hover="linear-gradient(135deg, #5253cc, #7c3aed)",
        button_primary_border_color="transparent",
        block_label_text_color="#4f46e5",
        block_label_text_weight="600",
    )
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True,
        theme=theme,
        css=CSS,
    )
