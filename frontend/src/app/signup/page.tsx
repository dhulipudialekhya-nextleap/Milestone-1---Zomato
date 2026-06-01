import Link from "next/link";

import { DineAiLogo } from "@/components/DineAiLogo";

export default function SignupPage() {
  return (
    <div className="flex min-h-screen flex-col bg-surface-muted">
      <header className="border-b border-brand-border bg-white px-4 py-4 sm:px-6">
        <Link href="/">
          <DineAiLogo />
        </Link>
      </header>

      <main className="mx-auto flex w-full max-w-md flex-1 flex-col justify-center px-4 py-12">
        <h1 className="text-2xl font-bold text-ink">Create your DineAI account</h1>
        <p className="mt-2 text-sm text-ink-muted">
          Sign up to get personalized restaurant picks tailored to your taste.
        </p>

        <form className="mt-8 space-y-4">
          <div>
            <label htmlFor="name" className="mb-2 block text-xs font-semibold uppercase tracking-wider text-ink-muted">
              Full name
            </label>
            <input
              id="name"
              type="text"
              placeholder="Your name"
              className="w-full rounded-xl border border-brand-border px-4 py-3 text-sm input-surface outline-none focus:border-brand"
            />
          </div>
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
            Sign Up
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-ink-muted">
          Already have an account?{" "}
          <Link href="/login" className="font-semibold text-brand hover:underline">
            Log in
          </Link>
        </p>
      </main>
    </div>
  );
}
