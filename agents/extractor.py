import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL
from models.schemas import SCHEMA_MAP

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def extract(text: str, template_name: str) -> dict:
    """Извлекает структурированные данные из текста по схеме шаблона."""
    schema_class = SCHEMA_MAP.get(template_name)
    if schema_class is None:
        raise ValueError(f"Неизвестный шаблон: {template_name}")

    schema = schema_class.model_json_schema()

    response = _get_client().messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        tools=[{
            "name": "fill_template",
            "description": "Заполни поля шаблона данными, извлечёнными из текста.",
            "input_schema": schema,
        }],
        tool_choice={"type": "tool", "name": "fill_template"},
        messages=[{
            "role": "user",
            "content": (
                f"Извлеки структурированные данные из текста и заполни шаблон.\n\n"
                f"Текст:\n{text}"
            ),
        }],
    )

    for block in response.content:
        if block.type == "tool_use":
            print(f"[Extractor] Извлечено полей: {len(block.input)}")
            return block.input

    raise RuntimeError("Claude не вернул tool_use блок")
