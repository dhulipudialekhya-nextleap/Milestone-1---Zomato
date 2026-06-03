import { describe, expect, it, vi } from "vitest";

import { getApiBaseUrl, useMockData, useSameOriginApi } from "./env";

describe("env", () => {
  it("strips trailing slash from API URL", () => {
    vi.stubEnv("NODE_ENV", "development");
    vi.stubEnv("NEXT_PUBLIC_API_URL", "https://api.example.com/");
    expect(getApiBaseUrl()).toBe("https://api.example.com");
    vi.unstubAllEnvs();
  });

  it("defaults to localhost when unset", () => {
    vi.stubEnv("NODE_ENV", "development");
    vi.stubEnv("NEXT_PUBLIC_API_URL", "");
    expect(getApiBaseUrl()).toBe("http://localhost:8000");
    vi.unstubAllEnvs();
  });

  it("reads mock flag from NEXT_PUBLIC_USE_MOCK", () => {
    vi.stubEnv("NEXT_PUBLIC_USE_MOCK", "true");
    expect(useMockData()).toBe(true);
    vi.unstubAllEnvs();
  });

  it("uses same-origin API in production", () => {
    vi.stubEnv("NODE_ENV", "production");
    expect(useSameOriginApi()).toBe(true);
    expect(getApiBaseUrl()).toBe("");
    vi.unstubAllEnvs();
  });
});
