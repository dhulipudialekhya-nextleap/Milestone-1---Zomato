import { STITCH_IMAGES } from "@/lib/designConstants";
import type { PresentableRecommendation } from "@/lib/types";

const FALLBACK_IMAGES = [
  STITCH_IMAGES.butterChicken,
  STITCH_IMAGES.masalaDosa,
  STITCH_IMAGES.muttonBiryani,
  STITCH_IMAGES.paneerTikka,
];

interface RecommendationCardProps {
  item: PresentableRecommendation;
  showExplanation?: boolean;
}

export function RecommendationCard({
  item,
  showExplanation = false,
}: RecommendationCardProps) {
  const image =
    item.imageUrl ?? FALLBACK_IMAGES[(item.rank - 1) % FALLBACK_IMAGES.length];

  return (
    <article className="group cursor-pointer overflow-hidden rounded-2xl border border-brand-border bg-white shadow-card transition hover:shadow-card-hover">
      <div className="aspect-square overflow-hidden">
        <img
          src={image}
          alt={item.name}
          className="h-full w-full object-cover transition duration-500 group-hover:scale-110"
        />
      </div>
      <div className="flex flex-col gap-1 p-4">
        <div className="flex items-start justify-between gap-2">
          <h3 className="text-sm font-bold text-ink">{item.name}</h3>
          <div className="flex shrink-0 items-center gap-1 text-brand">
            <svg viewBox="0 0 24 24" className="h-4 w-4 fill-brand" aria-hidden="true">
              <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
            </svg>
            <span className="text-xs font-bold">{item.ratingText}</span>
          </div>
        </div>
        <p className="text-xs text-ink-muted">{item.cuisinesText}</p>
        {showExplanation && item.explanation ? (
          <p className="mt-2 line-clamp-2 text-[11px] leading-relaxed text-ink-muted">
            {item.explanation}
          </p>
        ) : null}
      </div>
    </article>
  );
}
