"""Phase 6 backend service boundary and orchestration."""

from __future__ import annotations

import logging
from typing import Any

from src.config import ConfigError, settings
from src.data import load_restaurants
from src.filters import build_shortlist_with_metadata
from src.input.phase2 import InputValidationError, build_user_preferences
from src.llm import generate_recommendations
from src.models import RecommendationResult, UserPreferences

from src.backend.phase8.models import ApiRecommendationsRequest

from .contracts import BackendErrorResponse, BackendRequest, BackendResponse, BackendSuccessResponse

logger = logging.getLogger(__name__)


def execute_backend_pipeline(
    preferences: UserPreferences,
    *,
    use_mock_data: bool = False,
) -> RecommendationResult:
    """Run backend pipeline independent from UI layer."""
    logger.info("Starting backend pipeline (provider=%s)", settings.llm_provider)

    restaurants = load_restaurants(use_mock=use_mock_data)
    logger.info("Loaded %d restaurant(s)", len(restaurants))

    selection = build_shortlist_with_metadata(restaurants, preferences)
    shortlist = selection.shortlist
    if not shortlist:
        logger.warning("Empty shortlist - skipping LLM (E3.1)")
        result = generate_recommendations(preferences, [])
        result.filter_match_count = selection.counts.after_budget
        return result

    result = generate_recommendations(preferences, shortlist)
    result.filter_match_count = selection.counts.after_budget
    logger.info("Backend pipeline completed successfully")
    return result


def run_backend_request(
    payload: dict[str, Any] | BackendRequest,
    *,
    use_mock_data: bool = False,
) -> BackendResponse:
    """
    Backend boundary function:
    - accepts normalized request payload
    - returns deterministic success/error response shapes
    """
    mock_flag = use_mock_data
    try:
        if isinstance(payload, BackendRequest):
            req = payload
        elif isinstance(payload, ApiRecommendationsRequest):
            api_req = payload
            req = BackendRequest(
                location=api_req.location,
                budget=api_req.budget,
                cuisine=api_req.cuisine,
                min_rating=api_req.min_rating,
                extras=api_req.extras,
            )
            mock_flag = mock_flag or api_req.use_mock_data
        else:
            api_req = ApiRecommendationsRequest.model_validate(payload)
            req = BackendRequest(
                location=api_req.location,
                budget=api_req.budget,
                cuisine=api_req.cuisine,
                min_rating=api_req.min_rating,
                extras=api_req.extras,
            )
            mock_flag = mock_flag or api_req.use_mock_data
        preferences = build_user_preferences(
            location=req.location,
            budget=req.budget,
            cuisine=req.cuisine,
            min_rating=req.min_rating,
            extras=req.extras,
        )
    except (InputValidationError, ValueError) as exc:
        return BackendErrorResponse(error_code="validation_error", message=str(exc))

    try:
        result = execute_backend_pipeline(preferences, use_mock_data=mock_flag)
        return BackendSuccessResponse(result=result)
    except ConfigError as exc:
        return BackendErrorResponse(error_code="config_error", message=str(exc))
    except Exception as exc:  # noqa: BLE001
        logger.exception("Backend runtime failure")
        return BackendErrorResponse(error_code="runtime_error", message=str(exc))

