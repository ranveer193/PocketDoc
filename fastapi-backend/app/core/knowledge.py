# Make a tiny knowledge base: {disease: set(symptom)}
import json, re, itertools
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW = json.loads((BASE_DIR / "disease_facts.json").read_text())  # {disease: str facts}

SYMPTOMS_BY_DISEASE = {}
simple_tok = lambda s: re.findall(r"[a-z']+", s.lower())

for dis, facts in RAW.items():
    # crude: extract tokens after '•', ',', ';'
    tokens = set(itertools.chain.from_iterable(simple_tok(x) for x in re.split(r"[•,;]", facts)))
    # filter obvious stopwords
    tokens -= {"the","and","of","to","in","or","a","an","with","on","for","is","are","at"}
    SYMPTOMS_BY_DISEASE[dis] = tokens
