# Google Stitch — Next.js Frontend UI Prompt

Use the prompt below with [Google Stitch](https://stitch.withgoogle.com/) to generate UI mockups and screen designs for the Zomato-inspired AI restaurant recommendation app. The target implementation framework is **Next.js** (App Router, React, TypeScript).

---

## Quick context

| Item | Detail |
|------|--------|
| Product | AI-powered restaurant recommendation web app |
| Frontend stack | Next.js 14+, TypeScript, Tailwind CSS |
| Backend | Python API (FastAPI) — frontend consumes JSON only |
| Brand feel | Modern food-discovery app; clean, trustworthy, Zomato-inspired (not a copy) |
| Primary accent | Warm red/coral (`#E23744` family) with neutral grays and white surfaces |

---

## Screens to generate

Ask Stitch to produce designs for these views:

1. **Landing / Home** — hero + preference form (default state)
2. **Loading** — form submitted, recommendations in progress
3. **Results** — top 5 recommendation cards with AI summary
4. **Empty state** — no restaurants matched filters
5. **Fallback banner** — AI unavailable, filter-based results shown
6. **Validation error** — inline field errors on the form
7. **Mobile responsive** — same flows optimized for phone width

---

## Copy-paste prompt for Google Stitch

```
Design a modern, production-ready web app UI for an AI-powered restaurant recommendation product inspired by Zomato. The frontend will be built with Next.js (App Router), React, TypeScript, and Tailwind CSS.

PRODUCT SUMMARY
- Users enter dining preferences and receive personalized top restaurant recommendations.
- An AI backend ranks restaurants and writes short explanations for each pick.
- The UI must feel premium, fast, and food-focused — clean layout, strong typography, subtle shadows, rounded cards.

BRAND & VISUAL STYLE
- Primary accent: warm red/coral (#E23744 or similar)
- Background: light gray (#F8F9FA) with white card surfaces
- Typography: modern sans-serif (Inter or similar)
- Style: minimal, spacious, mobile-first responsive
- Use subtle food/restaurant iconography (plate, star rating, map pin) — no cluttered stock photos
- Rounded corners (12–16px), soft shadows, clear visual hierarchy

LAYOUT STRUCTURE (DESKTOP)
- Top navigation bar:
  - Left: app logo + name "Zomato AI Recommendations" (or "DineAI")
  - Right: optional "About" link and settings icon
- Main content: centered max-width container (~960px)
- Optional right sidebar (desktop only): dev toggle "Use mock dataset" with helper text

PAGE 1 — HOME / PREFERENCE FORM (DEFAULT STATE)
- Page title: "Restaurant Recommendations"
- Subtitle: "AI-powered suggestions based on your taste and budget"
- Preference form card with fields:
  1. Location (required text input) — placeholder: "e.g. Delhi, Bangalore"
  2. Preferred cuisine (required text input) — placeholder: "e.g. Italian, Chinese"
  3. Budget (required dropdown) — options: Low, Medium, High
  4. Minimum rating (slider 0.0 to 5.0, step 0.5, default 4.0)
  5. Additional preferences (optional textarea) — placeholder: "e.g. family-friendly, quick service"
- Primary CTA button: "Get recommendations" (full width on mobile, prominent red button)
- Below form: helper text — "Fill in your preferences and click Get recommendations."
- Show required field markers (*)

PAGE 2 — LOADING STATE
- Same form visible but disabled/grayed out
- Centered loading indicator with text: "Finding restaurants for you…"
- Skeleton placeholders for 3 recommendation cards below the form

PAGE 3 — RESULTS STATE (SUCCESS)
- Success banner: "Found 5 recommendation(s) (showing top 5)"
- Optional AI summary info block at top (light blue/neutral info panel) with 1–2 sentence summary comparing top picks
- Stack of 5 recommendation cards, each containing:
  - Rank badge: "#1", "#2", etc.
  - Restaurant name (bold, large)
  - Row of metadata chips or columns:
    - Rating: "4.5" with star icon
    - Cuisine: "North Indian, Chinese"
    - Estimated cost: "₹800 for two"
  - "Why this pick" section with AI explanation paragraph (2–3 lines)
- Cards have hover state on desktop
- Optional secondary actions on results page: "Search again" and "Export JSON"

PAGE 4 — EMPTY STATE
- Warning/empty banner: "No restaurants matched your filters. Try a different location, cuisine, or lower the minimum rating."
- Form remains editable above
- Illustration or icon suggesting no results (empty plate or search icon)

PAGE 5 — FALLBACK STATE (AI UNAVAILABLE)
- Amber warning banner at top: "AI unavailable — showing filter-based results."
- Results cards same as success state but banner indicates degraded mode

PAGE 6 — VALIDATION ERROR STATE
- Inline red error messages under invalid fields (e.g. "Location is required")
- Top error alert: "Invalid input: please fix the highlighted fields"
- Do not hide the form

MOBILE RESPONSIVE (375px width)
- Single column layout
- Sticky bottom CTA or full-width submit button
- Recommendation cards stack vertically with compact metadata row
- Collapsible sidebar options into a bottom sheet or settings menu

COMPONENTS TO SHOW AS A DESIGN SYSTEM STRIP (optional footer section)
- Primary button, secondary button, text input, select, slider, textarea
- Info/warning/success/error alert banners
- Recommendation card component
- Rating chip, cuisine tag, cost label
- Loading spinner and skeleton card

ACCESSIBILITY & UX
- High contrast text
- Clear focus states on inputs
- Error states use icon + color (not color alone)
- Touch-friendly tap targets (min 44px)

TECH NOTES FOR IMPLEMENTATION (annotate in design if possible)
- Framework: Next.js App Router
- Data comes from POST /api/recommendations returning JSON
- Form maps to: location, budget, cuisine, min_rating, extras
- Results map to: rank, name, cuisines, rating, estimated_cost, explanation, summary

OUTPUT REQUEST
Generate high-fidelity mockups for desktop (1440px) and mobile (375px) covering: default form, loading, results with 5 cards, empty state, and fallback banner state. Use a cohesive component library look suitable for direct handoff to Next.js + Tailwind development.
```

---

## Sample data for realistic mockups

Use this content when asking Stitch to fill screens with realistic placeholder data:

### Form defaults

| Field | Sample value |
|-------|----------------|
| Location | Bellandur |
| Cuisine | North Indian |
| Budget | Medium |
| Min rating | 4.0 |
| Extras | family-friendly, outdoor seating |

### AI summary (results page)

> Based on your preferences in Bellandur with a medium budget and 4.0+ rating, these five spots balance strong reviews, familiar North Indian flavors, and value for two.

### Sample recommendation cards

| Rank | Name | Cuisine | Rating | Cost | Why this pick |
|------|------|---------|--------|------|---------------|
| 1 | The Spice Route | North Indian, Mughlai | 4.6 | ₹800 for two | Highly rated for consistent flavors and generous portions; fits your budget and cuisine preference. |
| 2 | Coastal Cravings | Seafood, South Indian | 4.5 | ₹700 for two | Great reviews for fresh coastal dishes; good for a family-friendly outing. |
| 3 | Urban Tandoor | North Indian, BBQ | 4.4 | ₹900 for two | Popular local choice with fast service and reliable 4+ ratings in Bellandur. |
| 4 | Garden Bistro | Continental, Cafe | 4.3 | ₹600 for two | Relaxed ambiance with outdoor seating options mentioned in your extras. |
| 5 | Wok & Roll | Chinese, Pan-Asian | 4.2 | ₹750 for two | Solid backup pick with diverse menu and steady ratings in your area. |

---

## Suggested Next.js page map

| Route | Purpose |
|-------|---------|
| `/` | Home — preference form + results on same page (SPA-style) |
| `/about` | Optional — how AI recommendations work |
| `/api/recommendations` | Route handler proxy to Python backend (Phase 8+) |

---

## API contract reference (for accurate UI states)

Frontend sends:

```json
{
  "location": "Bellandur",
  "budget": "medium",
  "cuisine": "North Indian",
  "min_rating": 4.0,
  "extras": "family-friendly"
}
```

Backend returns (success):

```json
{
  "ok": true,
  "result": {
    "recommendations": [
      {
        "rank": 1,
        "name": "The Spice Route",
        "cuisines": ["North Indian", "Mughlai"],
        "rating": 4.6,
        "average_cost": 800,
        "cost_band": "medium",
        "explanation": "Highly rated for consistent flavors..."
      }
    ],
    "summary": "Based on your preferences...",
    "used_llm_fallback": false,
    "filter_match_count": 42
  }
}
```

Backend returns (validation error):

```json
{
  "ok": false,
  "error_code": "validation_error",
  "message": "Location is required."
}
```

---

## Tips for best Stitch results

1. **Run the prompt once for desktop**, then ask: *"Generate mobile (375px) versions of all screens above."*
2. **Ask for a component sheet** if you need buttons, inputs, and cards isolated for dev handoff.
3. **Iterate on one screen** at a time (e.g. "Refine the recommendation card with rank badge and explanation block").
4. **Mention Tailwind-friendly spacing** if you want designs that map cleanly to utility classes.

---

## Related docs

- [architecture.md](./architecture.md) — Phase 7 (Frontend) and Phase 8 (API contract)
- [problemstatement.md](./problemstatement.md) — product requirements and display fields
