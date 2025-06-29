import json, math, random, difflib
from pathlib import Path
from typing import List, Dict
from collections import Counter
from app.services.hf_client   import hf_classify
from app.services.or_client   import generate_followup
from app.utils.llm_intent     import looks_like_symptom
from app.core.memory          import summarize
from app.core.knowledge       import SYMPTOMS_BY_DISEASE as KB

BASE_DIR  = Path(__file__).resolve().parent.parent.parent
FACTS     = json.loads((BASE_DIR / "disease_facts.json").read_text())

# ─── utility ──────────────────────────────────────────────
def entropy(dist: List[float]) -> float:
    return -sum(p*math.log2(p+1e-9) for p in dist)

def info_gain(symptom: str, candidates: List[Dict]) -> float:
    """Expected reduction in entropy if we knew YES/NO for symptom."""
    present, absent = [], []
    for c in candidates:
        dis = c["disease"]; p = c["confidence"]
        (present if symptom in KB.get(dis, set()) else absent).append(p)
    def H(lst): return entropy([p/sum(lst) for p in lst]) if lst else 0.0
    total = sum(c["confidence"] for c in candidates)
    weight_yes, weight_no = sum(present)/total, sum(absent)/total
    return entropy([c["confidence"]/total for c in candidates]) - (
        weight_yes*H(present) + weight_no*H(absent))

def pick_best_symptom(candidates: List[Dict], asked: List[str]) -> str|None:
    # union of candidate‑disease symptoms
    pool = set().union(*(KB.get(c["disease"], set()) for c in candidates))
    pool -= set(asked)                 # avoid repeats
    scored = [(info_gain(s, candidates), s) for s in pool]
    scored.sort(reverse=True)
    return scored[0][1] if scored and scored[0][0] > 0.05 else None

def jaccard(a: str, b: str) -> float:
    tok = lambda x: set(x.lower().split())
    return len(tok(a)&tok(b))/max(1, len(tok(a)|tok(b)))

# ─── main loop ────────────────────────────────────────────
MAX_LOOPS = 6         # hard stop
MIN_ENTROPY = 1.0     # bits
MIN_GAIN    = 0.05    # info gain threshold

def cycle(state: dict) -> dict:
    """
    state: {"history":[(role,text)], "asked":[q], "loops":int}
    """
    hist, asked, loops = state["history"], state["asked"], state["loops"]
    user_full = " ".join(t for r,t in hist if r=="user")

    # 1️⃣  greeting filter
    preds = hf_classify(user_full, top_k=5)
    if not looks_like_symptom(user_full, preds):
        return {"finished":False,
                "predictions":[],
                "question":"I’m here to help with health issues. Could you describe any symptoms you’re experiencing?"}

    # normalize distribution
    total = sum(p["confidence"] for p in preds)
    for p in preds: p["confidence"] /= total

    # 2️⃣  termination checks
    if entropy([p["confidence"] for p in preds]) < MIN_ENTROPY or loops >= MAX_LOOPS:
        best = preds[0]["disease"]
        return {"finished":True,
                "diagnosis":best,
                "predictions":preds,
                "facts":FACTS.get(best,"No facts in database.")}

    # 3️⃣  pick symptom with highest info gain
    new_sym = pick_best_symptom(preds, asked)
    if not new_sym:   # no informative symptom left
        best = preds[0]["disease"]
        return {"finished":True,
                "diagnosis":best,
                "predictions":preds,
                "facts":FACTS.get(best,"No facts in database.")}

    # 4️⃣  build follow‑up prompt
    summ, last_two = summarize(hist)
    last_block = "\n".join(f"{r.capitalize()}: {t}" for r,t in last_two)
    ctx = (
        f"{summ}\n\n{last_block}\n\n"
        f"Ask the patient whether they experience: **{new_sym.replace('_',' ')}**. "
        f"Phrase it as ONE short question."
    )
    q = generate_followup(ctx).strip()

    # avoid near‑duplicate wording
    if any(jaccard(q, old) > 0.8 for old in asked):
        q = f"Do you have {new_sym.replace('_',' ')}?"

    asked.append(q)
    state["loops"] += 1
    return {"finished":False,
            "question":q,
            "predictions":preds}
