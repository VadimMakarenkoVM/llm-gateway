import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.request_id import request_id_ctx, new_request_id

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("x-request-id") or new_request_id()
        token = request_id_ctx.set(rid)

        start = time.perf_counter()
        try:
            response: Response = await call_next(request)
        finally:
            request_id_ctx.reset(token)

        elapsed_ms = int((time.perf_counter() - start) * 1000)

        response.headers["x-request-id"] = rid
        response.headers["x-response-time-ms"] = str(elapsed_ms)
        return response
