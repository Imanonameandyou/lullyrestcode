# LullyRest PDP Rebuild + BOGO Offer + Cart Drawer — Design Spec

**Date:** 2026-08-21
**Status:** Approved by user, proceeding to implementation.

## Goal

Build a brand-new product page (not a rebuild of the existing one) for the LullyRest
Orthopedic Cervical Pillow that closes the prospect the presell listicle already warmed
up, using Elixir's native section/block library. Ship the offer that makes this close:
BOGO on the pillow + a free ThermaFlow cooling case gift-with-purchase. Overhaul the cart
drawer with a free-shipping/free-gift progress bar and a cross-sell rail.

Supersedes the BOGO-rejection rationale in `research/OFFER.md` and
`marketing/BONUS_PRODUCTS.md` — explicit user decision, 2026-08-21.

## Scope & phasing

- **A — Offer mechanics.** BOGO automatic discount, free-shipping automatic discount,
  cart-drawer free-gift wiring. The cooling case product itself is being built in a
  parallel Claude Code session — this work proceeds without it and wires it in once its
  product ID is available.
- **B — PDP rebuild.** New template file, new product-facing section, does not touch or
  replace `product.lullyrest.json`.
- **C — Cart drawer.** Configure the existing (previously-unpulled, now-pulled) Elixir
  `cart-drawer.liquid` section — no new code, section/block settings only.

## Store facts this design depends on

- Core product: `gid://shopify/Product/9589261009154`, $149.00 / compare-at $199.00,
  SKU `LR-OCP-001`, templateSuffix `lullyrest`.
- Draft theme: `LullyRest — Presell + PDP (draft)`
  (`gid://shopify/OnlineStoreTheme/163498656002`), duplicated from `elixir-1-6-1-pillow`.
  Live theme (Horizon, `163498262786`) is never touched.
- Elixir ships a **fully-built cart drawer** (`sections/cart-drawer.liquid`,
  4481 lines) with:
  - `cart_progress_bar` block: dual-goal progress bar. `product_free_shipping` (price
    threshold) and `product_free_amount` (price threshold) + `progress_bar_free_product`
    (product picker) drive a free-shipping goal and a free-gift goal independently or
    together. **The vendor's own settings copy confirms these are display-only** — a real
    Shopify automatic discount must exist for free shipping to actually apply at
    checkout, and the gift product must actually be priced free for the auto-add to give
    it away at $0.
  - `cart_upsell` blocks (repeatable, `upsell_product_1` picker) — cross-sell rail.
  - `cart_timer_bar`, `cart-discount-banner`, `cart-social_proof_bar`, `cart_promo_banner`
    blocks — urgency/promo/social-proof rows in the drawer header.
- Elixir's buy box (`sections/shop-product-details.liquid`, 19045 lines) ships:
  - A **Premium Attachment Kit** block (`snippets/premium-attachment-kit.liquid`) — a
    native gift-with-purchase widget. Configured with `apply_to_product` (show only on
    this product) and up to 10 `item_N_product` pickers; renders a "what's included free"
    list and exposes `data-free-gift-product-ids` / `data-rely-on-product-id` for the cart
    drawer's auto-add JS (`assets/premium-attachment-kit.js`, vendor-only, not in this
    repo). **This is the free-cooling-case mechanism** — no custom code needed.
  - A native **BOGO display mode** inside its `quantity_break`/bundle blocks
    (`selected_custom_price_format: "bogo"`, with a `bogo_multiplier` setting). This is
    cosmetic pricing display only (savings badge, "2nd free" labeling) — the real price
    cut at checkout still requires a matching Shopify automatic discount.

This means Phase A/C are almost entirely section-and-block configuration on top of
already-built vendor code, not new Liquid/JS.

## Offer mechanics (Phase A)

1. **BOGO discount** — automatic discount, "Buy 1 LullyRest Orthopedic Cervical Pillow,
   get 1 free" (100% off 2nd unit, same product, max 1 free per order). Created via
   `discountAutomaticBasicCreate` (or the buy-x-get-y automatic discount type), **status
   inactive/draft** until final go-ahead. Given a real end date (see Urgency below) so the
   countdown timer that references it is honest, not fabricated.
2. **Free shipping discount** — automatic discount, free shipping when subtotal ≥
   **$160** (chosen so any single upsell — earplugs $19 / mask $24 / wrap $29 / cooling
   case at full price if not gifted — crosses it; the pillow alone at $149, or 2 pillows
   at $149 under BOGO, does not). Created via the free-shipping automatic discount type,
   **status inactive/draft**.
3. **Free cooling case gift** — `premium_attachment_kit` block on the buy box,
   `apply_to_product` = the pillow, one item slot pointing at the cooling case product.
   Depends on the parallel session's product; the block config is written with a
   placeholder and finished once that product ID exists. **Flag for the parallel
   session:** the theme's own docs say the gift product must be priced at $0 (or have a
   dedicated always-free variant) for the auto-add-at-$0 behavior to work — not priced
   normally and zeroed by a discount. I'll confirm this with that product once it's
   built, before wiring the block.

## PDP structure (Phase B) — new template

New template file, new product-facing template suffix (does not touch
`product.lullyrest.json`), built from `theme/build_templates.py`'s generator pattern.
Nine sections, each mapped to a real Elixir section type:

1. **Product info** → `shop-product-details` — title, price, variant picker, BOGO-mode
   quantity/bundle block, `premium_attachment_kit` (free cooling case), guarantee badges,
   shipping notice, payment icons.
2. **Social proof #1** → `statistics-grid` or `as-seen-in-logos` — verifiable structural
   claims only (zero-VOC, 4-zone core, DPT-designed, 60-night trial), not testimonials.
3. **Problem restated → features as fix** → `alternating-features`, condensed (2–3 short
   blocks, not long-form editorial) — each problem from the listicle mapped to the zone
   that fixes it.
4. **Social proof #2** → reserved `[EMPTY]`-labeled slot (`lullyrest-proof-placeholder`
   pattern) — no UGC/video assets exist yet.
5. **Physical features** → `product-benefits` — the 4 zones, reusing existing content.
6. **Social proof #3** → reserved `[EMPTY]`-labeled slot.
7. **FAQ** → `product-faq` — reusing existing 7-item content (2 items still carry
   `[VERIFY]` markers, kept as-is).
8. **Social proof #4** → reserved `[EMPTY]`-labeled slot.
9. **Guarantee + Offer + Scarcity + Urgency** → `satisfaction-guarantee` (60-night
   guarantee) + BOGO/free-gift offer restatement + `sale-countdown-banner` tied to the
   BOGO discount's real end date (honest countdown, not fabricated) + real
   inventory-count scarcity line (queried from the actual product's inventory, not
   invented) + sticky CTA.

**Claim-integrity decision (per standing rule, not re-litigated with the user):** only
one social-proof slot ships with real, verifiable claims; the other three ship
`[EMPTY]`-labeled per the existing `lullyrest-proof-placeholder` convention rather than
fabricated reviews, since no real reviews/UGC/press exist yet.

## Cart drawer (Phase C)

Configure `cart-drawer.liquid`'s existing blocks — no new template/section files:

- `cart_progress_bar`: `product_free_shipping` = 160, `product_free_amount` = cooling
  case's price (so the same dollar goal doubles as the free-gift goal once that product
  exists), `progress_bar_free_product` = the cooling case.
- `cart_upsell` × 4: the three existing bonus products (Cooling Migraine Wrap, Blackout
  Sleep Mask, Filtered Earplugs) + the cooling case when not already gifted.
- `cart_timer_bar`: same honest BOGO end-date as the PDP countdown.
- Applied to the draft theme only.

## Rollout / publish gating

Everything above ships in Draft/inactive state: discounts created inactive, new PDP
template built but the live product record's template is not switched to it, cart-drawer
changes live only on the unpublished draft theme. Per CLAUDE.md rule 4, activating the
discounts, switching the product's live template, or publishing the draft theme requires
one final explicit go-ahead — tracked as the last step of the implementation plan, not
skipped by the general "proceed."

## Out of scope / deferred

- A Shopify Function / cart-transform for gift injection — not needed, the native
  Premium Attachment Kit + progress-bar mechanisms cover it.
- Real photography-gated sections (before/after posture shots, UGC video) — stay
  `[EMPTY]` until assets exist, per `research/swipes/dosaze-pdp-breakdown.md` §5.
- Domain resolution — unrelated, still open per `brand/BRAND_GUIDE.md`.
