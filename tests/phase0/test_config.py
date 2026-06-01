"""Tests for configuration loading and validation."""

import pytest

from src.config import ConfigError, load_settings


def test_load_settings_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    monkeypatch.delenv("SHORTLIST_SIZE", raising=False)
    monkeypatch.delenv("DISPLAY_TOP_K", raising=False)
    settings = load_settings()
    assert settings.shortlist_size == 15
    assert settings.display_top_k == 5
    assert settings.llm_provider == "mock"


def test_invalid_shortlist_size(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SHORTLIST_SIZE", "-1")
    with pytest.raises(ConfigError, match="SHORTLIST_SIZE"):
        load_settings()


def test_display_top_k_exceeds_shortlist(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SHORTLIST_SIZE", "5")
    monkeypatch.setenv("DISPLAY_TOP_K", "10")
    with pytest.raises(ConfigError, match="DISPLAY_TOP_K"):
        load_settings()


def test_require_llm_api_key_for_openai(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    settings = load_settings()
    with pytest.raises(ConfigError, match="LLM_API_KEY"):
        settings.require_llm_api_key()

