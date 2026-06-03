import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "#C11F2E",
          dark: "#b7122a",
          light: "#E23744",
          border: "#EDF0F2",
        },
        surface: {
          DEFAULT: "#FFFFFF",
          muted: "#F8F9FA",
          container: "#f3f4f5",
        },
        ink: {
          DEFAULT: "#191c1d",
          muted: "#5b403f",
          secondary: "#5a5d70",
        },
      },
      maxWidth: {
        page: "1280px",
      },
      fontFamily: {
        sans: ["var(--font-inter)", "Inter", "system-ui", "sans-serif"],
      },
      boxShadow: {
        card: "0 2px 4px rgba(0, 0, 0, 0.04)",
        "card-hover": "0 8px 16px rgba(0, 0, 0, 0.08)",
      },
    },
  },
  plugins: [],
};

export default config;
