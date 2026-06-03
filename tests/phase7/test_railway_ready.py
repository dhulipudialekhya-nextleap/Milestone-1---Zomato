"""Railway deployment readiness checks for the FastAPI backend."""

from __future__ import annotations

from fastapi.testclient import TestClient

from src.backend.phase6.cors import get_cors_settings
from src.backend.phase6.server import app
from src.data.loader import _should_skip_auto_ingest

client = TestClient(app)


def test_root_endpoint_lists_routes() -> None:
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["health"] == "/health"
    assert "recommendations" in body["recommendations"]


def test_cors_includes_vercel_regex() -> None:
    origins, regex = get_cors_settings()
    assert "http://localhost:3000" in origins
    assert regex is not None
    assert "vercel" in regex


def test_skip_auto_ingest_when_railway_env(monkeypatch) -> None:
    monkeypatch.setenv("RAILWAY_ENVIRONMENT", "production")
    monkeypatch.delenv("DISABLE_DATA_INGEST", raising=False)
    assert _should_skip_auto_ingest() is True
