import joblib, numpy as np
from functools import lru_cache
from pathlib import Path
from typing import List, Union
from .features import SYMPTOMS

@lru_cache(maxsize=1)
def _load():
    base = Path(__file__).resolve().parents[2] / "models"
    return (
        joblib.load(base / "model.joblib"),
        joblib.load(base / "label_encoder.joblib"),
        np.load(base / "feat_imp.npy"),
    )

def _vectorize(symptoms: Union[List[str], List[int]]) -> np.ndarray:
    """Return a binary vector of length len(SYMPTOMS)."""
    if not symptoms:
        raise ValueError("Symptom list is empty.")

    # Case A: caller gave a full 0/1 vector already
    if all(isinstance(x, (int, np.integer)) for x in symptoms):
        if len(symptoms) != len(SYMPTOMS):
            raise ValueError(
                f"Expected vector of length {len(SYMPTOMS)}, got {len(symptoms)}"
            )
        return np.asarray(symptoms, dtype=int)

    # Case B: list of symptom names
    vec = np.zeros(len(SYMPTOMS), dtype=int)
    for s in symptoms:
        if s in SYMPTOMS:
            vec[SYMPTOMS.index(s)] = 1
        else:
            # Unknown symptom – ignore, but could log for debugging
            pass
    return vec

def predict(symptoms: Union[List[str], List[int]], top_k: int = 3, suggest_k: int = 5):
    """Return top-k disease predictions + smart symptom suggestions."""
    model, enc, imp = _load()
    vec = _vectorize(symptoms)

    probs = model.predict_proba(vec.reshape(1, -1))[0]
    top_idx = np.argsort(probs)[::-1][:top_k]
    top = [
        {
            "disease": enc.inverse_transform([i])[0],
            "prob": round(float(probs[i] * 100), 2),  # percentage
        }
        for i in top_idx
    ]

    absent = np.where(vec == 0)[0]
    ranked = sorted(absent, key=lambda i: imp[i], reverse=True)
    suggestions = [SYMPTOMS[i] for i in ranked[:suggest_k]]

    return {"top": top, "suggest": suggestions}
