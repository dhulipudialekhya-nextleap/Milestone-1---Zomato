"""Phase 1: data ingestion and preprocessing."""

from src.data.loader import load_restaurants, load_mock_restaurants
from src.data.phase1 import ingest_and_persist_dataset, load_processed_restaurants

__all__ = [
    "load_restaurants",
    "load_mock_restaurants",
    "ingest_and_persist_dataset",
    "load_processed_restaurants",
]
