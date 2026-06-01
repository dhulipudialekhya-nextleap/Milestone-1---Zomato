"""Tests for Phase 2 input collection and validation service."""

import pytest

from src.input.phase2 import InputValidationError, build_user_preferences


def test_build_user_preferences_valid_payload() -> None:
    prefs = build_user_preferences(
        location=" Bangalore ",
        budget="MEDIUM",
        cuisine=" Italian ",
        min_rating="4.0",
        extras=" family-friendly ",
    )
    assert prefs.location == "Bangalore"
    assert prefs.budget == "medium"
    assert prefs.cuisine == "Italian"
    assert prefs.min_rating == 4.0
    assert prefs.extras == "family-friendly"


def test_build_user_preferences_rejects_empty_location() -> None:
    with pytest.raises(InputValidationError, match="location is required"):
        build_user_preferences(
            location=" ",
            budget="medium",
            cuisine="Italian",
            min_rating=3.5,
        )


def test_build_user_preferences_rejects_invalid_budget() -> None:
    with pytest.raises(InputValidationError, match="budget must be one of"):
        build_user_preferences(
            location="Delhi",
            budget="cheap",
            cuisine="Italian",
            min_rating=3.5,
        )


def test_build_user_preferences_rejects_invalid_rating() -> None:
    with pytest.raises(InputValidationError, match="between 0 and 5"):
        build_user_preferences(
            location="Delhi",
            budget="low",
            cuisine="Chinese",
            min_rating=8,
        )

