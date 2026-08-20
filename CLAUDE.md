# LullyRest — Shopify Store Project Conventions

This file records the standing rules for how Claude Code operates on this Shopify store. These rules apply to every session unless the user explicitly overrides them in the moment.

## Always-do rules (safety)

1. **Always `/plan` first.** For any task that mutates store data (products, discounts, theme files, pages, navigation, etc.), outline the plan — what will be read, what will be created/changed, and how it will be verified — before executing.
2. **Never edit the Live theme directly.** All theme/code changes happen in a duplicated draft theme. The Live theme is only touched via an explicit, user-approved "publish" step at the very end.
3. **New products, discounts, and pages default to Draft/Hidden.** Nothing goes live-facing without the user reviewing it first and giving explicit go-ahead to publish.
4. **Confirm before irreversible or customer-visible actions**: publishing a theme, activating a discount, publishing a product, sending customer-facing emails, deleting anything.
5. **Log every mutation.** Every API call or file change that alters store state gets an entry in `PROGRESS.md` (see below) — what was called, when, and the result.
6. **Pull before starting any work.** At the start of every session, and before making any file changes, run `git pull` on this repo to ensure the local copy is up to date and avoid merge conflicts.
7. **Push after every change.** Any commit made to this repo gets pushed to `origin main` immediately (`git push origin main`) — don't let local commits pile up unpushed. This does not override rule 2 (never publish the Live theme) or rule 4 (confirm before customer-visible actions) — pushing to this git repo is a code-storage action, not a storefront-publish action.

## Store access

- Connection method: Shopify CLI v4.6.1. Store-scoped API operations run via `shopify store auth --store <domain> --scopes <scopes>` + `shopify store execute --store <domain> --query '...'` — no custom app / manually-generated Admin API token needed.
- **Store domain: gcvy0q-cb.myshopify.com** ("LullyRest" — renamed from "Washa", Basic plan, admin: https://admin.shopify.com/store/gcvy0q-cb). **Active store as of 2026-08-19** — the project migrated here from `eug1kz-w0.myshopify.com`, which is no longer used but was not deleted; its draft theme/product/page were read as the migration source and are not touched going forward.
- Themes on the store (verified 2026-08-19, post-migration):
  - **Horizon** (`163498262786`) — role **MAIN** (live). Never written to.
  - `elixir-1-6-1-pillow` (`163498426626`) — UNPUBLISHED. Elixir is a DTC/advertorial theme shipping `page.advertorial.json`, `page.listicle.json` and a conversion PDP; added directly to this store by the user (not via API).
  - **`LullyRest — Presell + PDP (draft)`** (`163498656002`) — UNPUBLISHED. Duplicated from `elixir-1-6-1-pillow`. **This is the working theme.** See `theme/README.md`.
- Bonus/GWP products (created 2026-08-20, all DRAFT): Cooling Migraine Wrap `9591781064962` ($29, `LR-CMW-001`), Contoured Blackout Sleep Mask `9591783981314` ($24, `LR-CBM-001`), Filtered Sleep Earplugs `9591784243458` ($19, `LR-FSE-001`). Rationale/tiers in `marketing/BONUS_PRODUCTS.md`.
- **`shopify store execute` returns the raw result object, not wrapped in a GraphQL `data` key** — parsers assuming `data` will silently miss `userErrors` and crash after a mutation has already committed.
- **Store auth is per-machine.** A machine with no `~/.config/shopify` needs `shopify auth login` + `shopify store auth` again, regardless of consent granted elsewhere.
- Store objects: product `9589261009154` (DRAFT, `templateSuffix: lullyrest`), page `136591114498` handle `presell` (unpublished, `templateSuffix: presell`).
- **Windows gotchas hit during the 2026-08-19 migration** (this machine runs Windows, prior session notes above were from a Mac): a `shopify theme pull` run immediately after `themeDuplicate` can return an incomplete/assets-only tree — re-run pull (optionally scoped with repeated `--only "<dir>/*"` flags) if `sections/`, `blocks/`, etc. are missing after a pull that reported success. `theme/build_templates.py`'s file opens needed explicit `encoding="utf-8"` — Python's default `open()` uses the OS codepage (cp1252) on Windows and raises `UnicodeEncodeError` on the file's em-dashes/arrows without it (already fixed in the script).

## Swipe files

Two competitor captures live in the **parent** folder (one level above this repo), not in git:
`FireShot Capture 001 — Dosaze Contoured Orthopedic Pillow` (their PDP) and
`FireShot Capture 002 — 10 Reasons Chiropractors Recommend The Dosaze Pillow` (their presell listicle).
**Read these before writing any page copy or choosing a page format.** They are image-only PDFs with no text layer — render with `pdftoppm -r 150` to read. Structural breakdowns are in `marketing/PRESELL_LISTICLE.md`.

## Claim integrity (standing rule)

Never ship a review, star rating, review count, testimonial, named endorsement, certification, or clinical result that does not actually exist. The swipes rely heavily on all of these; the Elixir theme ships demo versions of all of them. Hold the slots open and label them `[EMPTY]` instead. Keep product language structural ("supports", "designed to") rather than therapeutic ("treats", "cures", "relieves migraines"). Unverified claims carry an inline `[VERIFY: …]` marker.

## Session objectives (current)

DTC launch prep for the LullyRest Orthopedic Cervical Pillow (target: knowledge workers 30–46 with cervicogenic morning headaches). Presell listicle and PDP built on the draft theme 2026-08-19; both draft/hidden. See `README.md` for the project index, `research/` for audience/offer research, and `brand/BRAND_GUIDE.md` for positioning/voice — those are the working references for any copy or product-listing work in this project.

Name, price and visual identity are now locked. **Domain remains unresolved and still blocks public launch** — see `brand/BRAND_GUIDE.md`.

## Git / version control

- Remote: https://github.com/Imanonameandyou/lullyrestcode.git — branch `main`.
- This repo tracks project files (research, brand docs, progress log, theme/code work once it starts). It does **not** deploy anything by itself — pushing here is separate from theme publishing (rule 2) or any storefront-visible action (rule 4).
- Workflow: `git pull` before starting work (rule 6) → make changes → commit → `git push origin main` (rule 7).

## Notes

- Store-specific schema details (custom metafields, product types, collection structure, etc.) get captured in Claude's memory as they're discovered, not duplicated here.
