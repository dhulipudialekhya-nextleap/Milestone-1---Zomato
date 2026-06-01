"""CLI entry point for the Phase 6/7 backend API server."""

from __future__ import annotations

import uvicorn

from src.config import setup_logging

setup_logging()


def main() -> None:
    uvicorn.run(
        "src.backend.phase6.server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )


if __name__ == "__main__":
    main()
