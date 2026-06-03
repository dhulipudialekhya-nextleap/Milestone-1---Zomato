import type { ApiRecommendationsRequest } from "./contract";
import { isInvalidBackendUrl } from "./serverBackendUrl";

function normalizeBaseUrl(raw: string): string {
  return raw.trim().replace(/\/$/, "");
}

function firstValidBackendUrl(): string | null {
  for (const value of [
    process.env.BACKEND_API_URL,
    process.env.NEXT_PUBLIC_API_URL,
  ]) {
    if (!value?.trim()) continue;
    const base = normalizeBaseUrl(value);
    if (!isInvalidBackendUrl(base)) return base;
  }
  return null;
}

/** True when a Railway (or local) backend URL is configured for proxying. */
export function hasConfiguredBackend(): boolean {
  return firstValidBackendUrl() !== null;
}

export function getServerBackendApiUrl(): string {
  return firstValidBackendUrl() ?? "http://localhost:8000";
}

export function shouldUseMockFallback(
  request: ApiRecommendationsRequest,
): boolean {
  if (request.use_mock_data) return true;
  if (process.env.NEXT_PUBLIC_USE_MOCK === "true") return true;
  if (process.env.FORCE_MOCK_RECOMMENDATIONS === "true") return true;
  return !hasConfiguredBackend();
}
