import json, os, re

THEME = os.environ.get("LR_THEME")
REPO = os.environ.get("LR_REPO", os.path.dirname(os.path.abspath(__file__)))
if not THEME:
    raise SystemExit("Set LR_THEME to the pulled draft-theme directory before running.")

# BOGO note: quantity_break's option_N_bogo_multiplier = "how many of the N units
# you pay for". Buy-1-get-1-free at qty=2 => bogo_multiplier = 1.
# (theme/build_templates.py builds product.lullyrest.json — the CURRENT PDP.
#  This script builds a separate, new template: product.lullyrest-close.json.
#  It does not modify or import from build_templates.py.)


def stock(section_type):
    """Deep-copy a section of the given type from the theme's stock product.json."""
    path = os.path.join(THEME, "templates", "product.json")
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
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


# Blocks present in the stock product.json buy box that we don't want on the
# new close-focused PDP: fabricated/demo social proof (trustpilot_rating,
# number_one_award, replica_warning, customer_review), empty demo video
# carousels (carousel_default_video, video_carousel_standalone), and content
# duplicated by this PDP's own dedicated sections (faq -> section 7,
# money_back_guarantee -> section 9, divider -> cosmetic only).
MAIN_DROP_TYPES = {
    "trustpilot_rating", "number_one_award", "replica_warning", "customer_review",
    "carousel_default_video", "video_carousel_standalone",
    "product_faq", "money_back_guarantee", "divider", "custom_text",
}


def drop_blocks(sec, types):
    keys = [k for k in sec.get("block_order", []) if sec["blocks"][k].get("type") in types]
    for k in keys:
        del sec["blocks"][k]
        sec["block_order"].remove(k)


def new_block(sec, btype, key, settings, after_type=None):
    """Insert a block of a type that has no stock instance to build on."""
    sec["blocks"][key] = {"type": btype, "settings": settings}
    if after_type is not None:
        after_key = next((k for k in sec["block_order"] if sec["blocks"][k]["type"] == after_type), None)
        if after_key is not None:
            idx = sec["block_order"].index(after_key) + 1
            sec["block_order"].insert(idx, key)
            return
    sec["block_order"].append(key)


def build_main():
    main = stock("shop-product-details")
    if main is None:
        raise SystemExit("shop-product-details not found in stock product.json — check theme pull")

    drop_blocks(main, MAIN_DROP_TYPES)

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

    # premium_attachment_kit has no stock instance in product.json (it's only
    # a registered block TYPE in the section schema) -- must be constructed,
    # not found via block_of(). Used for DISPLAY only (the "included free"
    # list with struck-through value) -- it is NOT the add-to-cart delivery
    # mechanism, since that would require the pillowcase to be priced $0.
    # Delivery is the real Buy-X-Get-Y discount (Task 9) + the cart-drawer's
    # "claim your free gift" upsell card (Task 11).
    new_block(main, "premium_attachment_kit", "premium_attachment_kit", {
        "apply_to_product": "lullyrest-orthopedic-cervical-pillow",
        "title": "Included Free With Your Order",
        "show_item_count": False,
        "original_price": True,
        "item_1_name": "Charcoal Satin Pillowcase",
        "item_1_price": 0,
        "item_1_compare_price": 28,
        "item_1_product": "lullyrest-charcoal-satin-pillowcase",
    }, after_type="quantity_break")

    put(block_of(main, "add_to_cart"), button_text="ADD TO CART — 2ND PILLOW FREE")
    put(block_of(main, "guarantee_badges"))
    put(block_of(main, "shipping_notice"))
    put(block_of(main, "payment_icons"))
    return main


if __name__ == "__main__":
    pdp_sections, pdp_order = {}, []
    add(pdp_sections, pdp_order, "main", build_main())
    out_path = os.path.join(THEME, "templates", "product.lullyrest-close.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"sections": pdp_sections, "order": pdp_order}, f, indent=2, ensure_ascii=False)
    print("wrote templates/product.lullyrest-close.json —", pdp_order)
