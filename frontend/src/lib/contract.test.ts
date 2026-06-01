import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";

import {
  CONTRACT_VERSION,
  buildApiRequestBody,
  parseBackendResponse,
} from "./contract";
import { DEFAULT_FORM_VALUES } from "./types";

const fixturesDir = join(process.cwd(), "..", "contracts", "v1", "fixtures");

function loadFixture<T>(name: string): T {
  return JSON.parse(
    readFileSync(join(fixturesDir, name), "utf-8"),
  ) as T;
}

describe("Phase 8 contract", () => {
  it("uses version 1.0.0", () => {
    expect(CONTRACT_VERSION).toBe("1.0.0");
  });

  it("parses success fixture", () => {
    const payload = loadFixture<unknown>("response_success.json");
    const parsed = parseBackendResponse(payload);
    expect(parsed.ok).toBe(true);
    if (parsed.ok) {
      expect(parsed.result.recommendations[0].name).toBe("Pasta Palace");
    }
  });

  it("parses validation error fixture", () => {
    const payload = loadFixture<unknown>("response_validation_error.json");
    const parsed = parseBackendResponse(payload);
    expect(parsed.ok).toBe(false);
    if (!parsed.ok) {
      expect(parsed.error_code).toBe("validation_error");
    }
  });

  it("builds normalized API request from form defaults", () => {
    const body = buildApiRequestBody({
      ...DEFAULT_FORM_VALUES,
      use_mock_data: true,
    });
    expect(body.location).toBe("Koramangala");
    expect(body.budget).toBe("medium");
    expect(body.cuisine).toBe("Indian");
    expect(body.extras).toBeNull();
    expect(body.use_mock_data).toBe(true);
  });

  it("rejects malformed responses", () => {
    expect(() => parseBackendResponse({ ok: true })).toThrow();
  });
});
