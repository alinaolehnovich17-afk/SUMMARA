"""
⚠️ Совместимость / редирект.

Канонический MCP-сервер SUMMARA теперь живёт в `summara_mcp/mcp_server.py`
(там все актуальные инструменты, включая generate_landing).

Этот файл оставлен только для обратной совместимости: если в конфиге Claude
Desktop прописан старый путь `.../summara/mcp_server.py`, он продолжит работать
и запустит актуальную версию. В новых конфигах указывайте напрямую
`.../summara/summara_mcp/mcp_server.py`.
"""
import runpy
from pathlib import Path

_CANONICAL = Path(__file__).parent / "summara_mcp" / "mcp_server.py"

if __name__ == "__main__":
    runpy.run_path(str(_CANONICAL), run_name="__main__")
