import Link from "next/link";

import { DineAiLogo } from "@/components/DineAiLogo";

export default function LoginPage() {
  return (
    <div className="flex min-h-screen flex-col bg-surface-muted">
      <header className="border-b border-brand-border bg-white px-4 py-4 sm:px-6">
        <Link href="/">
          <DineAiLogo />
        </Link>
      </header>

      <main className="mx-auto flex w-full max-w-md flex-1 flex-col justify-center px-4 py-12">
        <h1 className="text-2xl font-bold text-ink">Log in to DineAI</h1>
        <p className="mt-2 text-sm text-ink-muted">
          Welcome back. Sign in to save preferences and view your recommendations.
        </p>

        <form className="mt-8 space-y-4">
          <div>
            <label htmlFor="email" className="mb-2 block text-xs font-semibold uppercase tracking-wider text-ink-muted">
              Email
            </label>
            <input
              id="email"
              type="email"
              placeholder="you@example.com"
              className="w-full rounded-xl border border-brand-border px-4 py-3 text-sm input-surface outline-none focus:border-brand"
            />
          </div>
          <div>
            <label htmlFor="password" className="mb-2 block text-xs font-semibold uppercase tracking-wider text-ink-muted">
              Password
            </label>
            <input
              id="password"
              type="password"
              placeholder="••••••••"
              className="w-full rounded-xl border border-brand-border px-4 py-3 text-sm input-surface outline-none focus:border-brand"
            />
          </div>
          <button
            type="button"
            className="w-full rounded-xl bg-brand py-3 text-sm font-semibold text-white transition hover:bg-brand-dark"
          >
            Log In
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-ink-muted">
          Don&apos;t have an account?{" "}
          <Link href="/signup" className="font-semibold text-brand hover:underline">
            Sign up
          </Link>
        </p>
      </main>
    </div>
  );
}
