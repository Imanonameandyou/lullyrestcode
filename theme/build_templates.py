#!/usr/bin/env python3
"""Build LullyRest templates into the pulled draft theme and register custom blocks."""
import json, re, shutil, os

# Machine-specific; override with LR_THEME / LR_REPO env vars rather than editing.
THEME = os.environ.get("LR_THEME", "/private/tmp/claude-501/-Users-t-Downloads-LullyRest/d0c347d9-c107-44d9-92d2-0e12e4f54b5d/scratchpad/theme-new")
REPO  = os.environ.get("LR_REPO",  os.path.dirname(os.path.abspath(__file__)))

# ---------- 1. copy our custom files in ----------
for sub in ("sections", "blocks", "snippets", "assets", "templates"):
    src = os.path.join(REPO, sub)
    if not os.path.isdir(src):
        continue
    os.makedirs(os.path.join(THEME, sub), exist_ok=True)
    for fn in os.listdir(src):
        shutil.copy2(os.path.join(src, fn), os.path.join(THEME, sub, fn))
        print("copied", sub + "/" + fn)

# ---------- 2. register our blocks with Elixir's container sections ----------
def register(path, new_types):
    p = os.path.join(THEME, path)
    s = open(p, encoding="utf-8").read()
    m = re.search(r'({%\s*schema\s*%})(.*?)({%\s*endschema\s*%})', s, re.S)
    d = json.loads(m.group(2))
    have = {b.get("type") for b in d.get("blocks", [])}
    added = [t for t in new_types if t not in have]
    d.setdefault("blocks", []).extend({"type": t} for t in added)
    s = s[:m.start(2)] + "\n" + json.dumps(d, indent=2) + "\n" + s[m.end(2):]
    open(p, "w", encoding="utf-8").write(s)
    print("registered", added, "->", path)

register("sections/listicle.liquid", ["lullyrest-mechanism", "lullyrest-zones"])
register("blocks/cs-content.liquid", ["lullyrest-mechanism", "lullyrest-zones"])

# ---------- 3. presell listicle template ----------
IMG = "shopify://shop_images/"
V = "  ⚠ VERIFY BEFORE PUBLISH — "

items = [
  ("1. It isn't your desk. It's the eight hours nobody examined.", IMG+"lullyrest-hero.png",
   "<p>You've raised the monitor, bought the chair, done the physical therapy. Some of it even worked — for a few hours. Then you slept, and by 6:00 AM it was all back.</p>"
   "<p>Look at the arithmetic. <strong>A great PT session is 45 minutes. Sleep is eight hours.</strong> You spend roughly ten times longer in your sleeping position than in every correction combined. If those eight hours hold your neck wrong, they don't just cancel out the therapy — they overwrite it. Every night.</p>"),

  ("2. Your neck is a power cable — and a flat pillow kinks it.", None,
   "<p>Your neck runs from your body up into a junction box at the base of your skull. Inside are bundles of nerves carrying signals into your head, and the whole thing is built to run along a gentle curve. Not straight. Not folded.</p>"
   "<p>Fold it — the way a garden hose folds when you drag it round a corner — and pressure builds at the pinch. The C1–C3 segments compress, the small suboccipital muscles clamp down and stay clamped, and the nerves get squeezed against the tissue around them <strong>for eight straight hours</strong>.</p>"),

  ("3. [AWAITING CLINICAL REVIEW]", None,
   "<p><em>This slot is reserved for a named, credentialed reviewer — a DPT, DC or ergonomics researcher — and their actual assessment of the design.</em></p>"
   "<p><em>It is deliberately empty. The swipe this page is modelled on carries a chiropractor endorsement here; ours stays blank until a real one exists. Do not fill this with an invented name.</em></p>"),

  ("4. That's why the pain shows up behind your eyes.", None,
   "<p>If the compression is at the back of your neck, why does your forehead hurt?</p>"
   "<p>Because the nerves from the top of your neck feed into the same brainstem relay that handles sensation for your face. <strong>One shared fuse box, two rooms.</strong> Trip it from the neck and the alarm rings in the temple, the forehead, behind the eye.</p>"
   "<p>Which is why medication aimed at your head underperforms — it's chasing the alarm, not the fault — and why head imaging keeps coming back clean.</p>"),

  ("5. One height cannot serve two sleeping positions.", IMG+"lullyrest-side.png",
   "<p>This is why the pillow graveyard exists.</p>"
   "<p>On your back, the back of your skull sticks out further than your neck — you need a low spot for your head and support underneath your neck. On your side, your whole shoulder width is beneath you, and the gap from ear to mattress is several inches taller.</p>"
   "<p>One height cannot do both. A pillow tuned for back sleeping lets your head sag sideways when you turn. A pillow tuned for side sleeping pushes your chin to your chest when you turn back. <strong>And you roll over all night.</strong></p>"
   "<p>You weren't buying badly. You were buying from a category that never solved the problem.</p>"),

  ("6. Four zones, four jobs.", IMG+"lullyrest-top.png",
   "<p><strong>01 — Lordotic Cervical Extension Roll.</strong> Holds the 30°–35° arc so the cable stays curved.</p>"
   "<p><strong>02 — Recessed Central Occipital Cavity.</strong> Set 1.5–2in below the roll, so on your back the base of the skull opens instead of compressing.</p>"
   "<p><strong>03 — Dual-Loft Lateral Sleeping Wings.</strong> Outer thirds at 4.5–5.5in to match shoulder width — roll onto your side and you land on a surface already the right height.</p>"
   "<p><strong>04 — Integrated Ear Depressions.</strong> So your outer ear isn't crushed against firm foam all night.</p>"),

  ("7. The ear-and-jaw problem most contour pillows never fixed.", None,
   "<p>Ear pain and jaw soreness are what kill firm contour pillows by week two — the reason a &ldquo;closet full of expensive, useless foam shapes&rdquo; exists.</p>"
   "<p>The fix isn't a softer pillow. It's firm support under the <em>neck</em> with pressure deliberately relieved under the <em>ears</em>. The pillows that hurt you were uniformly firm everywhere. Zone 4 exists specifically for this.</p>"),

  ("8. It still has to hold its shape in month six.", IMG+"lullyrest-cross.png",
   "<p><em>&ldquo;Every brand advertises an orthopedic contour, but after three weeks the foam collapses in the middle and you're right back to waking up with a stiff neck.&rdquo;</em> — from public patient forums, not a LullyRest customer</p>"
   "<p>Geometry is worthless if it flattens. High-density open-cell viscoelastic foam is dense enough to hold the zone structure rather than sagging out from under you by hour three, and open-celled so heat moves through it instead of pooling under your head.</p>"),

  ("9. The smell is the dealbreaker — so the foam is vacuum-baked.", None,
   "<p><em>&ldquo;I too have a pillow graveyard. And can someone please make a pillow that doesn't come with an instant migraine scent.&rdquo;</em> — from public patient forums, not a LullyRest customer</p>"
   "<p>For someone whose migraines are triggered by chemical odour, an off-gassing pillow isn't an annoyance. It's the entire product failing on night one — and it's the single most common complaint across every competitor studied.</p>"
   "<p>Residual volatile compounds are driven off at the factory rather than in your bedroom.</p>"),

  ("10. 60 nights to decide — and 7–14 nights is a different number.", None,
   "<p><strong>7–14 nights: the adaptation window.</strong> Muscles contracted for years feel strange in correct alignment at first, sometimes mildly sore. That's tissue adjusting. Don't judge the pillow on night two.</p>"
   "<p><strong>60 nights: the money-back window.</strong> The full &ldquo;Painless Morning&rdquo; in-home trial. If your mornings aren't measurably better, return it for a full refund.</p>"
   "<p>Two numbers, two jobs. We keep them separate on purpose — conflating them is how customers quit on night three and how brands get accused of moving the goalposts.</p>"),
]

blocks, order = {}, []

blocks["header"] = {"type": "listicle-header", "settings": {
    "title": "10 Reasons Your Morning Neck Pain Starts Hours Before Your Alarm Goes Off",
    "title_size": 44, "alignment": "left",
    "show_author_info": True,
    "author_name": "By [NAME PENDING], [CREDENTIAL]",
    "author_date": "[DATE PENDING] — must be a real credentialed reviewer before publish",
}}
order.append("header")

blocks["summary"] = {"type": "listicle-summary", "settings": {"content":
    "<p><strong>TL;DR —</strong> The pain you wake up with isn't caused by your desk, your age, or your stress levels. "
    "It's caused by eight hours of mechanical compression at the top of your neck — and it's fixable with geometry, not medication.</p>"}}
order.append("summary")

for i, (title, image, content) in enumerate(items, start=1):
    key = "item_%d" % i
    st = {"title": title, "content": content}
    if image:
        st["image"] = image
    blocks[key] = {"type": "listicle-item", "settings": st}
    order.append(key)
    if i == 2:
        blocks["mechanism"] = {"type": "lullyrest-mechanism", "settings": {
            "caption": "Left: a flat, single-height pillow leaves the neck unsupported, so it sags and then turns a hard corner at the base of the skull. "
                       "Right: a recessed cavity lets the skull settle while a raised roll holds the neck, so the same cable runs one continuous curve."}}
        order.append("mechanism")
    if i == 6:
        blocks["zones"] = {"type": "lullyrest-zones", "settings": {}}
        order.append("zones")

blocks["offer"] = {"type": "listicle-callout-quote", "settings": {"content":
    "<p><strong>LullyRest Orthopedic Cervical Pillow — $149</strong> (was $199, save $50)</p>"
    "<p>Includes the ThermaFlow Phase-Change Cooling Cover and the 5-Minute Craniocervical Reset Protocol.</p>"
    "<p>60-night in-home trial · Full refund if your mornings aren't better · Zero-VOC vacuum-baked foam</p>"}}
order.append("offer")

blocks["sticky_atc"] = {"type": "listicle-sticky-atc", "settings": {
    "button_text": "See the four zones →",
    "button_link": "/products/lullyrest-orthopedic-cervical-pillow",
    "show_subtext": True,
    "subtext": "60-night in-home trial · Full refund if your mornings aren't better",
    "sticky": True}}
order.append("sticky_atc")

blocks["footer"] = {"type": "advertorial-footer", "settings": {
    "disclaimer_text": "This page describes how the LullyRest pillow is built and what it is designed to support. "
                       "It does not claim to treat, cure or prevent any medical condition. Individual results vary. "
                       "[VERIFY] Legal review required before publish.",
    "copyright_text": "© LullyRest",
    "show_links": False}}
order.append("footer")

presell = {"sections": {"listicle": {"type": "listicle", "blocks": blocks, "block_order": order,
                                     "settings": {"section_max_width": 900}}},
           "order": ["listicle"]}

with open(os.path.join(THEME, "templates/page.presell.json"), "w", encoding="utf-8") as f:
    json.dump(presell, f, indent=2, ensure_ascii=False)
print("wrote templates/page.presell.json —", len(order), "blocks")


# ---------- 4. PDP template ----------
# Mirrors the Dosaze PDP structure captured in research/swipes/ as closely as the
# theme allows, EXCEPT for anything that would render proof we don't have.
raw = re.sub(r'/\*.*?\*/', '', open(os.path.join(THEME, "templates/product.json"), encoding="utf-8").read(), flags=re.S)
prod = json.loads(raw)
main = prod["sections"]["main"]

# Blocks dropped because they render social proof LullyRest does not have. Not
# populated with placeholder text: a star widget or review carousel reads as real
# proof regardless of what its copy says. Tracked in lullyrest-proof-placeholder.
# trustpilot_rating and customer_review are now KEPT and filled with explicitly
# labelled placeholder copy at the user's request, so the layout can be reviewed.
# They contain NO real rating or customer words and must be replaced or removed
# before publish — tracked in lullyrest-proof-placeholder.
DROP_BLOCKS = {"number_one_award", "replica_warning",
               "carousel_default_video", "video_carousel_standalone"}
kept = [b for b in main.get("block_order", []) if main["blocks"][b]["type"] not in DROP_BLOCKS]
main["blocks"] = {k: main["blocks"][k] for k in kept}
main["block_order"] = kept


def block_of(sec, btype, nth=0):
    hits = [sec["blocks"][k] for k in sec["block_order"] if sec["blocks"][k]["type"] == btype]
    return hits[nth] if len(hits) > nth else None


def put(block, **kw):
    if block is not None:
        block.setdefault("settings", {}).update(kw)


# --- buy box copy (marketing/PDP_COPY.md) ---
put(block_of(main, "custom_text", 0),
    text="<p>Four-zone dual-loft core. Engineered for the two positions you actually sleep in.</p>")
put(block_of(main, "custom_text", 1), show_description=True,
    description=("<p><strong>Included:</strong> ThermaFlow&trade; Phase-Change Cooling Cover &middot; "
                 "5-Minute Craniocervical Reset Protocol (video + printable routine)</p>"))
put(block_of(main, "shipping_notice"), notice_text_before="Order today, expect delivery by", days_ahead=5)
put(block_of(main, "guarantee_badges"),
    badge_1_show=True, badge_1_text="60-night in-home trial",
    badge_2_show=True, badge_2_text="Zero-VOC vacuum-baked foam")
put(block_of(main, "money_back_guarantee"),
    text_small="60-Night Painless Morning Guarantee",
    text_large="Full refund if your mornings aren't better.")

# --- placeholder proof (LABELLED — not real data) ---
PH_NOTE = "PLACEHOLDER — replace before publish"
put(block_of(main, "trustpilot_rating"),
    rating_text=f"[{PH_NOTE}] Rating shown is sample layout data, not a real score",
    rating_score="4.9")
put(block_of(main, "customer_review"),
    reviewer_name="[PLACEHOLDER REVIEWER]", rating=5,
    review_text=("[PLACEHOLDER REVIEW — layout only] No LullyRest customer has written this. "
                 "Replace with a real verified review, or remove this block, before publish."))

# --- pack tiers. Free-gift TEXT ONLY: quantity_break renders the label, it does not
# add anything to the cart. Fulfilment needs a bundle app or Shopify Function. ---
put(block_of(main, "quantity_break"),
    show_radio_buttons=True, enable_custom_pricing=True, show_savings_text=True,
    preselected_option="2", show_option_4=False,
    show_option_1=True, option_1_title="1 Pillow", option_1_quantity=1,
    option_1_show_free_gift=True, option_1_free_gift_count=1,
    option_1_free_gift_text="+ Cooling Migraine Wrap",
    show_option_2=True, option_2_title="2 Pillows", option_2_quantity=2,
    enable_option_2_custom_price=True, option_2_custom_price_amount="249",
    option_2_compare_at_price="298",
    option_2_show_free_gift=True, option_2_free_gift_count=3,
    option_2_free_gift_text="+ Wrap, Blackout Sleep Mask & Filtered Earplugs",
    enable_option_2_badge=True, option_2_badge="BEST VALUE",
    show_option_3=True, option_3_title="3 Pillows", option_3_quantity=3,
    enable_option_3_custom_price=True, option_3_custom_price_amount="329",
    option_3_compare_at_price="447",
    option_3_show_free_gift=True, option_3_free_gift_count=3,
    option_3_free_gift_text="+ Full Sleep Kit for every pillow")

# --- FAQ (PDP_COPY.md Section G) ---
FAQ = [
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
fq = block_of(main, "product_faq")
if fq is not None:
    for i, (q, a) in enumerate(FAQ, 1):
        fq["settings"][f"question_{i}"] = q
        fq["settings"][f"answer_{i}"] = a
        fq["settings"][f"show_faq_{i}"] = True

pdp_sections, pdp_order = {"main": main}, ["main"]


def stock(t):
    for k in prod.get("order", []):
        if prod["sections"][k]["type"] == t:
            return json.loads(json.dumps(prod["sections"][k]))
    return None


def add(key, sec):
    if sec is not None:
        pdp_sections[key] = sec
        pdp_order.append(key)


def rebuild_blocks(sec, btype, items):
    """Replace every block of btype with our own, preserving the stock block's
    settings as a styling base so the section keeps Elixir's look."""
    base = {}
    for k in list(sec.get("block_order", [])):
        if sec["blocks"][k]["type"] == btype:
            if not base:
                base = dict(sec["blocks"][k].get("settings", {}))
            del sec["blocks"][k]
            sec["block_order"].remove(k)
    for i, settings in enumerate(items, 1):
        k = f"{btype}_{i}"
        merged = dict(base)
        merged.update(settings)
        sec["blocks"][k] = {"type": btype, "settings": merged}
        sec["block_order"].append(k)


# 1. trust bar
bar = stock("scrolling-features-bar")
if bar is not None:
    rebuild_blocks(bar, "feature_item", [
        {"text": "4-ZONE DUAL-LOFT CORE"},
        {"text": "ENGINEERED FOR BACK & SIDE SLEEPING"},
        {"text": "ZERO-VOC VACUUM-BAKED FOAM"},
        {"text": "THERMAFLOW™ COOLING COVER INCLUDED"},
        {"text": "60-NIGHT IN-HOME TRIAL"},
    ])
add("features_bar", bar)

# 2. benefit tabs  (Dosaze: "What Can Dosaze Do For You?")
ben = stock("product-benefits")
if ben is not None:
    rebuild_blocks(ben, "benefit", [
        {"title": "Zone 01 — Lordotic Cervical Extension Roll",
         "description": "A firmer roll under the neck that holds your natural 30°–35° arc, so the cable stays curved instead of folding."},
        {"title": "Zone 02 — Recessed Occipital Cavity",
         "description": "A cradle set 1.5–2in below the neck roll. On your back the skull settles in, and the base of the skull opens instead of compressing."},
        {"title": "Zone 03 — Dual-Loft Lateral Wings",
         "description": "Outer thirds built to 4.5–5.5in to match shoulder width, so rolling onto your side lands you on a surface that is already the right height."},
        {"title": "Zone 04 — Integrated Ear Depressions",
         "description": "Recesses in each wing so your outer ear isn't crushed against a firm surface all night. Ear and jaw pain is what kills most firm contour pillows by week two."},
    ])
add("benefits", ben)

# 3-4. our mechanism + zones diagrams (Dosaze: "How it works" + annotated diagram)
for key, stype in [("lullyrest_mechanism", "lullyrest-mechanism"), ("lullyrest_zones", "lullyrest-zones")]:
    add(key, {"type": stype, "settings": {}})

# 5. comparison  (Dosaze: "Why we're different")
cmp_ = stock("product-comparison")
if cmp_ is not None:
    cmp_["settings"].update({"show_heading": True, "column_count": "3",
                             "title_part_1": "Why we're", "title_part_2": "different",
                             "subheading": "<p>Compared against the two pillow types in most people's graveyard.</p>"})
    rebuild_blocks(cmp_, "product_column", [
        {"product_name": "LullyRest", "product_subtitle": "4-zone dual-loft", "highlight_column": True},
        {"product_name": "Standard contour pillow", "product_subtitle": "Single-height wave"},
        {"product_name": "Flat foam or fibre pillow", "product_subtitle": "One uniform surface"},
    ])
    rebuild_blocks(cmp_, "feature_row", [
        {"feature_name": "Different height for back vs side sleeping", "value_type": "checkmark",
         "value_1": "yes", "value_2": "no", "value_3": "no"},
        {"feature_name": "Holds a 30°–35° cervical curve", "value_type": "checkmark",
         "value_1": "yes", "value_2": "no", "value_3": "no"},
        {"feature_name": "Recessed occipital cavity", "value_type": "checkmark",
         "value_1": "yes", "value_2": "yes", "value_3": "no"},
        {"feature_name": "Ear-pressure relief cavities", "value_type": "checkmark",
         "value_1": "yes", "value_2": "no", "value_3": "no"},
        {"feature_name": "Vacuum-baked to drive off residual VOCs", "value_type": "checkmark",
         "value_1": "yes", "value_2": "no", "value_3": "no"},
        {"feature_name": "60-night in-home trial", "value_type": "checkmark",
         "value_1": "yes", "value_2": "no", "value_3": "no"},
    ])
add("comparison", cmp_)

# 5b. placeholder review carousel (LABELLED — not real customers)
rev = stock("customer-reviews-carousel")
if rev is not None:
    rev["settings"].update({"title_text": "[PLACEHOLDER] Customer reviews",
                            "accent_text": "sample layout only"})
    rebuild_blocks(rev, "review", [
        {"reviewer_name": "[PLACEHOLDER NAME 1]", "rating": 5, "show_verified_badge": False,
         "review_text": "[PLACEHOLDER REVIEW 1 — layout only] Replace with a real verified customer review before publish. No LullyRest customer has written this text."},
        {"reviewer_name": "[PLACEHOLDER NAME 2]", "rating": 5, "show_verified_badge": False,
         "review_text": "[PLACEHOLDER REVIEW 2 — layout only] Replace with a real verified customer review before publish. No LullyRest customer has written this text."},
        {"reviewer_name": "[PLACEHOLDER NAME 3]", "rating": 4, "show_verified_badge": False,
         "review_text": "[PLACEHOLDER REVIEW 3 — layout only] Replace with a real verified customer review before publish. No LullyRest customer has written this text."},
    ])
add("reviews_carousel", rev)

# 6. guarantee (our own section, already on-brand)
add("lullyrest_guarantee", {"type": "lullyrest-guarantee", "settings": {}})

# 7. store FAQ  (Dosaze: tabbed FAQ block)
sf = stock("store-faq")
if sf is not None:
    sf["settings"].update({"heading": "Questions", "subtitle": "<p>The ones that actually decide it.</p>"})
    rebuild_blocks(sf, "faq_item", [{"question": q, "answer": a} for q, a in FAQ])
add("store_faq", sf)

# 8. explicit inventory of the proof we do NOT have
pdp_sections["lullyrest_proof"] = {
    "type": "lullyrest-proof-placeholder",
    "blocks": {
        "s1": {"type": "slot", "settings": {"slot_name": "Star rating & review count",
               "slot_note": "The swipe carries “4.9 from 1628 reviews” here. LullyRest has zero. Elixir's trustpilot_rating block is removed from the buy box until real numbers exist.",
               "slot_status": "[EMPTY — no reviews exist]"}},
        "s2": {"type": "slot", "settings": {"slot_name": "Clinical endorsement",
               "slot_note": "The swipe uses a named chiropractor quote. Needs a real credentialed reviewer and their actual assessment.",
               "slot_status": "[EMPTY — no clinician on record]"}},
        "s3": {"type": "slot", "settings": {"slot_name": "UGC video testimonials",
               "slot_note": "Elixir's carousel_default_video and video_carousel_standalone are removed from the buy box; restore them once footage exists.",
               "slot_status": "[EMPTY — no customers yet]"}},
        "s4": {"type": "slot", "settings": {"slot_name": "Written customer reviews",
               "slot_note": "Elixir's customer-reviews and customer-reviews-carousel sections are ready to populate.",
               "slot_status": "[EMPTY — no customers yet]"}},
    },
    "block_order": ["s1", "s2", "s3", "s4"], "settings": {}}
pdp_order.append("lullyrest_proof")

# 9. sticky ATC last
for key in prod.get("order", []):
    if prod["sections"][key]["type"] == "sticky-add-to-cart":
        add(key, prod["sections"][key])

with open(os.path.join(THEME, "templates/product.lullyrest.json"), "w", encoding="utf-8") as f:
    json.dump({"sections": pdp_sections, "order": pdp_order}, f, indent=2, ensure_ascii=False)
print("wrote templates/product.lullyrest.json —", pdp_order)
