import { NextRequest, NextResponse } from "next/server";

import {
  getServerBackendApiUrl,
  hasConfiguredBackend,
  shouldUseMockFallback,
} from "@/lib/backendRouting";
import type { ApiRecommendationsRequest } from "@/lib/contract";
import { buildMockRecommendations } from "@/lib/mockRecommendations";

export const runtime = "nodejs";

function parseRequestBody(bodyText: string): ApiRecommendationsRequest | null {
  try {
    return JSON.parse(bodyText) as ApiRecommendationsRequest;
  } catch {
    return null;
  }
}

/** Proxies to Railway when configured; otherwise returns in-app mock recommendations. */
export async function POST(request: NextRequest) {
  const bodyText = await request.text();
  const payload = parseRequestBody(bodyText);

  if (!payload?.location?.trim()) {
    return NextResponse.json(
      {
        ok: false,
        error_code: "validation_error",
        message: "location is required",
      },
      { status: 400 },
    );
  }

  if (shouldUseMockFallback(payload)) {
    return NextResponse.json(buildMockRecommendations(payload));
  }

  const backend = getServerBackendApiUrl();

  try {
    const upstream = await fetch(`${backend}/api/recommendations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: bodyText,
      cache: "no-store",
    });

    if (upstream.ok) {
      const text = await upstream.text();
      return new NextResponse(text, {
        status: upstream.status,
        headers: {
          "Content-Type":
            upstream.headers.get("Content-Type") ?? "application/json",
        },
      });
    }

    if (!hasConfiguredBackend()) {
      return NextResponse.json(buildMockRecommendations(payload));
    }
  } catch {
    if (!hasConfiguredBackend()) {
      return NextResponse.json(buildMockRecommendations(payload));
    }
  }

  return NextResponse.json(
    {
      detail: `Could not reach backend at ${backend}. Using mock is automatic when Railway URL is not set.`,
    },
    { status: 502 },
  );
}
