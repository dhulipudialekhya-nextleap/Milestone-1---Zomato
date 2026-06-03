"""CORS configuration for local dev and production (Vercel + Railway)."""

from __future__ import annotations

import os
import re

# Vercel production and preview deployments
_VERCEL_ORIGIN_REGEX = r"https://.*\.vercel\.app"

_DEFAULT_ORIGINS = "http://localhost:3000,http://127.0.0.1:3000"


def get_cors_settings() -> tuple[list[str], str | None]:
    """
    Return (allow_origins, allow_origin_regex) for FastAPI CORSMiddleware.

    Set CORS_ORIGINS to a comma-separated list of exact origins (no trailing slashes).
    Example: https://my-app.vercel.app,http://localhost:3000
    """
    raw = os.getenv("CORS_ORIGINS", _DEFAULT_ORIGINS)
    origins = [origin.strip() for origin in raw.split(",") if origin.strip()]

    regex = os.getenv("CORS_ORIGIN_REGEX", _VERCEL_ORIGIN_REGEX).strip() or None
    if regex and not _is_valid_origin_regex(regex):
        regex = _VERCEL_ORIGIN_REGEX

    return origins, regex


def _is_valid_origin_regex(pattern: str) -> bool:
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False
