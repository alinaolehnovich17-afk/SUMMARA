import anthropic
from pydantic import ValidationError
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL
from models.schemas import SCHEMA_MAP

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def validate(source_text: str, template_name: str, data: dict) -> dict:
    """
    Проверяет извлечённые данные.
    Возвращает {"ok": bool, "issues": [...], "suggestions": [...], "score": int}
    """
    issues: list[str] = []

    # 1. Структурная проверка через Pydantic
    schema_class = SCHEMA_MAP.get(template_name)
    if schema_class is None:
        return {"ok": False, "issues": [f"Неизвестный шаблон: {template_name}"], "suggestions": [], "score": 0}

    try:
        schema_class(**data)
    except ValidationError as e:
        for err in e.errors():
            field = " → ".join(str(x) for x in err["loc"])
            issues.append(f"Поле '{field}': {err['msg']}")

    # 2. Семантическая проверка через Claude
    fields_summary = "\n".join(f"  {k}: {v}" for k, v in data.items())
    response = _get_client().messages.create(
        model=CLAUDE_MODEL,
        max_tokens=512,
        tools=[{
            "name": "validation_result",
            "description": "Результат семантической проверки инструкции",
            "input_schema": {
                "type": "object",
                "properties": {
                    "completeness_score": {
                        "type": "integer",
                        "description": "Полнота инструкции от 1 до 10",
                    },
                    "semantic_issues": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Критичные проблемы: противоречия, явно пропущенные обязательные детали",
                    },
                    "suggestions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Рекомендации по улучшению (не критичные)",
                    },
                },
                "required": ["completeness_score", "semantic_issues", "suggestions"],
            },
        }],
        tool_choice={"type": "tool", "name": "validation_result"},
        messages=[{
            "role": "user",
            "content": (
                f"Проверь качество извлечённой инструкции.\n\n"
                f"Исходный текст:\n{source_text}\n\n"
                f"Шаблон: {template_name}\n"
                f"Извлечённые поля:\n{fields_summary}\n\n"
                f"Оцени полноту (1-10), найди критичные проблемы и дай рекомендации."
            ),
        }],
    )

    semantic_issues: list[str] = []
    suggestions: list[str] = []
    score = 5

    for block in response.content:
        if block.type == "tool_use":
            inp = block.input
            score = inp.get("completeness_score", 5)
            semantic_issues = inp.get("semantic_issues", [])
            suggestions = inp.get("suggestions", [])
            break

    all_issues = issues + semantic_issues
    print(f"[Validator] Оценка: {score}/10, проблем: {len(all_issues)}, рекомендаций: {len(suggestions)}")

    return {
        "ok": len(all_issues) == 0,
        "issues": all_issues,
        "suggestions": suggestions,
        "score": score,
    }
