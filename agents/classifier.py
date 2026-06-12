import yaml
import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, TEMPLATES_DIR

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def _load_templates() -> list[dict]:
    templates = []
    for path in sorted(TEMPLATES_DIR.glob("*.yaml")):
        with open(path, encoding="utf-8") as f:
            templates.append(yaml.safe_load(f))
    return templates


def classify(text: str) -> str:
    """Определяет имя шаблона, наиболее подходящего для текста."""
    templates = _load_templates()
    template_descriptions = "\n".join(
        f"- {t['name']}: {t['description']} "
        f"(ключевые слова: {', '.join(t.get('trigger_keywords', []))})"
        for t in templates
    )
    names = [t["name"] for t in templates]

    response = _get_client().messages.create(
        model=CLAUDE_MODEL,
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": (
                f"Выбери шаблон, который ТОЧНЕЕ всего соответствует тексту.\n\n"
                f"Шаблоны:\n{template_descriptions}\n\n"
                f"Правила выбора:\n"
                f"- Если текст упоминает встречу, совещание, созвон, собрание — "
                f"даже в контексте планирования ('провести', 'организовать', 'запланировать') — выбирай meeting.\n"
                f"- task выбирай только если в тексте нет слов встречи/совещания.\n"
                f"- bug_report выбирай только при описании ошибки или неисправности.\n\n"
                f"Текст:\n{text}\n\n"
                f"Ответь ТОЛЬКО одним словом из списка: {' | '.join(names)}"
            ),
        }],
    )

    result = response.content[0].text.strip().lower()
    print(f"[Classifier] Ответ Claude: '{result}'")

    for name in names:
        if name in result:
            return name

    print(f"[Classifier] Шаблон не распознан, используется '{names[0]}'")
    return names[0]
