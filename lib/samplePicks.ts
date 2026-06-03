import { STITCH_IMAGES } from "./designConstants";
import type { PresentableRecommendation } from "./types";

/** Placeholder picks shown before search — matches screens/screen.png */
export const SAMPLE_PICKS: PresentableRecommendation[] = [
  {
    rank: 1,
    name: "Butter Chicken",
    cuisinesText: "The Great Kebab Factory",
    ratingText: "4.8",
    estimatedCostText: "₹1200 for two",
    explanation: "Rich, creamy curry with tender chicken — a crowd favourite.",
    imageUrl: STITCH_IMAGES.butterChicken,
  },
  {
    rank: 2,
    name: "Masala Dosa",
    cuisinesText: "Saravana Bhavan",
    ratingText: "4.6",
    estimatedCostText: "₹400 for two",
    explanation: "Crispy dosa with spiced potato filling and chutneys.",
    imageUrl: STITCH_IMAGES.masalaDosa,
  },
  {
    rank: 3,
    name: "Mutton Biryani",
    cuisinesText: "Paradise Biryani",
    ratingText: "4.9",
    estimatedCostText: "₹900 for two",
    explanation: "Fragrant basmati rice layered with slow-cooked mutton.",
    imageUrl: STITCH_IMAGES.muttonBiryani,
  },
  {
    rank: 4,
    name: "Paneer Tikka",
    cuisinesText: "Punjab Grill",
    ratingText: "4.7",
    estimatedCostText: "₹700 for two",
    explanation: "Smoky char-grilled paneer with mint chutney.",
    imageUrl: STITCH_IMAGES.paneerTikka,
  },
];
