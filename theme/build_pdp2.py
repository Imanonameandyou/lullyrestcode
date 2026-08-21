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
        preselected_option="2",
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
        "original_price": "28",
        "item_1_name": "Charcoal Satin Pillowcase",
        "item_1_price": "0",
        "item_1_compare_price": "28",
        "item_1_product": "lullyrest-charcoal-satin-pillowcase",
    }, after_type="quantity_break")

    put(block_of(main, "add_to_cart"), button_text="ADD TO CART — 2ND PILLOW FREE")
    put(block_of(main, "guarantee_badges"))
    put(block_of(main, "shipping_notice"))
    put(block_of(main, "payment_icons"))
    return main


def build_social_proof_1():
    """Real, verifiable structural claims only -- no invented ratings/review counts."""
    sec = stock("statistics-grid")
    if sec is None:
        sec = {"type": "statistics-grid", "blocks": {}, "block_order": [], "settings": {}}
    rebuild_blocks(sec, "statistic", [
        {"percentage": 100, "title": "Zero-VOC Foam", "description": "Vacuum-baked core — no off-gassing smell on night one."},
        {"percentage": 100, "title": "4-Zone Engineered Core", "description": "Two dedicated height planes: one for back sleeping, one for side."},
        {"percentage": 60, "title": "Night In-Home Trial", "description": "Sleep on it for up to 60 nights before deciding."},
        {"percentage": 100, "title": "Designed By a DPT", "description": "Spine & sleep biomechanics specialist, Dr. Brady Menoles."},
    ])
    # Verified setting IDs (grepped sections/statistics-grid.liquid schema directly --
    # earlier guesses like "text_color" don't exist on this section).
    sec["settings"].update({
        "use_theme_colors": False,
        "background_color": "#FCFCFA",
        "heading_color": "#23262B",
        "statistic_title_color": "#23262B",
        "statistic_description_color": "#6F6F69",
        "accent_color": "#0E7C86",
    })
    return sec


def build_proof_placeholder(heading, slot_name, slot_note):
    sec = stock("lullyrest-proof-placeholder")
    if sec is None:
        sec = {"type": "lullyrest-proof-placeholder", "blocks": {}, "block_order": [], "settings": {}}
    sec["settings"]["heading"] = heading
    sec["settings"]["intro"] = "This space is reserved for real customer proof. Nothing here is invented."
    rebuild_blocks(sec, "slot", [
        {"slot_name": slot_name, "slot_note": slot_note, "slot_status": "[EMPTY]"},
    ])
    return sec


def build_problem_to_fix():
    sec = stock("alternating-features")
    if sec is None:
        sec = {"type": "alternating-features", "blocks": {}, "block_order": [], "settings": {}}
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


def build_physical_features():
    sec = stock("product-benefits")
    if sec is None:
        sec = {"type": "product-benefits", "blocks": {}, "block_order": [], "settings": {}}
    icon_svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewbox="0 0 24 24" fill="currentColor">'
                '<path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"></path></svg>')
    sec["blocks"] = {
        "benefit_1": {"type": "benefit", "settings": {
            "title": "Zone 01 — Lordotic Cervical Extension Roll",
            "description": "A firmer roll under the neck that holds your natural 30°–35° arc, so the cable stays curved instead of folding.",
            "benefit_color": "", "benefit_description_color": "", "use_image": False,
            "preset_icon": "check", "use_custom_icon": False, "custom_icon_svg": icon_svg,
        }},
        "benefit_2": {"type": "benefit", "settings": {
            "title": "Zone 02 — Recessed Occipital Cavity",
            "description": "A cradle set 1.5–2in below the neck roll. On your back the skull settles in, and the base of the skull opens instead of compressing.",
            "benefit_color": "", "benefit_description_color": "", "use_image": False,
            "preset_icon": "check", "use_custom_icon": False, "custom_icon_svg": icon_svg,
        }},
        "benefit_3": {"type": "benefit", "settings": {
            "title": "Zone 03 — Dual-Loft Lateral Wings",
            "description": "Outer thirds built to 4.5–5.5in to match shoulder width, so rolling onto your side lands you on a surface that is already the right height.",
            "benefit_color": "", "benefit_description_color": "", "use_image": False,
            "preset_icon": "check", "use_custom_icon": False, "custom_icon_svg": icon_svg,
        }},
        "benefit_4": {"type": "benefit", "settings": {
            "title": "Zone 04 — Integrated Ear Depressions",
            "description": "Recesses in each wing so your outer ear isn't crushed against a firm surface all night. Ear and jaw pain is what kills most firm contour pillows by week two.",
            "benefit_color": "", "benefit_description_color": "", "use_image": False,
            "preset_icon": "check", "use_custom_icon": False, "custom_icon_svg": icon_svg,
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


def build_guarantee():
    sec = stock("satisfaction-guarantee")
    if sec is None:
        sec = {"type": "satisfaction-guarantee", "blocks": {}, "block_order": [], "settings": {}}
    sec["settings"].update({
        "heading": "The 60-Night Painless Morning Guarantee",
        "body": (
            "Sleep on it for up to 60 nights. Give your neck the 7–14 night adaptation "
            "window. If your morning migraines, neck stiffness, and brain fog haven't "
            "meaningfully improved, send it back for a full refund."
        ),
    })
    return sec


import datetime


def build_urgency():
    sec = stock("sale-countdown-banner")
    if sec is None:
        sec = {"type": "sale-countdown-banner", "blocks": {}, "block_order": [], "settings": {}}
    end = datetime.date(2026, 9, 20)  # matches the BOGO/free-pillowcase discount end date (Task 9)
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


def build_sticky_atc():
    sec = stock("sticky-add-to-cart")
    if sec is None:
        sec = {"type": "sticky-add-to-cart", "blocks": {}, "block_order": [], "settings": {}}
    sec["settings"]["button_text"] = "CLAIM BOGO OFFER"
    return sec


if __name__ == "__main__":
    pdp_sections, pdp_order = {}, []
    add(pdp_sections, pdp_order, "main", build_main())                                # 1. Product info
    add(pdp_sections, pdp_order, "social_proof_1", build_social_proof_1())            # 2. Social proof
    add(pdp_sections, pdp_order, "problem_to_fix", build_problem_to_fix())            # 3. Problem -> fix
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
