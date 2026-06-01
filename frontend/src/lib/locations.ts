/** Bangalore area options for the location filter (no city headings). */

export const BANGALORE_LOCATIONS: readonly string[] = [
  "Koramangala",
  "Indiranagar",
  "HSR",
  "BTM",
  "Whitefield",
  "Bellandur",
  "Jayanagar",
  "Marathahalli",
  "Electronic City",
  "MG Road",
  "Brigade Road",
  "Sarjapur Road",
  "Banashankari",
  "Frazer Town",
  "Malleshwaram",
] as const;

export function getAllLocationValues(): string[] {
  return [...BANGALORE_LOCATIONS];
}

export function isValidLocation(value: string): boolean {
  return BANGALORE_LOCATIONS.includes(value as (typeof BANGALORE_LOCATIONS)[number]);
}
