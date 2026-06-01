"""Phase 8 — frontend-backend contract regression tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.backend.phase6.server import app
from src.backend.phase6.service import run_backend_request
from src.backend.phase8 import (
    CONTRACT_VERSION,
    build_contract_manifest,
    validate_api_request,
    validate_api_response,
)
from src.backend.phase8.export import export_contract_artifacts

client = TestClient(app)

_FIXTURES = Path(__file__).resolve().parents[2] / "contracts" / "v1" / "fixtures"


def _load_fixture(name: str) -> dict:
    return json.loads((_FIXTURES / name).read_text(encoding="utf-8"))


def test_contract_version_matches_frontend_constant() -> None:
    manifest = build_contract_manifest()
    assert manifest["version"] == CONTRACT_VERSION == "1.0.0"


def test_get_api_contract_endpoint() -> None:
    response = client.get("/api/contract")
    assert response.status_code == 200
    body = response.json()
    assert body["version"] == CONTRACT_VERSION
    assert "request" in body
    assert "response" in body
    assert body["endpoints"]["recommendations"]["path"] == "/api/recommendations"


def test_fixture_request_validates() -> None:
    payload = _load_fixture("request_valid.json")
    req = validate_api_request(payload)
    assert req.location == "Koramangala"
    assert req.budget == "medium"
    assert req.use_mock_data is True


def test_fixture_success_response_validates() -> None:
    payload = _load_fixture("response_success.json")
    response = validate_api_response(payload)
    assert response.ok is True
    assert len(response.result.recommendations) == 1


def test_fixture_error_response_validates() -> None:
    payload = _load_fixture("response_validation_error.json")
    response = validate_api_response(payload)
    assert response.ok is False
    assert response.error_code == "validation_error"


def test_live_success_response_matches_contract() -> None:
    raw = run_backend_request(_load_fixture("request_valid.json"), use_mock_data=True)
    serialized = json.loads(raw.model_dump_json())
    response = validate_api_response(serialized)
    assert response.ok is True
    assert isinstance(response.result.filter_match_count, int)


def test_live_validation_error_matches_contract() -> None:
    raw = run_backend_request(
        {
            "location": "",
            "budget": "medium",
            "cuisine": "Italian",
            "min_rating": 4.0,
        },
        use_mock_data=True,
    )
    serialized = json.loads(raw.model_dump_json())
    response = validate_api_response(serialized)
    assert response.ok is False
    assert response.error_code == "validation_error"
    assert response.message


def test_recommendations_endpoint_returns_contract_shape() -> None:
    response = client.post("/api/recommendations", json=_load_fixture("request_valid.json"))
    assert response.status_code == 200
    validate_api_response(response.json())


def test_export_contract_artifacts_writes_version_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import src.backend.phase8.export as export_mod

    monkeypatch.setattr(export_mod, "_CONTRACT_DIR", tmp_path)
    monkeypatch.setattr(export_mod, "_FIXTURES_DIR", tmp_path / "fixtures")
    export_contract_artifacts()
    assert (tmp_path / "VERSION").read_text(encoding="utf-8").strip() == CONTRACT_VERSION
    assert (tmp_path / "manifest.json").exists()
    assert (tmp_path / "request.schema.json").exists()
    assert (tmp_path / "response.schema.json").exists()
