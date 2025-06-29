import os, motor.motor_asyncio
from dotenv import load_dotenv
load_dotenv()   

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("MONGO_URI is missing. Add it to your .env file.")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client["pocketdoc"]
history_col = db["history"]