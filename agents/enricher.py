"""
Обогатитель/обработчик готового текста: делает документ живее, понятнее и
эмоциональнее (примеры, пояснения, сноски) и оформляет его как нужный
ВИД документа (инструкция / регламент / пояснение / …) — НЕ ломая
Markdown-структуру (## заголовки, **Метка:** значение, списки),
чтобы парсеры PDF и HTML продолжали работать.

Промпты (системная роль, правила) и вид документа берутся из settings.py
и редактируются пользователем в разделе «Настройки» веб-интерфейса.
"""
import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL
import settings as user_settings

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def enrich(instruction_md: str, source_text: str = "", template_name: str = "") -> str:
    """Возвращает обработанную версию документа в Markdown (структура сохранена)."""
    cfg = user_settings.load_settings()
    system = cfg["enrich_system"]
    rules = cfg["enrich_rules"]
    output_kind = cfg["output_kind"]

    try:
        response = _get_client().messages.create(
            model=CLAUDE_MODEL,
            max_tokens=2048,
            system=system,
            messages=[{
                "role": "user",
                "content": (
                    f"Обработай документ ниже: сделай его живее, понятнее и эмоциональнее, "
                    f"добавь примеры, поясни термины и при необходимости сноски. "
                    f"Оформи его как «{output_kind}».\n\n"
                    f"{rules}\n\n"
                    f"Вид итогового документа: {output_kind}\n"
                    f"Тип шаблона: {template_name or 'не указан'}\n"
                    + (f"Исходный текст пользователя (для контекста):\n{source_text}\n\n" if source_text else "")
                    + f"Документ для обработки (Markdown):\n{instruction_md}"
                ),
            }],
        )
        parts = [b.text for b in response.content if getattr(b, "type", None) == "text"]
        result = "\n".join(parts).strip()
        if result:
            print(f"[Enricher] Обработано: {len(instruction_md)} -> {len(result)} символов (вид: {output_kind})")
            return result
    except Exception as e:
        print(f"[Enricher] Ошибка, возвращаю исходный текст: {e}")

    return instruction_md
