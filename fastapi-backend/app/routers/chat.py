from fastapi import APIRouter, HTTPException, status
from app.models import ChatTurn, ChatResponse, ChatRecord
from app.core.logic import cycle
from app.db import history_col
import uuid, time

router = APIRouter(prefix="/chat", tags=["chat"])

# each chat id ⇒ {"history":[(role,text)], "asked":[], "loops":int}
MEM: dict[str, dict] = {}

# ───────────────── start ─────────────────
@router.post("/start", response_model=ChatResponse)
def start(turn: ChatTurn):
    cid = turn.chat_id or str(uuid.uuid4())
    MEM[cid] = {"history":[("user", turn.user)], "asked":[], "loops":0}
    return _run_cycle(cid)

# ──────────────── continue ───────────────
@router.post("/continue", response_model=ChatResponse)
def cont(turn: ChatTurn):
    if not turn.chat_id or turn.chat_id not in MEM:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Unknown chat_id")
    MEM[turn.chat_id]["history"].append(("user", turn.user))
    return _run_cycle(turn.chat_id)

# ─────────────── save history ────────────
@router.post("/save")
async def save_chat(record: ChatRecord):
    await history_col.insert_one(record.model_dump())
    return {"status": "ok"}

# ───────────── helper ────────────────────
def _run_cycle(cid: str) -> ChatResponse:
    t0 = time.time()
    result = cycle(MEM[cid])     # modifies state inside
    elapsed = round(time.time() - t0, 2)

    bot_msg = result.get("diagnosis") or result.get("question")
    MEM[cid]["history"].append(("bot", bot_msg))

    return ChatResponse(
        chat_id      = cid,
        elapsed      = elapsed,
        finished     = result["finished"],
        predictions  = result["predictions"],
        question     = result.get("question"),
        diagnosis    = result.get("diagnosis")
    )