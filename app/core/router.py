from dataclasses import dataclass
from typing import Tuple

from app.providers.ollama import OllamaProvider
from app.core.config import settings
from app.providers.base import LLMProvider

@dataclass(frozen=True)
class RoutedModel:
    provider: str
    model: str

class ModelRouter:
    """
    Правило:
      - model строка может быть вида "provider:model"
        пример: "ollama:llama3.2:3b"
      - если префикса нет, используем settings.default_provider
    """

    def parse(self, model_str: str) -> RoutedModel:
        if ":" in model_str:
            provider, model = model_str.split(":", 1)
            provider = provider.strip().lower()
            model = model.strip()
        else:
            provider = settings.default_provider
            model = model_str.strip()

        if not model:
            raise ValueError("Empty model name")

        return RoutedModel(provider=provider, model=model)

    def get_provider(self, routed: RoutedModel) -> LLMProvider:
        if routed.provider == "ollama":
            return OllamaProvider()

        # for future providers
        # if routed.provider == "openai":
        #     return OpenAIProvider()

        raise ValueError(f"Unknown provider '{routed.provider}'")
