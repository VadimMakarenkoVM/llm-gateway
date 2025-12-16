from pydantic import BaseModel
from typing import List, Literal

class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: float = 0.7

class ChatResponse(BaseModel):
    model: str
    content: str
    latency_ms: int