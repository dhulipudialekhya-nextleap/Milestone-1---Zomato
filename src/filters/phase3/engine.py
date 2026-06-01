"""Phase 3 filter engine, ranker, and shortlist builder."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from src.config import settings
from src.models import Restaurant, UserPreferences

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class FilterStageCounts:
    """Track record counts after each deterministic filter stage."""

    total: int
    after_location: int
    after_cuisine: int
    after_rating: int
    after_budget: int


@dataclass(frozen=True)
class Phase3SelectionResult:
    """Output bundle from Phase 3 candidate selection."""

    shortlist: list[Restaurant]
    counts: FilterStageCounts


def _matches_location(restaurant: Restaurant, location: str) -> bool:
    return location.lower() in restaurant.location.lower()


def _matches_cuisine(restaurant: Restaurant, cuisine: str) -> bool:
    needle = cuisine.lower()
    return any(needle in c.lower() for c in restaurant.cuisines)


def _matches_rating(restaurant: Restaurant, min_rating: float) -> bool:
    return restaurant.rating >= min_rating


def _matches_budget(restaurant: Restaurant, budget: str) -> bool:
    # If cost band is unknown, exclude for strict budget filtering.
    if restaurant.cost_band is None:
        return False
    return restaurant.cost_band == budget


def _votes_for_ranking(restaurant: Restaurant) -> int:
    votes = restaurant.metadata.get("votes", 0)
    try:
        return int(votes)
    except (TypeError, ValueError):
        return 0


def filter_restaurants(
    restaurants: list[Restaurant],
    preferences: UserPreferences,
) -> tuple[list[Restaurant], FilterStageCounts]:
    """Apply deterministic filters (location → cuisine → rating → budget)."""
    location_filtered = [r for r in restaurants if _matches_location(r, preferences.location)]
    cuisine_filtered = [r for r in location_filtered if _matches_cuisine(r, preferences.cuisine)]
    rating_filtered = [r for r in cuisine_filtered if _matches_rating(r, preferences.min_rating)]
    budget_filtered = [r for r in rating_filtered if _matches_budget(r, preferences.budget)]

    counts = FilterStageCounts(
        total=len(restaurants),
        after_location=len(location_filtered),
        after_cuisine=len(cuisine_filtered),
        after_rating=len(rating_filtered),
        after_budget=len(budget_filtered),
    )
    logger.info(
        "Phase3 counts total=%d location=%d cuisine=%d rating=%d budget=%d",
        counts.total,
        counts.after_location,
        counts.after_cuisine,
        counts.after_rating,
        counts.after_budget,
    )
    return budget_filtered, counts


def _rank_restaurants(restaurants: list[Restaurant]) -> list[Restaurant]:
    """
    Pre-LLM deterministic ranking.

    Order by:
    1) rating desc
    2) votes desc (from metadata)
    3) name asc (stable tie-break)
    """
    return sorted(
        restaurants,
        key=lambda r: (-r.rating, -_votes_for_ranking(r), r.name.lower()),
    )


def build_shortlist_with_metadata(
    restaurants: list[Restaurant],
    preferences: UserPreferences,
) -> Phase3SelectionResult:
    """Filter, rank, and cap at SHORTLIST_SIZE while returning metadata counts."""
    filtered, counts = filter_restaurants(restaurants, preferences)
    ranked = _rank_restaurants(filtered)
    shortlist = ranked[: settings.shortlist_size]
    logger.info("Phase3 shortlist size=%d max=%d", len(shortlist), settings.shortlist_size)
    return Phase3SelectionResult(shortlist=shortlist, counts=counts)


def build_shortlist(
    restaurants: list[Restaurant],
    preferences: UserPreferences,
) -> list[Restaurant]:
    """Compatibility helper returning only shortlist rows."""
    return build_shortlist_with_metadata(restaurants, preferences).shortlist

