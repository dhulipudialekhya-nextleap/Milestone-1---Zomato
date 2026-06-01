/**
 * Phase 7 view-model builder — mirrors Python `build_phase5_view_model`.
 * Frontend renders only from this shape; no backend business logic here.
 */

import {
  DISPLAY_TOP_K,
  type Phase5ViewModel,
  type PresentableRecommendation,
  type RecommendationResult,
} from "./types";

function formatCost(
  averageCost: number | null,
  costBand: string | null,
): string {
  if (averageCost !== null && averageCost !== undefined) {
    return `₹${averageCost} for two`;
  }
  if (costBand) {
    return `${costBand} budget`;
  }
  return "N/A";
}

export function buildPhase5ViewModel(
  result: RecommendationResult,
  topK: number = DISPLAY_TOP_K,
): Phase5ViewModel {
  const rows = result.recommendations.slice(0, topK);

  const items: PresentableRecommendation[] = rows.map((item) => ({
    rank: item.rank,
    name: item.name,
    cuisinesText: item.cuisines.length > 0 ? item.cuisines.join(", ") : "N/A",
    ratingText: item.rating !== null ? item.rating.toFixed(1) : "N/A",
    estimatedCostText: formatCost(item.average_cost, item.cost_band),
    explanation: item.explanation,
  }));

  return {
    title: "Restaurant Recommendations",
    summary: result.summary,
    showFallbackBanner: result.used_llm_fallback,
    emptyMessage: items.length === 0 ? "No recommendations to display." : null,
    filterMatchCount: result.filter_match_count,
    items,
  };
}
