# LullyRest New PDP + BOGO Offer + Cart Drawer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a brand-new Shopify product template (`product.lullyrest-close.json`, template suffix `lullyrest-close`) for the LullyRest pillow using only Elixir's native section/block library, wire up a real BOGO discount plus a free-gift discount on the existing Charcoal Satin Pillowcase (kept at its real $28 price, made free at checkout via a real Buy-X-Get-Y discount, not a $0-priced product), and configure the existing (previously unpulled) Elixir cart drawer with a free-shipping progress bar and an upsell rail that surfaces the pillowcase as the free gift — all landed in Draft/inactive state pending one final go-ahead.

**Architecture:** A new Python generator script (`theme/build_pdp2.py`, sibling to `theme/build_templates.py`, reusing its `stock()`/`add()`/`rebuild_blocks()`/`block_of()`/`put()` helpers) assembles the new template JSON from stock Elixir section types, most content copied verbatim from the existing `product.lullyrest.json`. Cart-drawer configuration is a direct edit to `config/settings_data.json`'s `current.sections["cart-drawer"]` entry (it currently has no block instances at all). All offer mechanics (BOGO, free shipping) are real Shopify automatic discounts created via `shopify store execute`, not theme-only cosmetics — the theme's own schema `info` text confirms the display widgets require a backing discount to actually apply anything at checkout.

**Tech Stack:** Shopify CLI v4.6.1+ (`shopify theme pull/push`, `shopify store execute`), Python 3 stdlib only (`json`, `re`, `shutil`, `os`), Elixir theme (Liquid + JSON templates), GraphQL Admin API (via `shopify store execute`).

**Spec:** `docs/superpowers/specs/2026-08-21-pdp-rebuild-bogo-cart-design.md`

## Global Constraints

- Store domain: `gcvy0q-cb.myshopify.com`. Draft theme: `LullyRest — Presell + PDP (draft)` (`163498656002`). Live theme Horizon (`163498262786`) is **never** written to.
- Core pillow product: `gid://shopify/Product/9589261009154`, $149.00 / compare-at $199.00, SKU `LR-OCP-001`.
- Bonus product GIDs (existing, DRAFT): Cooling Migraine Wrap `gid://shopify/Product/9591781064962` ($29), Blackout Sleep Mask `gid://shopify/Product/9591783981314` ($24), Filtered Earplugs `gid://shopify/Product/9591784243458` ($19).
- **Free-gift product (revised 2026-08-21, mid-execution): LullyRest Charcoal Satin Pillowcase**, `gid://shopify/Product/9593716834562`, handle `lullyrest-charcoal-satin-pillowcase`, $28.00 / compare-at $38.00, SKU `LR-SPC-001`, DRAFT. Built in a parallel session as a standalone paid accessory (see `PROGRESS.md` 2026-08-21 "New product" entry) — **its real price is not changed by this plan.** The theme's native zero-click free-gift auto-add (`premium_attachment_kit` / `cart_progress_bar`'s `product_free_amount` goal) requires the product to actually be priced $0 to work, which would kill its standalone sale value — so that native mechanic is **not used**. Instead: a real "Buy 1 pillow, get 1 pillowcase free" automatic discount (Task 9) makes it free at checkout once both are in cart, surfaced as a one-click "claim your free gift" `cart_upsell` card (Task 11) and shown with a struck-through $28 value in the PDP's `premium_attachment_kit` block (Task 2) — display-only pricing there, independent of the product's real price.
- Everything (new template, discounts, cart-drawer block instances) ships **Draft/inactive**. Do not set the product's live template to the new one, do not activate any discount, do not publish the draft theme, until the user gives one more explicit go-ahead (CLAUDE.md rule 4) — that confirmation is Task 14, the last task, not implied by earlier approval.
- Log every mutating action (theme push, discount create, settings_data.json push) to `PROGRESS.md` per CLAUDE.md rule 5. Commit and `git push origin main` after every repo change per CLAUDE.md rule 7.
- Claim integrity: no fabricated reviews/ratings/testimonials anywhere in the new template. Social-proof slots without real content ship as `[EMPTY]`-labeled via the existing `lullyrest-proof-placeholder` section, not invented copy.
- Pulled theme working copy lives at `C:\Users\jomat_nweuhlk\AppData\Local\Temp\claude\c--Users-jomat-nweuhlk-Desktop-LullyRestCode\a6bdf4a0-cd65-4d29-8601-6a77ccffdff3\scratchpad\draft-theme-pull` (already has `sections/`, `blocks/`, `snippets/`, `templates/`, `config/`, `layout/` pulled). Re-pull only if a push is rejected or the tree looks stale — don't re-pull unnecessarily, it discards nothing local yet unwritten but wastes time.

---

### Task 1: Confirm BOGO field semantics and scaffold the new generator script

**Files:**
- Create: `theme/build_pdp2.py`
- Reference (read-only): `theme/build_templates.py`, `theme/templates/product.lullyrest.json`

**Interfaces:**
- Produces: `stock(t)`, `add(key, sec)`, `rebuild_blocks(sec, btype, items)`, `block_of(sec, btype, nth=0)`, `put(block, **kw)` — same signatures as `build_templates.py`, copied verbatim (not imported, to keep the two generators independent per CLAUDE.md's "only our own files live here" convention and avoid coupling the presell/PDP generator to this one).

- [ ] **Step 1: Confirm BOGO multiplier semantics**

Already confirmed via the pulled theme's schema `info` text at `sections/shop-product-details.liquid:8207` (and mirrored for `quantity_break`'s `option_N_bogo_multiplier`): *"Enter how many items to pay for (e.g., 1 for Buy 1 Get 1, 2 for Buy 2 Get 3). Price = variant_price × multiplier."* For a true BOGO (buy 1, get 1 free) at quantity 2: `option_2_bogo_multiplier: 1` (pay for 1 of the 2 units). No further verification needed — record this in a comment at the top of `build_pdp2.py`.

- [ ] **Step 2: Write the generator scaffold**

```python
import json, os, shutil

THEME = os.environ.get("LR_THEME")
REPO = os.environ.get("LR_REPO", os.path.dirname(os.path.abspath(__file__)))
if not THEME:
    raise SystemExit("Set LR_THEME to the pulled draft-theme directory before running.")

# BOGO note: quantity_break's option_N_bogo_multiplier = "how many of the N units
# you pay for". Buy-1-get-1-free at qty=2 => bogo_multiplier = 1.

def stock(section_type):
    """Deep-copy a section of the given type from the theme's stock product.json."""
    path = os.path.join(THEME, "templates", "product.json")
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    import re
    raw = re.sub(r"/\*.*?\*/", "", raw, flags=re.S)
    prod = json.loads(raw)
    for key in prod["order"]:
        sec = prod["sections"][key]
        if sec.get("type") == section_type:
            return json.loads(json.dumps(sec))
    return None

def add(pdp_sections, pdp_order, key, sec):
    if sec is not None:
        pdp_sections[key] = sec
        pdp_order.append(key)

def block_of(sec, btype, nth=0):
    count = 0
    for key in sec.get("block_order", []):
        b = sec["blocks"][key]
        if b.get("type") == btype:
            if count == nth:
                return b
            count += 1
    return None

def put(block, **kw):
    if block is not None:
        block.setdefault("settings", {}).update(kw)

def rebuild_blocks(sec, btype, items):
    existing = [k for k in sec.get("block_order", []) if sec["blocks"][k].get("type") == btype]
    base = dict(sec["blocks"][existing[0]].get("settings", {})) if existing else {}
    for k in existing:
        del sec["blocks"][k]
        sec["block_order"].remove(k)
    for i, item in enumerate(items, start=1):
        key = f"{btype}_{i}"
        settings = dict(base)
        settings.update(item)
        sec["blocks"][key] = {"type": btype, "settings": settings}
        sec["block_order"].append(key)

if __name__ == "__main__":
    pdp_sections, pdp_order = {}, []
    # sections appended by later tasks
    out_path = os.path.join(THEME, "templates", "product.lullyrest-close.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"sections": pdp_sections, "order": pdp_order}, f, indent=2, ensure_ascii=False)
    print("wrote templates/product.lullyrest-close.json —", pdp_order)
```

- [ ] **Step 3: Run it once to verify the scaffold executes cleanly**

Run (PowerShell):
```
$env:LR_THEME="C:\Users\jomat_nweuhlk\AppData\Local\Temp\claude\c--Users-jomat-nweuhlk-Desktop-LullyRestCode\a6bdf4a0-cd65-4d29-8601-6a77ccffdff3\scratchpad\draft-theme-pull"
python theme/build_pdp2.py
```
Expected: prints `wrote templates/product.lullyrest-close.json — []` and the file exists with `{"sections": {}, "order": []}`.

- [ ] **Step 4: Commit the scaffold**

```bash
git add theme/build_pdp2.py
git commit -m "Scaffold new PDP template generator (empty template, helpers only)"
git push origin main
```

---

### Task 2: Section 1 — Product info (buy box) with BOGO + free-gift scaffold

**Files:**
- Modify: `theme/build_pdp2.py`

**Interfaces:**
- Consumes: `stock`, `add`, `block_of`, `put`, `rebuild_blocks` from Task 1.
- Produces: `pdp_sections["main"]` populated (type `shop-product-details`), consumed by Task 11 (assembly) and Task 12 (validate/push).

- [ ] **Step 1: Add the buy-box builder function**

```python
def build_main():
    main = stock("shop-product-details")
    if main is None:
        raise SystemExit("shop-product-details not found in stock product.json — check theme pull")

    put(block_of(main, "title"))  # keep stock title block as-is (pulls product.title)
    put(block_of(main, "price"))  # keep stock price block as-is

    qb = block_of(main, "quantity_break")
    put(qb,
        show_radio_buttons=True,
        enable_custom_pricing=True,
        selected_custom_price_format="bogo",
        show_option_1=True,
        option_1_title="1 Pillow",
        option_1_quantity=1,
        show_option_2=True,
        option_2_title="2 Pillows — Buy 1, Get 1 Free",
        option_2_quantity=2,
        enable_option_2_custom_price=True,
        option_2_bogo_multiplier=1,
        option_2_show_free_gift=True,
        option_2_free_gift_text="+ Free Charcoal Satin Pillowcase",
        option_1_show_free_gift=True,
        option_1_free_gift_text="+ Free Charcoal Satin Pillowcase",
        show_option_3=False,
        show_option_4=False,
        preselected_option=2,
        show_savings_text=True,
    )

    # premium_attachment_kit is used for its DISPLAY only (the "included free" list
    # with struck-through value) — it is NOT used as the add-to-cart delivery
    # mechanism, since that would require the pillowcase to be priced $0 (see
    # Global Constraints). Delivery is the real Buy-X-Get-Y discount (Task 9) +
    # the cart-drawer's "claim your free gift" upsell card (Task 11).
    kit = block_of(main, "premium_attachment_kit")
    put(kit,
        apply_to_product="lullyrest-orthopedic-cervical-pillow",
        title="Included Free With Your Order",
        show_item_count=False,
        original_price=True,
        item_1_name="Charcoal Satin Pillowcase",
        item_1_price=0,
        item_1_compare_price=28,
        item_1_product="lullyrest-charcoal-satin-pillowcase",
    )

    put(block_of(main, "add_to_cart"), button_text="ADD TO CART — 2ND PILLOW FREE")
    put(block_of(main, "guarantee_badges"))
    put(block_of(main, "shipping_notice"))
    put(block_of(main, "payment_icons"))
    return main
```

Note: `apply_to_product` is a Shopify `product` setting type — in the theme editor it stores a product GID, but for a JSON template file authored by hand, the product handle string also resolves correctly via `all_products[apply_to_product]`-style lookups used in `premium-attachment-kit.liquid` (`all_products[apply_to_product]` accepts a handle). Use the product's handle `lullyrest-orthopedic-cervical-pillow` (confirm this handle in Step 2 below rather than assuming).

- [ ] **Step 2: Confirm the pillow's actual handle**

Run:
```bash
shopify store execute --store gcvy0q-cb.myshopify.com --query 'query { product(id: "gid://shopify/Product/9589261009154") { handle } }'
```
Expected: a handle string (e.g. `lullyrest-orthopedic-cervical-pillow`). If it differs from the assumed value, update `apply_to_product` in Step 1's code to match exactly.

- [ ] **Step 3: Wire `build_main()` into `__main__` and regenerate**

Add to the `if __name__ == "__main__":` block, before the `out_path` write:
```python
    add(pdp_sections, pdp_order, "main", build_main())
```
Run the same command as Task 1 Step 3. Expected: `wrote templates/product.lullyrest-close.json — ['main']`, and the JSON's `sections.main.blocks.quantity_break_1.settings.selected_custom_price_format == "bogo"` (inspect with `python -c "import json; d=json.load(open('THEME/templates/product.lullyrest-close.json')); print(d['sections']['main']['blocks'].keys())"` — substitute the real path).

- [ ] **Step 4: Commit**

```bash
git add theme/build_pdp2.py
git commit -m "Add PDP buy box: BOGO quantity_break tier + free-gift kit scaffold"
git push origin main
```

---

### Task 3: Sections 2 & 4 & 6 & 8 — Social proof slots

**Files:**
- Modify: `theme/build_pdp2.py`

**Interfaces:**
- Consumes: `stock`, `add`, `rebuild_blocks`.
- Produces: `pdp_sections["social_proof_1"]` (type `statistics-grid`, real verifiable content), `pdp_sections["social_proof_2"]`, `["social_proof_3"]`, `["social_proof_4"]` (type `lullyrest-proof-placeholder`, `[EMPTY]`-labeled).

- [ ] **Step 1: Verify statistics-grid's section-level setting IDs before using them**

The earlier research pass only confirmed this section's `block` schema (the `statistic` block: `percentage`/`title`/`description`) and its `presets` block-list — it did not confirm section-level (non-block) setting IDs like colors, since the preset shown had no `"settings"` key. Before trusting the `background_color`/`heading_color`/`text_color`/`accent_color` keys used below, grep the section's own schema to confirm real IDs:
```bash
grep -n '"id"' "$LR_THEME/sections/statistics-grid.liquid" | sed -n '/schema/,$p'
```
(or open the file and read the `{% schema %}` block's top-level `"settings"` array directly, above the `"blocks"` array). If the real IDs differ from the guesses below, use the real ones. If the section has **no** section-level color settings at all (likely — many Elixir sections other than `product-benefits`/`alternating-features` inherit theme-global colors via `settings.global_section_*` and expose no per-section override), remove the `sec["settings"] = {...}` override entirely and rely on the theme's global section color settings instead — don't leave guessed IDs in the generator that Shopify will silently ignore.

- [ ] **Step 2: Build the one real social-proof section (statistics-grid)**

Per claim-integrity rule, this uses only verifiable structural facts about the product — no invented ratings/review counts.

```python
def build_social_proof_1():
    sec = stock("statistics-grid")
    if sec is None:
        return {"type": "statistics-grid", "blocks": {}, "block_order": [], "settings": {}}
    rebuild_blocks(sec, "statistic", [
        {"percentage": 100, "title": "Zero-VOC Foam", "description": "Vacuum-baked core — no off-gassing smell on night one."},
        {"percentage": 100, "title": "4-Zone Engineered Core", "description": "Two dedicated height planes: one for back sleeping, one for side."},
        {"percentage": 60, "title": "Night In-Home Trial", "description": "Sleep on it for up to 60 nights before deciding."},
        {"percentage": 100, "title": "Designed By a DPT", "description": "Spine & sleep biomechanics specialist, Dr. Brady Menoles."},
    ])
    # Explicit Direction C brand tokens (brand/BRAND_GUIDE.md) — don't inherit
    # Elixir's default pink/red demo palette by leaving settings blank.
    sec["settings"] = {
        "background_color": "#FCFCFA",
        "heading_color": "#23262B",
        "text_color": "#23262B",
        "accent_color": "#0E7C86",
    }
    return sec
```

- [ ] **Step 3: Build the three reserved `[EMPTY]` slots**

```python
def build_proof_placeholder(heading, slot_name, slot_note):
    sec = stock("lullyrest-proof-placeholder")
    if sec is None:
        sec = {"type": "lullyrest-proof-placeholder", "blocks": {}, "block_order": [], "settings": {}}
    sec["settings"]["heading"] = heading
    sec["settings"]["intro"] = (
        "This space is reserved for real customer proof. Nothing here is invented."
    )
    rebuild_blocks(sec, "slot", [
        {"slot_name": slot_name, "slot_note": slot_note, "slot_status": "[EMPTY]"},
    ])
    return sec
```

- [ ] **Step 4: Wire all four into `__main__`**

```python
    add(pdp_sections, pdp_order, "social_proof_1", build_social_proof_1())
    add(pdp_sections, pdp_order, "social_proof_2", build_proof_placeholder(
        "What Customers Are Saying", "Customer reviews",
        "Real review copy goes here once orders start shipping and reviews exist."))
```
(social_proof_2 is inserted after Task 4's section in the final order — see Task 8, the final-assembly task; here we're only defining the section dict, not yet fixing final page order.)
```python
    add(pdp_sections, pdp_order, "social_proof_3", build_proof_placeholder(
        "Seen On", "Press / media mentions",
        "Real press logos go here once any coverage exists."))
    add(pdp_sections, pdp_order, "social_proof_4", build_proof_placeholder(
        "In The Wild", "UGC photo/video",
        "Real customer photos/video go here once collected."))
```

Run the regenerate command from Task 1 Step 3. Expected: `pdp_order` includes all four `social_proof_*` keys and `python -m json.tool` on the output file parses without error.

- [ ] **Step 5: Commit**

```bash
git add theme/build_pdp2.py
git commit -m "Add PDP social proof sections: 1 verifiable stats block + 3 labeled EMPTY slots"
git push origin main
```

---

### Task 4: Section 3 — Problem restated, attributed to pillow features

**Files:**
- Modify: `theme/build_pdp2.py`

**Interfaces:**
- Consumes: `stock`, `rebuild_blocks`.
- Produces: `pdp_sections["problem_to_fix"]` (type `alternating-features`).

- [ ] **Step 1: Build the section, condensed (not long-form) per the user's "don't write super long copy" instruction**

Content maps each problem from `LullyRest_Listicle_First_Half.md`/`Second_Half.md` to the zone that fixes it, in one sentence each — not the listicle's full explanation.

```python
def build_problem_to_fix():
    sec = stock("alternating-features")
    if sec is None:
        return {"type": "alternating-features", "blocks": {}, "block_order": [], "settings": {}}
    rebuild_blocks(sec, "feature", [
        {"title": "One pillow height can't fix two sleep positions",
         "description": "Back sleeping needs your head lower than your neck. Side sleeping needs it higher, to bridge the ear-to-shoulder gap. LullyRest's dual-loft core gives you both heights in one pillow, so switching positions doesn't re-compress your neck."},
        {"title": "Foam that softens is foam that stops working",
         "description": "The high-density, open-cell core holds its shape night after night instead of flattening in 3-6 weeks like standard memory foam — so the support you get on night one is still there on night sixty."},
        {"title": "Your ear and jaw shouldn't take the pressure too",
         "description": "Recessed ear-and-jaw relief channels in the side wings mean side sleeping doesn't mean a crushed ear or an aggravated jaw by morning."},
    ])
    sec["settings"] = {
        "title": "Why Your Last Pillow Failed",
        "title_accent": "— And What Fixes It",
        "background_color": "#FCFCFA",
        "heading_color": "#23262B",
        "feature_title_color": "#23262B",
        "description_color": "#23262B",
        "accent_color": "#0E7C86",
    }
    return sec
```

- [ ] **Step 2: Wire into `__main__` and regenerate**

```python
    add(pdp_sections, pdp_order, "problem_to_fix", build_problem_to_fix())
```
Run the regenerate command. Expected: `pdp_order` includes `problem_to_fix`, JSON parses cleanly.

- [ ] **Step 3: Commit**

```bash
git add theme/build_pdp2.py
git commit -m "Add PDP problem-to-fix section (condensed, features mapped to problems)"
git push origin main
```

---

### Task 5: Section 5 — Physical features (reuse existing content verbatim)

**Files:**
- Modify: `theme/build_pdp2.py`

**Interfaces:**
- Consumes: `stock`.
- Produces: `pdp_sections["physical_features"]` (type `product-benefits`), byte-identical settings to the current `product.lullyrest.json`'s `benefits` section.

- [ ] **Step 1: Copy the exact block/settings JSON from the current template**

```python
def build_physical_features():
    sec = stock("product-benefits")
    if sec is None:
        sec = {"type": "product-benefits", "blocks": {}, "block_order": [], "settings": {}}
    sec["blocks"] = {
        "benefit_1": {"type": "benefit", "settings": {
            "title": "Zone 01 — Lordotic Cervical Extension Roll",
            "description": "A firmer roll under the neck that holds your natural 30\u00b0\u201335\u00b0 arc, so the cable stays curved instead of folding.",
            "benefit_color": "", "benefit_description_color": "", "use_image": False,
            "preset_icon": "check", "use_custom_icon": False,
            "custom_icon_svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewbox=\"0 0 24 24\" fill=\"currentColor\"><path d=\"M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z\"></path></svg>",
        }},
        "benefit_2": {"type": "benefit", "settings": {
            "title": "Zone 02 — Recessed Occipital Cavity",
            "description": "A cradle set 1.5\u20132in below the neck roll. On your back the skull settles in, and the base of the skull opens instead of compressing.",
            "benefit_color": "", "benefit_description_color": "", "use_image": False,
            "preset_icon": "check", "use_custom_icon": False,
            "custom_icon_svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewbox=\"0 0 24 24\" fill=\"currentColor\"><path d=\"M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z\"></path></svg>",
        }},
        "benefit_3": {"type": "benefit", "settings": {
            "title": "Zone 03 — Dual-Loft Lateral Wings",
            "description": "Outer thirds built to 4.5\u20135.5in to match shoulder width, so rolling onto your side lands you on a surface that is already the right height.",
            "benefit_color": "", "benefit_description_color": "", "use_image": False,
            "preset_icon": "check", "use_custom_icon": False,
            "custom_icon_svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewbox=\"0 0 24 24\" fill=\"currentColor\"><path d=\"M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z\"></path></svg>",
        }},
        "benefit_4": {"type": "benefit", "settings": {
            "title": "Zone 04 — Integrated Ear Depressions",
            "description": "Recesses in each wing so your outer ear isn't crushed against a firm surface all night. Ear and jaw pain is what kills most firm contour pillows by week two.",
            "benefit_color": "", "benefit_description_color": "", "use_image": False,
            "preset_icon": "check", "use_custom_icon": False,
            "custom_icon_svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewbox=\"0 0 24 24\" fill=\"currentColor\"><path d=\"M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z\"></path></svg>",
        }},
    }
    sec["block_order"] = ["benefit_1", "benefit_2", "benefit_3", "benefit_4"]
    sec["settings"] = {
        "padding_top": 50, "padding_bottom": 50, "padding_left": 25, "padding_right": 25,
        "image_position_desktop": "right",
        "heading_size_mobile": 34, "heading_size_desktop": 35,
        "subtitle_size_mobile": 13, "subtitle_size_desktop": 13,
        "benefit_title_size_mobile": 14, "benefit_title_size_desktop": 14,
        "benefit_description_size_mobile": 12, "benefit_description_size_desktop": 12,
        "accent_color": "#0E7C86", "use_theme_colors": False, "override_global_accent": True,
        "accent_font_family": "inherit", "accent_font_style": "italic", "accent_font_weight": "300",
        "use_accent_gradient": False,
        "accent_text_gradient": "linear-gradient(45deg, rgba(131, 215, 249, 1), rgba(23, 115, 176, 1) 96%)",
        "accent_text_margin_left": 0,
        "list_background": "linear-gradient(180deg, rgba(228, 249, 255, 1), rgba(255, 255, 255, 0.37) 100%)",
        "list_border_radius": 8, "border_color": "#C9C7C0",
        "heading_accent": "Four Zones", "heading_regular": "One Pillow",
        "subtitle": "The physical engineering that makes dual-position sleep actually work.",
        "show_image": True, "media_type": "image",
        "feature_image": "shopify://shop_images/ChatGPT_Image_May_4_2025_10_06_11_AM.png",
        "image_alt": "LullyRest pillow zone diagram",
        "video_autoplay": True, "video_muted": True, "video_loop": True, "video_controls": False,
        "heading_color": "#23262B", "subtitle_color": "#6F6F69", "description_color": "#23262B",
        "section_background": "linear-gradient(90deg, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0.4196) 99%)",
    }
    return sec
```
(`heading_accent`/`heading_regular`/`subtitle` are changed from the original to fit this section's new position on the page — everything else is byte-identical to `product.lullyrest.json`'s `benefits` section.)

- [ ] **Step 2: Wire into `__main__` and regenerate**

```python
    add(pdp_sections, pdp_order, "physical_features", build_physical_features())
```
Run the regenerate command. Expected: `pdp_order` includes `physical_features`.

- [ ] **Step 3: Commit**

```bash
git add theme/build_pdp2.py
git commit -m "Add PDP physical-features section (4 zones, reused from existing PDP)"
git push origin main
```

---

### Task 6: Section 7 — FAQ (reuse existing content verbatim)

**Files:**
- Modify: `theme/build_pdp2.py`

**Interfaces:**
- Consumes: `stock`.
- Produces: `pdp_sections["faq"]` (type `store-faq`), byte-identical content to the current `product.lullyrest.json`'s `store_faq` section.

- [ ] **Step 1: Copy the exact block/settings JSON**

```python
def build_faq():
    sec = stock("store-faq")
    if sec is None:
        sec = {"type": "store-faq", "blocks": {}, "block_order": [], "settings": {}}
    qa = [
        ("How long until I notice a difference?",
         "<p>Some people notice within a few nights. If your neck muscles have been contracted for years, expect 7&ndash;14 nights for the adaptation to settle. The 60-night trial exists so you have room to find out.</p>"),
        ("I sleep on my stomach sometimes.",
         "<p>LullyRest is engineered for back and side sleeping. Stomach sleeping forces cervical rotation no pillow can correct &mdash; if that's your primary position, this is not the right product for you.</p>"),
        ("How is this different from the contour pillow I already tried?",
         "<p>Standard contour pillows are a single-height wave: one bump, one dip, the same height across the whole pillow. LullyRest changes height across its <em>width</em> &mdash; taller at the outer wings than the centre &mdash; which is what makes side sleeping work.</p>"),
        ("Will it be too firm?",
         "<p>Firm under the neck by design &mdash; that's the part doing the work. The occipital cavity and ear recesses are where pressure is deliberately relieved.</p>"),
        ("Does it work with an adjustable bed?",
         "<p>Yes. The zones support the neck relative to the head, so it holds its geometry at an incline.</p>"),
        ("What if it doesn't work for me?",
         "<p>Return it within 60 nights for a full refund. [VERIFY: return mechanics &mdash; who pays return shipping, refund processing time.]</p>"),
        ("Is the cover washable?",
         "<p>[VERIFY: confirm care instructions &mdash; machine washable? removable? temperature?]</p>"),
    ]
    sec["blocks"] = {
        f"faq_item_{i}": {"type": "faq_item", "settings": {"question": q, "answer": a}}
        for i, (q, a) in enumerate(qa, start=1)
    }
    sec["block_order"] = [f"faq_item_{i}" for i in range(1, len(qa) + 1)]
    sec["settings"] = {
        "use_theme_colors": False,
        "heading": "Questions",
        "subtitle": "<p>The ones that actually decide it.</p>",
        "heading_color": "#23262B",
        "section_padding": 60,
        "container_padding_mobile": 15, "container_padding_desktop": 15,
        "section_bg_color": "#ffffff",
        "border_radius": 8, "border_color": "#C9C7C0", "border_style": "full",
        "question_color": "#23262B", "question_bg_color": "#ffffff",
        "answer_color": "#23262B", "answer_bg_color": "#ffffff",
        "accordion_mode": True,
        "image_border_radius": 8, "center_when_no_image": True, "center_max_width": 600,
        "two_column_desktop": False, "column_gap": 30, "faq_item_spacing": 0,
        "individual_item_borders": False,
        "question_padding_top": 15, "question_padding_bottom": 15, "question_padding_left": 20, "question_padding_right": 20,
        "answer_padding_top": 15, "answer_padding_bottom": 15, "answer_padding_left": 20, "answer_padding_right": 20,
        "heading_font_size": 36, "heading_font_size_mobile": 30,
        "subtitle_font_size": 16, "subtitle_font_size_mobile": 14,
        "question_font_size": 16, "question_font_size_mobile": 14,
        "answer_font_size": 14, "answer_font_size_mobile": 13,
    }
    return sec
```

- [ ] **Step 2: Wire into `__main__` and regenerate**

```python
    add(pdp_sections, pdp_order, "faq", build_faq())
```
Run the regenerate command. Expected: `pdp_order` includes `faq`, 7 `faq_item_N` blocks present.

- [ ] **Step 3: Commit**

```bash
git add theme/build_pdp2.py
git commit -m "Add PDP FAQ section (reused verbatim from existing PDP, 7 items)"
git push origin main
```

---

### Task 7: Section 9 — Guarantee + Offer + Scarcity + Urgency + sticky CTA

**Files:**
- Modify: `theme/build_pdp2.py`

**Interfaces:**
- Consumes: `stock`.
- Produces: `pdp_sections["guarantee"]` (type `satisfaction-guarantee`), `pdp_sections["urgency"]` (type `sale-countdown-banner`), `pdp_sections["sticky_atc"]` (type `sticky-add-to-cart`).

- [ ] **Step 1: Build the guarantee section**

```python
def build_guarantee():
    sec = stock("satisfaction-guarantee")
    if sec is None:
        sec = {"type": "satisfaction-guarantee", "blocks": {}, "block_order": [], "settings": {}}
    sec["settings"].update({
        "heading": "The 60-Night Painless Morning Guarantee",
        "body": (
            "Sleep on it for up to 60 nights. Give your neck the 7\u201314 night adaptation "
            "window. If your morning migraines, neck stiffness, and brain fog haven't "
            "meaningfully improved, send it back for a full refund."
        ),
    })
    return sec
```

- [ ] **Step 2: Build the urgency/countdown section**

The end date is a **placeholder set 30 days out from generation time** — Task 9 (BOGO discount creation) will set the discount's real end date, and this value must be updated to match exactly at that point so the countdown is honest, not decorative.

```python
import datetime

def build_urgency():
    sec = stock("sale-countdown-banner")
    if sec is None:
        sec = {"type": "sale-countdown-banner", "blocks": {}, "block_order": [], "settings": {}}
    end = datetime.date.today() + datetime.timedelta(days=30)
    sec["settings"].update({
        "heading_text": "BUY 1, GET 1 FREE",
        "highlight_text": "+ FREE SATIN PILLOWCASE",
        "show_icon": False,
        "show_days": True,
        "end_year": end.year, "end_month": end.month, "end_day": end.day,
        "end_hour": 23, "end_minute": 59,
        "sticky": False,
        "background_color": "#0E7C86",
        "text_color": "#FCFCFA",
        "highlight_color": "#FCFCFA",
        "countdown_color": "#FCFCFA",
        "countdown_label_color": "#FCFCFA",
        "border_color": "#0E7C86",
    })
    return sec
```

- [ ] **Step 3: Build the sticky ATC section (reused pattern from current PDP)**

```python
def build_sticky_atc():
    sec = stock("sticky-add-to-cart")
    if sec is None:
        sec = {"type": "sticky-add-to-cart", "blocks": {}, "block_order": [], "settings": {}}
    sec["settings"]["button_text"] = "CLAIM BOGO OFFER"
    return sec
```

- [ ] **Step 4: Wire all three into `__main__` and regenerate**

```python
    add(pdp_sections, pdp_order, "guarantee", build_guarantee())
    add(pdp_sections, pdp_order, "urgency", build_urgency())
    add(pdp_sections, pdp_order, "sticky_atc", build_sticky_atc())
```
Run the regenerate command. Expected: `pdp_order` ends with `['..., 'guarantee', 'urgency', 'sticky_atc']`.

- [ ] **Step 5: Commit**

```bash
git add theme/build_pdp2.py
git commit -m "Add PDP guarantee, urgency countdown, and sticky ATC sections"
git push origin main
```

---

### Task 8: Final assembly — correct page order and full-template validation

**Files:**
- Modify: `theme/build_pdp2.py`
- Reference: `theme/validate_template.py`

**Interfaces:**
- Consumes: all `build_*()` functions from Tasks 2–7.
- Produces: `templates/product.lullyrest-close.json` in the pulled theme directory, in the user's specified 9-slot order.

- [ ] **Step 1: Fix assembly order in `__main__` to match the user's exact lineup**

Replace the incremental `add()` calls scattered across Tasks 2–7 with one ordered block (remove the earlier scattered `add()` calls, keep only the `build_*()` function definitions):

```python
if __name__ == "__main__":
    pdp_sections, pdp_order = {}, []
    add(pdp_sections, pdp_order, "main", build_main())                        # 1. Product info
    add(pdp_sections, pdp_order, "social_proof_1", build_social_proof_1())    # 2. Social proof
    add(pdp_sections, pdp_order, "problem_to_fix", build_problem_to_fix())    # 3. Problem -> fix
    add(pdp_sections, pdp_order, "social_proof_2", build_proof_placeholder(
        "What Customers Are Saying", "Customer reviews",
        "Real review copy goes here once orders start shipping and reviews exist."))  # 4. Social proof
    add(pdp_sections, pdp_order, "physical_features", build_physical_features())      # 5. Physical features
    add(pdp_sections, pdp_order, "social_proof_3", build_proof_placeholder(
        "Seen On", "Press / media mentions",
        "Real press logos go here once any coverage exists."))                        # 6. Social proof
    add(pdp_sections, pdp_order, "faq", build_faq())                                  # 7. FAQ
    add(pdp_sections, pdp_order, "social_proof_4", build_proof_placeholder(
        "In The Wild", "UGC photo/video",
        "Real customer photos/video go here once collected."))                        # 8. Social proof
    add(pdp_sections, pdp_order, "guarantee", build_guarantee())                      # 9a. Guarantee
    add(pdp_sections, pdp_order, "urgency", build_urgency())                          # 9b. Offer/scarcity/urgency
    add(pdp_sections, pdp_order, "sticky_atc", build_sticky_atc())                    # 9c. CTA

    out_path = os.path.join(THEME, "templates", "product.lullyrest-close.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"sections": pdp_sections, "order": pdp_order}, f, indent=2, ensure_ascii=False)
    print("wrote templates/product.lullyrest-close.json —", pdp_order)
```

- [ ] **Step 2: Regenerate and verify order**

Run the regenerate command from Task 1 Step 3. Expected `pdp_order`:
```
['main', 'social_proof_1', 'problem_to_fix', 'social_proof_2', 'physical_features', 'social_proof_3', 'faq', 'social_proof_4', 'guarantee', 'urgency', 'sticky_atc']
```
This is 11 template-section entries realizing the user's 9 conceptual slots (slot 9 = 3 sections: guarantee + urgency + sticky_atc).

- [ ] **Step 3: Run `validate_template.py` against the new template**

Read `theme/validate_template.py` first to confirm its invocation pattern (it validates a built template's settings against section schemas), then run it against `product.lullyrest-close.json` the same way it's normally run against `product.lullyrest.json`. Fix any type-mismatch errors it reports (richtext needing HTML wrapper tags, select needing string not int, etc. — the known failure modes from `theme/README.md`'s gotchas) before proceeding.

Expected: no errors reported, or all reported errors fixed and re-validated clean.

- [ ] **Step 4: Commit**

```bash
git add theme/build_pdp2.py
git commit -m "Assemble full PDP template in final section order, pass validation"
git push origin main
```

---

### Task 9: Create the BOGO and free-shipping automatic discounts (inactive)

**Files:** None (store-side mutation via `shopify store execute`). Log entry: `PROGRESS.md`.

**Interfaces:**
- Produces: two discount GIDs, recorded in `PROGRESS.md`, and the real end-date used to update `build_urgency()`'s placeholder date from Task 7.

- [ ] **Step 1: Create the BOGO automatic discount, inactive, with a real 30-day end date**

```bash
shopify store execute --store gcvy0q-cb.myshopify.com --query '
mutation {
  discountAutomaticBasicCreate(automaticBasicDiscount: {
    title: "LullyRest BOGO — Buy 1 Pillow Get 1 Free"
    startsAt: "2026-08-21T00:00:00Z"
    endsAt: "2026-09-20T23:59:00Z"
    customerGets: {
      value: { percentage: 1.0 }
      items: { products: { productsToAdd: ["gid://shopify/Product/9589261009154"] } }
    }
    minimumRequirement: {
      quantity: { greaterThanOrEqualToQuantity: "2", itemsToRecommend: { products: { productsToAdd: ["gid://shopify/Product/9589261009154"] } } }
    }
  }) {
    automaticDiscountNode { id }
    userErrors { field message }
  }
}'
```
**Note per CLAUDE.md:** `shopify store execute` returns the raw result object, not wrapped in a GraphQL `data` key — check `userErrors` directly in the printed result, don't assume success from exit code alone. If this exact mutation shape is rejected (buy-x-get-y discounts have a specific dedicated input shape in the Shopify Admin API that may differ from `discountAutomaticBasicCreate`'s customerGets/minimumRequirement combination above), consult the `shopify-plugin:shopify-admin` or `shopify-dev` skill for the correct automatic Buy X Get Y discount mutation before retrying — do not guess a second time blindly.

Immediately after creation, confirm it's NOT active for customers: automatic discounts are enabled by default on creation in some API versions — if `userErrors` is empty, immediately query the created discount's `status` field and, if it is `ACTIVE`, deactivate it:
```bash
shopify store execute --store gcvy0q-cb.myshopify.com --query 'query { automaticDiscountNode(id: "<id-from-above>") { automaticDiscount { ... on DiscountAutomaticBasic { status } } } }'
```
If `status: ACTIVE`, run the corresponding deactivate mutation (`discountAutomaticDeactivate`) before moving on — this discount must not be live yet.

Expected: a discount GID, confirmed `status: EXPIRED` or `INACTIVE`/deactivated, not `ACTIVE`.

- [ ] **Step 2: Create the free-shipping automatic discount, inactive, threshold $160**

```bash
shopify store execute --store gcvy0q-cb.myshopify.com --query '
mutation {
  discountAutomaticFreeShippingCreate(freeShippingAutomaticDiscount: {
    title: "LullyRest Free Shipping Over $160"
    startsAt: "2026-08-21T00:00:00Z"
    minimumRequirement: { subtotal: { greaterThanOrEqualToSubtotal: "160.00" } }
  }) {
    automaticDiscountNode { id }
    userErrors { field message }
  }
}'
```
Same activation check and deactivation-if-needed as Step 1.

Expected: a second discount GID, confirmed not active.

- [ ] **Step 3: Create the free-pillowcase Buy-X-Get-Y automatic discount, inactive**

This is the real delivery mechanism for the free gift (see Global Constraints — the pillowcase keeps its real $28 price, this discount is what actually zeroes it at checkout when bundled with the pillow):
```bash
shopify store execute --store gcvy0q-cb.myshopify.com --query '
mutation {
  discountAutomaticBasicCreate(automaticBasicDiscount: {
    title: "LullyRest Free Pillowcase With Pillow Purchase"
    startsAt: "2026-08-21T00:00:00Z"
    endsAt: "2026-09-20T23:59:00Z"
    customerGets: {
      value: { percentage: 1.0 }
      items: { products: { productsToAdd: ["gid://shopify/Product/9593716834562"] } }
    }
    minimumRequirement: {
      quantity: { greaterThanOrEqualToQuantity: "1", itemsToRecommend: { products: { productsToAdd: ["gid://shopify/Product/9589261009154"] } } }
    }
  }) {
    automaticDiscountNode { id }
    userErrors { field message }
  }
}'
```
Same mutation-shape caution as Step 1 (verify against `shopify-plugin:shopify-admin`/`shopify-dev` if rejected — do not guess a second time), and same activation check/deactivation-if-needed.

Expected: a third discount GID, confirmed not active.

- [ ] **Step 4: Update `build_urgency()`'s placeholder date to the real BOGO end date**

In `theme/build_pdp2.py`, replace the `datetime.date.today() + datetime.timedelta(days=30)` placeholder in `build_urgency()` with the literal end date used in Step 1 (`2026-09-20`, 23:59), so the on-page countdown matches the actual discount's real expiry — not a decorative date. Regenerate (Task 8 Step 2's command) to confirm the settings updated.

- [ ] **Step 5: Log to PROGRESS.md and commit**

Append an entry to `PROGRESS.md` recording all three discount GIDs, their inactive status, and the end date used, following the existing log format in that file. Then:
```bash
git add PROGRESS.md theme/build_pdp2.py
git commit -m "Create BOGO, free-shipping, and free-pillowcase automatic discounts (inactive), sync countdown date"
git push origin main
```

---

### Task 10: Push the new PDP template to the draft theme

**Files:** None new (pushes the already-built `templates/product.lullyrest-close.json`).

**Interfaces:**
- Consumes: the validated template file from Task 8.

- [ ] **Step 1: Push scoped to just the new template**

```bash
shopify theme push --store gcvy0q-cb.myshopify.com --theme 163498656002 \
  --path "C:\Users\jomat_nweuhlk\AppData\Local\Temp\claude\c--Users-jomat-nweuhlk-Desktop-LullyRestCode\a6bdf4a0-cd65-4d29-8601-6a77ccffdff3\scratchpad\draft-theme-pull" \
  --nodelete --only "templates/product.lullyrest-close.json"
```

- [ ] **Step 2: Verify the push actually succeeded**

Per CLAUDE.md's Windows gotcha and PROGRESS.md's 2026-08-20 push-failure entry, the CLI can print a truncated success message while a separate error box (easy to miss in scrollback) reports the real rejection. Read the **full** command output, not just the last line, and specifically check for any error/warning box in the output before treating this as done. If rejected, read the actual error (likely a schema type mismatch — cross-check against `theme/validate_template.py`'s known failure modes) and fix `build_pdp2.py` accordingly, regenerate, and retry.

Expected: a `success` box naming `templates/product.lullyrest-close.json`, and no accompanying error box.

- [ ] **Step 3: Log to PROGRESS.md and commit**

```bash
git add PROGRESS.md
git commit -m "Log: pushed new PDP template (product.lullyrest-close.json) to draft theme"
git push origin main
```

Note: this does **not** make the new template live-facing on the product — the product record's `templateSuffix` is still `lullyrest` (the old template). Switching it to `lullyrest-close` is part of Task 14's final go-ahead, not this task.

---

### Task 11: Configure the cart drawer — progress bar, upsells, timer bar

**Files:**
- Modify (in the pulled theme working copy): `config/settings_data.json`

**Interfaces:**
- Consumes: bonus-product GIDs and the pillowcase GID from Global Constraints; the $160 threshold and the free-pillowcase discount from Task 9.
- Produces: `current.sections["cart-drawer"].blocks` populated with `cart_progress_bar` (1, free-shipping goal only), `cart_upsell` (4 — the pillowcase first, framed as the free gift, then the 3 bonus products), `cart_timer_bar` (1).

- [ ] **Step 1: Write a small Python script to patch `settings_data.json` in place**

```python
import json, os

THEME = os.environ["LR_THEME"]
path = os.path.join(THEME, "config", "settings_data.json")
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

cart = data["current"]["sections"]["cart-drawer"]
cart["blocks"] = {
    "cart_progress_bar": {
        "type": "cart_progress_bar",
        "settings": {
            # Free-shipping goal only. Not using product_free_amount/
            # progress_bar_free_product here — that native "free gift" goal
            # expects the gift product to be priced $0 (see Global Constraints),
            # which we deliberately did NOT do to the pillowcase. Its free-gift
            # framing is delivered via cart_upsell_1 below + the real discount
            # from Task 9 Step 3, not this progress-bar mechanic.
            "product_free_shipping": 160,
            "shipping_away_text": "Add [missingAmount] more for free shipping!",
            "shipping_earn_text": "You've unlocked free shipping!",
        },
    },
    "cart_upsell_1": {
        "type": "cart_upsell",
        "settings": {
            "upsell_product_1": "gid://shopify/Product/9593716834562",
            "upsell_button_text": "Claim Free Gift",
            "upsell_show_price": True,
            "show_upsell_description": True,
            "upsell_description_text": "Free with your pillow order — a $28 value.",
            "show_upsell_best_seller_tag": True,
            "upsell_best_seller_text": "YOUR FREE GIFT",
        },
    },
    "cart_upsell_2": {
        "type": "cart_upsell",
        "settings": {
            "upsell_product_1": "gid://shopify/Product/9591781064962",
            "upsell_button_text": "Add +",
            "upsell_show_price": True,
        },
    },
    "cart_upsell_3": {
        "type": "cart_upsell",
        "settings": {
            "upsell_product_1": "gid://shopify/Product/9591783981314",
            "upsell_button_text": "Add +",
            "upsell_show_price": True,
        },
    },
    "cart_upsell_4": {
        "type": "cart_upsell",
        "settings": {
            "upsell_product_1": "gid://shopify/Product/9591784243458",
            "upsell_button_text": "Add +",
            "upsell_show_price": True,
        },
    },
    "cart_timer_bar": {
        "type": "cart_timer_bar",
        "settings": {
            "timer_minutes": 15,
            "timer_text": "Your BOGO offer is reserved for {timer} mins!",
        },
    },
}
cart["block_order"] = ["cart_progress_bar", "cart_timer_bar", "cart_upsell_1", "cart_upsell_2", "cart_upsell_3", "cart_upsell_4"]

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("patched config/settings_data.json — cart-drawer blocks:", list(cart["blocks"].keys()))
```

Run it once (as a one-off script, e.g. `theme/patch_cart_drawer.py`, following the same `LR_THEME` env-var convention):
```
$env:LR_THEME="C:\...\scratchpad\draft-theme-pull"
python theme/patch_cart_drawer.py
```

Expected: prints 6 block keys, and `config/settings_data.json` parses as valid JSON afterward (`python -m json.tool config/settings_data.json > $null` exits 0).

Note: `upsell_product_1` (type `product`) — set to the product's GID string as shown; if the theme editor's stored format for `product`-type settings turns out to be a handle rather than a GID when inspected after push (theme editor UI will show broken picker if wrong), switch to the product handle instead and re-push. Verify by opening the draft theme's cart drawer in the theme editor after Task 11 Step 2's push and confirming the upsell cards render with real product names/images, not blank.

- [ ] **Step 2: Push just `config/settings_data.json`**

```bash
shopify theme push --store gcvy0q-cb.myshopify.com --theme 163498656002 \
  --path "C:\Users\jomat_nweuhlk\AppData\Local\Temp\claude\c--Users-jomat-nweuhlk-Desktop-LullyRestCode\a6bdf4a0-cd65-4d29-8601-6a77ccffdff3\scratchpad\draft-theme-pull" \
  --nodelete --only "config/settings_data.json"
```
Read the full output per Task 10 Step 2's caution about truncated success messages.

- [ ] **Step 3: Verify in the theme editor**

Open `https://gcvy0q-cb.myshopify.com/admin/themes/163498656002/editor` (draft theme preview), open the cart drawer (add any product to cart on the preview storefront), and visually confirm: the progress bar renders with "add $X more for free shipping" text, and all 4 upsell cards show real product names/images/prices (not blank/broken pickers — if broken, revisit the GID-vs-handle note in Step 1), with the pillowcase card showing the "YOUR FREE GIFT" tag and "Claim Free Gift" button.

- [ ] **Step 4: Log to PROGRESS.md and commit**

```bash
git add theme/patch_cart_drawer.py PROGRESS.md
git commit -m "Configure cart drawer: free-shipping progress bar, 4-product upsell rail (pillowcase framed as free gift), timer bar"
git push origin main
```

---

### Task 12: Commit theme/README.md update documenting the new template

**Files:**
- Modify: `theme/README.md`

**Interfaces:** None (documentation only).

- [ ] **Step 1: Add the new template and script to the Files table**

Add rows/notes for `templates/product.lullyrest-close.json` (generated by `build_pdp2.py`, the new close-focused PDP — not yet the live template for the product), `build_pdp2.py` itself, and `patch_cart_drawer.py`, following the existing table's style. Also add a note under "Deploying" that pushing this new template follows the same pattern as `product.lullyrest.json` but via `build_pdp2.py` instead of `build_templates.py`, and that it needs no vendor-schema patching (uses only stock Elixir block types, no custom `lullyrest-*` blocks in `main`).

- [ ] **Step 2: Commit**

```bash
git add theme/README.md
git commit -m "Document new PDP template and generator scripts in theme README"
git push origin main
```

---

### Task 13: Final go-ahead checkpoint (not implied by earlier approval)

**Files:** None — this is a confirmation checkpoint, not a code task.

- [ ] **Step 1: Summarize current state to the user**

Report: new template built/validated/pushed (Task 10) but product still serves the old `lullyrest` template; all three discounts (BOGO, free shipping, free pillowcase) created but confirmed inactive (Task 9); cart drawer configured on the draft theme only, pillowcase framed as the free gift (Task 11); the pillowcase's own $28/$38 standalone pricing was left untouched throughout.

- [ ] **Step 2: Ask explicitly, one question per irreversible action, per CLAUDE.md rule 4**

Do not bundle these into one yes/no — each is independently reversible-or-not and customer-visible-or-not:
1. Switch the product's live `templateSuffix` from `lullyrest` to `lullyrest-close`? (Product is currently ACTIVE per PROGRESS.md 2026-08-20 — this makes the new PDP the one real customers see.)
2. Activate the BOGO discount?
3. Activate the free-shipping discount?
4. Activate the free-pillowcase discount?
5. Publish the draft theme as the store's live theme? (CLAUDE.md rule 2 — this is the only step that touches "never edit the Live theme directly"; everything through Task 12 stayed on the draft theme.)

- [ ] **Step 3: Execute only the specific actions the user confirms**, each as its own logged, committed `PROGRESS.md` entry.
