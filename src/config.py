"""Central configuration loaded from environment variables."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv

# Project root (parent of src/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load .env from project root if present
load_dotenv(PROJECT_ROOT / ".env")

BudgetBand = Literal["low", "medium", "high"]
LlmProvider = Literal["mock", "groq", "openai", "gemini", "ollama"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

VALID_LLM_PROVIDERS: tuple[LlmProvider, ...] = ("mock", "groq", "openai", "gemini", "ollama")
VALID_LOG_LEVELS: tuple[LogLevel, ...] = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


class ConfigError(ValueError):
    """Raised when configuration is invalid or incomplete."""


@dataclass(frozen=True)
class Settings:
    """Immutable application settings."""

    schema_version: int
    log_level: LogLevel
    processed_data_path: Path
    dataset_source: str
    shortlist_size: int
    display_top_k: int
    llm_provider: LlmProvider
    llm_api_key: str | None
    llm_model: str
    budget_low_max: int
    budget_medium_max: int

    @property
    def project_root(self) -> Path:
        return PROJECT_ROOT

    def resolve_path(self, path: Path) -> Path:
        """Resolve relative paths against project root."""
        if path.is_absolute():
            return path
        return self.project_root / path

    def require_llm_api_key(self) -> str:
        """Return API key or raise if a real provider is configured without one."""
        if self.llm_provider == "mock":
            return ""
        if not self.llm_api_key:
            raise ConfigError(
                f"LLM_API_KEY is required when LLM_PROVIDER={self.llm_provider!r}. "
                "Set it in .env or use LLM_PROVIDER=mock."
            )
        return self.llm_api_key


def _get_env(key: str, default: str | None = None) -> str | None:
    value = os.getenv(key, default)
    if value is not None:
        value = value.strip()
    return value if value else default


def _parse_int(name: str, raw: str | None, default: int, *, minimum: int | None = None) -> int:
    if raw is None:
        value = default
    else:
        try:
            value = int(raw)
        except ValueError as exc:
            raise ConfigError(f"{name} must be an integer, got {raw!r}") from exc
    if minimum is not None and value < minimum:
        raise ConfigError(f"{name} must be >= {minimum}, got {value}")
    return value


def _parse_log_level(raw: str | None) -> LogLevel:
    level = (raw or "INFO").upper()
    if level not in VALID_LOG_LEVELS:
        raise ConfigError(f"LOG_LEVEL must be one of {VALID_LOG_LEVELS}, got {raw!r}")
    return level  # type: ignore[return-value]


def _parse_llm_provider(raw: str | None) -> LlmProvider:
    provider = (raw or "mock").lower()
    if provider not in VALID_LLM_PROVIDERS:
        raise ConfigError(f"LLM_PROVIDER must be one of {VALID_LLM_PROVIDERS}, got {raw!r}")
    return provider  # type: ignore[return-value]


def load_settings() -> Settings:
    """Load and validate settings from the environment."""
    budget_low = _parse_int("BUDGET_LOW_MAX", _get_env("BUDGET_LOW_MAX"), 300, minimum=1)
    budget_medium = _parse_int(
        "BUDGET_MEDIUM_MAX", _get_env("BUDGET_MEDIUM_MAX"), 700, minimum=budget_low + 1
    )

    shortlist_size = _parse_int(
        "SHORTLIST_SIZE", _get_env("SHORTLIST_SIZE"), 15, minimum=1
    )
    display_top_k = _parse_int(
        "DISPLAY_TOP_K", _get_env("DISPLAY_TOP_K"), 5, minimum=1
    )
    if display_top_k > shortlist_size:
        logging.getLogger(__name__).warning(
            "DISPLAY_TOP_K (%s) exceeds SHORTLIST_SIZE (%s); clamping to shortlist size",
            display_top_k,
            shortlist_size,
        )
        display_top_k = shortlist_size

    processed_path = Path(_get_env("PROCESSED_DATA_PATH", "data/processed/restaurants.csv") or "")
    default_dataset = (
        "https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation"
    )
    dataset_source = _get_env("DATASET_SOURCE", default_dataset) or default_dataset

    return Settings(
        schema_version=_parse_int("SCHEMA_VERSION", _get_env("SCHEMA_VERSION"), 1, minimum=1),
        log_level=_parse_log_level(_get_env("LOG_LEVEL")),
        processed_data_path=processed_path,
        dataset_source=dataset_source,
        shortlist_size=shortlist_size,
        display_top_k=display_top_k,
        llm_provider=_parse_llm_provider(_get_env("LLM_PROVIDER")),
        llm_api_key=_get_env("LLM_API_KEY"),
        llm_model=_get_env("LLM_MODEL", "gpt-4o-mini") or "gpt-4o-mini",
        budget_low_max=budget_low,
        budget_medium_max=budget_medium,
    )


def setup_logging(level: LogLevel | None = None) -> None:
    """Configure root logger for the application."""
    settings = load_settings()
    log_level = level or settings.log_level
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
    )


# Singleton loaded on first import of settings
settings: Settings = load_settings()
