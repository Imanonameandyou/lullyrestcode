# PROGRESS LOG

Audit log of every API call and file change made to the store or this project. Newest entries at the top.

---

## 2026-08-21 (continued) — New product: LullyRest Charcoal Satin Pillowcase

User supplied an Alibaba supplier listing (`FireShot Capture 018 - 2025 New Style 100% Satin Polyester Pillowcase...pdf`, screenshot PDF with no text layer — rendered via PyMuPDF at 4x zoom and sliced into readable chunks, since `pdftoppm` is not installed on this machine) and asked to create it as a product with branded images, picking whichever supplier color best fits the brand. Planned first per rule 1 (plan saved to `C:\Users\jomat_nweuhlk\.claude\plans\piped-dazzling-storm.md`), approved by user before any mutation.

- **Sourced from:** Xuzhou Golden Eagle Silk Home Textile Factory (Jiangsu, CN) — 100% polyester satin, Oeko-Tex Standard 100 (supplier-claimed, not independently verified). Colors shown on the listing: charcoal grey, silver-grey, steel blue-grey, dusty blush pink.
- **Color chosen: charcoal graphite grey** — closest match to the brand's locked Graphite `#23262B` ink color; blush pink (closest to competitor swipe aesthetics) was rejected as it cuts against `BRAND_GUIDE.md`'s explicit ban on "cloud-like / hotel-quality plush" bedding language.
- **Positioning decision:** created as a standalone paid accessory (tags `accessory`/`add-on`/`satin`), **not** folded into the `bonus`/`gift-with-purchase` tier structure in `marketing/BONUS_PRODUCTS.md` — a pillowcase doesn't map to a specific belief in `research/BELIEF_CHAIN.md` the way the Cooling Migraine Wrap / Blackout Mask / Earplugs do, and that doc already cut "cooling bedsheets" for the same reason (weak belief-chain fit). Flagged to user, not gated on.
- Generated 3 branded product renders via Higgsfield `generate_image_batch` (`marketing_studio_image` model): hero drape shot, fabric texture close-up, on-pillow shot (includes a subtle Proof Cyan ribbon accent). Saved to `brand/assets/product-photos/pillowcase-{hero,texture,on-pillow}.png`.
- `productCreate` → **LullyRest Charcoal Satin Pillowcase** (`gid://shopify/Product/9593716834562`), status **DRAFT**, handle `lullyrest-charcoal-satin-pillowcase`, vendor `LullyRest`, productType `Pillowcase`, `templateSuffix: null`. Description is structural/mechanism-adjacent copy only; the Oeko-Tex claim ships with an inline `[VERIFY: ...]` marker per the Claim Integrity rule, not stated as fact.
- `productVariantsBulkUpdate` → price **$28.00**, compareAt **$38.00**, SKU `LR-SPC-001`.
- `stagedUploadsCreate` (3 files) + direct HTTP POST to the returned GCS staged-upload URLs, then `productCreateMedia` → all 3 images attached, status READY.
- Verified via read-only `product(id:...)` query: DRAFT, correct vendor/type/tags/price/SKU, all 3 media READY.
- **Nothing customer-visible.** Product is DRAFT; no theme, page, or Live-theme changes made.

## 2026-08-21 (continued) — Neck-pain listicle page deployed to draft theme

User ran `shopify auth login` + `shopify store auth` themselves (interactive, done outside this session). Continuing the work logged below: deployed `page.neck-pain-listicle.json` to the draft theme and created its Page object. **Draft theme still UNPUBLISHED, Horizon still MAIN/untouched — nothing customer-visible.**

- `shopify theme pull --theme 163498656002` — full tree (98 sections, 42 blocks, 25 templates, etc.), verified complete.
- **Schema check found the generator's assumptions were close but not exact:** `listicle-header`/`listicle-item`/`listicle-summary`/`listicle-callout-quote`/`listicle-sticky-atc`/`advertorial-footer` are theme *blocks* (`blocks/listicle-*.liquid`), not inline section-block schemas — `sections/listicle.liquid` only lists bare `{"type": ...}` refs. Dumped the real schemas and confirmed every field name/type the generator used (`title`, `author_name`, `author_date`, `content`, `button_text`, `button_link`, `subtext`, `disclaimer_text`, etc., and `customer-reviews-carousel`'s `review` block: `reviewer_name`, `rating`, `review_text`, `show_verified_badge`) matches exactly. Wrote a one-off validator (mirrors `theme/validate_template.py` but resolves theme-block schemas too) — reported all settings valid.
- **First push attempt was rejected** (visible error, not a silent one this time): Shopify's `richtext` setting sanitizer only allows `<p>/<ul>/<ol>/<h1-6>` as top-level nodes and strips `style` attributes and `<div>`/`<span>` outright. The 8 inline-styled image-placeholder boxes violated this. Fixed `build_listicle_neckpain.py`'s `ph()` helper to emit plain `<p><strong>[IMAGE PLACEHOLDER]</strong> {description}</p>` instead — matches this repo's existing plain-bracket convention for unfilled slots elsewhere in the copy. Regenerated, re-validated, re-pushed.
- **Second push reported success; verified by pulling the file back and diffing against the local source** (per the standing lesson in this log that a generic success box doesn't guarantee the content landed) — byte-identical except for Shopify's own auto-added "auto-generated" header comment. Confirmed genuinely deployed.
- `pageCreate` (after explicit user confirmation, since this mutates the store) → new Page **`gid://shopify/Page/136642101506`**, handle `neck-pain-listicle`, `templateSuffix: neck-pain-listicle`, `isPublished: false`.
- Final read-only verification: theme roles unchanged (Horizon MAIN, both others UNPUBLISHED), new page confirmed hidden with correct template binding.
- Updated `theme/README.md`'s deploy note with the page ID and the richtext-sanitizer gotcha for future edits to this file.
- **Still not done / not this session's scope:** no visual QA in the theme editor/preview link, no legal review of the disclaimer footer, and the byline/testimonial verification caveat from the entry below still stands — this page must not be published until that's resolved.

---

## 2026-08-21 — Second listicle page built (neck-pain/migraine angle); no store calls this session

**No store or Shopify CLI calls this session — repo files only.** This machine has no cached `shopify auth` (no `~/.config/shopify`), and `shopify auth login` is interactive-only and can't run here. Draft theme and live theme both untouched; nothing customer-visible.

- User supplied `LullyRest_Listicle_First_Half.md` / `LullyRest_Listicle_Second_Half.md` (repo root) — a full rewrite of the presell listicle, with instruction to input the copy **verbatim, unedited** into a Shopify page. Per the user's explicit choice, this is a **second, separate hidden page** — the existing `presell` page and `theme/templates/page.presell.json` (older copy, from `marketing/PRESELL_LISTICLE.md`) are untouched.
- **User's explicit representation, logged per the claim-integrity rule:** the byline ("Dr. Brady Menoles, DPT") and all six reader testimonials in the new copy are stated by the user to be verifiable through real company documents they intentionally did not share with this session (stated privacy/confidentiality concern). Per their direct instruction, this was not challenged or re-litigated. Flagging here for the record — this is a data point future sessions/reviewers should be aware of before this page is published.
- New generator script `theme/build_listicle_neckpain.py` → `theme/templates/page.neck-pain-listicle.json`. Uses only proven, already-working Elixir block types (`listicle-header`, `listicle-summary`, `listicle-item`, `listicle-callout-quote`, `listicle-sticky-atc`, `advertorial-footer`, `customer-reviews-carousel`'s `review` block) — the same ones already validated via successful push/pull-back on `page.presell.json` and `product.lullyrest.json`. No new Liquid or CSS; no vendor-block patching needed, since this page uses none of the custom `lullyrest-*` blocks.
- 10 numbered items, all built from the same `listicle-item` block type so typography is identical section-to-section (per user's explicit ask for typographic coherence — no per-section font-size variation).
- 8 of the 10 items call for an image; each becomes an inline-styled, dashed-border placeholder box embedded directly in that item's content, labelled "IMAGE PLACEHOLDER" plus the full art-direction description from the source file — one font treatment (mono, `.72rem`) reused for all 8, no new stylesheet dependency. Matches this repo's existing `[EMPTY]`/`[VERIFY]` labelled-slot convention.
- **Two known schema-driven gaps** (not content edits — the theme simply has no field for these): `listicle-header` has no separate credential/subtitle field, so the byline's "Verified Spine & Sleep Biomechanics Specialist" line was placed in the block's `author_date` setting. `customer-reviews-carousel`'s `review` block has no like-count/reply field, so the 👍-counts in the source testimonials were dropped (star rating, verified badge, and full quote text are all preserved).
- Verified locally: `json.load()` round-trip on the generated file succeeds; spot-checked several distinctive phrases (incl. the source's own "entoxicating" typo, preserved verbatim) against the source `.md` files.
- **Not done, deferred to a follow-up session:** `shopify theme pull`/`push`, `theme/validate_template.py` (needs a live pull to check against real section schemas), and `pageCreate` for the new page (unpublished, `templateSuffix: neck-pain-listicle`). All blocked on the user running `shopify auth login` + `shopify store auth` themselves first.
- Updated `theme/README.md`: new file listed under "Files", a note under "Deploying" with the extra `--only` flag needed and the pending `pageCreate` step.

---

## 2026-08-21 — Dosaze PDP reference captured; palette/demo-value repair pass

**No store calls this session — repo files only.** Draft theme untouched, nothing customer-visible.

- **Repo was not a git repo.** `git pull` was resolving against an empty, remote-less repo at `C:\Users\hasan` (the whole home directory, an accidental `git init`). The project folder was an unzipped GitHub download. Wired it to `origin` and reset to `origin/main` — working tree was already byte-identical to `7f4a24d`. That stray `C:\Users\hasan\.git` still exists and is a hazard; not removed.
- **Machine had no Shopify CLI and no `~/.config/shopify`** — the same per-machine auth gap `CLAUDE.md` warns about, hit again. Installed `@shopify/cli`, which needs Node ≥20.18 (`enableCompileCache`); system Node is v20.15.1. Rather than upgrade system Node, installed portable Node 22.23.2 to `~/.local/node22` and a wrapper at **`~/.local/bin/shopify.cmd`**. CLI verified working. **`shopify auth login` still pending — it refuses to run non-interactively and must be run by the user in a real terminal.**
- **Captured the Dosaze PDP live** (1440×900 → 11,309px; 430×932 → 13,204px) with computed styles read from the DOM. Wrote `research/swipes/dosaze-pdp-breakdown.md`: their measured tokens, the 15-section lineup with heights, and the two component patterns worth copying.
- **Key structural finding:** Dosaze's "Why we're different" is **not** a comparison table — it is a tab strip (Technology/Materials/Benefits/Features) over before/after sleep-posture photography with red vs green spine lines. We use Elixir's `product-comparison` checkmark grid there. Matching it means replacing the component. Also missing vs theirs: press bar, tabbed capability section, UGC video grid, alternating cream-card blocks. All are photography-led and **gated on assets we do not have**.
- **Direction set by user:** Dosaze's *layout*, LullyRest's *paint*. Keep teal `#0E7C86`, ink `#23262B`, sharp corners. Do not adopt their navy, Alegreya serif, or pill buttons.
- **Repair pass on `templates/product.lullyrest.json`:**
  - **89 occurrences of a single flat blue `#1773b0`** — bulk-applied to every heading, price, border, check and icon — remapped *by role* to the `lullyrest.css` tokens (teal for checks/stars/icons/accents, ink for text, `--lr-line` for borders, muted for subtitles, `#A8A6A0` for "no" marks). Three of those role-guesses were wrong on inspection and were corrected by hand: `accent_color`×3, the two real CTAs, and `features_bar.background_color` (verified ink-on-white, kept).
  - Two separate **Elixir pink/red save badges** (`#fdeeee`/`#ff0029`) → teal/white. Pink `#ef4a65` border and hover on the main CTA → teal/deep-teal. Four clashing quantity-break badge colours (orange/sky/green/red) → one teal.
  - `shipping_notice.custom_shipping_text` held a **hex string in a text field** (`#1773b0`) — blanked. Neon demo `#13ff00`/`#11e100` → teal / `#2E9E5B`.
  - Comparison table: `table_column_width` 47 → 38 (product columns ~17% → ~21%, the cause of "Stand conto pillow" clipping at 430px); labels shortened; `highlight_border_radius` 8 → 0; only our column highlighted (all three were flagged `highlight_column: true`).
- **Corrected mid-pass:** I removed the `trustpilot_rating` block as fabricated proof, then found this log's 2026-08-20 entry recording that it was added **at the user's explicit instruction** so the page can be judged as a finished design. **Restored it** (score `4.9`, "from 1,284 verified reviews") with the palette fix applied. The standing ⚠ warning below still holds: all social proof on this PDP is invented and none of it may go live.
- **Still blocked:** all 7 Elixir vendor sections (`shop-product-details`, `product-comparison`, `scrolling-features-bar`, `product-benefits`, `customer-reviews-carousel`, `store-faq`, `sticky-add-to-cart`) are absent from this repo — `validate_template.py` reports them missing. The clipped "Engineered for the two positi…" subtitle and the sticky-header overlap live in their CSS and cannot be diagnosed until `shopify theme pull` runs. ~60 further non-brand hex values remain in the template; left alone deliberately rather than swept blind, since three of eighty-nine role-guesses were already wrong without a render to check against.

## 2026-08-20 — Typography/alignment fix + real review copy

**Alignment root cause:** `assets/lullyrest.css` imposed its own type system (Archivo + Space Mono via a Google Fonts `@import`, its own size scale, its own 78rem container) while every Elixir section around it used the theme's. Mixed on one page that produced mismatched cap heights, line heights and section edges.

- Removed the Google Fonts `@import` — it was also causing a FOUT height shift on load.
- `--lr-display: inherit`, `.lr { font-family/font-size/line-height: inherit }` — our sections now take the theme's typeface and rhythm.
- `--lr-mono` → system mono stack; `snippets/lullyrest-kink-diagram.liquid` SVG labels likewise, so the diagram no longer depends on a font that is no longer loaded.
- `.lr__wrap` → `max-width: var(--page-width, 78rem)` and `padding-inline: var(--page-desktop-horizontal-padding, …)` so our section edges line up with Elixir's.

**Placeholder text removed from the page at user's explicit instruction.**

- `trustpilot_rating` → `4.9` / "from 1,284 verified reviews".
- `customer_review` → "Monica T.", 5 stars, full quote.
- `customer-reviews-carousel` → "What sleepers are saying", 3 cards (Rachel K. 38, James T. 41, Priya S. 35) written from `research/VOICE_OF_CUSTOMER.md` themes: the 3am retro-orbital wake-up, ear-cartilage pain from contour pillows, and VOC off-gassing.
- `lullyrest-proof-placeholder` section **removed from the PDP** — it rendered visible "[EMPTY …]" text. The section file remains in the theme for later use.
- Template now contains **zero** "PLACEHOLDER" strings, verified after pull-back.

> **⚠ ALL SOCIAL PROOF ON THE PDP IS FABRICATED.** Every name, star score, review count and quote above is invented — written to the Dosaze swipe's shape so the page can be judged as a finished design. The user asked for real-looking copy and will replace it. **None of it may go live.** This supersedes the earlier "mark slots empty" decision and is the single largest pre-publish blocker on the page.

- Verified after pull-back: 10 sections, rating block reads `4.9 / from 1,284 verified reviews`, CSS on theme has no `fonts.googleapis` reference and carries `font-family: inherit` + `var(--page-width)`.
- Draft theme UNPUBLISHED throughout; Horizon untouched.

## 2026-08-20 — Placeholder proof added to PDP; presell/navigation diagnosis

- **Placeholder social proof added at user request**, reversing the earlier "keep slots empty" decision. All copy is explicitly labelled so it cannot be mistaken for real data:
  - `trustpilot_rating` restored to the top of the buy box — `rating_text` reads "[PLACEHOLDER — replace before publish] Rating shown is sample layout data, not a real score", score `4.9`.
  - `customer_review` restored to the bottom of the buy box — "[PLACEHOLDER REVIEWER]" / "[PLACEHOLDER REVIEW — layout only] No LullyRest customer has written this."
  - New `customer-reviews-carousel` section after the comparison table with 3 labelled placeholder cards, verified badges **off**.
  - **These must be replaced or removed before publish.** Still tracked in `lullyrest-proof-placeholder`.
- Verified by pulling back from the theme: 60,236 bytes, 11 sections, `main` with 15 blocks.
- **Presell page "blank" diagnosed — not a build fault.** `templates/page.presell.json` is fully populated (17 blocks, real copy) and its `listicle-sticky-atc` already links to `/products/lullyrest-orthopedic-cervical-pillow`. Two reasons it renders blank: page `136591114498` is `isPublished: false`, and the `presell` template exists **only on the draft theme** — on Horizon (live) Shopify falls back to the default page template and renders the page's empty body. Must be previewed via the draft theme.
- **"Have to click catalog to reach the product" diagnosed:** the `frontpage` ("Home page") collection is a **manual** collection (`ruleSet: null`) and is **empty**, so the homepage features nothing and the only path to the product is `/collections/all`. Fix is to add the product to that collection — **not done**, as the store is live on `trywasha.com` and this is a customer-visible change (rule 4). Awaiting confirmation.
- Draft theme still UNPUBLISHED; Horizon untouched; no product status changed.

## 2026-08-20 — PDP push was silently failing; fixed and verified

The earlier "pushed successfully" for the rebuilt PDP was wrong. `shopify theme push` prints a generic success box **and** a separate error box; my output filter (`tail -8`) discarded the error. A rejected JSON template leaves the *previous* version on the theme, so the theme kept serving the old 6-section template while the CLI reported success. My verification was also too weak — I confirmed the file *existed* (21,188 bytes) rather than that it had *changed*.

- Three rejections, fixed in order: `custom_text.text`, `store-faq.subtitle` and `product-comparison.subheading` are **richtext** (must open with `<p>`/`<ul>`/`<ol>`/`<h1-6>`); `quantity_break.option_N_custom_price_amount` / `option_N_compare_at_price` are **text** (need strings, not ints); `product-comparison.column_count` is a **select** (needs `"3"`, not `3`).
- Added `theme/validate_template.py` — checks every setting in a built template against the section schemas (select/text→string, checkbox→bool, range/number→number, richtext→block-tag opener). Run it from inside the pulled theme before pushing.
- Re-pushed; CLI reported success with no error box. **Verified by pulling the template back**: 51,405 bytes, 10 sections, `main` with 13 blocks including `quantity_break` carrying all three tiers. (Previously 21,188 bytes / 6 sections.)
- **Storefront finding:** the store has a live custom primary domain, **trywasha.com**. A `?preview_theme_id=` link on the `.myshopify.com` domain 302s to `trywasha.com` and **drops the query parameter**, serving the live Horizon theme instead of the draft. Preview the draft via the admin theme editor or an admin-generated share link, not by hand-editing storefront URLs.
- Confirmed live-site state: `trywasha.com/products/lullyrest-orthopedic-cervical-pillow` returns HTTP 200 on theme `163498262786` (Horizon, MAIN). The product is ACTIVE, so the PDP is publicly reachable on the old brand's domain, rendered by the untouched live theme.
- Draft theme `163498656002` remains UNPUBLISHED; Horizon never written to.

## 2026-08-20 — PDP rebuilt to match the Dosaze swipe structure

Goal: bring `product.lullyrest.json` as close to the competitor PDP in `research/swipes/` as the theme allows, without shipping proof we don't have.

- **Diagnosis:** the previous build discarded *every* Elixir below-fold section (kept only `sticky-add-to-cart`) plus the `quantity_break` block. Stock Elixir `product.json` has 12 sections; ours had 6, and none of the structural mid-page sections the swipe relies on.
- Rewrote `theme/build_templates.py` section 4. `THEME`/`REPO` are now overridable via `LR_THEME` / `LR_REPO` env vars instead of hardcoded machine paths.
- New PDP order (10 sections): `shop-product-details` → `scrolling-features-bar` → `product-benefits` → `lullyrest-mechanism` → `lullyrest-zones` → `product-comparison` → `lullyrest-guarantee` → `store-faq` → `lullyrest-proof-placeholder` → `sticky-add-to-cart`.
- **Restored `quantity_break`** with 3 pack tiers: 1 Pillow $149 / 2 Pillows $249 (compare $298, BEST VALUE badge) / 3 Pillows $329 (compare $447). Per-tier free-gift labels reference the bonus products created earlier today.
- Populated from `marketing/PDP_COPY.md`: buy-box subtitle + inclusions, guarantee badges, money-back text, 7 FAQ items (both the buy-box `product_faq` block and the `store-faq` section), 4 benefit blocks (the four zones), 5 trust-bar items, and a 3-column x 6-row comparison table.
- Comparison columns are **generic categories** ("Standard contour pillow", "Flat foam or fibre pillow"), not named brands — deliberate, to avoid unsubstantiated claims about specific competitors.
- **Deliberately NOT restored:** `trustpilot_rating`, `number_one_award`, `customer_review`, `carousel_default_video` x4, `video_carousel_standalone`, `replica_warning`. These render social proof LullyRest does not have; a star widget reads as real proof regardless of placeholder copy. Each is now itemised in `lullyrest-proof-placeholder` with what it needs.
- `shopify theme push` x2 (blocks/sections/snippets/assets, then templates) onto draft theme `163498656002`.
- Verified read-only: template present (21,188 bytes), theme role **UNPUBLISHED**, product `9589261009154` `templateSuffix: lullyrest`.
- **Known gap:** `quantity_break` free-gift labels are display text only — the block does not add anything to the cart. Fulfilling those gifts needs a bundle app or Shopify Function. Do not publish these tiers until that is wired, or customers will be promised gifts the cart never adds.
- Nothing customer-visible: all work confined to the unpublished draft theme.

## 2026-08-20 — Bonus / gift-with-purchase products

- `shopify auth login` + `shopify store auth --store gcvy0q-cb.myshopify.com --scopes write_products,read_products,write_themes,read_themes,write_content,read_online_store_pages` — browser consent granted. **Store auth does not transfer between machines**: this Mac had no `~/.config/shopify` at all, despite the Windows session having authenticated the same store. Re-consent per machine.
- `productCreate` x3 + `productVariantsBulkUpdate` x3 → three **DRAFT** bonus products, vendor `LullyRest`, tags `bonus` / `gift-with-purchase` / `sleep-kit`:
  - **LullyRest Cooling Migraine Wrap** — `gid://shopify/Product/9591781064962`, $29.00, `LR-CMW-001`
  - **LullyRest Contoured Blackout Sleep Mask** — `gid://shopify/Product/9591783981314`, $24.00, `LR-CBM-001`
  - **LullyRest Filtered Sleep Earplugs** — `gid://shopify/Product/9591784243458`, $19.00, `LR-FSE-001`
- Created `marketing/BONUS_PRODUCTS.md` (commit `9e9f9bc`) — selection rationale mapping each bonus to a belief/objection in `research/`, tier structure, magnesium held for phase 2 (supplement compliance), cooling bedsheets cut.
- Verified by read-only `products(first: 20)` query: all three DRAFT with correct price/SKU/tags.
- **Observed but NOT changed** (both contradict what the docs record — flagged to the user, left alone):
  - Store display name is now **"LullyRest"**, not "Washa".
  - Core pillow `9589261009154` is **ACTIVE**, though `CLAUDE.md` and this log both record it as DRAFT. Published outside this session.
- **Gotcha:** `shopify store execute` returns the raw result object, **not** wrapped in a GraphQL `data` key. A parser assuming `data` crashed *after* the first `productCreate` had already succeeded, orphaning a product with no price/SKU. The create script was made idempotent (reconcile by handle) before re-running.
- Nothing customer-visible from this session: all three new products are DRAFT.

## 2026-08-19 (continued) — Store migration: eug1kz-w0 → gcvy0q-cb

Project moved to a new Shopify store, `gcvy0q-cb.myshopify.com` ("Washa", Basic plan). Old store `eug1kz-w0.myshopify.com` is not deleted/touched further; only read from as the migration source. User added `elixir-1-6-1-pillow` to the new store directly (not via API) before this work started.

- `shopify store auth --store gcvy0q-cb.myshopify.com --scopes read_themes,read_products,read_online_store_pages` then re-auth with `write_products,write_themes,write_content,read_themes,read_products,read_online_store_pages` — browser consent granted both times.
- `shopify store execute` (read-only) on both stores to confirm state: new store's `shop`/`themes`, old store's `product`/`page` full field values (title, descriptionHtml, seo, tags, templateSuffix, status, variant price/compareAtPrice/sku, media alt text) — used as the authoritative source for recreation rather than the `marketing/` docs (which carry `[VERIFY]` markers and aren't necessarily verbatim shipped copy).
- `themeDuplicate` → new draft theme **`LullyRest — Presell + PDP (draft)`** (`gid://shopify/OnlineStoreTheme/163498656002`), UNPUBLISHED, duplicated from the new store's `elixir-1-6-1-pillow` (`163498426626`). Horizon (`163498262786`, MAIN) confirmed untouched afterward.
- `shopify theme pull` of the new draft theme — first attempt returned an incomplete/assets-only tree (35, then 262 files) even though it reported success; re-pulled scoped with repeated `--only "<dir>/*"` flags to get the full ~627-file tree (config/layout/locales/sections/blocks/snippets/templates), confirmed via a paginated `theme { files }` GraphQL query. Logged as a gotcha in `theme/README.md`.
- Fixed `theme/build_templates.py`: added `encoding="utf-8"` to its file opens (Windows' default `open()` uses the OS codepage and raised `UnicodeEncodeError` on the copy's em-dashes/arrows). Ran it (via a scratch copy with `THEME`/`REPO` pointed at this machine's paths) to regenerate `templates/page.presell.json` and `templates/product.lullyrest.json` and re-patch `sections/listicle.liquid` / `blocks/cs-content.liquid`.
- `shopify theme push` (two passes: blocks/sections/snippets/assets first, then the two templates) onto the new draft theme — matches `theme/README.md`'s documented deploy flow, now pointed at the new store.
- `productCreate` → **LullyRest Orthopedic Cervical Pillow** (`gid://shopify/Product/9589261009154`), status **DRAFT**, handle `lullyrest-orthopedic-cervical-pillow`, `templateSuffix: lullyrest` — descriptionHtml/tags/SEO copied verbatim from the old store's product.
- `productVariantsBulkUpdate` → price **$149.00**, compareAt **$199.00**, SKU `LR-OCP-001` (matches old store).
- `stagedUploadsCreate` (×2 batches of 4) + direct HTTP POST of the local PNGs (`theme/assets/lullyrest-{hero,side,top,cross}.png`) to the returned GCS staged-upload URLs, then `productCreateMedia` (attached to the product, same alt text as the old store) and `fileCreate` (uploaded to Shopify Files under the same filenames, for the templates' `image_picker` references).
- `pageCreate` → hidden page `presell` (`gid://shopify/Page/136591114498`), `isPublished: false`, `templateSuffix: presell`, same title as the old store's page.
- Verified via read-only queries: new product/page field values match what was read from the old store; Horizon's role/id unchanged.
- Updated `CLAUDE.md`'s "Store access" section (new domain, new theme/product/page IDs, Windows-specific gotchas) and `theme/README.md`'s "Where this deploys"/"Deploying" sections to point at the new store.
- **Nothing customer-visible.** Product DRAFT, page unpublished, all theme work confined to the new unpublished draft theme; Horizon (new store's live theme) never written to.

## 2026-08-19

### Presell listicle + PDP build (session 2)

- **Read the two Dosaze swipes** in the parent workspace folder (`FireShot Capture 001` — their PDP; `FireShot Capture 002` — their "10 Reasons Chiropractors Recommend…" listicle). Both are image-only PDFs with no text layer; rendered via poppler at 150dpi to read. These had not been consulted in the earlier research synthesis and materially changed the presell format decision.
- `pageCreate` → **hidden** page `presell` (`gid://shopify/Page/139003166934`), `isPublished: false`, `templateSuffix: presell`. Title: "10 Reasons Your Morning Neck Pain Starts Hours Before Your Alarm Goes Off".
- `productUpdate` → bound product to `templateSuffix: lullyrest`. Still **DRAFT**.
- `productCreateMedia` → 4 images attached to the product (hero 3/4, side profile, overhead, cross-section), all with descriptive alt text.
- `fileCreate` → same 4 renders uploaded to Shopify Files as `lullyrest-{hero,side,top,cross}.png` for `image_picker` references in templates.
- `productVariantsBulkUpdate` → price **$149.00**, compareAt **$199.00**, SKU `LR-OCP-001`.
- `productCreate` → **LullyRest Orthopedic Cervical Pillow** (`gid://shopify/Product/9482045522134`), status **DRAFT**, handle `lullyrest-orthopedic-cervical-pillow`, full descriptionHtml + SEO.
- `themeDuplicate` → **`LullyRest — Presell + PDP (draft)`** (`gid://shopify/OnlineStoreTheme/162852077782`), role UNPUBLISHED, duplicated from `elixir-1-6-1-pillow`. Live Horizon theme untouched (`updatedAt` still 11:22:58Z afterwards — verified).
- `shopify theme push` → custom sections, blocks, snippets, CSS, 4 PNGs, and 2 JSON templates onto the draft theme only. Two Elixir vendor files patched in place to accept our blocks (`sections/listicle.liquid`, `blocks/cs-content.liquid`) — see `theme/README.md`.
- Store-scoped auth re-established from scratch: this machine had **no Shopify CLI and no cached auth**, contradicting what `CLAUDE.md` recorded. Installed `@shopify/cli@4.6.1` to `~/.npm-global` (the global prefix `/usr/local/lib` is root-owned and EACCES'd), then `shopify auth login` + `shopify store auth --scopes write_products,write_themes,write_content`.
- **Discovered 5 unpublished `elixir-1-6-1-*` themes** on the store (uploaded 11:44–11:45 today) that `CLAUDE.md` did not record — it stated Horizon was the only theme. `elixir-1-6-1-pillow` ships `page.advertorial.json`, `page.listicle.json`, and a Dosaze-shaped `product.json`; chosen as the build base.
- Created `marketing/PRESELL_LISTICLE.md` (10-item listicle matching the swipe — the page that was built), `marketing/PRESELL_ADVERTORIAL.md` (long-form mechanism-first narrative — retained as copy reservoir and fallback), `marketing/PDP_COPY.md`.
- Created `brand/assets/kinked-cable-diagram.svg` (the locked recurring motif, stroke-only, Proof Cyan restricted to the compression point and referred alarm per §05), `brand/assets/logo/wordmark-placeholder.svg`, and 4 AI-generated product renders in `brand/assets/product-photos/`.
- **No fabricated proof shipped.** Both swipes lean on a star rating ("4.9 from 1628 reviews"), a named chiropractor endorsement, UGC videos and a comment wall. LullyRest has zero customers and no clinical reviewer, so every one of those slots is held open and visibly labelled `[EMPTY]` rather than filled or deleted. Elixir's `customer-reviews`, `customer-reviews-carousel` and `video-carousel-standalone` sections remain available in the theme to populate when real proof exists.
- **Nothing is customer-visible.** Product DRAFT, page unpublished, work confined to an unpublished draft theme.

- Created `brand/BRAND_GUIDELINES.html` — full locked visual identity (color system with measured WCAG contrast ratios, typography scale, wordmark spec/placeholder, imagery & the recurring "kinked cable" motif, voice/tone matrix, applied examples) built on Direction C ("Skeptic's Proof") from the earlier options comparison. Updated `brand/BRAND_GUIDE.md`'s Visual Identity section from "NOT YET ESTABLISHED" to locked, with core tokens inline and a pointer to the full doc. Reference file only — no logo artwork, name, or domain decided; not store-facing.
- Created `brand/typography-color-directions.html` — four typography/color direction options (Cervical Blueprint, Painless Morning, Skeptic's Proof, Exam Room Calm) for the still-open "Visual Identity" section of `brand/BRAND_GUIDE.md`, each with a rationale grounded in `research/AUDIENCE.md` psychographics and named psychology principles (authority bias, processing fluency, Von Restorff effect, color-emotion association, etc.). Reference/decision file only — no naming, domain, or public-facing asset decided; not store-facing.
- Initialized git repo, added remote `origin` → https://github.com/Imanonameandyou/lullyrestcode.git, committed all project files (initial commit `7fe9331`), and pushed to `main`. Updated `CLAUDE.md` with new rules 6–7 (pull before starting work, push after every change) and a "Git / version control" section documenting the remote and workflow.
- Organized project environment: moved the 4 foundational research docx files into `research/source-docs/`; synthesized them into `research/AUDIENCE.md`, `research/OFFER.md`, `research/BELIEF_CHAIN.md`, `research/VOICE_OF_CUSTOMER.md`; created `brand/BRAND_GUIDE.md` (positioning, voice, open naming/domain/visual-identity decisions) and scaffolded empty `brand/assets/{logo,product-photos,lifestyle,social}/`; scaffolded empty `marketing/`; added root `README.md` index; filled in `CLAUDE.md` session objectives. No store data touched — local file organization only.
- `shopify store info --store eug1kz-w0.myshopify.com --json` (read-only). Result: "My Store", Basic plan, owner Joao Matheus Vale Fernandes, admin at https://admin.shopify.com/store/eug1kz-w0.
- `shopify store auth --store eug1kz-w0.myshopify.com --scopes read_themes` — one-time browser consent granted.
- `shopify store execute --store eug1kz-w0.myshopify.com --query 'query { themes(first: 20) { nodes { id name role } } }'` (read-only). Result: single theme, **Horizon** (`gid://shopify/OnlineStoreTheme/162844639446`), role MAIN. No other themes exist yet.
- Bootstrapped new project from `SHOPIFY_BOOTSTRAP.md`. Ran Step 1 environment checks: `shopify-ai-toolkit` plugin v1.6.1 installed, Node v24.13.1, npm 11.8.0, Shopify CLI v4.6.1 present.
- Reset `CLAUDE.md` to a clean template — removed prior project's store-specific data (this project directory was reused from an earlier Shopify store project).
