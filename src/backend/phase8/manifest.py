"""Contract manifest and JSON Schema export for Phase 8."""

from __future__ import annotations

from typing import Any

from pydantic import TypeAdapter

from src.backend.phase6.contracts import BackendErrorResponse, BackendResponse, BackendSuccessResponse
from src.backend.phase8.models import ApiRecommendationsRequest

CONTRACT_VERSION = "1.0.0"

_ERROR_CODES = ("validation_error", "config_error", "runtime_error")


def _model_schema(model: type[Any]) -> dict[str, Any]:
    return model.model_json_schema(mode="serialization")


def build_contract_manifest() -> dict[str, Any]:
    """Machine-readable contract document served at GET /api/contract."""
    response_adapter = TypeAdapter(BackendResponse)
    return {
        "version": CONTRACT_VERSION,
        "endpoints": {
            "health": {"method": "GET", "path": "/health"},
            "recommendations": {
                "method": "POST",
                "path": "/api/recommendations",
                "request_content_type": "application/json",
                "response_content_type": "application/json",
                "success_http_status": 200,
                "error_http_status": 200,
                "notes": (
                    "Business errors return HTTP 200 with ok=false. "
                    "Transport failures use non-2xx status."
                ),
            },
            "contract": {"method": "GET", "path": "/api/contract"},
        },
        "request": {
            "description": "Normalized preference payload sent by the frontend.",
            "schema": _model_schema(ApiRecommendationsRequest),
            "required_fields": ["location", "budget", "cuisine"],
            "optional_fields": ["min_rating", "extras", "use_mock_data"],
        },
        "response": {
            "description": "Discriminated union on ok; shape is stable for success and error paths.",
            "schema": response_adapter.json_schema(mode="serialization"),
            "success": _model_schema(BackendSuccessResponse),
            "error": _model_schema(BackendErrorResponse),
        },
        "error_codes": list(_ERROR_CODES),
    }
