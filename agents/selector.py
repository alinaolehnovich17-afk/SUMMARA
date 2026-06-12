"""
Селектор дизайна: по контексту текста выбирает 3 наиболее подходящих
стиля HTML-лэндинга из доступных в HTML_STYLES.
"""
import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL
from .html_templates import HTML_STYLES, DEFAULT_TRIPLES

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def _fallback(template_name: str, n: int) -> list[str]:
    keys = list(HTML_STYLES.keys())
    triple = DEFAULT_TRIPLES.get(template_name, keys[:n])
    # дополняем до n уникальными ключами
    out = list(dict.fromkeys(triple))
    for k in keys:
        if len(out) >= n:
            break
        if k not in out:
            out.append(k)
    return out[:n]


def select_designs(text: str, template_name: str, data: dict | None = None, n: int = 3) -> list[str]:
    """Возвращает список из n ключей стилей, наиболее подходящих по контексту."""
    keys = list(HTML_STYLES.keys())
    if n >= len(keys):
        return keys

    catalog = "\n".join(
        f"- {key}: {meta['label']} — подходит для: {', '.join(meta['context_tags'])}"
        for key, meta in HTML_STYLES.items()
    )

    try:
        response = _get_client().messages.create(
            model=CLAUDE_MODEL,
            max_tokens=60,
            tools=[{
                "name": "pick_designs",
                "description": "Выбор подходящих стилей оформления",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "styles": {
                            "type": "array",
                            "items": {"type": "string", "enum": keys},
                            "description": f"Ровно {n} ключей стилей в порядке убывания уместности",
                        }
                    },
                    "required": ["styles"],
                },
            }],
            tool_choice={"type": "tool", "name": "pick_designs"},
            messages=[{
                "role": "user",
                "content": (
                    f"Подбери {n} наиболее уместных по СМЫСЛУ и НАСТРОЕНИЮ стиля оформления "
                    f"для инструкции ниже.\n\n"
                    f"Тип инструкции: {template_name}\n"
                    f"Текст:\n{text}\n\n"
                    f"Доступные стили:\n{catalog}\n\n"
                    f"Верни ровно {n} разных ключа, лучший — первым."
                ),
            }],
        )
        for block in response.content:
            if block.type == "tool_use":
                picked = block.input.get("styles", [])
                # фильтруем валидные и уникальные
                seen, out = set(), []
                for k in picked:
                    if k in HTML_STYLES and k not in seen:
                        seen.add(k)
                        out.append(k)
                if len(out) >= n:
                    print(f"[Selector] Выбраны стили: {out[:n]}")
                    return out[:n]
                # добиваем фолбэком
                for k in _fallback(template_name, n):
                    if k not in seen:
                        out.append(k)
                        seen.add(k)
                    if len(out) >= n:
                        break
                print(f"[Selector] Стили (с добивкой): {out[:n]}")
                return out[:n]
    except Exception as e:
        print(f"[Selector] Ошибка, фолбэк: {e}")

    return _fallback(template_name, n)
