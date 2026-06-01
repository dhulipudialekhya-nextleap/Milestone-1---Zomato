"""Compatibility wrapper for Phase 3 filter engine."""

from __future__ import annotations

from src.models import Restaurant, UserPreferences
from src.filters.phase3.engine import (
    build_shortlist as _build_shortlist,
    filter_restaurants as _filter_restaurants,
)

def filter_restaurants(
    restaurants: list[Restaurant],
    preferences: UserPreferences,
) -> list[Restaurant]:
    """Compatibility helper returning filtered rows only."""
    filtered, _counts = _filter_restaurants(restaurants, preferences)
    return filtered


def build_shortlist(
    restaurants: list[Restaurant],
    preferences: UserPreferences,
) -> list[Restaurant]:
    """Compatibility helper delegating to Phase 3 engine."""
    return _build_shortlist(restaurants, preferences)
