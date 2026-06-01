"""CLI runner for Phase 1 data ingestion."""

from __future__ import annotations

from src.config import settings, setup_logging
from src.data.phase1.ingestion import ingest_and_persist_dataset


def main() -> int:
    setup_logging()
    output_path = settings.resolve_path(settings.processed_data_path)
    ingest_and_persist_dataset(settings.dataset_source, output_path)
    print(f"Processed dataset saved to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

