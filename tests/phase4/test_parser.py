"""Tests for Phase 4 parser and Groq fallback behavior."""

from __future__ import annotations

from src.llm.phase4.parser import parse_recommendation_response
from src.llm.phase4.service import generate_recommendations
from src.models import Restaurant, UserPreferences


def _shortlist() -> list[Restaurant]:
    return [
        Restaurant(
            id="r1",
            name="Alpha",
            location="Bangalore",
            cuisines=["Italian"],
            average_cost=500,
            cost_band="medium",
            rating=4.4,
            metadata={"votes": 21},
        ),
        Restaurant(
            id="r2",
            name="Bravo",
            location="Bangalore",
            cuisines=["Italian", "Continental"],
            average_cost=650,
            cost_band="medium",
            rating=4.6,
            metadata={"votes": 45},
        ),
    ]


def _prefs() -> UserPreferences:
    return UserPreferences(
        location="Bangalore",
        budget="medium",
        cuisine="Italian",
        min_rating=4.0,
        extras="family-friendly",
    )


def test_parser_accepts_valid_json_response() -> None:
    text = """
    {
      "summary": "Top fits in Bangalore",
      "recommendations": [
        {"rank": 1, "restaurant_id": "r2", "name": "Bravo", "explanation": "Best match"},
        {"rank": 2, "restaurant_id": "r1", "name": "Alpha", "explanation": "Great value"}
      ]
    }
    """
    result = parse_recommendation_response(text, _shortlist())
    assert len(result.recommendations) == 2
    assert result.recommendations[0].restaurant_id == "r2"
    assert result.summary == "Top fits in Bangalore"


def test_parser_handles_markdown_fenced_json() -> None:
    text = """```json
    {"summary":"ok","recommendations":[{"rank":1,"restaurant_id":"r1","name":"Alpha","explanation":"Nice"}]}
    ```"""
    result = parse_recommendation_response(text, _shortlist())
    assert len(result.recommendations) == 1
    assert result.recommendations[0].restaurant_id == "r1"


def test_groq_failure_returns_fallback(monkeypatch) -> None:
    import src.llm.phase4.service as service

    class DummySettings:
        llm_provider = "groq"
        llm_model = "llama-3.1-8b-instant"

        @staticmethod
        def require_llm_api_key() -> str:
            return "test-key"

    monkeypatch.setattr(service, "settings", DummySettings())

    def fake_call(*args, **kwargs):
        raise RuntimeError("simulated failure")

    monkeypatch.setattr(service, "call_groq_chat_completion", fake_call)
    result = generate_recommendations(_prefs(), _shortlist())
    assert result.used_llm_fallback is True
    assert len(result.recommendations) == 2

