"""Phase 8 — frontend-backend interface contract (schemas, manifest, validation)."""

from .manifest import CONTRACT_VERSION, build_contract_manifest
from .models import ApiRecommendationsRequest
from .validate import validate_api_request, validate_api_response

__all__ = [
    "CONTRACT_VERSION",
    "ApiRecommendationsRequest",
    "build_contract_manifest",
    "validate_api_request",
    "validate_api_response",
]
