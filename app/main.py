from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.core.middleware import RequestIdMiddleware
from app.core.logging import setup_logging
from app.api.embed import router as embed_router

setup_logging()

app = FastAPI(title="LLM Gateway")
app.add_middleware(RequestIdMiddleware)

app.include_router(chat_router)
app.include_router(embed_router)

@app.get("/health")
def health():
    return {"status": "ok"}
