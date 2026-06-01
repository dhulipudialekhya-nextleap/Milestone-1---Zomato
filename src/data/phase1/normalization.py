"""Normalization helpers for Phase 1 ingestion."""

from __future__ import annotations

import re
import uuid
from collections.abc import Iterable
from typing import Any

from src.config import settings
from src.models import Restaurant

COLUMN_ALIASES: dict[str, tuple[str, ...]] = {
    "id": ("id", "restaurant_id", "res_id", "url"),
    "name": ("name", "restaurant_name", "title"),
    "location": ("location", "city", "address", "listed_in(city)"),
    "cuisines": ("cuisines", "cuisine", "tags"),
    "average_cost": (
        "average_cost",
        "cost_for_two",
        "approx_cost",
        "approx_cost(for two people)",
        "price",
        "avg_cost",
    ),
    "rating": ("rating", "aggregate_rating", "stars", "user_rating", "rate"),
}

CITY_ALIASES: dict[str, str] = {
    "new delhi": "Delhi",
    "delhi ncr": "Delhi",
    "bengaluru": "Bangalore",
}


def normalize_raw_record(raw: dict[str, Any]) -> Restaurant | None:
    """Convert a raw dataset row into canonical `Restaurant` model."""
    name = _as_clean_string(_pick(raw, "name"))
    location = _normalize_location(_pick(raw, "location"))
    if not name or not location:
        return None

    cuisines = _normalize_cuisines(_pick(raw, "cuisines"))
    rating = _normalize_rating(_pick(raw, "rating"))
    if rating is None:
        rating = 0.0

    average_cost = _normalize_cost(_pick(raw, "average_cost"))
    cost_band = _map_cost_band(average_cost)

    restaurant_id = _as_clean_string(_pick(raw, "id")) or str(uuid.uuid4())
    metadata = _build_metadata(raw)

    try:
        return Restaurant(
            id=restaurant_id,
            name=name,
            location=location,
            cuisines=cuisines,
            average_cost=average_cost,
            cost_band=cost_band,
            rating=rating,
            metadata=metadata,
        )
    except ValueError:
        return None


def _pick(raw: dict[str, Any], canonical_field: str) -> Any:
    aliases = COLUMN_ALIASES.get(canonical_field, ())
    lowered = {str(k).lower(): k for k in raw.keys()}
    for alias in aliases:
        if alias in raw and raw[alias] not in (None, ""):
            return raw[alias]
        key = lowered.get(alias.lower())
        if key is not None and raw[key] not in (None, ""):
            return raw[key]
    return None


def _as_clean_string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _normalize_location(value: Any) -> str | None:
    text = _as_clean_string(value)
    if not text:
        return None
    normalized = " ".join(text.split())
    lowered = normalized.lower()
    if lowered in CITY_ALIASES:
        return CITY_ALIASES[lowered]
    return normalized.title()


def _normalize_cuisines(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        parts = re.split(r"[,/|]", value)
        return [p.strip().title() for p in parts if p and p.strip()]
    if isinstance(value, Iterable):
        output: list[str] = []
        for item in value:
            text = _as_clean_string(item)
            if text:
                output.append(text.title())
        return output
    return []


def _normalize_rating(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        num = float(value)
    else:
        text = _as_clean_string(value)
        if not text:
            return None
        match = re.search(r"\d+(\.\d+)?", text)
        if not match:
            return None
        num = float(match.group(0))

    if num < 0:
        return 0.0
    if num > 5:
        return 5.0
    return round(num, 1)


def _normalize_cost(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        number = int(value)
        return number if number > 0 else None

    text = _as_clean_string(value)
    if not text:
        return None
    numbers = re.findall(r"\d+", text.replace(",", ""))
    if not numbers:
        return None
    values = [int(n) for n in numbers if int(n) > 0]
    if not values:
        return None
    if len(values) == 1:
        return values[0]
    return int(sum(values) / len(values))


def _map_cost_band(cost: int | None) -> str | None:
    if cost is None:
        return None
    if cost <= settings.budget_low_max:
        return "low"
    if cost <= settings.budget_medium_max:
        return "medium"
    return "high"


def _build_metadata(raw: dict[str, Any]) -> dict[str, Any]:
    metadata: dict[str, Any] = {"source": "phase1-ingestion"}
    mapped_keys = set()
    for aliases in COLUMN_ALIASES.values():
        mapped_keys.update(aliases)
        mapped_keys.update(alias.lower() for alias in aliases)

    for key, value in raw.items():
        if key in mapped_keys or str(key).lower() in mapped_keys:
            continue
        metadata[key] = value
    return metadata

