import uuid
from contextvars import ContextVar

# Available anywhere in the code without passing parameters
request_id_ctx: ContextVar[str | None] = ContextVar("request_id", default=None)

def new_request_id() -> str:
    return uuid.uuid4().hex
