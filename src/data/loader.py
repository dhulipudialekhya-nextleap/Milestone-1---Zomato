"""Dataset loader with Phase 1 processed-data support."""

from __future__ import annotations

import logging
import os
from pathlib import Path

from src.config import settings
from src.data.phase1 import ingest_and_persist_dataset, load_processed_restaurants
from src.models import Restaurant

logger = logging.getLogger(__name__)


def load_mock_restaurants() -> list[Restaurant]:
    """In-memory demo dataset aligned with Bangalore frontend locations."""
    return [
        Restaurant(
            id="mock-1",
            name="Trattoria Koramangala",
            location="Koramangala",
            cuisines=["Italian", "Continental"],
            average_cost=800,
            cost_band="medium",
            rating=4.5,
            metadata={"source": "mock"},
        ),
        Restaurant(
            id="mock-2",
            name="Spice Route HSR",
            location="HSR",
            cuisines=["North Indian", "Chinese"],
            average_cost=600,
            cost_band="medium",
            rating=4.3,
            metadata={"source": "mock"},
        ),
        Restaurant(
            id="mock-3",
            name="Indiranagar Tandoor House",
            location="Indiranagar",
            cuisines=["North Indian", "Mughlai"],
            average_cost=700,
            cost_band="medium",
            rating=4.4,
            metadata={"source": "mock"},
        ),
        Restaurant(
            id="mock-4",
            name="Bellandur Biryani Co.",
            location="Bellandur",
            cuisines=["Biryani", "Hyderabadi"],
            average_cost=500,
            cost_band="low",
            rating=4.2,
            metadata={"source": "mock"},
        ),
        Restaurant(
            id="mock-5",
            name="Whitefield Wok",
            location="Whitefield",
            cuisines=["Chinese", "Asian"],
            average_cost=450,
            cost_band="low",
            rating=4.1,
            metadata={"source": "mock"},
        ),
        Restaurant(
            id="mock-6",
            name="BTM Budget Meals",
            location="BTM",
            cuisines=["South Indian", "Fast Food"],
            average_cost=300,
            cost_band="low",
            rating=4.0,
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

    if _should_skip_auto_ingest():
        logger.warning(
            "Processed data missing at %s; auto-ingest disabled (Railway/demo). Using mock data.",
            path,
        )
        return load_mock_restaurants()

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


def _should_skip_auto_ingest() -> bool:
    """Skip slow Hugging Face ingest on Railway when no CSV is bundled (see railway.toml)."""
    if os.getenv("DISABLE_DATA_INGEST", "").strip().lower() in ("1", "true", "yes"):
        return True
    if os.getenv("RAILWAY_ENVIRONMENT", "").strip():
        return True
    return False
