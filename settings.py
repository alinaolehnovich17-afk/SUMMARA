"""
Пользовательские настройки SUMMARA: редактируемые промпты обработки готового
текста и вид итогового документа. Хранятся в user_settings.json (рядом с проектом),
применяются «на лету» — без перезапуска приложения.
"""
import json
from pathlib import Path
from config import BASE_DIR

SETTINGS_PATH = BASE_DIR / "user_settings.json"

# ── Значения по умолчанию ─────────────────────────────────────────────────────

DEFAULT_OUTPUT_KIND = "инструкция"

DEFAULT_ENRICH_SYSTEM = (
    "Ты — редактор, который делает деловые документы живыми, тёплыми и понятными, "
    "сохраняя их структуру."
)

DEFAULT_ENRICH_RULES = """\
ПРАВИЛА (соблюдай строго):
1. СОХРАНИ Markdown-скелет без изменений типов строк:
   - строки `## Заголовок` оставь заголовками (текст можно слегка оживить, но формат `## ` сохрани);
   - строки вида `**Метка:** значение` оставь ровно в этом формате (метку НЕ переименовывай, обогащай только значение);
   - маркированные списки `- пункт` и нумерованные `1. пункт` оставь списками того же вида.
2. Можно РАСШИРЯТЬ значения полей и пункты: добавлять пояснения, примеры, делать тон теплее и эмоциональнее (умеренно, без китча).
3. Поясняй непонятные термины прямо в тексте или короткой сноской.
4. Сноски: помечай в тексте маркером вида [1], [2], а в самом конце добавь новую секцию:
   `## Пояснения`
   и под ней список: `1. ...`, `2. ...` с расшифровками. Добавляй сноски только если они реально полезны.
5. Не выдумывай факты (даты, имена, цифры), которых нет в исходных данных. Примеры помечай словом «например».
6. Не добавляй преамбул вроде «Вот обогащённая версия». Верни ТОЛЬКО готовый Markdown."""

DEFAULTS: dict[str, str] = {
    "output_kind": DEFAULT_OUTPUT_KIND,
    "enrich_system": DEFAULT_ENRICH_SYSTEM,
    "enrich_rules": DEFAULT_ENRICH_RULES,
}

# Человекочитаемые названия полей — для UI
FIELD_LABELS = {
    "output_kind": "Вид итогового документа",
    "enrich_system": "Роль обработчика текста (системный промпт)",
    "enrich_rules": "Правила обработки готового текста",
}


# ── API ───────────────────────────────────────────────────────────────────────

def load_settings() -> dict:
    """Возвращает настройки: дефолты, переопределённые сохранённым файлом."""
    data = dict(DEFAULTS)
    if SETTINGS_PATH.exists():
        try:
            saved = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
            for k in DEFAULTS:
                if isinstance(saved.get(k), str) and saved[k].strip():
                    data[k] = saved[k]
        except Exception as e:
            print(f"[Settings] Ошибка чтения {SETTINGS_PATH.name}: {e}")
    return data


def get(key: str) -> str:
    return load_settings().get(key, DEFAULTS.get(key, ""))


def save_settings(output_kind: str, enrich_system: str, enrich_rules: str) -> str:
    """Сохраняет настройки. Пустые поля заменяются дефолтами. Возвращает статус."""
    data = {
        "output_kind": (output_kind or "").strip() or DEFAULTS["output_kind"],
        "enrich_system": (enrich_system or "").strip() or DEFAULTS["enrich_system"],
        "enrich_rules": (enrich_rules or "").strip() or DEFAULTS["enrich_rules"],
    }
    try:
        SETTINGS_PATH.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return "✅ Настройки сохранены — применятся при следующей генерации."
    except Exception as e:
        return f"❌ Не удалось сохранить: {e}"


def reset_settings() -> tuple[str, str, str, str]:
    """Сбрасывает к стандартным. Возвращает (output_kind, system, rules, статус)."""
    try:
        if SETTINGS_PATH.exists():
            SETTINGS_PATH.unlink()
    except Exception as e:
        return (
            DEFAULTS["output_kind"], DEFAULTS["enrich_system"], DEFAULTS["enrich_rules"],
            f"❌ Не удалось удалить файл настроек: {e}",
        )
    return (
        DEFAULTS["output_kind"], DEFAULTS["enrich_system"], DEFAULTS["enrich_rules"],
        "↩️ Возвращены стандартные настройки.",
    )
