"""Phase 1 ingestion: fetch, normalize, and persist processed restaurants."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import pandas as pd
from datasets import load_dataset

from src.models import Restaurant
from src.data.phase1.normalization import normalize_raw_record

logger = logging.getLogger(__name__)


def ingest_and_persist_dataset(dataset_source: str, output_path: Path) -> list[Restaurant]:
    """
    Ingest from Hugging Face dataset source, normalize, and persist to output path.

    Supports `.csv`, `.json`, and `.parquet` output extensions.
    """
    logger.info("Starting Phase 1 ingestion from %s", dataset_source)
    records = _load_raw_records(dataset_source)
    restaurants = _normalize_records(records)
    if not restaurants:
        raise ValueError("No valid restaurants after normalization.")

    _persist_restaurants(restaurants, output_path)
    logger.info("Phase 1 ingestion completed: %d rows saved to %s", len(restaurants), output_path)
    return restaurants


def load_processed_restaurants(path: Path) -> list[Restaurant]:
    """Load processed restaurants from disk."""
    suffix = path.suffix.lower()
    if suffix == ".csv":
        frame = pd.read_csv(path)
        return _frame_to_restaurants(frame)
    if suffix == ".json":
        rows = json.loads(path.read_text(encoding="utf-8"))
        return [Restaurant.model_validate(row) for row in rows]
    if suffix == ".parquet":
        frame = pd.read_parquet(path)
        return _frame_to_restaurants(frame)
    raise ValueError(f"Unsupported processed data format: {suffix}")


def _load_raw_records(dataset_source: str) -> list[dict[str, Any]]:
    dataset_ref = _normalize_dataset_source(dataset_source)
    dataset_dict = load_dataset(dataset_ref)
    if "train" in dataset_dict:
        split = dataset_dict["train"]
    else:
        first_split_name = next(iter(dataset_dict.keys()))
        split = dataset_dict[first_split_name]
    return [dict(row) for row in split]


def _normalize_records(records: list[dict[str, Any]]) -> list[Restaurant]:
    normalized: list[Restaurant] = []
    invalid = 0
    for raw in records:
        row = normalize_raw_record(raw)
        if row is None:
            invalid += 1
            continue
        normalized.append(row)
    logger.info("Normalized %d records; dropped %d invalid records", len(normalized), invalid)
    return normalized


def _persist_restaurants(restaurants: list[Restaurant], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    suffix = output_path.suffix.lower()
    frame = _restaurants_to_frame(restaurants)

    if suffix == ".csv":
        frame.to_csv(output_path, index=False)
        return
    if suffix == ".json":
        rows = [r.model_dump() for r in restaurants]
        output_path.write_text(json.dumps(rows, ensure_ascii=True, indent=2), encoding="utf-8")
        return
    if suffix == ".parquet":
        frame.to_parquet(output_path, index=False)
        return

    raise ValueError(
        f"Unsupported output format {suffix!r}. Use .csv, .json, or .parquet for PROCESSED_DATA_PATH."
    )


def _restaurants_to_frame(restaurants: list[Restaurant]) -> pd.DataFrame:
    rows = []
    for r in restaurants:
        rows.append(
            {
                "id": r.id,
                "name": r.name,
                "location": r.location,
                "cuisines": json.dumps(r.cuisines, ensure_ascii=True),
                "average_cost": r.average_cost,
                "cost_band": r.cost_band,
                "rating": r.rating,
                "metadata": json.dumps(r.metadata, ensure_ascii=True),
            }
        )
    return pd.DataFrame(rows)


def _frame_to_restaurants(frame: pd.DataFrame) -> list[Restaurant]:
    restaurants: list[Restaurant] = []
    for _, row in frame.iterrows():
        cuisines_raw = row.get("cuisines", "[]")
        metadata_raw = row.get("metadata", "{}")
        cuisines = _safe_json_list(cuisines_raw)
        metadata = _safe_json_dict(metadata_raw)

        restaurant = Restaurant(
            id=str(row.get("id", "")),
            name=str(row.get("name", "")),
            location=str(row.get("location", "")),
            cuisines=cuisines,
            average_cost=_to_optional_int(row.get("average_cost")),
            cost_band=_to_cost_band(row.get("cost_band")),
            rating=_to_rating(row.get("rating")),
            metadata=metadata,
        )
        restaurants.append(restaurant)
    return restaurants


def _normalize_dataset_source(dataset_source: str) -> str:
    source = dataset_source.strip()
    marker = "huggingface.co/datasets/"
    if marker in source:
        return source.split(marker, maxsplit=1)[1].strip("/")
    return source


def _safe_json_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(v) for v in value]
    if value is None:
        return []
    text = str(value).strip()
    if not text:
        return []
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return [str(v) for v in parsed]
    except json.JSONDecodeError:
        pass
    return [segment.strip() for segment in text.split(",") if segment.strip()]


def _safe_json_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if value is None:
        return {}
    text = str(value).strip()
    if not text:
        return {}
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    return {}


def _to_optional_int(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if value != value:  # NaN check
            return None
        return int(value)
    text = str(value).strip()
    if not text:
        return None
    try:
        return int(float(text))
    except ValueError:
        return None


def _to_optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if text.lower() == "nan":
        return None
    return text if text else None


def _to_cost_band(value: Any) -> str | None:
    text = _to_optional_str(value)
    if text in {"low", "medium", "high"}:
        return text
    return None


def _to_rating(value: Any) -> float:
    if value is None:
        return 0.0
    try:
        num = float(value)
    except (TypeError, ValueError):
        return 0.0
    if num != num:  # NaN check
        return 0.0
    if num < 0:
        return 0.0
    if num > 5:
        return 5.0
    return num

