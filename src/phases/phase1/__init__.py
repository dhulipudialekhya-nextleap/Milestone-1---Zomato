"""Phase 1: dataset ingestion, preprocessing, and loading."""

from src.data import (
    ingest_and_persist_dataset,
    load_mock_restaurants,
    load_processed_restaurants,
    load_restaurants,
)

__all__ = [
    "ingest_and_persist_dataset",
    "load_mock_restaurants",
    "load_processed_restaurants",
    "load_restaurants",
]

