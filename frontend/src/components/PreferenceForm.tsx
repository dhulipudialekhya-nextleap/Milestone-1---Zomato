import {
  BUDGET_OPTIONS,
  CRAVING_OPTIONS,
  CUISINE_OPTIONS,
} from "@/lib/designConstants";
import { BANGALORE_LOCATIONS } from "@/lib/locations";
import type { FieldErrors, PreferenceFormValues } from "@/lib/types";

interface PreferenceFormProps {
  values: PreferenceFormValues;
  errors: FieldErrors;
  disabled: boolean;
  onChange: (values: PreferenceFormValues) => void;
  onSubmit: () => void;
}

function FieldError({ message }: { message?: string }) {
  if (!message) {
    return null;
  }
  return <p className="mt-1 text-xs text-red-600">{message}</p>;
}

function FieldLabel({ htmlFor, children }: { htmlFor: string; children: React.ReactNode }) {
  return (
    <label
      htmlFor={htmlFor}
      className="mb-2 block text-xs font-semibold uppercase tracking-wider text-ink-muted"
    >
      {children}
    </label>
  );
}

const selectClass =
  "select-field active-ring w-full appearance-none rounded-xl border border-brand-border px-4 py-3 text-sm text-ink outline-none transition input-surface focus:border-brand disabled:opacity-60";

export function PreferenceForm({
  values,
  errors,
  disabled,
  onChange,
  onSubmit,
}: PreferenceFormProps) {
  const update = <K extends keyof PreferenceFormValues>(
    key: K,
    value: PreferenceFormValues[K],
  ) => {
    onChange({ ...values, [key]: value });
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    onSubmit();
  };

  const cravingValue =
    CRAVING_OPTIONS.find((option) => values.extras === option || values.extras.includes(option)) ??
    (values.extras ? values.extras : "Anything delicious");

  const ratingProgress = `${((values.min_rating - 3) / 2) * 100}%`;

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-2xl border border-brand-border bg-white p-6 shadow-card transition hover:shadow-card-hover sm:p-8"
    >
      {errors.form ? (
        <div className="mb-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {errors.form}
        </div>
      ) : null}

      <div className="grid gap-6 md:grid-cols-2">
        <div className="md:col-span-2">
          <FieldLabel htmlFor="location">Location</FieldLabel>
          <select
            id="location"
            value={values.location}
            disabled={disabled}
            onChange={(event) => update("location", event.target.value)}
            className={selectClass}
          >
            {BANGALORE_LOCATIONS.map((place) => (
              <option key={place} value={place}>
                {place}
              </option>
            ))}
          </select>
          <FieldError message={errors.location} />
        </div>

        <div>
          <FieldLabel htmlFor="cuisine">Cuisine Style</FieldLabel>
          <select
            id="cuisine"
            value={values.cuisine}
            disabled={disabled}
            onChange={(event) => update("cuisine", event.target.value)}
            className={selectClass}
          >
            {CUISINE_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
          <FieldError message={errors.cuisine} />
        </div>

        <div>
          <FieldLabel htmlFor="budget">Budget Range (INR)</FieldLabel>
          <select
            id="budget"
            value={values.budget}
            disabled={disabled}
            onChange={(event) => update("budget", event.target.value)}
            className={selectClass}
          >
            {BUDGET_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          <FieldError message={errors.budget} />
        </div>

        <div>
          <FieldLabel htmlFor="min_rating">Minimum Rating</FieldLabel>
          <div className="flex items-center gap-4 py-2">
            <input
              id="min_rating"
              type="range"
              min={3}
              max={5}
              step={0.5}
              value={values.min_rating}
              disabled={disabled}
              style={{ "--range-progress": ratingProgress } as React.CSSProperties}
              onChange={(event) => update("min_rating", Number(event.target.value))}
              className="w-full cursor-pointer disabled:opacity-50"
            />
            <span className="min-w-[3.5ch] text-sm font-bold text-brand">
              {values.min_rating.toFixed(1)}+
            </span>
          </div>
          <FieldError message={errors.min_rating} />
        </div>

        <div>
          <FieldLabel htmlFor="extras">Specific Cravings</FieldLabel>
          <select
            id="extras"
            value={cravingValue}
            disabled={disabled}
            onChange={(event) =>
              update(
                "extras",
                event.target.value === "Anything delicious" ? "" : event.target.value,
              )
            }
            className={selectClass}
          >
            {CRAVING_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
          <FieldError message={errors.extras} />
        </div>

        <div className="md:col-span-2 mt-2">
          <button
            type="submit"
            disabled={disabled}
            className="flex w-full items-center justify-center gap-3 rounded-xl bg-brand px-12 py-4 text-base font-semibold text-white shadow-card-hover transition hover:bg-brand-dark active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60 md:w-auto"
          >
            <svg viewBox="0 0 24 24" className="h-5 w-5" fill="currentColor" aria-hidden="true">
              <path d="M12 2a2 2 0 012 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 017 7h1a1 1 0 011 1v3a1 1 0 01-1 1h-1v1a2 2 0 01-2 2H5a2 2 0 01-2-2v-1H2a1 1 0 01-1-1v-3a1 1 0 011-1h1a7 7 0 017-7h1V5.73A2 2 0 0112 2z" />
            </svg>
            Get Recommendations
          </button>
        </div>
      </div>
    </form>
  );
}
