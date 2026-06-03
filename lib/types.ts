/** Phase 7 UI types; API contract types live in contract.ts (Phase 8). */

import type { BudgetBand } from "./contract";

export type {
  ApiRecommendationsRequest,
  BackendErrorResponse,
  BackendResponse,
  BackendSuccessResponse,
  BudgetBand,
  ErrorCode,
  RecommendationItem,
  RecommendationResult,
  RecommendationsRequest,
} from "./contract";

export interface PreferenceFormValues {
  location: string;
  budget: string;
  cuisine: string;
  min_rating: number;
  extras: string;
}

export interface PresentableRecommendation {
  rank: number;
  name: string;
  cuisinesText: string;
  ratingText: string;
  estimatedCostText: string;
  explanation: string;
  imageUrl?: string;
}

export interface Phase5ViewModel {
  title: string;
  summary: string | null;
  showFallbackBanner: boolean;
  emptyMessage: string | null;
  filterMatchCount: number;
  items: PresentableRecommendation[];
}

export type UiStatus = "idle" | "loading" | "success" | "error";

export interface FieldErrors {
  location?: string;
  cuisine?: string;
  budget?: string;
  min_rating?: string;
  extras?: string;
  form?: string;
}

export const DEFAULT_FORM_VALUES: PreferenceFormValues = {
  location: "Koramangala",
  budget: "1000-2000",
  cuisine: "Any Cuisine",
  min_rating: 4.0,
  extras: "",
};

export const VALID_BUDGETS: BudgetBand[] = ["low", "medium", "high"];

export const DISPLAY_TOP_K = 5;
