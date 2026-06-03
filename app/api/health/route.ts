import { NextResponse } from "next/server";

/** Vercel smoke test — GET /api/health should return 200 JSON */
export async function GET() {
  return NextResponse.json({
    status: "ok",
    service: "zomato-ai-frontend",
    routes: ["/", "/login", "/signup"],
  });
}
