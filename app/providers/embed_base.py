from abc import ABC, abstractmethod
from typing import List, Tuple
from app.schemas.embed import EmbedRequest

class EmbeddingProvider(ABC):
    @abstractmethod
    async def embed(self, request: EmbedRequest) -> Tuple[List[float], int]:
        pass
