import os, requests
from dotenv import load_dotenv

# ──────────────────────────── load .env early ───────────────────────────
load_dotenv()                                        # must be called once
HF_TOKEN = os.getenv("HF_TOKEN")                     # read from .env
if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN is missing. Add it to your .env file.")

# ─────────────────── disease‑label integer → human name ─────────────────
LABEL2DISEASE = {
     0:"(Vertigo) Paroxysmal Positional Vertigo",  1:"AIDS",           2:"Acne",
     3:"Alcoholic hepatitis",                      4:"Allergy",        5:"Arthritis",
     6:"Bronchial Asthma",                         7:"Cervical spondylosis",
     8:"Chicken pox",                              9:"Chronic cholestasis",
    10:"Common Cold",                             11:"Dengue",        12:"Diabetes",
    13:"Dimorphic hemorrhoids (piles)",           14:"Drug Reaction", 15:"Fungal infection",
    16:"GERD",                                    17:"Gastroenteritis",
    18:"Heart attack",                            19:"Hepatitis B",   20:"Hepatitis C",
    21:"Hepatitis D",                             22:"Hepatitis E",   23:"Hypertension",
    24:"Hyperthyroidism",                         25:"Hypoglycemia",  26:"Hypothyroidism",
    27:"Impetigo",                                28:"Jaundice",      29:"Malaria",
    30:"Migraine",                                31:"Osteoarthritis",
    32:"Paralysis (brain hemorrhage)",            33:"Peptic ulcer disease",
    34:"Pneumonia",                               35:"Psoriasis",     36:"Tuberculosis",
    37:"Typhoid",                                 38:"Urinary tract infection",
    39:"Varicose veins",                          40:"Hepatitis A",
}

# ───────────────────────── model + endpoint setup ───────────────────────
MODEL   = "shanover/symps_disease_bert_v3_c41"       # public, 41 classes
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json",
}

# ───────────────────────────── main function ────────────────────────────
def hf_classify(symptoms: str, top_k: int = 3):
    """
    Call HF Inference API and return:
    [
      {"disease": "Common Cold", "confidence": 0.42},
      {"disease": "Pneumonia",   "confidence": 0.13},
      ...
    ]
    """
    payload = {
        "inputs": symptoms,
        "parameters": {"top_k": top_k}
    }

    r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
    if r.status_code == 404:
        raise RuntimeError("❌ 404 – model slug incorrect or repo private.")
    if r.status_code == 401:
        raise RuntimeError("❌ 401 – HF_TOKEN invalid or missing.")
    if r.status_code not in (200, 202, 503):
        raise RuntimeError(f"HF error {r.status_code}: {r.text[:160]}")

    raw = r.json()[0]    # HF returns list[list[dict(label,score)]]
    results = []
    for rec in raw:
        label_idx = int(rec["label"].split("_")[-1])   # "LABEL_34" -> 34
        disease   = LABEL2DISEASE.get(label_idx, f"Unknown_{label_idx}")
        results.append({"disease": disease, "confidence": rec["score"]})

    return results