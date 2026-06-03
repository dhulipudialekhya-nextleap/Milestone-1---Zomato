import type { ReactNode } from "react";

type AlertVariant = "info" | "success" | "warning" | "error";

const variantStyles: Record<AlertVariant, string> = {
  info: "border-sky-200 bg-sky-50 text-sky-900",
  success: "border-emerald-200 bg-emerald-50 text-emerald-900",
  warning: "border-amber-200 bg-amber-50 text-amber-900",
  error: "border-red-200 bg-red-50 text-red-900",
};

interface AlertBannerProps {
  variant: AlertVariant;
  children: ReactNode;
}

export function AlertBanner({ variant, children }: AlertBannerProps) {
  return (
    <div
      className={`rounded-xl border px-4 py-3 text-sm leading-relaxed ${variantStyles[variant]}`}
      role="alert"
    >
      {children}
    </div>
  );
}
