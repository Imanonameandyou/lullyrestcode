#!/usr/bin/env python3
"""Build LullyRest templates into the pulled draft theme and register custom blocks."""
import json, re, shutil, os

THEME = "/private/tmp/claude-501/-Users-t-Downloads-LullyRest/d0c347d9-c107-44d9-92d2-0e12e4f54b5d/scratchpad/draft-theme"
REPO  = "/Users/t/Downloads/LullyRest/lullyrestcode/theme"

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
    s = open(p).read()
    m = re.search(r'({%\s*schema\s*%})(.*?)({%\s*endschema\s*%})', s, re.S)
    d = json.loads(m.group(2))
    have = {b.get("type") for b in d.get("blocks", [])}
    added = [t for t in new_types if t not in have]
    d.setdefault("blocks", []).extend({"type": t} for t in added)
    s = s[:m.start(2)] + "\n" + json.dumps(d, indent=2) + "\n" + s[m.end(2):]
    open(p, "w").write(s)
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

with open(os.path.join(THEME, "templates/page.presell.json"), "w") as f:
    json.dump(presell, f, indent=2, ensure_ascii=False)
print("wrote templates/page.presell.json —", len(order), "blocks")

# ---------- 4. PDP template ----------
raw = re.sub(r'/\*.*?\*/', '', open(os.path.join(THEME, "templates/product.json")).read(), flags=re.S)
prod = json.loads(raw)
main = prod["sections"]["main"]

DROP_BLOCKS = {"trustpilot_rating", "number_one_award", "customer_review", "quantity_break",
               "replica_warning", "carousel_default_video", "video_carousel_standalone"}
kept = [b for b in main.get("block_order", []) if main["blocks"][b]["type"] not in DROP_BLOCKS]
main["blocks"] = {k: main["blocks"][k] for k in kept}
main["block_order"] = kept
print("PDP main blocks kept:", [main["blocks"][k]["type"] for k in kept])

pdp_sections = {"main": main}
pdp_order = ["main"]

for key, stype, settings in [
    ("lullyrest_zones", "lullyrest-zones", {}),
    ("lullyrest_mechanism", "lullyrest-mechanism", {}),
    ("lullyrest_guarantee", "lullyrest-guarantee", {}),
]:
    pdp_sections[key] = {"type": stype, "settings": settings}
    pdp_order.append(key)

pdp_sections["lullyrest_proof"] = {
    "type": "lullyrest-proof-placeholder",
    "blocks": {
        "s1": {"type": "slot", "settings": {"slot_name": "Star rating & review count",
               "slot_note": "The swipe carries “4.9 from 1628 reviews” here. LullyRest has zero reviews.",
               "slot_status": "[EMPTY — no reviews exist]"}},
        "s2": {"type": "slot", "settings": {"slot_name": "Clinical endorsement",
               "slot_note": "A named, credentialed reviewer and their actual assessment of the design.",
               "slot_status": "[EMPTY — no clinician on record]"}},
        "s3": {"type": "slot", "settings": {"slot_name": "UGC video testimonials",
               "slot_note": "Elixir's video-carousel-standalone section is already in this theme, ready to populate.",
               "slot_status": "[EMPTY — no customers yet]"}},
        "s4": {"type": "slot", "settings": {"slot_name": "Written customer reviews",
               "slot_note": "Elixir's customer-reviews and customer-reviews-carousel sections are ready to populate.",
               "slot_status": "[EMPTY — no customers yet]"}},
    },
    "block_order": ["s1", "s2", "s3", "s4"],
    "settings": {}}
pdp_order.append("lullyrest_proof")

for key in prod.get("order", []):
    if prod["sections"][key]["type"] == "sticky-add-to-cart":
        pdp_sections[key] = prod["sections"][key]
        pdp_order.append(key)

with open(os.path.join(THEME, "templates/product.lullyrest.json"), "w") as f:
    json.dump({"sections": pdp_sections, "order": pdp_order}, f, indent=2, ensure_ascii=False)
print("wrote templates/product.lullyrest.json —", pdp_order)
