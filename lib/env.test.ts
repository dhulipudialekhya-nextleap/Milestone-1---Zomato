import { describe, expect, it, vi } from "vitest";

import { getApiBaseUrl, useMockData } from "./env";

describe("env", () => {
  it("strips trailing slash from API URL", () => {
    vi.stubEnv("NEXT_PUBLIC_API_URL", "https://api.example.com/");
    expect(getApiBaseUrl()).toBe("https://api.example.com");
    vi.unstubAllEnvs();
  });

  it("defaults to localhost when unset", () => {
    vi.stubEnv("NEXT_PUBLIC_API_URL", "");
    expect(getApiBaseUrl()).toBe("http://localhost:8000");
    vi.unstubAllEnvs();
  });

  it("reads mock flag from NEXT_PUBLIC_USE_MOCK", () => {
    vi.stubEnv("NEXT_PUBLIC_USE_MOCK", "true");
    expect(useMockData()).toBe(true);
    vi.unstubAllEnvs();
  });
});
