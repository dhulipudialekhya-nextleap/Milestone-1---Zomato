"""Tests for Phase 5 view model and renderer."""

from src.models import RecommendationItem, RecommendationResult
from src.presentation.phase5 import build_phase5_view_model, format_recommendations


def test_build_phase5_view_model_with_items() -> None:
    result = RecommendationResult(
        summary="Top picks",
        recommendations=[
            RecommendationItem(
                rank=1,
                restaurant_id="r1",
                name="Alpha",
                explanation="Great fit",
                cuisines=["Indian"],
                rating=4.5,
                average_cost=1200,
                cost_band="high",
            )
        ],
        used_llm_fallback=False,
        filter_match_count=1,
    )
    vm = build_phase5_view_model(result, top_k=5)
    assert vm.summary == "Top picks"
    assert vm.empty_message is None
    assert len(vm.items) == 1
    assert vm.items[0].estimated_cost_text == "₹1200 for two"


def test_build_phase5_view_model_empty_state() -> None:
    result = RecommendationResult(
        summary=None,
        recommendations=[],
        used_llm_fallback=True,
        filter_match_count=0,
    )
    vm = build_phase5_view_model(result)
    assert vm.show_fallback_banner is True
    assert vm.empty_message == "No recommendations to display."
    assert vm.filter_match_count == 0


def test_format_recommendations_renders_expected_sections() -> None:
    result = RecommendationResult(
        summary="Top picks",
        recommendations=[
            RecommendationItem(
                rank=1,
                restaurant_id="r1",
                name="Alpha",
                explanation="Great fit",
                cuisines=["Indian", "Chinese"],
                rating=4.2,
                average_cost=900,
                cost_band="medium",
            )
        ],
        used_llm_fallback=False,
        filter_match_count=1,
    )
    output = format_recommendations(result)
    assert "Restaurant Recommendations" in output
    assert "Summary: Top picks" in output
    assert "#1  Alpha" in output
    assert "Est. cost: ₹900 for two" in output

