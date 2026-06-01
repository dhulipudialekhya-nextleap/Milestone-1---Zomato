"""End-to-end skeleton pipeline tests (Phase 0)."""

import pytest

from src.app import execute_pipeline, run_pipeline
from src.data import load_mock_restaurants
from src.filters import build_shortlist
from src.llm import generate_recommendations
from src.models import UserPreferences


@pytest.fixture
def sample_preferences() -> UserPreferences:
    return UserPreferences(
        location="Bangalore",
        budget="medium",
        cuisine="Italian",
        min_rating=4.0,
    )


def test_mock_data_loads() -> None:
    restaurants = load_mock_restaurants()
    assert len(restaurants) >= 1
    assert restaurants[0].name


def test_filter_produces_shortlist(sample_preferences: UserPreferences) -> None:
    restaurants = load_mock_restaurants()
    shortlist = build_shortlist(restaurants, sample_preferences)
    assert len(shortlist) >= 1
    assert all("Italian" in " ".join(r.cuisines) for r in shortlist)


def test_empty_shortlist_skips_llm_content() -> None:
    prefs = UserPreferences(
        location="NonexistentCity",
        budget="low",
        cuisine="Italian",
        min_rating=5.0,
    )
    shortlist = build_shortlist(load_mock_restaurants(), prefs)
    assert shortlist == []
    result = generate_recommendations(prefs, shortlist)
    assert result.recommendations == []


def test_mock_llm_returns_ranked_items(sample_preferences: UserPreferences) -> None:
    shortlist = build_shortlist(load_mock_restaurants(), sample_preferences)
    result = generate_recommendations(sample_preferences, shortlist)
    assert len(result.recommendations) >= 1
    assert result.recommendations[0].rank == 1
    assert "[Mock]" in result.recommendations[0].explanation


def test_execute_pipeline_returns_result(sample_preferences: UserPreferences) -> None:
    result = execute_pipeline(sample_preferences, use_mock_data=True)
    assert len(result.recommendations) >= 1


def test_run_pipeline_no_crash(sample_preferences: UserPreferences, capsys: pytest.CaptureFixture[str]) -> None:
    run_pipeline(sample_preferences, use_mock_data=True)
    captured = capsys.readouterr()
    assert "Restaurant Recommendations" in captured.out

