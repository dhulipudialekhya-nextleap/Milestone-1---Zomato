import { describe, expect, it } from "vitest";

import { buildMockRecommendations } from "./mockRecommendations";

describe("mockRecommendations", () => {
  it("returns contract-shaped success for Koramangala", () => {
    const response = buildMockRecommendations({
      location: "Koramangala",
      budget: "medium",
      cuisine: "Italian",
      min_rating: 4.0,
      extras: null,
      use_mock_data: true,
    });

    expect(response.ok).toBe(true);
    if (!response.ok) return;
    expect(response.result.recommendations.length).toBeGreaterThan(0);
    expect(response.result.recommendations[0].name).toContain("Trattoria");
  });
});
