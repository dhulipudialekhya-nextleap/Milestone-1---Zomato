import {
  buildApiRequestBody,
  ContractError,
  parseBackendResponse,
} from "./contract";
import {
  API_REQUEST_TIMEOUT_MS,
  formatApiErrorHint,
  getApiBaseUrl,
} from "./env";
import type { BackendResponse, RecommendationsRequest } from "./types";

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export async function checkApiHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${getApiBaseUrl()}/health`, {
      method: "GET",
      cache: "no-store",
    });
    if (!response.ok) return false;
    const body = (await response.json()) as { status?: string };
    return body.status === "ok";
  } catch {
    return false;
  }
}

export async function fetchRecommendations(
  payload: RecommendationsRequest,
): Promise<BackendResponse> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), API_REQUEST_TIMEOUT_MS);

  let response: Response;
  try {
    response = await fetch(`${getApiBaseUrl()}/api/recommendations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(buildApiRequestBody(payload)),
      signal: controller.signal,
    });
  } catch (error) {
    if (error instanceof Error && error.name === "AbortError") {
      throw new ApiError(
        `Request timed out. ${formatApiErrorHint()}`,
        408,
      );
    }
    throw new ApiError(
      `Could not reach the API. ${formatApiErrorHint()}`,
      0,
    );
  } finally {
    clearTimeout(timeoutId);
  }

  if (!response.ok) {
    throw new ApiError(
      `Backend request failed (${response.status}). ${formatApiErrorHint()}`,
      response.status,
    );
  }

  let json: unknown;
  try {
    json = await response.json();
  } catch {
    throw new ApiError("Backend returned invalid JSON.", response.status);
  }

  try {
    return parseBackendResponse(json);
  } catch (error) {
    const detail =
      error instanceof ContractError ? error.message : "Invalid response shape.";
    throw new ApiError(detail, response.status);
  }
}

export function downloadJson(filename: string, data: unknown): void {
  const blob = new Blob([JSON.stringify(data, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
}
