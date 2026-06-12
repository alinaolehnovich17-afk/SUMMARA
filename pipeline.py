import yaml
from jinja2 import Template
from config import TEMPLATES_DIR
from agents.transcription import transcribe
from agents.classifier import classify
from agents.extractor import extract
from agents.validator import validate
from agents.enricher import enrich as enrich_text


def _load_template_config(name: str) -> dict:
    path = TEMPLATES_DIR / f"{name}.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _render(template_name: str, data: dict) -> str:
    config = _load_template_config(template_name)
    jinja_tpl = Template(config["output_template"])
    return jinja_tpl.render(**data)


def run(text: str = None, audio_path: str = None, enrich: bool = False) -> dict:
    """
    Полный пайплайн: текст или аудио → готовая инструкция.

    Параметры:
      enrich       — если True, текст обогащается (живее, примеры, пояснения, сноски)

    Возвращает:
      template       — имя шаблона
      source_text    — исходный текст (после транскрипции)
      data           — извлечённые поля (dict)
      rendered       — финальная инструкция (Markdown; обогащённая, если enrich=True)
      rendered_plain — инструкция без обогащения (для отладки)
      validation     — {"ok", "issues", "suggestions", "score"}
    """
    if audio_path:
        print("[Pipeline] Транскрипция аудио...")
        text = transcribe(audio_path)
        print(f"[Pipeline] Транскрипция: {text[:100]}...")

    if not text or not text.strip():
        raise ValueError("Пустой ввод — нет текста для обработки.")

    print("[Pipeline] Классификация шаблона...")
    template_name = classify(text)
    print(f"[Pipeline] Шаблон: {template_name}")

    print("[Pipeline] Извлечение данных...")
    data = extract(text, template_name)

    print("[Pipeline] Рендер инструкции...")
    rendered_plain = _render(template_name, data)

    rendered = rendered_plain
    if enrich:
        print("[Pipeline] Обогащение текста...")
        rendered = enrich_text(rendered_plain, source_text=text, template_name=template_name)

    print("[Pipeline] Валидация...")
    validation = validate(text, template_name, data)

    return {
        "template": template_name,
        "source_text": text,
        "data": data,
        "rendered": rendered,
        "rendered_plain": rendered_plain,
        "validation": validation,
    }
