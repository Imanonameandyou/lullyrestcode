# PROGRESS LOG

Audit log of every API call and file change made to the store or this project. Newest entries at the top.

---

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
