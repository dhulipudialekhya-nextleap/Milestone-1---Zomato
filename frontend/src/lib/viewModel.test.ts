import { describe, expect, it } from "vitest";

import { buildPhase5ViewModel } from "./viewModel";
import type { RecommendationResult } from "./types";

describe("buildPhase5ViewModel", () => {
  it("maps recommendation result into presentable items", () => {
    const result: RecommendationResult = {
      summary: "Top picks for Italian lovers.",
      recommendations: [
        {
          rank: 1,
          restaurant_id: "r1",
          name: "Pasta Palace",
          explanation: "Great Italian spot.",
          cuisines: ["Italian"],
          rating: 4.5,
          average_cost: 800,
          cost_band: "medium",
        },
      ],
      used_llm_fallback: false,
      filter_match_count: 10,
    };

    const vm = buildPhase5ViewModel(result);

    expect(vm.summary).toBe("Top picks for Italian lovers.");
    expect(vm.items).toHaveLength(1);
    expect(vm.items[0].name).toBe("Pasta Palace");
    expect(vm.items[0].estimatedCostText).toBe("₹800 for two");
    expect(vm.emptyMessage).toBeNull();
  });

  it("returns empty message when no recommendations", () => {
    const result: RecommendationResult = {
      summary: null,
      recommendations: [],
      used_llm_fallback: true,
      filter_match_count: 0,
    };

    const vm = buildPhase5ViewModel(result);

    expect(vm.emptyMessage).toBe("No recommendations to display.");
    expect(vm.showFallbackBanner).toBe(true);
  });
});
