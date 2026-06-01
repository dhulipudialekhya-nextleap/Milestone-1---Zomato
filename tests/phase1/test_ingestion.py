"""Tests for Phase 1 normalization and processed-store persistence."""

from __future__ import annotations

from pathlib import Path

from src.data.phase1.ingestion import load_processed_restaurants
from src.data.phase1.normalization import normalize_raw_record


def test_normalize_raw_record_with_alias_columns() -> None:
    raw = {
        "restaurant_name": "  Test Bistro ",
        "city": "new delhi",
        "cuisine": "italian, chinese",
        "aggregate_rating": "4.6/5",
        "cost_for_two": "₹500 for two",
    }
    record = normalize_raw_record(raw)
    assert record is not None
    assert record.name == "Test Bistro"
    assert record.location == "Delhi"
    assert record.cuisines == ["Italian", "Chinese"]
    assert record.rating == 4.6
    assert record.average_cost == 500
    assert record.cost_band == "medium"


def test_normalize_raw_record_missing_required_fields_returns_none() -> None:
    raw = {"restaurant_name": "", "city": "", "aggregate_rating": "4.2"}
    assert normalize_raw_record(raw) is None


def test_load_processed_restaurants_from_csv(tmp_path: Path) -> None:
    csv_path = tmp_path / "restaurants.csv"
    csv_path.write_text(
        (
            "id,name,location,cuisines,average_cost,cost_band,rating,metadata\n"
            "r1,Alpha,Delhi,\"[\"\"Italian\"\", \"\"Mexican\"\"]\",600,medium,4.3,\"{\"\"votes\"\": 121}\"\n"
        ),
        encoding="utf-8",
    )
    rows = load_processed_restaurants(csv_path)
    assert len(rows) == 1
    assert rows[0].name == "Alpha"
    assert rows[0].cuisines == ["Italian", "Mexican"]
    assert rows[0].rating == 4.3

