/** Design tokens and options aligned with screens/code.html */

import type { BudgetBand } from "./types";
import { getAllLocationValues } from "./locations";

export const LOCATIONS = getAllLocationValues();

export const CUISINE_OPTIONS = [
  "Any Cuisine",
  "North Indian",
  "South Indian",
  "Chinese",
  "Italian",
  "Mughlai",
  "Biryani",
  "Modern Japanese",
  "Authentic Italian",
  "Plant-Based Contemporary",
] as const;

export const BUDGET_OPTIONS = [
  { value: "0-500", label: "0-500", band: "low" as BudgetBand },
  { value: "500-1000", label: "500-1000", band: "low" as BudgetBand },
  { value: "1000-2000", label: "1000-2000", band: "medium" as BudgetBand },
  { value: "2000-5000", label: "2000-5000", band: "high" as BudgetBand },
  { value: "5000+", label: "5000+", band: "high" as BudgetBand },
] as const;

export type BudgetOptionValue = (typeof BUDGET_OPTIONS)[number]["value"];

export const CRAVING_OPTIONS = [
  "Anything delicious",
  "Biryani",
  "Cakes",
  "Indian Breads",
  "Pizza",
  "Sushi",
  "Pasta",
] as const;

export const POPULAR_SEARCH_OPTIONS = [
  "Ice Cream",
  "Sweets",
  "Desserts",
  "Juices",
  "Cakes",
  "Waffles",
] as const;

export function budgetValueToBand(value: string): BudgetBand {
  const match = BUDGET_OPTIONS.find((option) => option.value === value);
  return match?.band ?? "medium";
}

export function bandToBudgetValue(band: BudgetBand): BudgetOptionValue {
  const match = BUDGET_OPTIONS.find((option) => option.band === band);
  return match?.value ?? "1000-2000";
}

export const STITCH_IMAGES = {
  iceCream:
    "https://lh3.googleusercontent.com/aida-public/AB6AXuChr2dmw-LKCY5VWZxhjBYKPR3R19QMewquvNTgn_x-tzf97gs2RBpx3XpvLk5_c2-rmeHP3ulv5pEhx2C2_IraJYZufXg9CTBvcNZg-Cfwu7i4go18Cg69E6htzUBdscgs8bMZbUxKcgUSm_UBjiEWW9kz0jlHEAajUWMeGZHtEk9ynzje19ixyQSgtiv0eQOTnPw4HZE-tkU-pNZ3Uaxs0RAIoddm0qq0uX82xyZDFvQ3YIFChZcNHA672CW0GuLTsAqc6c4r7HM",
  sweets:
    "https://lh3.googleusercontent.com/aida-public/AB6AXuDMwxYw8tpYRbwFRnKzfY5EQbBdZlSH9ZgGmSslNc2ZC1RoFPZBZp1oY67ZCFdYZ7lu28WzVJNHfliEyul9ybPfChUPd0FuCwjLcTTcAlf-6gCpFC7172hzyxNlxB66Me3aDrEBbXkpd8DO_u8M7wYLF9YBpwa0FoSou4ZX0XL-P0PI1eYqZBr5XVLtx8kNkaoa5dsbc_ZFN1H0SfZfut64pNi13A0WfB99nqJgpRL6tzwIwXsHf8K4v_Obnb7rZ7KsQOweg0Qox8s",
  juices:
    "https://lh3.googleusercontent.com/aida-public/AB6AXuA8xhprjkNS6Du8NhVtqYN5aI6dXLd7nydf6Hfsg6SH5Fz2iRjNrE-JT0A3ehDOIUXlarmhgzIJeSJ2v-fhDGBASTFUqOkKPPOcgHY0wP5YBUiicVJ-sBL26qk3AOUbZGeA6uqJf0TCvw3SaP9xPkFitVCC9D8fmLSd6OYdThgG8LO98swJdNKlhK3o17THmZwZIbQMVjsrLfZUbKX9T85GanoSV9DkfYeM23ttItIXK3elvs5R5aBtVDPCYhMuW6E1CLtD7rna9j0",
  waffles:
    "https://lh3.googleusercontent.com/aida-public/AB6AXuDvwsV4_3PbO3L_K_tZL14FdjMvIVXK5PaQAVACoDP7umcj1fLy-05hA4WspThMhcbi48va9-7y7HAa9lvBA-eoeUZi7jIM4fsBwwEKxQBzn64ho3ipfDVE8hKsJLqkla_cPEGZrPp-lAUhBuDI_8y44BT5GP-hYzF49BRdaZc4CHRCyG0537fVEFbhlDeKywRFvMCLAKB8n6Vev94gVaQt998qh9O-w_FXvHD0C_h3Kgp0cqTlB_GTb3r8ePL-BMePeccu89dH-F0",
  cakes:
    "https://lh3.googleusercontent.com/aida/ADBb0ugsDo9QCgjwJvymuql8g_UJsJMtAsJHBEGVK1qCzNRb2N5KyF4RcMnseU5FtOQd6421oqaRNXiTkjrqT4D987owjuV7tIOxUTbBFMVNjJ9xMnC0-mmKDprlBqmDOsG4uT5k7tPRK7-7z9w6B-wt8Q9AE59oZYZPN0ALQt1BNje_yO21CqkvkJ2F6oxws6YOEirHjOYWSNz3c6XfnhEvR1t5P-NLjK5TAoZOtVbChLTnPSAN_67a2As25jI",
  butterChicken:
    "https://lh3.googleusercontent.com/aida-public/AB6AXuAswIeEiifJWA0-o6hCQuoPc-SepH8hLb--gXLtmtMcHZfPCusevZujyrmGbK9KfCM_WDTP0c4OHv_88cLJikhpyl7Fvmc4MycE9VSoM6scFplG2SP7wyoAFTgpO1Oy3eruI-h7kZqF8euA2evAt0LhZvm9cd89YfvoVluwJmTjIUnvdFoKgFCyfP1Q7CoA6pNpiUybohkGSfGKgpS7L_tlddFRcbpb8J5oY4R6EHmIacsmcI5Y2QGyaq6Cl6W7QNS4EOmw8LItnoc",
  masalaDosa:
    "https://lh3.googleusercontent.com/aida-public/AB6AXuC496aq1oSBMCWR5Ft95UBiRPjkaayF0mu-ePoZs37TkWca8sPA9nwYkg7c5Ezpz6gsHP78c_qEAw6FYUImeVhcd_SLRTnZR-4ivqM6NWeOAVafDicD9a30dGv8qUZiqwqLDdEEAvBiJqfNe7--h82x7WyHB-CJNwTdp3pgH4WqPdpnCSM8BxngaVjZh5w_jZ6oV5856toDhQhQZ7S_3sXcBDNbnJvdA8s4I31j_vhOC_xycQO9Om2cdljWm19CDTlt2tNnLgJsEFg",
  muttonBiryani:
    "https://lh3.googleusercontent.com/aida-public/AB6AXuCAKY5nbpe6nTIUhiUTh1rM_oaxbI6I38Lg73QP1eU608unfWwgvxZ0iqzL-sHUrViwl3TVbKj1oe81O_mBQ0ryQpBzrxSGZjfRyO8OSs2wDXZYS7pTSZU9aGMUXkjHg2OqvwYMI1QYd3bfo6H23s-zzJHq9pKCqg1N98wCARkC5RgjMN5QrUVLspJt1PPDfPfehv7SyMdzfhcc63YJ8Wp6xbUSSKBuA-a5v5eejZ3WDC_gXd9i3F1BAPioT6XAiYH4SeNpDuy65L8",
  paneerTikka:
    "https://lh3.googleusercontent.com/aida-public/AB6AXuCISoDgDlnJu0wFPwEAE_84A_83eDWykmyIfTAyNzfRlWgTGfg2_G305j1KGXU5Iw3P7P2U5cf13rYmRGTCahBWesfMlPzZ_hsc6Bf5I0oBK_iZ5Lu3pBJjXpnpb8XaleV8a62qfwHuoYm9kKIZ28CoO8Uzf_TUmrnlHths9SyiWBWEWBmQ6eSviuWAXo7sMEAD2H3RmWMMZH2bHxwfMTSio9tEwICorF9RRfJGbKMMX6BmR0WLQlY61VQEvuHMI9gM7Fki_7_oAeY",
} as const;
