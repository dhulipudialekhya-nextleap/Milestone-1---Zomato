"use client";

import Link from "next/link";

import { DineAiLogo } from "@/components/DineAiLogo";

export function Navbar() {
  return (
    <header className="fixed top-0 z-50 w-full border-b border-brand-border bg-white shadow-sm">
      <div className="mx-auto flex h-16 max-w-page items-center justify-between px-4 md:px-12">
        <Link href="/" className="hover:opacity-90">
          <DineAiLogo />
        </Link>

        <nav className="flex items-center gap-8">
          <Link
            href="/"
            className="text-sm font-semibold text-ink-muted transition hover:text-brand"
          >
            Home
          </Link>
          <Link
            href="/login"
            className="text-sm font-semibold text-ink-muted transition hover:text-brand"
          >
            Log In
          </Link>
          <Link
            href="/signup"
            className="text-sm font-bold text-brand transition hover:opacity-90"
          >
            Sign Up
          </Link>
        </nav>
      </div>
    </header>
  );
}
