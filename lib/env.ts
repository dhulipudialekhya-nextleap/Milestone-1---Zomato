/**
 * Vercel / local environment (see Docs/deployment-railway-vercel.md).
 * Only NEXT_PUBLIC_* vars are available in the browser.
 */

const DEFAULT_API_URL = "http://localhost:8000";

/**
 * Production browser calls use same-origin /api/* routes (Vercel proxies to Railway).
 * Local dev calls Railway/localhost directly unless NEXT_PUBLIC_USE_SAME_ORIGIN_API=true.
 */
export function useSameOriginApi(): boolean {
  if (process.env.NEXT_PUBLIC_USE_SAME_ORIGIN_API === "true") return true;
  return process.env.NODE_ENV === "production";
}

/** Client API base: "" in production (proxy), else NEXT_PUBLIC_API_URL or localhost. */
export function getApiBaseUrl(): string {
  if (useSameOriginApi()) return "";
  const raw = process.env.NEXT_PUBLIC_API_URL?.trim();
  return (raw || DEFAULT_API_URL).replace(/\/$/, "");
}

/** Demo on Railway without CSV: set NEXT_PUBLIC_USE_MOCK=true on Vercel. */
export function useMockData(): boolean {
  if (process.env.NEXT_PUBLIC_USE_MOCK === "true") return true;
  if (process.env.NEXT_PUBLIC_USE_MOCK === "false") return false;
  // Production works without Railway env — server route serves mock data
  if (process.env.NODE_ENV === "production") return true;
  return false;
}

export function isLocalApi(): boolean {
  const base = getApiBaseUrl();
  return base.includes("localhost") || base.includes("127.0.0.1");
}

/** True when Vercel prod has no Railway URL configured for the server proxy. */
export function isProductionApiMisconfigured(): boolean {
  return false;
}

/** Allow time for cold starts on hosted API tiers. */
export const API_REQUEST_TIMEOUT_MS = 90_000;

export function formatApiErrorHint(): string {
  if (isLocalApi()) {
    return "Is the backend running? Start it with: python -m src.backend.phase6.run_server";
  }
  if (useSameOriginApi()) {
    return "Set BACKEND_API_URL (or NEXT_PUBLIC_API_URL) on Vercel to your Railway URL, then redeploy.";
  }
  return `Check that the API is up at ${getApiBaseUrl()} (hosted backend may take a moment on first request).`;
}
