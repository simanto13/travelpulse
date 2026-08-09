from uuid import uuid4
from fastapi import APIRouter

router=APIRouter(prefix="/weather",tags=["Weather"])

@router.get("/health")
async def health():
    return {"status":"healthy"}

@router.post("/chat")
async def chat(payload:dict):
    return {
        "conversation_id":payload.get("conversation_id") or str(uuid4()),
        "answer":"Wire this endpoint to WeatherAgent.chat()",
        "weather":{},
        "sources":[]
    }
