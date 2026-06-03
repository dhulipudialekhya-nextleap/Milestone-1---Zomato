"""Tests for Phase 6 FastAPI server consumed by Phase 7 frontend."""

from __future__ import annotations

from fastapi.testclient import TestClient

from src.backend.phase6.server import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["platform"] == "local"


def test_contract_endpoint() -> None:
    response = client.get("/api/contract")
    assert response.status_code == 200
    body = response.json()
    assert body["version"] == "1.0.0"
    assert "request" in body and "response" in body


def test_recommendations_validation_error() -> None:
    response = client.post(
        "/api/recommendations",
        json={
            "location": "",
            "budget": "medium",
            "cuisine": "Italian",
            "min_rating": 4.0,
            "use_mock_data": True,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["ok"] is False
    assert payload["error_code"] == "validation_error"


def test_recommendations_success_with_mock_data() -> None:
    response = client.post(
        "/api/recommendations",
        json={
            "location": "Koramangala",
            "budget": "medium",
            "cuisine": "Italian",
            "min_rating": 4.0,
            "use_mock_data": True,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["ok"] is True
    assert "recommendations" in payload["result"]
