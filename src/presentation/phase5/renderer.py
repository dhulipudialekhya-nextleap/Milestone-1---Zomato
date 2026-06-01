"""Phase 5 renderers for console/UI presentation."""

from __future__ import annotations

import logging

from src.models import RecommendationResult
from src.presentation.phase5.view_model import build_phase5_view_model

logger = logging.getLogger(__name__)


def format_recommendations(result: RecommendationResult) -> str:
    """Build plain-text output for terminal rendering."""
    vm = build_phase5_view_model(result)
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append(f"  {vm.title}")
    lines.append("=" * 60)

    if vm.show_fallback_banner:
        lines.append("\nAI unavailable - showing filter-based results.\n")

    if vm.summary:
        lines.append(f"\nSummary: {vm.summary}\n")

    if vm.empty_message:
        lines.append(vm.empty_message)
        lines.append(f"(Matched {vm.filter_match_count} restaurant(s) after filtering.)")
        return "\n".join(lines)

    for item in vm.items:
        lines.append(f"\n#{item.rank}  {item.name}")
        lines.append(f"    Cuisine:   {item.cuisines_text}")
        lines.append(f"    Rating:    {item.rating_text}")
        lines.append(f"    Est. cost: {item.estimated_cost_text}")
        lines.append(f"    Why:       {item.explanation}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def render_recommendations_console(result: RecommendationResult) -> str:
    """Print recommendations to stdout and return rendered text."""
    output = format_recommendations(result)
    print(output)
    vm = build_phase5_view_model(result)
    if vm.items:
        logger.info("Rendered %d recommendation(s)", len(vm.items))
    return output

