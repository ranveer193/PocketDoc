from pydantic import BaseModel
from typing import List, Tuple, Optional, Dict

class Prediction(BaseModel):
    disease: str
    confidence: float

class ChatTurn(BaseModel):
    chat_id: Optional[str] = None   # filled by client after first turn
    user: str                       # user utterance

class ChatResponse(BaseModel):
    chat_id: str
    elapsed: float
    finished: bool
    predictions: List[Prediction]           # always present
    question: Optional[str] = None          # if !finished
    diagnosis: Optional[str] = None         # if finished

class ChatRecord(BaseModel):
    messages: List[Tuple[str, str]]
    predictions: List[Prediction]
    created_at: float
