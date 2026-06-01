"""Dataset loader with Phase 1 processed-data support."""

from __future__ import annotations

import logging
from pathlib import Path

from src.config import settings
from src.data.phase1 import ingest_and_persist_dataset, load_processed_restaurants
from src.models import Restaurant

logger = logging.getLogger(__name__)


def load_mock_restaurants() -> list[Restaurant]:
    """Return a small in-memory dataset for skeleton pipeline runs."""
    return [
        Restaurant(
            id="mock-1",
            name="Mock Italian Bistro",
            location="Bangalore",
            cuisines=["Italian", "Continental"],
            average_cost=600,
            cost_band="medium",
            rating=4.5,
            metadata={"source": "mock"},
        ),
        Restaurant(
            id="mock-2",
            name="Mock Chinese Wok",
            location="Bangalore",
            cuisines=["Chinese", "Asian"],
            average_cost=400,
            cost_band="low",
            rating=4.2,
            metadata={"source": "mock"},
        ),
        Restaurant(
            id="mock-3",
            name="Mock Fine Dine",
            location="Delhi",
            cuisines=["Italian", "French"],
            average_cost=1500,
            cost_band="high",
            rating=4.8,
            metadata={"source": "mock"},
        ),
        Restaurant(
            id="mock-4",
            name="Mock Street Spice",
            location="Delhi",
            cuisines=["North Indian", "Street Food"],
            average_cost=250,
            cost_band="low",
            rating=3.9,
            metadata={"source": "mock"},
        ),
    ]


def load_restaurants(*, use_mock: bool = False) -> list[Restaurant]:
    """
    Load restaurant data from processed store or mock.

    Priority:
    1) mock dataset if `use_mock=True`
    2) load processed dataset if present
    3) auto-ingest from HF and persist (Phase 1)
    4) fallback to mock dataset on ingestion failure
    """
    if use_mock:
        logger.info("Loading mock restaurant dataset")
        return load_mock_restaurants()

    path: Path = settings.resolve_path(settings.processed_data_path)
    if path.exists():
        logger.info("Loading processed dataset from %s", path)
        return load_processed_restaurants(path)

    logger.info("Processed data missing at %s, triggering Phase 1 ingestion", path)
    try:
        restaurants = ingest_and_persist_dataset(settings.dataset_source, path)
        return restaurants
    except Exception as exc:  # noqa: BLE001 - fallback by design for availability
        logger.warning(
            "Phase 1 ingestion failed (%s). Falling back to mock data for continuity.",
            exc,
        )
        return load_mock_restaurants()
