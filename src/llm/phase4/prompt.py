"""Prompt builder for Phase 4 recommendation calls."""

from __future__ import annotations

from src.filters.phase3 import serialize_shortlist_payload
from src.models import Restaurant, UserPreferences


def build_prompt_messages(
    preferences: UserPreferences,
    shortlist: list[Restaurant],
) -> list[dict[str, str]]:
    """Create Groq chat messages with strict JSON output contract."""
    payload = serialize_shortlist_payload(preferences, shortlist)
    system_prompt = (
        "You are a restaurant recommendation assistant. "
        "You MUST use only restaurants from the provided candidate list. "
        "Return valid JSON only, with no markdown fences and no extra prose. "
        "Required schema: "
        '{"summary": "string", "recommendations": [{"rank": 1, "restaurant_id": "id", '
        '"name": "string", "explanation": "string"}]}'
    )
    user_prompt = (
        "Rank the provided candidates for the user preferences. "
        "Use concise explanations grounded in location, cuisine, budget, and rating. "
        "Return 3 to 5 recommendations if available.\n\n"
        f"INPUT_PAYLOAD_JSON:\n{payload}"
    )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

