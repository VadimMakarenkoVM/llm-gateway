import time
import httpx

from app.providers.base import LLMProvider
from app.schemas.chat import ChatRequest
from app.core.config import settings
from app.core.logging import log_event
from app.core.errors import ProviderError

def _messages_to_prompt(request: ChatRequest) -> str:
    lines = []
    for m in request.messages:
        lines.append(f"{m.role.upper()}: {m.content}")
    lines.append("ASSISTANT:")
    return "\n".join(lines)

class OllamaProvider(LLMProvider):
    async def chat(self, request: ChatRequest):
        payload = {
            "model": request.model,
            "prompt": _messages_to_prompt(request),
            "options": {"temperature": request.temperature},
            "stream": False,
        }

        start = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=settings.http_timeout_s) as client:
                resp = await client.post(f"{settings.ollama_url}/api/generate", json=payload)
                resp.raise_for_status()
                data = resp.json()
        except httpx.HTTPStatusError as e:
            log_event(
                "llm.provider_error",
                provider="ollama",
                model=request.model,
                status_code=e.response.status_code,
            )
            raise ProviderError(
                message="Ollama returned error status",
                provider="ollama",
                status_code=502,
                detail=str(e),
            )
        except Exception as e:
            log_event(
                "llm.provider_error",
                provider="ollama",
                model=request.model,
                status_code=None,
            )
            raise ProviderError(
                message="Ollama request failed",
                provider="ollama",
                status_code=502,
                detail=str(e),
            )

        latency_ms = int((time.perf_counter() - start) * 1000)
        text = data.get("response", "")

        log_event(
            "llm.call",
            provider="ollama",
            model=request.model,
            latency_ms=latency_ms,
            output_chars=len(text),
            status="success",
        )

        return text, latency_ms
