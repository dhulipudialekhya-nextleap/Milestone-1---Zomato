"""Shared form option lists for Streamlit (aligned with frontend designConstants)."""

from __future__ import annotations

BANGALORE_LOCATIONS: tuple[str, ...] = (
    "Koramangala",
    "Indiranagar",
    "HSR",
    "BTM",
    "Whitefield",
    "Bellandur",
    "Jayanagar",
    "Marathahalli",
    "Electronic City",
    "MG Road",
    "Brigade Road",
    "Sarjapur Road",
    "Banashankari",
    "Frazer Town",
    "Malleshwaram",
)

CUISINE_OPTIONS: tuple[str, ...] = (
    "Any Cuisine",
    "North Indian",
    "South Indian",
    "Chinese",
    "Italian",
    "Mughlai",
    "Biryani",
    "Modern Japanese",
    "Authentic Italian",
    "Plant-Based Contemporary",
)

CRAVING_OPTIONS: tuple[str, ...] = (
    "Anything delicious",
    "Biryani",
    "Cakes",
    "Indian Breads",
    "Pizza",
    "Sushi",
    "Pasta",
)

STREAMLIT_DEFAULT_LOCATION = "Koramangala"
STREAMLIT_DEFAULT_CUISINE = "Any Cuisine"


def normalize_cuisine(cuisine: str) -> str:
    """Match Next.js: 'Any Cuisine' becomes a broad Indian search."""
    return "Indian" if cuisine.strip() == "Any Cuisine" else cuisine.strip()


def normalize_extras(extras: str | None) -> str | None:
    if not extras or not extras.strip():
        return None
    text = extras.strip()
    if text == "Anything delicious":
        return None
    return text
