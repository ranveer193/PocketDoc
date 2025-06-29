from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.chat import router as chat_router

app = FastAPI(title="PocketDoc API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # set your frontend URL in prod
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def health():
    return {"status": "ok"}
app.include_router(chat_router, prefix="/api")
