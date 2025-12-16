from dataclasses import dataclass

@dataclass
class ProviderError(Exception):
    message: str
    provider: str
    status_code: int = 502  # Bad Gateway as default
    detail: str | None = None

    def to_public(self) -> dict:
        return {
            "error": "provider_error",
            "message": self.message,
            "provider": self.provider,
        }
