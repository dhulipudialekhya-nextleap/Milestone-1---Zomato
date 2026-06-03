import { NextRequest, NextResponse } from "next/server";

import {
  getBackendConfigError,
  getServerBackendApiUrl,
} from "@/lib/serverBackendUrl";

export const runtime = "nodejs";

/** Proxies POST /api/recommendations → Railway FastAPI (avoids 404 on Vercel). */
export async function POST(request: NextRequest) {
  const configError = getBackendConfigError();
  if (configError) {
    return NextResponse.json({ detail: configError }, { status: 503 });
  }

  const backend = getServerBackendApiUrl();
  const body = await request.text();

  let upstream: Response;
  try {
    upstream = await fetch(`${backend}/api/recommendations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body,
      cache: "no-store",
    });
  } catch {
    return NextResponse.json(
      {
        detail: `Could not reach backend at ${backend}. Check Railway is running and BACKEND_API_URL is correct.`,
      },
      { status: 502 },
    );
  }

  const text = await upstream.text();
  return new NextResponse(text, {
    status: upstream.status,
    headers: {
      "Content-Type":
        upstream.headers.get("Content-Type") ?? "application/json",
    },
  });
}
