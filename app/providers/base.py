from abc import ABC, abstractmethod
from typing import Tuple
from app.schemas.chat import ChatRequest

class LLMProvider(ABC):
    @abstractmethod
    async def chat(self, request: ChatRequest) -> Tuple[str, int]:
        pass