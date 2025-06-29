from app.services.or_client import or_chat
import json

SYSTEM = (
    "You are a triage assistant. Decide if a user message is describing real physical "
    "symptoms that map to a disease. Respond with a single word: YES or NO."
)

def looks_like_symptom(user_text: str, preds: list[dict]) -> bool:
    prompt = (
        f"User message: \"{user_text}\"\n\n"
        f"Top disease predictions (may be nonsense): {json.dumps(preds[:3])}\n\n"
        "Is the user describing real health symptoms? Answer YES or NO."
    )
    ans = or_chat([{"role":"system","content":SYSTEM},{"role":"user","content":prompt}])
    return ans.strip().lower().startswith("y")
