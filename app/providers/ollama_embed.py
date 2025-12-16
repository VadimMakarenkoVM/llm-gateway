import time
import httpx

from app.core.config import settings
from app.core.logging import log_event
from app.core.errors import ProviderError
from app.providers.embed_base import EmbeddingProvider
from app.schemas.embed import EmbedRequest

class OllamaEmbeddingProvider(EmbeddingProvider):
    async def embed(self, request: EmbedRequest):
        payload = {
            "model": request.model,
            "prompt": request.text
        }

        start = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=settings.http_timeout_s) as client:
                resp = await client.post(f"{settings.ollama_url}/api/embeddings", json=payload)
                resp.raise_for_status()
                data = resp.json()
        except httpx.HTTPStatusError as e:
            log_event("embed.provider_error", provider="ollama", model=request.model, status_code=e.response.status_code)
            raise ProviderError(
                message="Ollama embeddings returned error status",
                provider="ollama",
                status_code=502,
                detail=str(e),
            )
        except Exception as e:
            log_event("embed.provider_error", provider="ollama", model=request.model, status_code=None)
            raise ProviderError(
                message="Ollama embeddings request failed",
                provider="ollama",
                status_code=502,
                detail=str(e),
            )

        latency_ms = int((time.perf_counter() - start) * 1000)
        emb = data.get("embedding", [])
        dim = len(emb)

        log_event("embed.call", provider="ollama", model=request.model, latency_ms=latency_ms, dim=dim, status="success")
        return emb, latency_ms
