---
name: DineAI
colors:
  surface: '#f8f9fa'
  surface-dim: '#d9dadb'
  surface-bright: '#f8f9fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f5'
  surface-container: '#edeeef'
  surface-container-high: '#e7e8e9'
  surface-container-highest: '#e1e3e4'
  on-surface: '#191c1d'
  on-surface-variant: '#5b403f'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f2'
  outline: '#8f6f6e'
  outline-variant: '#e4bebc'
  surface-tint: '#bb162c'
  primary: '#b7122a'
  on-primary: '#ffffff'
  primary-container: '#db313f'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb3b1'
  secondary: '#5a5d70'
  on-secondary: '#ffffff'
  secondary-container: '#dee1f8'
  on-secondary-container: '#606376'
  tertiary: '#795600'
  on-tertiary: '#ffffff'
  tertiary-container: '#986d00'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#dee1f8'
  secondary-fixed-dim: '#c2c5db'
  on-secondary-fixed: '#171b2b'
  on-secondary-fixed-variant: '#424658'
  tertiary-fixed: '#ffdea8'
  tertiary-fixed-dim: '#ffba20'
  on-tertiary-fixed: '#271900'
  on-tertiary-fixed-variant: '#5e4200'
  background: '#f8f9fa'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  container-padding-mobile: 16px
  container-padding-desktop: 48px
  gutter: 16px
  stack-gap-sm: 8px
  stack-gap-md: 16px
  stack-gap-lg: 32px
---

## Brand & Style

The brand personality is sophisticated yet accessible, acting as a high-end digital concierge for culinary exploration. It targets urban food enthusiasts who value efficiency and high-quality recommendations. 

The design style is **Minimalist with a Premium focus**, prioritizing high-resolution food photography and clean whitespace to reduce cognitive load. By utilizing soft depth and subtle transparency, the interface feels airy and modern. The emotional response should be one of confidence, appetite, and discovery.

## Colors

The palette is anchored by a vibrant **Warm Coral (#E23744)**, used strategically for primary actions and brand presence. The background utilizes a very light **Cool Gray (#F8F9FA)** to differentiate from white card surfaces (#FFFFFF), creating a layered effect without heavy borders.

- **Primary:** Warm Coral for key CTAs and active states.
- **Secondary:** Deep Slate (#2D3142) for high-contrast typography and icon accents.
- **Tertiary:** Amber (#FFB800) reserved specifically for ratings and "Top Pick" highlights.
- **Semantic:** 
    - Success: #27AE60 (Emerald)
    - Info: #2F80ED (Azure)
    - Warning: #F2994A (Orange)
    - Error: #EB5757 (Rose)

## Typography

The typography system relies entirely on **Inter**, chosen for its exceptional legibility and neutral, modern character. 

Hierarchy is established through significant weight shifts. Headlines use a tight letter spacing and bold weights to command attention, while body text remains airy for long-form AI explanations. Label styles are used for metadata like "Cuisine" or "Cost Level," often paired with a slightly increased letter-spacing when set in uppercase to maintain clarity at small sizes.

## Layout & Spacing

This design system uses a **Fluid Grid** model based on an 8px spacing system (with 4px increments for micro-adjustments). 

- **Mobile:** Single column layout with 16px side margins.
- **Tablet:** 6-column grid with 24px gutters.
- **Desktop:** 12-column grid with a max-width of 1280px and 32px gutters.

Horizontal spacing between interactive elements (like chips) should use the `stack-gap-sm` (8px). Vertical spacing between sections (e.g., "Trending Now" vs "Nearby") should use `stack-gap-lg` (32px) to ensure the layout feels premium and uncrowded.

## Elevation & Depth

Depth is achieved through **Tonal Layering** and **Ambient Shadows**. 

The base surface is the Neutral background (#F8F9FA). Interactive cards sit at a higher elevation on white surfaces (#FFFFFF). Shadows are extremely soft: 
- `shadow-sm`: 0px 2px 4px rgba(0,0,0,0.04) for static cards.
- `shadow-md`: 0px 8px 16px rgba(0,0,0,0.08) for hover states and active components.
- `shadow-lg`: 0px 16px 32px rgba(0,0,0,0.12) for modals and dropdowns.

Avoid harsh borders; instead, use a 1px stroke in #EDF0F2 for subtle definition on white surfaces.

## Shapes

The shape language is friendly and approachable. 
- **Standard Elements:** Buttons, inputs, and chips use a 12px radius. 
- **Container Elements:** Large cards and recommendation sections use a 24px radius (`rounded-xl`) to feel soft and high-end.
- **Images:** All restaurant thumbnails must carry a minimum of 12px radius to match the UI elements.

## Components

### Buttons
- **Primary:** Solid #E23744 with white text. 12px corner radius.
- **Secondary:** Surface-colored with a #E23744 border and text.
- **States:** On hover, apply a 10% black overlay to the primary color.

### Inputs & Selection
- **Text Inputs:** White background, 1px border (#EDF0F2), 12px radius. Focus state uses a 2px #E23744 stroke.
- **Dropdowns:** Use a chevron-down icon. List items have 8px padding and subtle hover highlights.
- **Sliders:** The track should be #EDF0F2, with the active range and handle in #E23744.

### Recommendation Card
- **Rank Badge:** A small circular badge in the top-left corner using Secondary (#2D3142) with white text.
- **Metadata Chips:** Small, semi-transparent gray backgrounds (#F1F3F5) with Label-sm text.
- **AI Explanation Section:** A light-tinted Coral area (#FFF5F6) at the bottom of the card with a "sparkle" icon to denote AI-generated insights.

### Alert Banners
- Minimalist banners with a 12px radius. Use high-saturation icons with low-saturation backgrounds of the same hue (e.g., Error uses a light pink background with a bright red icon).

### Icons
- Use thin-stroke (1.5px) icons. Icons like "Map Pin" or "Star" should use the brand Coral or Amber only when active/filled.