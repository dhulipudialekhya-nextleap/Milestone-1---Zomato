/**
 * Server-only Railway/backend URL validation.
 */

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

export { getServerBackendApiUrl, hasConfiguredBackend } from "./backendRouting";

export function getBackendConfigError(): string | null {
  const candidates = [
    process.env.BACKEND_API_URL,
    process.env.NEXT_PUBLIC_API_URL,
  ].filter(Boolean) as string[];

  for (const value of candidates) {
    const base = normalizeBaseUrl(value);
    if (isInvalidBackendUrl(base)) {
      return "BACKEND_API_URL must be your Railway API URL, not your Vercel website URL.";
    }
  }

  return null;
}
