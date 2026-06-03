/**
 * Vercel / local environment (see Docs/deployment-railway-vercel.md).
 * Only NEXT_PUBLIC_* vars are available in the browser.
 */

const DEFAULT_API_URL = "http://localhost:8000";

/** Railway + Vercel: set NEXT_PUBLIC_API_URL in Vercel dashboard (no trailing slash). */
export function getApiBaseUrl(): string {
  const raw = process.env.NEXT_PUBLIC_API_URL?.trim();
  return (raw || DEFAULT_API_URL).replace(/\/$/, "");
}

/** Demo on Railway without CSV: set NEXT_PUBLIC_USE_MOCK=true on Vercel. */
export function useMockData(): boolean {
  return process.env.NEXT_PUBLIC_USE_MOCK === "true";
}

export function isLocalApi(): boolean {
  const base = getApiBaseUrl();
  return base.includes("localhost") || base.includes("127.0.0.1");
}

/** True when Vercel prod build has no NEXT_PUBLIC_API_URL (shows setup hint). */
export function isProductionApiMisconfigured(): boolean {
  return process.env.NODE_ENV === "production" && isLocalApi();
}

/** Allow time for cold starts on hosted API tiers. */
export const API_REQUEST_TIMEOUT_MS = 90_000;

export function formatApiErrorHint(): string {
  if (isLocalApi()) {
    return "Is the backend running? Start it with: python -m src.backend.phase6.run_server";
  }
  return `Check that the API is up at ${getApiBaseUrl()} (hosted backend may take a moment on first request).`;
}
