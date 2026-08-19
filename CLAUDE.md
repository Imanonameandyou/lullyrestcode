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

- Connection method: `shopify-ai-toolkit` plugin (v1.6.1) + Shopify CLI v4.6.1. Store-scoped API operations run via `shopify store auth --store <domain> --scopes <scopes>` + `shopify store execute --store <domain> --query '...'` — no custom app / manually-generated Admin API token needed.
- Store domain: eug1kz-w0.myshopify.com ("My Store", Basic plan, admin: https://admin.shopify.com/store/eug1kz-w0)
- Primary theme in use: **Horizon** (`gid://shopify/OnlineStoreTheme/162844639446`) — role **MAIN** (live), confirmed 2026-08-19 via direct `themes` query. Only theme on the store — no customization yet. Rule 2 applies: any theme/code changes need a new duplicated draft theme first.

## Session objectives (current)

DTC launch prep for the LullyRest Orthopedic Cervical Pillow (target: knowledge workers 30–46 with cervicogenic morning headaches). No products or theme customization started yet. See `README.md` for the project index, `research/` for audience/offer research, and `brand/BRAND_GUIDE.md` for positioning/voice — those are the working references for any copy or product-listing work in this project.

Open decisions blocking launch-facing work (product name, domain, visual identity) are tracked in `brand/BRAND_GUIDE.md`.

## Git / version control

- Remote: https://github.com/Imanonameandyou/lullyrestcode.git — branch `main`.
- This repo tracks project files (research, brand docs, progress log, theme/code work once it starts). It does **not** deploy anything by itself — pushing here is separate from theme publishing (rule 2) or any storefront-visible action (rule 4).
- Workflow: `git pull` before starting work (rule 6) → make changes → commit → `git push origin main` (rule 7).

## Notes

- Store-specific schema details (custom metafields, product types, collection structure, etc.) get captured in Claude's memory as they're discovered, not duplicated here.
