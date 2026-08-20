# Dosaze PDP — structural breakdown

**Source:** `https://dosaze.com/collections/pillows/products/contoured-orthopedic-pillow`, captured live
2026-08-21 at 1440×900 (11,309px tall) and 430×932 (13,204px tall). Computed styles read from the
live DOM, not eyeballed from the swipe. Static swipe: `FireShot Capture 001 — Dosaze Contoured
Orthopedic Pillow` (parent folder, untracked).

**Direction (user decision, 2026-08-21): Dosaze's LAYOUT, LullyRest's PAINT.** Copy their section
lineup, component patterns and spacing rhythm; keep our teal/ink tokens, sharp corners and type.
Do **not** adopt their navy, their serif, or their pill buttons.

---

## 1. Their measured tokens (reference only — we do not adopt these)

| Role | Dosaze | Our equivalent |
|---|---|---|
| Ink / body text | `#1B335F` navy | `#23262B` `--lr-ink` |
| Accent heading | `#1A5290` | `#0E7C86` `--lr-proof` |
| Page background | `#FFFFFF` | `#FCFCFA` `--lr-paper` |
| Card / band fill | `#F7F4EF` cream | `#F2F1ED` `--lr-wash` |
| Heading face | Alegreya, **weight 400** | inherit, weight 800 |
| Body face | Nunito 14px / 19.6px / ls .14px | inherit |
| Section heading | 48px / 57.6px | `clamp(1.6rem, 3.4vw, 2.5rem)` |
| Block heading | 40px / 48px | `.lr h2` |
| Card radius | 8px, buttons full pill | **0 — brand rule** |

Their headings are serif at **regular weight**, never bold. That is what gives the page its
editorial calm. Our analogue is weight + tight tracking, not a serif.

## 2. Their section lineup (measured heights, desktop)

| # | Section | h | Pattern |
|---|---|---|---|
| 1 | Header | 69 | Sticky, announcement bar above |
| 2 | Gallery + buy box | 1856 | Two-col; badges overlaid on gallery |
| 3 | Trust sub-bar | 538 | — |
| 4 | "What Can Dosaze Do For You?" | 740 | **Tabbed** content |
| 5 | "Dosaze Has Been Loved By" | 264 | Press-logo bar |
| 6 | "How it works" | 105 | Centred heading only, 48px |
| 7 | "Innovative shape aligns your neck…" | 750 | **Cream card, copy L / captioned image R** |
| 8 | "Luxe memory foam…" | 590 | Same card, mirrored |
| 9 | "Works for side, back, stomach…" | 590 | Same card, mirrored back |
| 10 | "Our Happy Customers" | 963 | UGC video grid |
| 11 | "Why we're different" | 884 | **Tabs + before/after photos** |
| 12 | "FAQs" | 554 | Accordion |
| 13 | Reviews (Judge.me) | 1567 | — |
| 14–15 | Footer promos + footer | 1021 | — |

## 3. The two component patterns worth stealing

**A. The alternating "cream card" block** (§7–9, the workhorse)
A full-width card in `--lr-wash`, inside it two columns: copy left (heading + an italic customer
quote with the name bolded), captioned image right. The caption sits in a white bar *above* the
photo and uses italic emphasis on the key phrase — "Your sleep alignment with a *standard pillow*."
A red dashed line traces the misaligned spine on the photo; green when aligned. Mirrors L/R each
block. In our paint: `--lr-wash` card, **radius 0**, heading in `--lr-ink`, accent phrase in
`--lr-proof`.

**B. "Why we're different" is NOT a comparison table** (§11)
It is a tab strip — Technology / Materials / Benefits / Features — with an active-tab underline.
Each tab shows a stacked before/after pair: a navy label panel on the left edge ("Your sleep posture
with your current pillow" / "…with Dosaze") against a photo, red dotted spine vs green dotted spine,
then two paragraphs of body copy beneath.

**We currently use Elixir's `product-comparison` checkmark grid here.** Matching Dosaze means
replacing the component, not restyling it. That is the single biggest structural gap on our PDP.

## 4. Gap against our current lineup

Ours (10 sections): buy box → features bar → benefits → lullyrest-mechanism → lullyrest-zones →
comparison → reviews carousel → guarantee → FAQ → sticky ATC.

- **Missing:** press/"loved by" bar, tabbed capability section, UGC video grid, the alternating
  cream-card blocks.
- **Mismatched:** our `comparison` is a checkmark grid where theirs is tabbed before/after.
- **Ours that they lack:** `lullyrest-mechanism` and `lullyrest-zones` are long-form editorial. They
  carry our Stage-4 mechanism argument, which Dosaze's lower-sophistication audience doesn't need.
  Per `research/OFFER.md` these should **stay** — reformat them into pattern A rather than delete.
- **Blocked on assets:** patterns A and B are photography-led. We have four product renders
  (`theme/assets/lullyrest-*.png`) and no sleep-posture photography, no UGC, no press logos.

## 5. Open blockers

- All 7 Elixir vendor sections (`shop-product-details`, `product-comparison`, …) are **absent from
  this repo** — `theme/validate_template.py` reports them missing. Their Liquid/CSS cannot be read
  or fixed until the theme is pulled.
- Sleep-posture before/after photography does not exist and gates §7–9 and §11.
- No press logos and no UGC video → §5 and §10 must stay `[EMPTY]` per the claim-integrity rule.
