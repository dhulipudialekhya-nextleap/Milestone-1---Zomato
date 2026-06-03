interface DineAiLogoProps {
  compact?: boolean;
  muted?: boolean;
}

export function DineAiLogo({ compact = false, muted = false }: DineAiLogoProps) {
  const colorClass = muted ? "text-ink-secondary" : "text-brand";

  return (
    <div className="flex items-center gap-2">
      <svg
        viewBox="0 0 24 24"
        fill="currentColor"
        className={`h-6 w-6 ${colorClass}`}
        aria-hidden="true"
      >
        <path d="M11 9H9V2H7v7H5V2H3v7c0 2.12 1.66 3.84 3.75 3.97V22h2.5v-9.03C11.34 12.84 13 11.12 13 9V2h-2v7zm5-3v8h2.5v8H21V2c-2.76 0-5 2.24-5 4z" />
      </svg>
      <span
        className={`font-bold tracking-tight ${colorClass} ${compact ? "text-lg" : "text-xl"}`}
      >
        DineAI
      </span>
    </div>
  );
}
