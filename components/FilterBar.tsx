"use client";

const FILTERS = [
  "Veg",
  "Non-Veg",
  "New to You",
  "Great Offers",
  "Previously Ordered",
  "No Packaging Charges",
] as const;

interface FilterBarProps {
  activeFilters: string[];
  onToggleFilter: (filter: string) => void;
}

export function FilterBar({ activeFilters, onToggleFilter }: FilterBarProps) {
  return (
    <div className="mt-8 flex flex-col gap-4">
      <h2 className="px-2 text-xs font-semibold uppercase tracking-widest text-ink-muted">
        Filters
      </h2>
      <div className="custom-scrollbar flex flex-wrap items-center gap-3">
        {FILTERS.map((filter) => {
          const active = activeFilters.includes(filter);
          return (
            <button
              key={filter}
              type="button"
              onClick={() => onToggleFilter(filter)}
              className={`shrink-0 rounded-full border px-6 py-2 text-sm transition ${
                active
                  ? "border-brand bg-brand text-white"
                  : "border-brand-border bg-white text-ink hover:border-brand hover:text-brand"
              }`}
            >
              {filter}
            </button>
          );
        })}

        <div className="group relative shrink-0">
          <button
            type="button"
            className="flex items-center gap-2 rounded-full border border-brand-border bg-white px-6 py-2 text-sm text-ink transition hover:border-brand hover:text-brand"
          >
            Sort by
            <svg viewBox="0 0 24 24" className="h-4 w-4" fill="currentColor" aria-hidden="true">
              <path d="M7 10l5 5 5-5H7z" />
            </svg>
          </button>
          <div className="invisible absolute left-0 top-full z-10 mt-2 w-56 rounded-xl border border-brand-border bg-white py-2 opacity-0 shadow-card-hover transition group-hover:visible group-hover:opacity-100">
            {["Distance: Low to High", "Rating: Low to High", "Price Range: Low to High"].map(
              (option) => (
                <button
                  key={option}
                  type="button"
                  className="block w-full px-4 py-2 text-left text-sm text-ink hover:bg-surface-container"
                  disabled
                >
                  {option}
                </button>
              ),
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
