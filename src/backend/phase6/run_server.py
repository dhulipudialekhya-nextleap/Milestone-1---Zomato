"""CLI entry point for the Phase 6/7 backend API server."""

from __future__ import annotations

import os

import uvicorn

from src.config import setup_logging

setup_logging()


def main() -> None:
    """Run uvicorn; on Railway, bind to $PORT (see Docs/deployment-railway-vercel.md)."""
    port_raw = os.getenv("PORT", "8000").strip()
    try:
        port = int(port_raw)
    except ValueError as exc:
        raise SystemExit(f"Invalid PORT environment variable: {port_raw!r}") from exc

    print(f"Starting API on 0.0.0.0:{port}", flush=True)
    uvicorn.run(
        "src.backend.phase6.server:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
    )


if __name__ == "__main__":
    main()
