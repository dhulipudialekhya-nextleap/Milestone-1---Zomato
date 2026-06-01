"""HTTP API models for Phase 8 contract (extends Phase 6 backend request)."""

from __future__ import annotations

from pydantic import Field

from src.backend.phase6.contracts import BackendRequest


class ApiRecommendationsRequest(BackendRequest):
    """POST /api/recommendations body — preferences plus optional dev toggle."""

    use_mock_data: bool = Field(
        default=False,
        description="When true, use in-memory mock restaurants instead of processed data.",
    )
