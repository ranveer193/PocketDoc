import os, requests
from dotenv import load_dotenv; load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL    = "abhirajeshbhai/Symptom2Disease"   # 41‑class public repo
URL      = f"https://api-inference.huggingface.co/models/{MODEL}"

headers  = {"Authorization": f"Bearer {HF_TOKEN}"}
data     = {"inputs": "fever, cough, headache, fatigue, sore throat"}

r = requests.post(URL, headers=headers, json=data)
print("HTTP:", r.status_code)
print(r.text[:300])