"""User preference input model."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

BudgetBand = Literal["low", "medium", "high"]
VALID_BUDGETS: tuple[BudgetBand, ...] = ("low", "medium", "high")


class UserPreferences(BaseModel):
    """Validated user constraints for recommendation."""

    location: str
    budget: BudgetBand
    cuisine: str
    min_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    extras: str | None = None

    model_config = {"frozen": True}

    @field_validator("location", "cuisine")
    @classmethod
    def strip_and_require(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("must not be empty")
        return stripped

    @field_validator("budget", mode="before")
    @classmethod
    def normalize_budget(cls, value: str | BudgetBand) -> BudgetBand:
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized not in VALID_BUDGETS:
                raise ValueError(f"budget must be one of {VALID_BUDGETS}")
            return normalized  # type: ignore[return-value]
        return value

    @field_validator("extras")
    @classmethod
    def strip_extras(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None
