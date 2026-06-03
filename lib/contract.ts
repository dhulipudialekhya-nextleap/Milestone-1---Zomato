/**
 * Phase 8 — frontend-backend API contract.
 * Keep in sync with src/backend/phase8/ and contracts/v1/.
 */

import { budgetValueToBand } from "./designConstants";
import { normalizeCuisine, normalizeExtras } from "./validation";
import type { PreferenceFormValues } from "./types";

export const CONTRACT_VERSION = "1.0.0";

export type BudgetBand = "low" | "medium" | "high";

export const ERROR_CODES = [
  "validation_error",
  "config_error",
  "runtime_error",
] as const;

export type ErrorCode = (typeof ERROR_CODES)[number];

/** POST /api/recommendations request body (after client normalization). */
export interface ApiRecommendationsRequest {
  location: string;
  budget: BudgetBand;
  cuisine: string;
  min_rating: number;
  extras: string | null;
  use_mock_data: boolean;
}

export interface RecommendationItem {
  rank: number;
  restaurant_id: string;
  name: string;
  explanation: string;
  cuisines: string[];
  rating: number | null;
  average_cost: number | null;
  cost_band: string | null;
}

export interface RecommendationResult {
  summary: string | null;
  recommendations: RecommendationItem[];
  used_llm_fallback: boolean;
  filter_match_count: number;
}

export interface BackendSuccessResponse {
  ok: true;
  result: RecommendationResult;
}

export interface BackendErrorResponse {
  ok: false;
  error_code: ErrorCode;
  message: string;
}

export type BackendResponse = BackendSuccessResponse | BackendErrorResponse;

export interface RecommendationsRequest extends PreferenceFormValues {
  use_mock_data?: boolean;
}

export class ContractError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ContractError";
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isBudgetBand(value: unknown): value is BudgetBand {
  return value === "low" || value === "medium" || value === "high";
}

function isErrorCode(value: unknown): value is ErrorCode {
  return (
    typeof value === "string" &&
    (ERROR_CODES as readonly string[]).includes(value)
  );
}

function isRecommendationItem(value: unknown): value is RecommendationItem {
  if (!isRecord(value)) return false;
  return (
    typeof value.rank === "number" &&
    typeof value.restaurant_id === "string" &&
    typeof value.name === "string" &&
    typeof value.explanation === "string" &&
    Array.isArray(value.cuisines) &&
    value.cuisines.every((c) => typeof c === "string") &&
    (value.rating === null || typeof value.rating === "number") &&
    (value.average_cost === null || typeof value.average_cost === "number") &&
    (value.cost_band === null || typeof value.cost_band === "string")
  );
}

function isRecommendationResult(value: unknown): value is RecommendationResult {
  if (!isRecord(value)) return false;
  return (
    (value.summary === null || typeof value.summary === "string") &&
    Array.isArray(value.recommendations) &&
    value.recommendations.every(isRecommendationItem) &&
    typeof value.used_llm_fallback === "boolean" &&
    typeof value.filter_match_count === "number"
  );
}

export function isBackendSuccessResponse(
  value: unknown,
): value is BackendSuccessResponse {
  return (
    isRecord(value) &&
    value.ok === true &&
    isRecommendationResult(value.result)
  );
}

export function isBackendErrorResponse(
  value: unknown,
): value is BackendErrorResponse {
  return (
    isRecord(value) &&
    value.ok === false &&
    isErrorCode(value.error_code) &&
    typeof value.message === "string"
  );
}

/** Parse and validate POST /api/recommendations JSON (Phase 8 contract). */
export function parseBackendResponse(payload: unknown): BackendResponse {
  if (isBackendSuccessResponse(payload) || isBackendErrorResponse(payload)) {
    return payload;
  }
  throw new ContractError("Response does not match the API contract.");
}

/** Build normalized request body from form values. */
export function buildApiRequestBody(
  payload: RecommendationsRequest,
): ApiRecommendationsRequest {
  return {
    location: payload.location.trim(),
    budget: budgetValueToBand(payload.budget),
    cuisine: normalizeCuisine(payload.cuisine),
    min_rating: payload.min_rating,
    extras: normalizeExtras(payload.extras) || null,
    use_mock_data: payload.use_mock_data ?? false,
  };
}
