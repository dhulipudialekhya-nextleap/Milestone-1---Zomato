"""Phase 6 backend architecture consolidation."""

from src.backend.phase6.contracts import (
    BackendErrorResponse,
    BackendRequest,
    BackendResponse,
    BackendSuccessResponse,
)
from src.backend.phase6.service import execute_backend_pipeline, run_backend_request

__all__ = [
    "BackendErrorResponse",
    "BackendRequest",
    "BackendResponse",
    "BackendSuccessResponse",
    "execute_backend_pipeline",
    "run_backend_request",
]
