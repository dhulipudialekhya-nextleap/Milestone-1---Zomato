"""LLM recommendation output models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class RecommendationItem(BaseModel):
    """A single ranked recommendation with AI explanation."""

    rank: int = Field(ge=1)
    restaurant_id: str
    name: str
    explanation: str
    # Display fields merged from dataset in Phase 5
    cuisines: list[str] = Field(default_factory=list)
    rating: float | None = None
    average_cost: int | None = None
    cost_band: str | None = None


class RecommendationResult(BaseModel):
    """Full recommendation response from the pipeline."""

    summary: str | None = None
    recommendations: list[RecommendationItem] = Field(default_factory=list)
    used_llm_fallback: bool = False
    filter_match_count: int = 0
