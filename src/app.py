"""
Application orchestrator — coordinates all pipeline phases.

Phase 0: runnable end-to-end skeleton; primary entry is the Streamlit web UI.
CLI is retained for development and automated tests.
"""

from __future__ import annotations

import argparse
import logging
import sys

from src.backend.phase6 import execute_backend_pipeline
from src.config import ConfigError, setup_logging, settings
from src.input.phase2 import InputValidationError, build_user_preferences
from src.models import RecommendationResult, UserPreferences
from src.presentation.renderer import render_recommendations_console

logger = logging.getLogger(__name__)


def execute_pipeline(
    preferences: UserPreferences,
    *,
    use_mock_data: bool = False,
) -> RecommendationResult:
    """Run pipeline via Phase 6 backend service boundary."""
    return execute_backend_pipeline(preferences, use_mock_data=use_mock_data)


def run_pipeline(
    preferences: UserPreferences,
    *,
    use_mock_data: bool = False,
) -> RecommendationResult:
    """Execute pipeline and print results to the console (dev/CLI path)."""
    result = execute_pipeline(preferences, use_mock_data=use_mock_data)
    render_recommendations_console(result)
    return result


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Zomato AI Restaurant Recommendation System — CLI (dev/testing). "
            "Use `streamlit run src/presentation/web_ui.py` for the primary web UI."
        ),
    )
    parser.add_argument("--location", default="Bangalore", help="City or area")
    parser.add_argument(
        "--budget",
        choices=["low", "medium", "high"],
        default="medium",
        help="Budget band",
    )
    parser.add_argument("--cuisine", default="Italian", help="Preferred cuisine")
    parser.add_argument(
        "--min-rating",
        type=float,
        default=4.0,
        help="Minimum rating (0–5)",
    )
    parser.add_argument("--extras", default=None, help="Additional preferences")
    parser.add_argument(
        "--mock-data",
        action="store_true",
        help="Force in-memory mock dataset",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point (development and tests)."""
    setup_logging()
    args = _parse_args(argv)

    try:
        preferences = build_user_preferences(
            location=args.location,
            budget=args.budget,
            cuisine=args.cuisine,
            min_rating=args.min_rating,
            extras=args.extras,
        )
    except InputValidationError as exc:
        logger.error("Invalid preferences: %s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    try:
        run_pipeline(preferences, use_mock_data=args.mock_data)
    except ConfigError as exc:
        logger.error("Configuration error: %s", exc)
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 1
    except NotImplementedError as exc:
        logger.error("%s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
