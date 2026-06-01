"""Phase 5 result presentation package."""

from src.presentation.phase5.renderer import format_recommendations, render_recommendations_console
from src.presentation.phase5.view_model import (
    Phase5ViewModel,
    PresentableRecommendation,
    build_phase5_view_model,
)

__all__ = [
    "Phase5ViewModel",
    "PresentableRecommendation",
    "build_phase5_view_model",
    "format_recommendations",
    "render_recommendations_console",
]

