"""Tests for Phase 6 backend boundary and contracts."""

from src.backend.phase6 import run_backend_request


def test_run_backend_request_success_with_mock_data() -> None:
    payload = {
        "location": "Bangalore",
        "budget": "medium",
        "cuisine": "Italian",
        "min_rating": 4.0,
    }
    response = run_backend_request(payload, use_mock_data=True)
    assert response.ok is True
    assert len(response.result.recommendations) >= 1


def test_run_backend_request_validation_error() -> None:
    payload = {
        "location": "",
        "budget": "medium",
        "cuisine": "Italian",
        "min_rating": 4.0,
    }
    response = run_backend_request(payload, use_mock_data=True)
    assert response.ok is False
    assert response.error_code == "validation_error"


def test_run_backend_request_schema_error() -> None:
    payload = {
        "location": "Bangalore",
        "budget": "invalid_budget",
        "cuisine": "Italian",
        "min_rating": 4.0,
    }
    response = run_backend_request(payload, use_mock_data=True)
    assert response.ok is False
    assert response.error_code == "validation_error"

