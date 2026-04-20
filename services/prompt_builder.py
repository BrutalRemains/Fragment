from pathlib import Path
from functools import lru_cache

TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "prompts" / "creature_system_prompt.txt"

@lru_cache(maxsize=1)
def _load_template() -> str:
    return TEMPLATE_PATH.read_text(encoding="utf-8")

def render_creature_prompt(context: dict):
    template = _load_template()
    return template.format_map(context)