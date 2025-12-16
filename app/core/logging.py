import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict

from app.core.request_id import request_id_ctx

logger = logging.getLogger("llm_gateway")

def setup_logging() -> None:
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.propagate = False

def log_event(event: str, **fields: Any) -> None:
    payload: Dict[str, Any] = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "request_id": request_id_ctx.get(),
        **fields,
    }
    logger.info(json.dumps(payload, ensure_ascii=False))
