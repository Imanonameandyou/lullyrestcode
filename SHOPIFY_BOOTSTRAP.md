# Shopify Project Bootstrap

A reusable setup runbook for starting a new Shopify + Claude Code project. Drop this file into any new project directory and say:

> "Follow the instructions outlined in the .md file at `<path-to-this-file>`"

Claude Code will run through environment setup, connect to the store, and lay down the standing project files — the same steps used to bootstrap this project.

---

## Step 1 — Environment check

Run these checks and report results before doing anything else:

```bash
claude mcp list
claude plugin list
node --version
npm --version
shopify version
```

Confirm: is `shopify-ai-toolkit` in the installed plugins list? Is Node/npm present? Is Shopify CLI present?

## Step 2 — Install the Shopify AI Toolkit plugin

This is Shopify's official Claude Code plugin (launched April 2026) — bundles doc search, GraphQL/Liquid validation, and CLI-based store execution skills (products, orders, discounts, pages, themes). It supersedes any need for a manually-created custom app / hand-copied Admin API token for most store operations.

```bash
claude plugin install shopify-ai-toolkit
```

If already installed, skip.

## Step 3 — Install Shopify CLI

```bash
npm install -g @shopify/cli@latest
shopify version
```

## Step 4 — Authenticate

Ask the user to run this themselves (it opens a browser OAuth flow tied to their personal Shopify account — do not attempt to script around it):

```bash
shopify auth login
```

Wait for them to confirm success before continuing.

## Step 5 — Get the store domain and verify connection

Ask the user for their store's domain (`something.myshopify.com`, findable in Shopify Admin under Settings → Domains, or in the browser URL when logged into `/admin`).

Then verify the connection (read-only, safe to run without asking):

```bash
shopify store info --store <store-domain>.myshopify.com --json
```

Report back the store name, plan, and owner so the user can confirm it's the right store.

## Step 6 — Store-scoped API access (no custom app needed)

For product/discount/order/theme operations, use the CLI's built-in store execution flow instead of a manually-created custom app:

```bash
shopify store auth --store <store-domain>.myshopify.com --scopes <needed-scopes>
shopify store execute --store <store-domain>.myshopify.com --query '...' [--allow-mutations]
```

- `shopify store auth` triggers a one-time browser consent click per new scope set — this is Shopify's own security gate and cannot (and should not) be scripted around.
- Read-only operations: omit `--allow-mutations`.
- Mutations (create/update/delete): include `--allow-mutations`.
- Sales/analytics questions: use ShopifyQL via the `shopifyqlQuery` Admin GraphQL field, scope `read_reports`.

## Step 7 — Create the standing project files

Create `CLAUDE.md` in the project root with these always-do rules (adjust the "Session objectives" section per project):

```markdown
# <Store/Project Name> — Shopify Store Project Conventions

## Always-do rules (safety)

1. **Always /plan first.** For any task that mutates store data (products, discounts, theme files, pages, navigation, etc.), outline the plan before executing.
2. **Never edit the Live theme directly.** All theme/code changes happen in a duplicated draft theme.
3. **New products, discounts, and pages default to Draft/Hidden.** Nothing goes live-facing without explicit user go-ahead to publish.
4. **Confirm before irreversible or customer-visible actions**: publishing a theme, activating a discount, publishing a product, sending customer-facing emails, deleting anything.
5. **Log every mutation** in PROGRESS.md — what was called, when, and the result.

## Store access

- Connection method: `shopify-ai-toolkit` plugin + Shopify CLI (`shopify store auth` / `shopify store execute`)
- Store domain: <fill in>
- Primary theme in use: <fill in>

## Session objectives (current)

<fill in per project>
```

Create `PROGRESS.md` in the project root as an audit log:

```markdown
# PROGRESS LOG

Audit log of every API call and file change made to the store or this project. Newest entries at the top.

---

## <date>

- <setup steps performed>
```

## Step 8 — Confirm and hand off

Summarize what's connected (store name, plan, owner) and ask the user what they want to work on first. Do not start mutating store data — creating products, discounts, pages, or theme changes — until they've told you the actual task; this file only covers environment setup.

---

## Notes for future updates to this file

- If Shopify changes the plugin name, CLI command surface, or the store-execution flow, update this file rather than relying on trained knowledge — the tooling around AI agents on Shopify is new and moves fast (this file was last validated 2026-08-07 against `shopify-ai-toolkit` v1.6.1 / Shopify CLI v4.6.0).
