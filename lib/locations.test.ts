import { describe, expect, it } from "vitest";

import { BANGALORE_LOCATIONS, getAllLocationValues } from "./locations";

describe("locations", () => {
  it("only includes Bangalore areas", () => {
    expect(BANGALORE_LOCATIONS.length).toBeGreaterThan(0);
    expect(getAllLocationValues()).toContain("Koramangala");
    expect(getAllLocationValues()).toContain("Bellandur");
    expect(getAllLocationValues()).not.toContain("Mumbai");
    expect(getAllLocationValues()).not.toContain("Delhi");
  });
});
