"""FastAPI HTTP bridge for Phase 6 backend (consumed by Phase 7 Next.js frontend)."""

from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.backend.phase6.contracts import BackendRequest, BackendResponse
from src.backend.phase6.service import run_backend_request
from src.backend.phase8 import ApiRecommendationsRequest, build_contract_manifest
from src.config import setup_logging

setup_logging()

app = FastAPI(
    title="Zomato AI Recommendations API",
    version="1.0.0",
    description="Backend API for the Phase 7 Next.js frontend (Phase 8 contract at GET /api/contract).",
)

_default_origins = "http://localhost:3000,http://127.0.0.1:3000"
_cors_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", _default_origins).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/contract")
def api_contract() -> dict:
    """Phase 8 — machine-readable request/response contract for the frontend."""
    return build_contract_manifest()


@app.post("/api/recommendations", response_model=BackendResponse)
def create_recommendations(payload: ApiRecommendationsRequest) -> BackendResponse:
    return run_backend_request(
        BackendRequest(
            location=payload.location,
            budget=payload.budget,
            cuisine=payload.cuisine,
            min_rating=payload.min_rating,
            extras=payload.extras,
        ),
        use_mock_data=payload.use_mock_data,
    )
