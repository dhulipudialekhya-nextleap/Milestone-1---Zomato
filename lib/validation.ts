/**
 * Client-side UX validation only — backend remains source of truth.
 */

import { BUDGET_OPTIONS } from "./designConstants";
import { getAllLocationValues } from "./locations";
import { type FieldErrors, type PreferenceFormValues } from "./types";

export function validatePreferenceForm(
  values: PreferenceFormValues,
): FieldErrors {
  const errors: FieldErrors = {};

  if (!values.location.trim()) {
    errors.location = "Location is required.";
  } else if (!getAllLocationValues().includes(values.location.trim())) {
    errors.location = "Please select a location from the list.";
  }

  const cuisine =
    values.cuisine === "Any Cuisine" ? "Indian" : values.cuisine.trim();
  if (!cuisine) {
    errors.cuisine = "Preferred cuisine is required.";
  } else if (cuisine.length > 100) {
    errors.cuisine = "Cuisine must be 100 characters or fewer.";
  }

  if (!BUDGET_OPTIONS.some((option) => option.value === values.budget)) {
    errors.budget = "Please select a valid budget range.";
  }

  if (values.min_rating < 0 || values.min_rating > 5) {
    errors.min_rating = "Minimum rating must be between 0 and 5.";
  }

  if (values.extras.trim().length > 500) {
    errors.extras = "Additional preferences must be 500 characters or fewer.";
  }

  return errors;
}

export function hasFieldErrors(errors: FieldErrors): boolean {
  return Object.keys(errors).length > 0;
}

export function normalizeCuisine(cuisine: string): string {
  return cuisine === "Any Cuisine" ? "Indian" : cuisine.trim();
}

export function normalizeExtras(extras: string): string {
  return extras === "Anything delicious" ? "" : extras.trim();
}
