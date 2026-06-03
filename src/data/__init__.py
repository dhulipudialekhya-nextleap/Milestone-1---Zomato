"""Data loading (lazy: Phase 1 pandas/datasets not imported until ingestion runs)."""

from src.data.loader import load_mock_restaurants, load_restaurants

__all__ = [
    "load_restaurants",
    "load_mock_restaurants",
]
