import { describe, expect, it, vi } from "vitest";

import {
  getServerBackendApiUrl,
  isInvalidBackendUrl,
} from "./serverBackendUrl";

describe("serverBackendUrl", () => {
  it("rejects vercel.app as backend", () => {
    expect(
      isInvalidBackendUrl("https://milestone-1-zomato.vercel.app"),
    ).toBe(true);
  });

  it("prefers BACKEND_API_URL over NEXT_PUBLIC", () => {
    vi.stubEnv("BACKEND_API_URL", "https://api.railway.test/");
    vi.stubEnv("NEXT_PUBLIC_API_URL", "https://other.test");
    expect(getServerBackendApiUrl()).toBe("https://api.railway.test");
    vi.unstubAllEnvs();
  });
});
