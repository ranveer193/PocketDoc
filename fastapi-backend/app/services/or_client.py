import os, requests

OR_URL = "https://openrouter.ai/api/v1/chat/completions"
OR_HEADERS = {
    "Authorization": f"Bearer {os.getenv('OPENROUTER_KEY')}",
    "Content-Type": "application/json"
}

def or_chat(messages, max_tokens=50, model="mistralai/mistral-7b-instruct", temperature=0.0):
    """
    Send a chat completion request to OpenRouter with given messages.
    """
    body = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    r = requests.post(OR_URL, headers=OR_HEADERS, json=body, timeout=30)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()

def generate_followup(context: str) -> str:
    """
    Returns a concise follow-up medical question from an AI doctor.
    """
    messages = [
        {"role": "system", "content": "You are an experienced doctor asking succinct follow-up questions."},
        {"role": "user",   "content": context}
    ]
    return or_chat(messages, max_tokens=64, temperature=0.7)
