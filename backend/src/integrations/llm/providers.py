"""Provider factory implementations for supported LLM vendors."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from agno.models.google import Gemini
from agno.models.ollama import Ollama
from agno.models.openai import OpenAIChat

from src.config import settings
from src.shared.exceptions import (
    LLMProviderNotConfiguredError,
    LLMProviderUnsupportedError,
)

from .model_config import LLMModelConfig

ProviderFactory = Callable[[LLMModelConfig, Mapping[str, Any]], Any]


def _build_openai_model(
    config: LLMModelConfig,
    overrides: Mapping[str, Any],
) -> OpenAIChat:
    secret_name = config.api_key_env or "OPENAI_API_KEY"
    api_key = settings.get_secret(secret_name)
    if not api_key:
        raise LLMProviderNotConfiguredError(
            provider="openai",
            secret_name=secret_name,
        )
    params: dict[str, Any] = {
        "id": config.model_id,
        "api_key": api_key,
    }
    if config.base_url:
        params["base_url"] = config.base_url
    params.update(config.default_params)
    params.update(overrides)
    return OpenAIChat(**params)


def _build_google_model(
    config: LLMModelConfig,
    overrides: Mapping[str, Any],
) -> Gemini:
    secret_name = config.api_key_env or "GOOGLE_API_KEY"
    api_key = settings.get_secret(secret_name)
    if not api_key:
        raise LLMProviderNotConfiguredError(
            provider="google",
            secret_name=secret_name,
        )
    
    # gemini-2.0-flash is the only one verified to work in Agno without 404
    model_id = "gemini-2.0-flash"
    
    return Gemini(id=model_id, api_key=api_key)


def _build_ollama_model(
    config: LLMModelConfig,
    overrides: Mapping[str, Any],
) -> Ollama:
    params: dict[str, Any] = {"id": config.model_id}
    if config.base_url:
        params["host"] = config.base_url

    # Ollama uses options for model parameters like temperature
    ollama_options = {}
    ollama_options.update(config.default_params)
    ollama_options.update(overrides)

    if ollama_options:
        params["options"] = ollama_options

    return Ollama(**params)


_PROVIDER_FACTORIES: dict[str, ProviderFactory] = {
    "openai": _build_openai_model,
    "google": _build_google_model,
    "ollama": _build_ollama_model,
}


def build_model(
    config: LLMModelConfig,
    overrides: Mapping[str, Any] | None = None,
) -> Any:
    """Create a provider-specific model instance based on configuration."""

    factory = _PROVIDER_FACTORIES.get(config.provider)
    if factory is None:
        raise LLMProviderUnsupportedError(provider=config.provider)
    return factory(config, overrides or {})
