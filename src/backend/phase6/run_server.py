"""CLI entry point for the Phase 6/7 backend API server."""

from __future__ import annotations

import os

import uvicorn

from src.config import setup_logging

setup_logging()


def main() -> None:
    """Run uvicorn; on Railway, bind to $PORT (see Docs/deployment-railway-vercel.md)."""
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "src.backend.phase6.server:app",
        host="0.0.0.0",
        port=port,
        reload=False,
    )


if __name__ == "__main__":
    main()
