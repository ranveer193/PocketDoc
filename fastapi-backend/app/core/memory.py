def summarize(history):
    """
    history = list[tuple(role, text)]  (the entire convo)
    Returns summary str  + last_two list[(role,text)]
    """
    if len(history) <= 4:
        return "", history[-2:]
    # very naive summary: merge user symptom phrases only
    user_symptoms = [txt for role, txt in history[:-2] if role == "user"]
    summary = "User previously mentioned: " + "; ".join(user_symptoms)
    return summary, history[-2:]
