"""Configuration from the environment or a .env file, and the model it selects."""

from pydantic import SecretStr
from pydantic_ai.models import Model
from pydantic_ai.models.openrouter import OpenRouterModel, OpenRouterModelSettings
from pydantic_ai.providers.openrouter import OpenRouterProvider
from pydantic_settings import BaseSettings, SettingsConfigDict

from cvxpert.errors import ConfigurationError

DEFAULT_MODEL = "deepseek/deepseek-v4.1-flash"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openrouter_api_key: SecretStr = SecretStr("")
    cvxpert_model: str = DEFAULT_MODEL


def get_model() -> Model:
    """The OpenRouter model for every Step; fails fast when the API key is missing.

    Callers look this up as ``config.get_model`` so tests can swap in a fake model.
    """
    settings = Settings()
    key = settings.openrouter_api_key.get_secret_value()
    if not key:
        raise ConfigurationError(
            "OPENROUTER_API_KEY is not set; set it in the environment or a .env file"
        )
    return OpenRouterModel(
        settings.cvxpert_model or DEFAULT_MODEL,
        provider=OpenRouterProvider(api_key=key),
        settings=OpenRouterModelSettings(
            openrouter_provider={"require_parameters": True}
        ),
    )
