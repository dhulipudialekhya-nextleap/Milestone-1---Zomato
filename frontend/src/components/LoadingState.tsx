import { isLocalApi } from "@/lib/env";

export function LoadingState() {
  return (
    <section className="flex flex-col gap-2 rounded-2xl border border-brand-border bg-white px-5 py-4 shadow-card sm:flex-row sm:items-center sm:gap-3">
      <span className="inline-block h-5 w-5 shrink-0 animate-spin rounded-full border-2 border-brand border-t-transparent" />
      <div>
        <p className="text-sm font-medium text-ink-muted">Finding restaurants for you…</p>
        {!isLocalApi() ? (
          <p className="mt-1 text-xs text-ink-muted">
            First request after idle may take up to a minute while the API wakes on Render.
          </p>
        ) : null}
      </div>
    </section>
  );
}
