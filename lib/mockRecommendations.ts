import type {
  ApiRecommendationsRequest,
  BackendSuccessResponse,
  BudgetBand,
  RecommendationItem,
} from "./contract";

interface MockRestaurant {
  id: string;
  name: string;
  location: string;
  cuisines: string[];
  average_cost: number;
  cost_band: BudgetBand;
  rating: number;
}

/** Mirrors src/data/loader.py mock dataset (Bangalore locations). */
const MOCK_RESTAURANTS: MockRestaurant[] = [
  {
    id: "mock-1",
    name: "Trattoria Koramangala",
    location: "Koramangala",
    cuisines: ["Italian", "Continental"],
    average_cost: 800,
    cost_band: "medium",
    rating: 4.5,
  },
  {
    id: "mock-2",
    name: "Spice Route HSR",
    location: "HSR",
    cuisines: ["North Indian", "Chinese"],
    average_cost: 600,
    cost_band: "medium",
    rating: 4.3,
  },
  {
    id: "mock-3",
    name: "Indiranagar Tandoor House",
    location: "Indiranagar",
    cuisines: ["North Indian", "Mughlai"],
    average_cost: 700,
    cost_band: "medium",
    rating: 4.4,
  },
  {
    id: "mock-4",
    name: "Bellandur Biryani Co.",
    location: "Bellandur",
    cuisines: ["Biryani", "Hyderabadi"],
    average_cost: 500,
    cost_band: "low",
    rating: 4.2,
  },
  {
    id: "mock-5",
    name: "Whitefield Wok",
    location: "Whitefield",
    cuisines: ["Chinese", "Asian"],
    average_cost: 450,
    cost_band: "low",
    rating: 4.1,
  },
  {
    id: "mock-6",
    name: "BTM Budget Meals",
    location: "BTM",
    cuisines: ["South Indian", "Fast Food"],
    average_cost: 300,
    cost_band: "low",
    rating: 4.0,
  },
];

function matchesCuisine(restaurant: MockRestaurant, cuisine: string): boolean {
  const needle = cuisine.trim().toLowerCase();
  if (!needle || needle === "any cuisine") return true;
  return restaurant.cuisines.some((c) => c.toLowerCase().includes(needle));
}

function matchesBudget(restaurant: MockRestaurant, budget: BudgetBand): boolean {
  return restaurant.cost_band === budget;
}

function buildExplanation(
  restaurant: MockRestaurant,
  request: ApiRecommendationsRequest,
): string {
  const cuisine = request.cuisine === "Any Cuisine" ? "your taste" : request.cuisine;
  return `Great ${restaurant.cuisines[0]} spot in ${restaurant.location} — matches ${cuisine} with rating ${restaurant.rating}+.`;
}

/** Demo recommendations when Railway is unavailable or use_mock_data is true. */
export function buildMockRecommendations(
  request: ApiRecommendationsRequest,
): BackendSuccessResponse {
  const locationNeedle = request.location.trim().toLowerCase();

  let matches = MOCK_RESTAURANTS.filter(
    (r) =>
      r.location.toLowerCase().includes(locationNeedle) &&
      r.rating >= request.min_rating &&
      matchesCuisine(r, request.cuisine) &&
      matchesBudget(r, request.budget),
  );

  if (matches.length === 0) {
    matches = MOCK_RESTAURANTS.filter(
      (r) =>
        r.rating >= request.min_rating &&
        matchesCuisine(r, request.cuisine),
    );
  }

  if (matches.length === 0) {
    matches = [...MOCK_RESTAURANTS];
  }

  const top = matches.slice(0, 5);
  const recommendations: RecommendationItem[] = top.map((r, index) => ({
    rank: index + 1,
    restaurant_id: r.id,
    name: r.name,
    explanation: buildExplanation(r, request),
    cuisines: r.cuisines,
    rating: r.rating,
    average_cost: r.average_cost,
    cost_band: r.cost_band,
  }));

  const cuisineLabel =
    request.cuisine === "Any Cuisine" ? "restaurants" : request.cuisine;

  return {
    ok: true,
    result: {
      summary: `Top ${cuisineLabel} picks near ${request.location} (demo mock data).`,
      recommendations,
      used_llm_fallback: true,
      filter_match_count: matches.length,
    },
  };
}
