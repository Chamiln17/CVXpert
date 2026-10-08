"""Test configuration: no test may reach a real model."""

import pydantic_ai.models
import pytest

from cvxpert import config

pydantic_ai.models.ALLOW_MODEL_REQUESTS = False


@pytest.fixture(autouse=True)
def _isolated_env(monkeypatch, tmp_path):
    """Keep a developer's real key, model choice or .env out of every test."""
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("CVXPERT_MODEL", raising=False)
    monkeypatch.chdir(tmp_path)


@pytest.fixture
def use_model(monkeypatch):
    """Make every Step use the given fake model (the key check is skipped with it)."""

    def install(model):
        monkeypatch.setattr(config, "get_model", lambda: model)
        return model

    return install
