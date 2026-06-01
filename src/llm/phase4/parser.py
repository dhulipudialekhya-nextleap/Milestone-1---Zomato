"""Parse and validate LLM recommendation output against shortlist."""

from __future__ import annotations

import json
import re
from typing import Any

from src.models import RecommendationItem, RecommendationResult, Restaurant


class LlmParseError(ValueError):
    """Raised when LLM output cannot be parsed into expected structure."""


def parse_recommendation_response(
    text: str,
    shortlist: list[Restaurant],
) -> RecommendationResult:
    """Parse JSON response and ground recommendations to shortlist records."""
    obj = _parse_json_object(_strip_markdown_fences(text))
    summary = obj.get("summary")
    if summary is not None:
        summary = str(summary)

    raw_items = obj.get("recommendations")
    if not isinstance(raw_items, list):
        raise LlmParseError("Missing or invalid `recommendations` list.")

    shortlist_by_id = {r.id: r for r in shortlist}
    shortlist_by_name = {r.name.lower(): r for r in shortlist}
    seen_ids: set[str] = set()
    parsed_items: list[RecommendationItem] = []

    # Preserve LLM intent by sorting on provided rank where possible.
    normalized_rows = _normalize_rows(raw_items)
    for row in normalized_rows:
        restaurant = _resolve_restaurant(row, shortlist_by_id, shortlist_by_name)
        if restaurant is None or restaurant.id in seen_ids:
            continue
        seen_ids.add(restaurant.id)
        explanation = str(row.get("explanation", "")).strip() or (
            f"{restaurant.name} matches your preferences."
        )
        parsed_items.append(
            RecommendationItem(
                rank=len(parsed_items) + 1,
                restaurant_id=restaurant.id,
                name=restaurant.name,
                explanation=explanation,
                cuisines=restaurant.cuisines,
                rating=restaurant.rating,
                average_cost=restaurant.average_cost,
                cost_band=restaurant.cost_band,
            )
        )

    if not parsed_items:
        raise LlmParseError("No grounded recommendations after validation.")

    return RecommendationResult(
        summary=summary,
        recommendations=parsed_items,
        used_llm_fallback=False,
        filter_match_count=len(shortlist),
    )


def _strip_markdown_fences(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```[a-zA-Z0-9_-]*\n?", "", stripped)
        stripped = re.sub(r"\n?```$", "", stripped)
    return stripped.strip()


def _parse_json_object(text: str) -> dict[str, Any]:
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    # Recovery path: extract likely JSON object in mixed output.
    first = text.find("{")
    last = text.rfind("}")
    if first == -1 or last == -1 or last <= first:
        raise LlmParseError("No JSON object found in LLM response.")
    fragment = text[first : last + 1]
    try:
        parsed = json.loads(fragment)
    except json.JSONDecodeError as exc:
        raise LlmParseError("Invalid JSON in LLM response.") from exc
    if not isinstance(parsed, dict):
        raise LlmParseError("Top-level LLM response is not a JSON object.")
    return parsed


def _normalize_rows(rows: list[Any]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for item in rows:
        if not isinstance(item, dict):
            continue
        normalized.append(item)

    def rank_key(row: dict[str, Any]) -> int:
        raw_rank = row.get("rank")
        try:
            value = int(raw_rank)
            return value if value > 0 else 999_999
        except (TypeError, ValueError):
            return 999_999

    return sorted(normalized, key=rank_key)


def _resolve_restaurant(
    row: dict[str, Any],
    shortlist_by_id: dict[str, Restaurant],
    shortlist_by_name: dict[str, Restaurant],
) -> Restaurant | None:
    restaurant_id = row.get("restaurant_id")
    if isinstance(restaurant_id, str) and restaurant_id in shortlist_by_id:
        return shortlist_by_id[restaurant_id]

    name = row.get("name")
    if isinstance(name, str):
        return shortlist_by_name.get(name.strip().lower())
    return None

