"""Phase 2 service layer: normalize and validate user preferences."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pydantic import ValidationError

from src.models import UserPreferences
from src.models.preferences import VALID_BUDGETS


@dataclass(frozen=True)
class FormDefaults:
    """Default form values for input collection."""

    location: str = "Bangalore"
    budget: str = "medium"
    cuisine: str = "Italian"
    min_rating: float = 4.0
    extras: str = ""


DEFAULT_FORM_VALUES = FormDefaults()


class InputValidationError(ValueError):
    """Raised when user input cannot be converted to valid preferences."""


def build_user_preferences(
    *,
    location: str,
    budget: str,
    cuisine: str,
    min_rating: float | int | str,
    extras: str | None = None,
) -> UserPreferences:
    """
    Build validated `UserPreferences` from UI/CLI inputs.

    This centralizes Phase 2 validation so both Streamlit and CLI use the same rules.
    """
    payload = {
        "location": _normalize_required_text(location, field_name="location"),
        "budget": _normalize_budget(budget),
        "cuisine": _normalize_required_text(cuisine, field_name="cuisine"),
        "min_rating": _normalize_min_rating(min_rating),
        "extras": _normalize_optional_text(extras),
    }

    try:
        return UserPreferences(**payload)
    except ValidationError as exc:
        raise InputValidationError(_pydantic_error_to_message(exc)) from exc


def _normalize_required_text(value: str, *, field_name: str) -> str:
    text = str(value).strip()
    if not text:
        raise InputValidationError(f"{field_name} is required.")
    if len(text) > 100:
        raise InputValidationError(f"{field_name} must be 100 characters or fewer.")
    return text


def _normalize_optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if len(text) > 500:
        return text[:500]
    return text


def _normalize_budget(value: str) -> str:
    budget = str(value).strip().lower()
    if budget not in VALID_BUDGETS:
        allowed = ", ".join(VALID_BUDGETS)
        raise InputValidationError(f"budget must be one of: {allowed}.")
    return budget


def _normalize_min_rating(value: float | int | str) -> float:
    try:
        rating = float(value)
    except (TypeError, ValueError) as exc:
        raise InputValidationError("min_rating must be a number between 0 and 5.") from exc
    if rating < 0 or rating > 5:
        raise InputValidationError("min_rating must be between 0 and 5.")
    return round(rating, 1)


def _pydantic_error_to_message(exc: ValidationError) -> str:
    errors = exc.errors()
    if not errors:
        return "Invalid input."
    first = errors[0]
    location = ".".join(str(part) for part in first.get("loc", []))
    message = first.get("msg", "invalid value")
    return f"{location}: {message}" if location else str(message)

