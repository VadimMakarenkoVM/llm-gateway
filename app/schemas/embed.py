from pydantic import BaseModel
from typing import List

class EmbedRequest(BaseModel):
    model: str
    text: str

class EmbedResponse(BaseModel):
    model: str
    embedding: List[float]
    latency_ms: int
    dim: int
