"""Phase 4 recommendation service with Groq provider and fallback."""

from __future__ import annotations

import logging

from src.config import settings
from src.llm.phase4.client import GroqClientError, call_groq_chat_completion
from src.llm.phase4.parser import LlmParseError, parse_recommendation_response
from src.llm.phase4.prompt import build_prompt_messages
from src.models import RecommendationItem, RecommendationResult, Restaurant, UserPreferences

logger = logging.getLogger(__name__)


def generate_recommendations(
    preferences: UserPreferences,
    shortlist: list[Restaurant],
) -> RecommendationResult:
    """
    Rank shortlist and generate explanations.

    Supported providers:
    - mock (deterministic local)
    - groq (real API)
    """
    if not shortlist:
        logger.warning("Empty shortlist — skipping LLM call")
        return RecommendationResult(
            summary="No restaurants matched your filters.",
            recommendations=[],
            filter_match_count=0,
        )

    if settings.llm_provider == "mock":
        logger.info("Using mock LLM provider")
        return _mock_recommendations(shortlist, preferences)

    if settings.llm_provider == "groq":
        return _groq_recommendations(shortlist, preferences)

    settings.require_llm_api_key()
    raise NotImplementedError(
        f"LLM provider {settings.llm_provider!r} is not implemented yet (Phase 4)."
    )


def _groq_recommendations(
    shortlist: list[Restaurant],
    preferences: UserPreferences,
) -> RecommendationResult:
    api_key = settings.require_llm_api_key()
    messages = build_prompt_messages(preferences, shortlist)
    try:
        raw_text = call_groq_chat_completion(
            api_key=api_key,
            model=settings.llm_model,
            messages=messages,
            temperature=0.3,
            timeout_seconds=40,
        )
        parsed = parse_recommendation_response(raw_text, shortlist)
        parsed.filter_match_count = len(shortlist)
        return parsed
    except (GroqClientError, LlmParseError, RuntimeError) as exc:
        logger.warning("Groq call failed (%s); returning fallback ranking", exc)
        return _fallback_recommendations(shortlist, preferences)


def _mock_recommendations(
    shortlist: list[Restaurant],
    preferences: UserPreferences,
) -> RecommendationResult:
    items: list[RecommendationItem] = []
    for rank, restaurant in enumerate(shortlist, start=1):
        items.append(
            RecommendationItem(
                rank=rank,
                restaurant_id=restaurant.id,
                name=restaurant.name,
                explanation=(
                    f"[Mock] {restaurant.name} matches your request for "
                    f"{preferences.cuisine} in {preferences.location} "
                    f"within a {preferences.budget} budget."
                ),
                cuisines=restaurant.cuisines,
                rating=restaurant.rating,
                average_cost=restaurant.average_cost,
                cost_band=restaurant.cost_band,
            )
        )

    return RecommendationResult(
        summary=(
            f"[Mock] Top {len(items)} pick(s) for {preferences.cuisine} "
            f"in {preferences.location}."
        ),
        recommendations=items,
        used_llm_fallback=False,
        filter_match_count=len(shortlist),
    )


def _fallback_recommendations(
    shortlist: list[Restaurant],
    preferences: UserPreferences,
) -> RecommendationResult:
    items: list[RecommendationItem] = []
    for rank, restaurant in enumerate(shortlist, start=1):
        items.append(
            RecommendationItem(
                rank=rank,
                restaurant_id=restaurant.id,
                name=restaurant.name,
                explanation=(
                    f"{restaurant.name} aligns with your {preferences.cuisine} preference "
                    f"in {preferences.location} and fits a {preferences.budget} budget."
                ),
                cuisines=restaurant.cuisines,
                rating=restaurant.rating,
                average_cost=restaurant.average_cost,
                cost_band=restaurant.cost_band,
            )
        )

    return RecommendationResult(
        summary="AI response unavailable. Showing deterministic shortlist ranking.",
        recommendations=items,
        used_llm_fallback=True,
        filter_match_count=len(shortlist),
    )

