"use client";

import { useMemo, useState } from "react";

import { FilterBar } from "@/components/FilterBar";
import { Footer } from "@/components/Footer";
import { LoadingState } from "@/components/LoadingState";
import { Navbar } from "@/components/Navbar";
import { PersonalizedPicks } from "@/components/PersonalizedPicks";
import { PopularSearches } from "@/components/PopularSearches";
import { PreferenceForm } from "@/components/PreferenceForm";
import { ApiError, fetchRecommendations } from "@/lib/api";
import { SAMPLE_PICKS } from "@/lib/samplePicks";
import {
  DEFAULT_FORM_VALUES,
  type FieldErrors,
  type Phase5ViewModel,
  type PreferenceFormValues,
  type RecommendationResult,
  type UiStatus,
} from "@/lib/types";
import { hasFieldErrors, validatePreferenceForm } from "@/lib/validation";
import { buildPhase5ViewModel } from "@/lib/viewModel";

export function HomePage() {
  const [formValues, setFormValues] =
    useState<PreferenceFormValues>(DEFAULT_FORM_VALUES);
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [popularCategory, setPopularCategory] = useState("Ice Cream");
  const [activeFilters, setActiveFilters] = useState<string[]>([]);
  const [status, setStatus] = useState<UiStatus>("idle");
  const [viewModel, setViewModel] = useState<Phase5ViewModel | null>(null);
  const [rawResult, setRawResult] = useState<RecommendationResult | null>(null);

  const useMockData = process.env.NEXT_PUBLIC_USE_MOCK === "true";

  const mergedExtras = useMemo(() => {
    const parts = [formValues.extras.trim(), ...activeFilters].filter(Boolean);
    return parts.join(", ");
  }, [formValues.extras, activeFilters]);

  const handleToggleFilter = (filter: string) => {
    setActiveFilters((current) =>
      current.includes(filter)
        ? current.filter((item) => item !== filter)
        : [...current, filter],
    );
  };

  const handleSubmit = async () => {
    const payload: PreferenceFormValues = {
      ...formValues,
      extras: mergedExtras,
    };

    const clientErrors = validatePreferenceForm(payload);
    if (hasFieldErrors(clientErrors)) {
      setFieldErrors(clientErrors);
      setStatus("error");
      return;
    }

    setFieldErrors({});
    setStatus("loading");
    setViewModel(null);
    setRawResult(null);

    try {
      const response = await fetchRecommendations({
        ...payload,
        use_mock_data: useMockData,
      });

      if (!response.ok) {
        setFieldErrors({ form: response.message });
        setStatus("error");
        return;
      }

      const vm = buildPhase5ViewModel(response.result, 4);
      setViewModel(vm);
      setRawResult(response.result);
      setStatus("success");
    } catch (error) {
      const message =
        error instanceof ApiError
          ? `${error.message}. Is the backend API running on port 8000?`
          : "Something went wrong while fetching recommendations.";
      setFieldErrors({ form: message });
      setStatus("error");
    }
  };

  const displayItems =
    status === "success" && viewModel ? viewModel.items : SAMPLE_PICKS;

  return (
    <div className="min-h-screen bg-surface-muted">
      <Navbar />

      <main className="hero-gradient pb-16 pt-24">
        <div className="mx-auto max-w-page px-4 sm:px-6 lg:px-12">
          <div className="grid grid-cols-12 gap-6">
            <div className="col-span-12 flex flex-col gap-8 lg:col-span-8">
              <div className="flex flex-col gap-2">
                <h1 className="text-[32px] font-bold leading-tight tracking-tight text-ink">
                  Find your perfect meal using DineAI
                </h1>
                <p className="max-w-2xl text-lg leading-relaxed text-ink-muted">
                  Tell us your preferences and our AI concierge will curate a list of
                  restaurants tailored specifically to your taste and current location.
                </p>
              </div>

              <PreferenceForm
                values={formValues}
                errors={fieldErrors}
                disabled={status === "loading"}
                onChange={setFormValues}
                onSubmit={handleSubmit}
              />

              <FilterBar
                activeFilters={activeFilters}
                onToggleFilter={handleToggleFilter}
              />
            </div>

            <aside className="col-span-12 lg:col-span-4">
              <PopularSearches
                selectedCategory={popularCategory}
                onSelectCategory={(category, cuisine) => {
                  setPopularCategory(category);
                  setFormValues((current) => ({ ...current, cuisine }));
                }}
              />
            </aside>
          </div>

          {status === "loading" ? (
            <div className="mt-8">
              <LoadingState />
            </div>
          ) : null}

          <PersonalizedPicks
            items={displayItems}
            summary={viewModel?.summary ?? null}
            showFallbackBanner={viewModel?.showFallbackBanner ?? false}
            emptyMessage={viewModel?.emptyMessage ?? null}
            isLiveResults={status === "success" && viewModel !== null}
          />
        </div>
      </main>

      <Footer />
    </div>
  );
}
