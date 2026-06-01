"""Compatibility wrapper for Phase 5 renderer."""

from src.presentation.phase5.renderer import format_recommendations, render_recommendations_console


# Backward-compatible alias
render_recommendations = render_recommendations_console
