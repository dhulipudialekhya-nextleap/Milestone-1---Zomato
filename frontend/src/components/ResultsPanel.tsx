import { AlertBanner } from "@/components/AlertBanner";
import { RecommendationCard } from "@/components/RecommendationCard";
import type { Phase5ViewModel, RecommendationResult } from "@/lib/types";
import { downloadJson } from "@/lib/api";

interface ResultsPanelProps {
  viewModel: Phase5ViewModel;
  rawResult: RecommendationResult;
}

export function ResultsPanel({ viewModel, rawResult }: ResultsPanelProps) {
  const totalCount = rawResult.recommendations.length;

  return (
    <section className="space-y-4">
      {viewModel.showFallbackBanner ? (
        <AlertBanner variant="warning">
          AI unavailable — showing filter-based results.
        </AlertBanner>
      ) : null}

      {viewModel.summary ? (
        <AlertBanner variant="info">{viewModel.summary}</AlertBanner>
      ) : null}

      {viewModel.emptyMessage ? (
        <AlertBanner variant="warning">
          No restaurants matched your filters. Try a different location, cuisine, or
          lower the minimum rating.
        </AlertBanner>
      ) : (
        <>
          <AlertBanner variant="success">
            Found {totalCount} recommendation(s) (showing top {viewModel.items.length})
          </AlertBanner>

          <div className="flex justify-end">
            <button
              type="button"
              onClick={() =>
                downloadJson("recommendations.json", rawResult)
              }
              className="rounded-lg border border-gray-300 px-3 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50"
            >
              Export JSON
            </button>
          </div>

          <div className="space-y-4">
            {viewModel.items.map((item) => (
              <RecommendationCard key={`${item.rank}-${item.name}`} item={item} />
            ))}
          </div>
        </>
      )}
    </section>
  );
}
