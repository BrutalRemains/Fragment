from pathlib import Path
from functools import lru_cache
# simply reads from our text files and builds the prompt using the context provided
# the prompts are used to constrain the llm to the expected behaviors

TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "services" / "prompts" / "creature_system_prompt.txt"
ACTION_TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "services" / "prompts" 

@lru_cache(maxsize=1)
def _load_template():
    return TEMPLATE_PATH.read_text(encoding="utf-8")

def render_creature_prompt(context):
    template = _load_template()
    return template.format_map(context)

def render_action_prompt(context, intent, action_result, user_text):
    # system = render_creature_prompt(context)
    action_file = ACTION_TEMPLATE_DIR / f"action_{intent}.txt"
    if not action_file.exists():
        action_file = ACTION_TEMPLATE_DIR / "action_chat.txt"
    
    template = action_file.read_text(encoding="utf-8")
    action = template.format_map({
        **context, 
        "user_text": user_text,
        "success": action_result.get("success"),
        "reason": action_result.get("reason"),
        "user_text": user_text,
        })

    return action