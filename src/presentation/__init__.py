"""Phase 5: result presentation; Phase 0/2: basic web UI."""

from src.presentation.phase5 import (
    Phase5ViewModel,
    PresentableRecommendation,
    build_phase5_view_model,
    format_recommendations,
    render_recommendations_console,
)
from src.presentation.renderer import render_recommendations

__all__ = [
    "Phase5ViewModel",
    "PresentableRecommendation",
    "build_phase5_view_model",
    "format_recommendations",
    "render_recommendations",
    "render_recommendations_console",
]
