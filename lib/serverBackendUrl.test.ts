import { describe, expect, it, vi } from "vitest";

import {
  getServerBackendApiUrl,
  hasConfiguredBackend,
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
    expect(hasConfiguredBackend()).toBe(true);
    vi.unstubAllEnvs();
  });

  it("has no backend when only vercel url is set", () => {
    vi.stubEnv("NEXT_PUBLIC_API_URL", "https://app.vercel.app");
    expect(hasConfiguredBackend()).toBe(false);
    vi.unstubAllEnvs();
  });
});
