"""Tests for Phase 3 candidate selection layer."""

from __future__ import annotations

import json

from src.filters import build_shortlist_with_metadata, serialize_shortlist_payload
from src.models import Restaurant, UserPreferences


def _sample_restaurants() -> list[Restaurant]:
    return [
        Restaurant(
            id="r1",
            name="Alpha",
            location="Bangalore",
            cuisines=["Italian", "Continental"],
            average_cost=600,
            cost_band="medium",
            rating=4.5,
            metadata={"votes": 10},
        ),
        Restaurant(
            id="r2",
            name="Bravo",
            location="Bangalore",
            cuisines=["Italian"],
            average_cost=550,
            cost_band="medium",
            rating=4.5,
            metadata={"votes": 50},
        ),
        Restaurant(
            id="r3",
            name="Charlie",
            location="Bangalore",
            cuisines=["Chinese"],
            average_cost=300,
            cost_band="low",
            rating=4.8,
            metadata={"votes": 999},
        ),
        Restaurant(
            id="r4",
            name="Delta",
            location="Delhi",
            cuisines=["Italian"],
            average_cost=700,
            cost_band="medium",
            rating=4.9,
            metadata={"votes": 100},
        ),
    ]


def test_phase3_filter_chain_and_counts() -> None:
    preferences = UserPreferences(
        location="Bangalore",
        budget="medium",
        cuisine="Italian",
        min_rating=4.0,
    )
    result = build_shortlist_with_metadata(_sample_restaurants(), preferences)
    assert result.counts.total == 4
    assert result.counts.after_location == 3
    assert result.counts.after_cuisine == 2
    assert result.counts.after_rating == 2
    assert result.counts.after_budget == 2
    assert len(result.shortlist) == 2


def test_phase3_ranking_uses_votes_tiebreak() -> None:
    preferences = UserPreferences(
        location="Bangalore",
        budget="medium",
        cuisine="Italian",
        min_rating=0.0,
    )
    result = build_shortlist_with_metadata(_sample_restaurants(), preferences)
    assert result.shortlist[0].id == "r2"
    assert result.shortlist[1].id == "r1"


def test_phase3_payload_serializer_contract() -> None:
    preferences = UserPreferences(
        location="Bangalore",
        budget="medium",
        cuisine="Italian",
        min_rating=4.0,
        extras="family-friendly",
    )
    result = build_shortlist_with_metadata(_sample_restaurants(), preferences)
    payload = serialize_shortlist_payload(preferences, result.shortlist)
    parsed = json.loads(payload)
    assert parsed["preferences"]["location"] == "Bangalore"
    assert len(parsed["candidates"]) == 2
    assert parsed["candidates"][0]["id"] in {"r1", "r2"}

