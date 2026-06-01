"""Phase 3 payload serializer for Phase 4 prompt input."""

from __future__ import annotations

import json

from src.models import Restaurant, UserPreferences


def serialize_shortlist_payload(
    preferences: UserPreferences,
    shortlist: list[Restaurant],
) -> str:
    """Serialize preferences + shortlist into compact JSON for LLM prompting."""
    payload = {
        "preferences": {
            "location": preferences.location,
            "budget": preferences.budget,
            "cuisine": preferences.cuisine,
            "min_rating": preferences.min_rating,
            "extras": preferences.extras,
        },
        "candidates": [
            {
                "id": r.id,
                "name": r.name,
                "location": r.location,
                "cuisines": r.cuisines,
                "average_cost": r.average_cost,
                "cost_band": r.cost_band,
                "rating": r.rating,
                "votes": r.metadata.get("votes"),
            }
            for r in shortlist
        ],
    }
    return json.dumps(payload, ensure_ascii=True)

