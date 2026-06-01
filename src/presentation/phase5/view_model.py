"""Phase 5 view-model builders for UI and console renderers."""

from __future__ import annotations

from dataclasses import dataclass

from src.config import settings
from src.models import RecommendationResult


@dataclass(frozen=True)
class PresentableRecommendation:
    """Normalized recommendation item ready for rendering."""

    rank: int
    name: str
    cuisines_text: str
    rating_text: str
    estimated_cost_text: str
    explanation: str


@dataclass(frozen=True)
class Phase5ViewModel:
    """Top-level representation for Phase 5 rendering."""

    title: str
    summary: str | None
    show_fallback_banner: bool
    empty_message: str | None
    filter_match_count: int
    items: list[PresentableRecommendation]


def build_phase5_view_model(
    result: RecommendationResult,
    *,
    top_k: int | None = None,
) -> Phase5ViewModel:
    """Create a renderer-friendly view model from recommendation result."""
    limit = top_k if top_k is not None else settings.display_top_k
    rows = result.recommendations[:limit]

    items = [
        PresentableRecommendation(
            rank=item.rank,
            name=item.name,
            cuisines_text=", ".join(item.cuisines) if item.cuisines else "N/A",
            rating_text=f"{item.rating:.1f}" if item.rating is not None else "N/A",
            estimated_cost_text=_format_cost(item.average_cost, item.cost_band),
            explanation=item.explanation,
        )
        for item in rows
    ]

    empty_message = None
    if not items:
        empty_message = "No recommendations to display."

    return Phase5ViewModel(
        title="Restaurant Recommendations",
        summary=result.summary,
        show_fallback_banner=result.used_llm_fallback,
        empty_message=empty_message,
        filter_match_count=result.filter_match_count,
        items=items,
    )


def _format_cost(average_cost: int | None, cost_band: str | None) -> str:
    if average_cost is not None:
        return f"₹{average_cost} for two"
    if cost_band:
        return f"{cost_band} budget"
    return "N/A"

