/**
 * Server-only Railway/backend URL for Vercel API route proxies.
 * Set BACKEND_API_URL or NEXT_PUBLIC_API_URL to your Railway public domain.
 */

const DEFAULT_BACKEND_URL = "http://localhost:8000";

function normalizeBaseUrl(raw: string): string {
  return raw.trim().replace(/\/$/, "");
}

/** Reject Vercel (or other frontend) URLs mistakenly used as the API base. */
export function isInvalidBackendUrl(url: string): boolean {
  try {
    const host = new URL(url).hostname.toLowerCase();
    return host.endsWith(".vercel.app") || host === "vercel.app";
  } catch {
    return true;
  }
}

export function getServerBackendApiUrl(): string {
  const candidates = [
    process.env.BACKEND_API_URL,
    process.env.NEXT_PUBLIC_API_URL,
  ];

  for (const value of candidates) {
    if (!value?.trim()) continue;
    const base = normalizeBaseUrl(value);
    if (!isInvalidBackendUrl(base)) return base;
  }

  return DEFAULT_BACKEND_URL;
}

export function getBackendConfigError(): string | null {
  const candidates = [
    process.env.BACKEND_API_URL,
    process.env.NEXT_PUBLIC_API_URL,
  ].filter(Boolean) as string[];

  if (candidates.length === 0) {
    return "Set BACKEND_API_URL (or NEXT_PUBLIC_API_URL) on Vercel to your Railway URL, e.g. https://your-service.up.railway.app";
  }

  for (const value of candidates) {
    const base = normalizeBaseUrl(value);
    if (isInvalidBackendUrl(base)) {
      return "BACKEND_API_URL must be your Railway API URL, not your Vercel website URL.";
    }
  }

  return null;
}
