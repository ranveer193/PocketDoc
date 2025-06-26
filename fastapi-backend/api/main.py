# api/main.py  (Pydantic v2 syntax)

from typing import Annotated, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from api.model import predict

app = FastAPI(title="PocketDoc API (XGBoost)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Pydantic v2 input schema
# -------------------------------
class Req(BaseModel):
    # Accept a list of symptom strings, 1-30 items
    symptoms: Annotated[
        List[str],
        Field(min_length=1, max_length=30)
    ]

# -------------------------------
# /predict endpoint
# -------------------------------
@app.post("/predict")
def predict_endpoint(r: Req):
    try:
        result = predict(r.symptoms, top_k=3, suggest_k=5)
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
