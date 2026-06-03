"use client";

import {
  POPULAR_SEARCH_OPTIONS,
  STITCH_IMAGES,
} from "@/lib/designConstants";

const CATEGORY_GRID = [
  { label: "Ice Cream", image: STITCH_IMAGES.iceCream, cuisine: "Ice Cream" },
  { label: "Sweets", image: STITCH_IMAGES.sweets, cuisine: "Sweets" },
  { label: "Juices", image: STITCH_IMAGES.juices, cuisine: "Juices" },
  { label: "Waffles", image: STITCH_IMAGES.waffles, cuisine: "Waffles" },
  {
    label: "Cakes",
    image: STITCH_IMAGES.cakes,
    cuisine: "Bakery",
    wide: true,
  },
] as const;

interface PopularSearchesProps {
  selectedCategory: string;
  onSelectCategory: (category: string, cuisine: string) => void;
}

export function PopularSearches({
  selectedCategory,
  onSelectCategory,
}: PopularSearchesProps) {
  return (
    <aside className="flex flex-col gap-4">
      <h2 className="px-2 text-xs font-semibold uppercase tracking-widest text-ink-muted">
        Popular Searches
      </h2>

      <select
        value={selectedCategory}
        onChange={(event) => {
          const label = event.target.value;
          const match = CATEGORY_GRID.find((item) => item.label === label);
          onSelectCategory(label, match?.cuisine ?? label);
        }}
        className="select-field active-ring mx-2 w-[calc(100%-1rem)] appearance-none rounded-xl border border-brand-border px-4 py-2 text-sm input-surface outline-none focus:border-brand"
      >
        {POPULAR_SEARCH_OPTIONS.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>

      <div className="grid grid-cols-2 gap-3 px-2">
        {CATEGORY_GRID.map((category) => (
          <button
            key={category.label}
            type="button"
            onClick={() => onSelectCategory(category.label, category.cuisine)}
            className={`flex flex-col gap-1.5 text-left ${
              "wide" in category && category.wide ? "col-span-2" : ""
            }`}
          >
            <div
              className={`overflow-hidden rounded-lg ${
                "wide" in category && category.wide ? "aspect-video" : "aspect-square"
              }`}
            >
              <img
                src={category.image}
                alt={category.label}
                loading="lazy"
                className="h-full w-full object-cover transition duration-500 hover:scale-105"
                onError={(event) => {
                  const img = event.currentTarget;
                  if (img.dataset.fallbackApplied) return;
                  img.dataset.fallbackApplied = "1";
                  img.src = STITCH_IMAGES.sweets;
                }}
              />
            </div>
            <span className="text-center text-[10px] font-bold uppercase tracking-tighter text-ink-muted">
              {category.label}
            </span>
          </button>
        ))}
      </div>
    </aside>
  );
}
