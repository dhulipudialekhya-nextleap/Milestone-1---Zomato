"""Runtime validation helpers for Phase 8 contract compatibility."""

from __future__ import annotations

from typing import Any

from pydantic import TypeAdapter, ValidationError

from src.backend.phase6.contracts import BackendResponse
from src.backend.phase8.models import ApiRecommendationsRequest

_request_adapter = ApiRecommendationsRequest
_response_adapter = TypeAdapter(BackendResponse)


def validate_api_request(payload: dict[str, Any]) -> ApiRecommendationsRequest:
    """Parse and validate an API request body; raises ValidationError on failure."""
    return _request_adapter.model_validate(payload)


def validate_api_response(payload: dict[str, Any]) -> BackendResponse:
    """Parse and validate an API response body; raises ValidationError on failure."""
    return _response_adapter.validate_python(payload)
