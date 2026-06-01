"""Restaurant entity — canonical schema after preprocessing."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator

from src.models.preferences import BudgetBand


class Restaurant(BaseModel):
    """A restaurant record ready for filtering and ranking."""

    id: str
    name: str
    location: str
    cuisines: list[str]
    average_cost: int | None = None
    cost_band: BudgetBand | None = None
    rating: float = Field(ge=0.0, le=5.0)
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}

    @field_validator("name", "location")
    @classmethod
    def strip_required_strings(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("must not be empty")
        return stripped

    @field_validator("cuisines")
    @classmethod
    def normalize_cuisines(cls, cuisines: list[str]) -> list[str]:
        return [c.strip() for c in cuisines if c and c.strip()]
