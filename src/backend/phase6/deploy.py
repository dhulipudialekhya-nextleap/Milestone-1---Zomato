"""Railway / production deployment helpers for the FastAPI backend."""

from __future__ import annotations

import os


def is_railway_runtime() -> bool:
    """True when the app runs on Railway (RAILWAY_ENVIRONMENT is set)."""
    return bool(os.getenv("RAILWAY_ENVIRONMENT", "").strip())


def get_public_base_url() -> str | None:
    """Railway public domain if configured (for logs / health metadata)."""
    domain = os.getenv("RAILWAY_PUBLIC_DOMAIN", "").strip()
    if not domain:
        return None
    if domain.startswith("http://") or domain.startswith("https://"):
        return domain.rstrip("/")
    return f"https://{domain}"


def deployment_metadata() -> dict[str, str | bool | None]:
    """Non-secret deployment info for /health (Railway dashboard checks)."""
    return {
        "platform": "railway" if is_railway_runtime() else "local",
        "railway_environment": os.getenv("RAILWAY_ENVIRONMENT"),
        "public_url": get_public_base_url(),
        "llm_provider": os.getenv("LLM_PROVIDER", "mock"),
        "data_ingest_disabled": os.getenv("DISABLE_DATA_INGEST", "").lower() in (
            "1",
            "true",
            "yes",
        )
        or is_railway_runtime(),
    }
