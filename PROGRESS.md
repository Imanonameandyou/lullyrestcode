# PROGRESS LOG

Audit log of every API call and file change made to the store or this project. Newest entries at the top.

---

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
