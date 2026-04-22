INTENT_THRESHOLD = 0.7

def parse_command(text: str):
    if not text.startswith("/"):
        return None
    return text[1:].split(" ", 1)[0].strip().lower()

# we first check for intent ourselves using simple keyword matching, faster than llm

def local_intent_parse(text: str):
    t = text.lower().strip()

    if any(p in t for p in ["feed", "give food", "hungry", "eat"]):
        return {"intent": "feed", "confidence": 0.9}
    if any(p in t for p in ["play", "fetch", "game"]):
        return {"intent": "play", "confidence": 0.85}
    if any(p in t for p in ["rest", "sleep", "nap"]):
        return {"intent": "rest", "confidence": 0.9}
    if any(p in t for p in ["teach", "learn trick", "new trick"]):
        return {"intent": "teach", "confidence": 0.85}
    if "status" in t:
        return {"intent": "status", "confidence": 0.95}

    return {"intent": "chat", "confidence": 0.0}

def run_action(creature, intent: str):
    if intent == "feed":
        return creature.feed()
    if intent == "play":
        return creature.play()
    if intent == "rest":
        return creature.rest()
    if intent == "teach":
        return creature.teach_trick()
    if intent == "status":
        return {"success": True, "reason": "status_only"}
    return {"success": True, "reason": "chat_only"}

def apply_user_input(creature, user_input: str) -> dict:
    text = user_input.strip()
    if not text:
        return {"intent": "chat", "action_result": {"success": False, "reason": "empty_input"}}

    cmd = parse_command(text)
    if cmd:
        intent = cmd
        action_result = run_action(creature, intent)
        return {"intent": intent, "action_result": action_result, "user_text_for_llm": text}

    parsed = local_intent_parse(text)
    intent = parsed["intent"]

    if parsed["confidence"] >= INTENT_THRESHOLD and intent != "chat":
        action_result = run_action(creature, intent)
        return {"intent": intent, "action_result": action_result, "user_text_for_llm": text}

    return {
        "intent": "chat",
        "action_result": {"success": True, "reason": "chat_only"},
        "user_text_for_llm": text,
    }