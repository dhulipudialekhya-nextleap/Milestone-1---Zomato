"use client";

import { useRef } from "react";

import { RecommendationCard } from "@/components/RecommendationCard";
import type { PresentableRecommendation } from "@/lib/types";

interface PersonalizedPicksProps {
  items: PresentableRecommendation[];
  summary: string | null;
  showFallbackBanner: boolean;
  emptyMessage: string | null;
  isLiveResults: boolean;
}

export function PersonalizedPicks({
  items,
  summary,
  showFallbackBanner,
  emptyMessage,
  isLiveResults,
}: PersonalizedPicksProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  const scroll = (direction: "left" | "right") => {
    const node = scrollRef.current;
    if (!node) {
      return;
    }
    node.scrollBy({ left: direction === "left" ? -280 : 280, behavior: "smooth" });
  };

  if (emptyMessage && isLiveResults) {
    return (
      <section className="mt-8 rounded-2xl border border-amber-200 bg-amber-50 px-5 py-6 text-sm text-amber-900">
        No restaurants matched your filters. Try a different location, cuisine, or lower
        the minimum rating.
      </section>
    );
  }

  const visibleItems = items.slice(0, 4);

  return (
    <section className="mt-8">
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-[32px] font-bold leading-tight text-ink">
          Personalized Picks for You
        </h2>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => scroll("left")}
            className="flex h-10 w-10 items-center justify-center rounded-full border border-brand-border bg-white text-ink-muted transition hover:shadow-card"
            aria-label="Scroll left"
          >
            <svg viewBox="0 0 24 24" className="h-5 w-5" fill="currentColor">
              <path d="M15 18l-6-6 6-6" />
            </svg>
          </button>
          <button
            type="button"
            onClick={() => scroll("right")}
            className="flex h-10 w-10 items-center justify-center rounded-full border border-brand-border bg-white text-ink-muted transition hover:shadow-card"
            aria-label="Scroll right"
          >
            <svg viewBox="0 0 24 24" className="h-5 w-5" fill="currentColor">
              <path d="M9 18l6-6-6-6" />
            </svg>
          </button>
        </div>
      </div>

      {showFallbackBanner ? (
        <div className="mb-4 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900">
          AI unavailable — showing filter-based results.
        </div>
      ) : null}

      {summary && isLiveResults ? (
        <div className="mb-4 rounded-xl border border-sky-200 bg-sky-50 px-4 py-3 text-sm text-sky-900">
          {summary}
        </div>
      ) : null}

      <div
        ref={scrollRef}
        className="custom-scrollbar -mx-1 grid grid-cols-1 gap-6 overflow-x-auto px-1 pb-2 sm:grid-cols-2 lg:grid-cols-4 lg:overflow-visible"
      >
        {visibleItems.map((item) => (
          <RecommendationCard
            key={`${item.rank}-${item.name}`}
            item={item}
            showExplanation={false}
          />
        ))}
      </div>
    </section>
  );
}
