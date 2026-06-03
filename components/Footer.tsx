import { DineAiLogo } from "@/components/DineAiLogo";

export function Footer() {
  return (
    <footer className="border-t border-brand-border bg-white py-12">
      <div className="mx-auto flex max-w-page flex-col items-center justify-between gap-6 px-4 sm:px-6 md:flex-row lg:px-12">
        <DineAiLogo muted />

        <nav className="flex flex-wrap items-center justify-center gap-8 text-sm font-semibold text-ink-muted">
          <a href="#" className="transition hover:text-brand">
            Privacy
          </a>
          <a href="#" className="transition hover:text-brand">
            Terms
          </a>
          <a href="#" className="transition hover:text-brand">
            Contact
          </a>
          <a href="#" className="transition hover:text-brand">
            Partners
          </a>
        </nav>

        <p className="text-xs text-ink-muted">
          © 2026 DineAI Culinary Concierge. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
