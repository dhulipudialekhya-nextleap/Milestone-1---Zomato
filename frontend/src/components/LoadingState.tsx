export function LoadingState() {
  return (
    <section className="flex items-center gap-3 rounded-2xl border border-brand-border bg-white px-5 py-4 shadow-card">
      <span className="inline-block h-5 w-5 animate-spin rounded-full border-2 border-brand border-t-transparent" />
      <p className="text-sm font-medium text-ink-muted">Finding restaurants for you…</p>
    </section>
  );
}
