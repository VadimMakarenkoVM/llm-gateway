from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.router import ModelRouter
from app.core.logging import log_event
from app.core.errors import ProviderError

router = APIRouter(tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    router_core = ModelRouter()

    try:
        routed = router_core.parse(request.model)
        provider = router_core.get_provider(routed)

        log_event("llm.route", requested_model=request.model, provider=routed.provider, routed_model=routed.model)

        clean_request = request.model_copy(update={"model": routed.model})
        content, latency = await provider.chat(clean_request)

        return ChatResponse(
            model=request.model,
            content=content,
            latency_ms=latency,
        )

    except ProviderError as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_public())

    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": "bad_request", "message": str(e)})
