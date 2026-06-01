"""Phase 6 request/response contracts for backend boundary."""

from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, Field

from src.models import RecommendationResult
from src.models.preferences import BudgetBand


class BackendRequest(BaseModel):
    """Normalized request shape expected by backend service."""

    location: str
    budget: BudgetBand
    cuisine: str
    min_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    extras: str | None = None


class BackendSuccessResponse(BaseModel):
    """Successful backend response."""

    ok: Literal[True] = True
    result: RecommendationResult


class BackendErrorResponse(BaseModel):
    """User-safe backend error response."""

    ok: Literal[False] = False
    error_code: Literal["validation_error", "config_error", "runtime_error"]
    message: str


BackendResponse = Union[BackendSuccessResponse, BackendErrorResponse]

