import {
  buildApiRequestBody,
  ContractError,
  parseBackendResponse,
} from "./contract";
import type { BackendResponse, RecommendationsRequest } from "./types";

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ?? "http://localhost:8000";

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export async function fetchRecommendations(
  payload: RecommendationsRequest,
): Promise<BackendResponse> {
  const response = await fetch(`${API_BASE}/api/recommendations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(buildApiRequestBody(payload)),
  });

  if (!response.ok) {
    throw new ApiError(
      `Backend request failed (${response.status})`,
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
