from fastapi import APIRouter, HTTPException
from app.schemas.embed import EmbedRequest, EmbedResponse
from app.core.router import ModelRouter
from app.core.logging import log_event
from app.core.errors import ProviderError

router = APIRouter(tags=["embed"])

@router.post("/embed", response_model=EmbedResponse)
async def embed(request: EmbedRequest):
    router_core = ModelRouter()

    try:
        routed = router_core.parse(request.model)
        provider = router_core.get_embed_provider(routed)

        log_event("embed.route", requested_model=request.model, provider=routed.provider, routed_model=routed.model)

        clean_request = request.model_copy(update={"model": routed.model})
        embedding, latency = await provider.embed(clean_request)

        return EmbedResponse(
            model=request.model,
            embedding=embedding,
            latency_ms=latency,
            dim=len(embedding),
        )

    except ProviderError as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_public())

    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": "bad_request", "message": str(e)})
