#!/usr/bin/env python3
"""Build templates/page.neck-pain-listicle.json directly into this repo's theme/
folder. Unlike build_templates.py, this does NOT need a live pulled theme (THEME
env var) -- it writes straight to REPO/templates/, the same place page.presell.json
already lives as a tracked, generated artifact. build_templates.py's existing
step-1 copy loop (copies everything under REPO/templates/ into the pulled theme)
will pick this file up automatically once a live pull/push happens.

Content is verbatim from LullyRest_Listicle_First_Half.md and
LullyRest_Listicle_Second_Half.md (repo root) -- nothing here is rewritten. This
is a second, separate page from the existing presell page/template; neither the
old page.presell.json nor build_templates.py are touched.
"""
import json, os

REPO = os.path.dirname(os.path.abspath(__file__))


def ph(text):
    """One inline-styled image-placeholder box. Same single font treatment
    (mono, .72rem) on every use -- no per-section type variation -- and no
    external stylesheet dependency, since this page uses no custom lullyrest-*
    blocks/sections and therefore never loads lullyrest.css. Labelled
    "IMAGE PLACEHOLDER" up top, matching this repo's existing [EMPTY]/[VERIFY]
    convention for unfilled slots (lullyrest-proof-placeholder, .lr__verify)."""
    return (
        '<div style="margin:1.5rem 0;border:1px dashed #C9C7C0;background:#F2F1ED;'
        'aspect-ratio:16/9;display:flex;align-items:center;justify-content:center;'
        'padding:1.25rem;">'
        '<span style="font-family:ui-monospace,SFMono-Regular,Menlo,monospace;'
        'font-size:.72rem;letter-spacing:.03em;line-height:1.5;text-align:center;'
        'opacity:.7;max-width:42ch;display:block;">'
        '<strong style="letter-spacing:.08em;">IMAGE PLACEHOLDER</strong><br>' + text + '</span></div>'
    )


items = [
    ("1. YOUR NECK PAIN AND YOUR MORNING MIGRAINES AREN'T TWO SEPARATE PROBLEMS",
     "<p>Most people treat these like different issues. The stiff neck is one thing. The headache that creeps from behind your skull into your temples and eye sockets by 9 AM is another.</p>"
     "<p>They're not.</p>"
     "<p>Your upper neck — the top three vertebrae right where your skull meets your spine — is where a bundle of nerves exits and runs upward into your head. When those nerves get physically squeezed during sleep, the pain doesn't just stay in your neck.</p>"
     "<p>Think of it like a power cable running from your body up into your skull. When that cable gets kinked (your head at the wrong angle for six, seven, eight hours straight) the wires inside get pinched.</p>"
     "<p>But the signals don't stop at the kink. They travel up and set off alarms in your forehead, behind your eyes, across your temples.</p>"
     "<p>That's why you can rub your neck in the morning and feel the headache ease for a few minutes.</p>"
     "<p>You're temporarily releasing pressure on the same nerve bundle that's sending pain signals into your face.</p>"
     "<p>Your physical therapist targets this exact spot during upper neck release work — except they fix it for 45 minutes, and then your pillow re-compresses it for 8 hours.</p>"
     + ph("Simple illustration showing upper neck vertebrae (C1–C3) with nerve pathways running upward into the head — arrows showing where compression at the neck creates referred pain behind the eyes, temples, and forehead. Clean, anatomical, not clinical.")),

    ("2. WHY EVERY CONTOUR PILLOW YOU'VE TRIED WORKED FOR TWO WEEKS, THEN STOPPED",
     "<p>You already know what happens. You get a new pillow. First few nights feel different — maybe better, maybe just unfamiliar.</p>"
     "<p>Then by week two, you're waking up with the same locked neck and creeping headache.</p>"
     "<p>And here's the part no pillow brand explains:</p>"
     "<p>Your neck needs two completely different things depending on whether you're on your back or on your side.</p>"
     "<p>When you're on your back, your head needs to sit <em>lower</em> than your neck. The base of your skull should drop back slightly so the natural curve of your cervical spine stays open. If the pillow pushes your head up and forward (chin toward chest) the nerves at the top of your spine get compressed all night.</p>"
     "<p>Then when you roll onto your side, the equation completely changes. Now your head needs to be <em>higher</em> — high enough to bridge the gap between your ear and your shoulder. If the pillow is too low for side sleeping, your neck sags sideways and those same nerves get pinched from a different angle.</p>"
     "<p>One height cannot do both.</p>"
     "<p>Every contour pillow you've tried had one curved surface. One height. It may have been the right height for your back — which means it was wrong for your side. Or it was right for your side and pushed your chin forward on your back.</p>"
     "<p>Either way, every time you switched positions during the night, the pillow that was \"aligned\" for one position compressed your neck in the other. And you woke up with the headache again.</p>"
     + ph("Side-by-side comparison showing the same person sleeping on a single-height contour pillow — back position vs. side position. Back position shows proper alignment. Side position shows neck sagging/buckling. Caption: “One height. Two positions. One of them always loses.”")),

    ("3. THE FOAM PROBLEM NOBODY PUTS ON THE LABEL",
     "<p>Even if a pillow had the right shape, the material can sabotage it.</p>"
     "<p><strong>The smell.</strong> That chemical off-gassing from synthetic memory foam isn't just unpleasant — for anyone with sensitized nerve pathways (which, if you're getting frequent migraines, you likely have), those fumes can trigger a headache within minutes of lying down.</p>"
     "<p><strong>The heat.</strong> Closed-cell memory foam traps body heat. You shift positions more, and every shift is another chance for your neck to land at the wrong angle. Heat plus compressed nerves is two triggers at once.</p>"
     "<p><strong>The collapse.</strong> This is the one that explains why every pillow \"stops working.\" Lower-density foam softens under body heat and repeated pressure. Within three to six weeks, the firm support that held your neck in position on night one degraded into a flatter, softer surface that lets your head sink. It lost structural integrity, and the nerve compression came back.</p>"
     + ph("Cross-section comparison of closed-cell vs. open-cell foam structure, showing airflow channels in open-cell. Second image: time-lapse concept showing foam core on Day 1 (firm, holding shape) vs. Week 6 (compressed, flattened in the center). Caption: “Same pillow. Six weeks apart.”")),

    ("4. YOUR EARS AND JAW ARE PAYING THE PRICE TOO",
     "<p>This one doesn't get talked about enough.</p>"
     "<p>If you're a side sleeper (and most people spend at least part of the night on their side) a pillow that's too firm or too flat creates direct pressure on your ear cartilage.</p>"
     "<p>Sleep on it for six hours and you wake up with a sore, red, throbbing ear. Do it every night and you develop chronic cartilage inflammation that makes side sleeping painful on its own, even without the neck issue.</p>"
     "<p>It gets worse if you clench your jaw at night. A hard surface pressing into the side of your face aggravates your TMJ — the jaw joint right in front of your ear. That creates a secondary pain loop: neck compression triggers the migraine, jaw compression adds face and temple pain on top of it, and now you're dealing with two overlapping pain sources that both started with the same pillow.</p>"
     "<p>Most contour pillows treat the side-sleeping surface as an afterthought — the same foam, the same density, no relief channel for the ear. That's another failure mode that has nothing to do with alignment and everything to do with pressure distribution.</p>"
     + ph("Close-up of side-sleeping position showing ear compressed against a flat foam surface vs. a surface with a recessed ear depression. Caption: “Standard contour: full pressure on ear and jaw. Zoned design: ear cavity eliminates cartilage compression.”")),

    ("5. WHAT YOUR NECK ACTUALLY NEEDS — FOR ALL 8 HOURS, NOT JUST THE FIRST 20 MINUTES",
     "<p>Your neck has a natural forward curve of about 30 to 35 degrees. When that curve is supported, the small spaces between your upper vertebrae stay open and the nerves running through them have room. When the curve flattens or reverses (which is what happens on a flat or collapsed pillow) those spaces close, the muscles at the base of your skull clamp down, and the compression cycle starts.</p>"
     "<p>Lasting relief means keeping that curve intact through every position you move into during the night. Not just when you first lie down. Not just on your back. Through every shift, every roll, every transition from back to side to back again — for a full 8 hours.</p>"
     "<p>That requires dedicated zones: a different height for back sleeping than for side sleeping, a recessed space for your skull so your head doesn't get pushed forward, relief channels for your ears and jaw, and a core dense enough to hold its shape night after night without softening under your body heat.</p>"
     + ph("Overhead diagram of a multi-zone pillow layout — labeled zones: center cervical roll, recessed skull cavity, elevated lateral wings with ear depressions. No brand name yet. Clean engineering-style diagram, not a product photo. Caption: “Four zones. Two sleeping planes. One pillow that doesn't force you to choose.”")),

    ("6. THE FIX ISN'T A BETTER CONTOUR PILLOW. IT'S A COMPLETELY DIFFERENT STRUCTURE.",
     "<p>The LullyRest Orthopedic Cervical Pillow was engineered around a different premise: back sleeping and side sleeping are two separate problems, and they need two separate solutions built into the same pillow.</p>"
     "<p>Instead of one contoured shape, LullyRest uses a 4-zone core — four distinct structural areas, each calibrated to a different height and function, so your upper neck stays decompressed no matter which position you're in or how many times you shift during the night.</p>"
     "<p>Here's what each zone does.</p>"),

    ("7. FOUR ZONES. EACH ONE SOLVES A SPECIFIC FAILURE MODE.",
     "<p><strong>Zone 1 — The Cervical Extension Roll.</strong> A firm, molded roll that sits under your neck when you're on your back. Its job is to hold your neck's natural 30- to 35-degree arc that keeps the spaces between your upper vertebrae open. Most contour pillows attempt this, but get the height wrong or use foam that softens within weeks. The LullyRest roll is calibrated to a specific height range and built from high-density foam that doesn't degrade under body heat.</p>"
     "<p><strong>Zone 2 — The Recessed Skull Cavity.</strong> A basin in the center of the pillow where the back of your head sits — about 1.5 to 2 inches lower than the neck roll. This keeps your skull dropped back naturally so your chin doesn't get pushed toward your chest.</p>"
     "<p><strong>Zone 3 — The Dual-Loft Side Wings.</strong> Elevated platforms on the left and right sides — 4.5 to 5.5 inches of height — that only engage when you roll onto your side. These bridge the gap between your ear and your shoulder so your neck stays level instead of sagging sideways.</p>"
     "<p><strong>Zone 4 — The Ear and Jaw Relief Channels.</strong> Shallow depressions carved into the side wings, right where your ear sits during side sleeping. Instead of your full body weight pressing your ear into a flat foam surface for 6 hours, the channel creates a pocket of space. Your ear sits in it instead of being crushed against it.</p>"
     + ph("Overhead photo or clean diagram of the LullyRest pillow with all four zones labeled — cervical roll, recessed skull cavity, dual-loft side wings, ear relief channels. Each label connected to a one-line function description. This is the first product image in the listicle.")),

    ("8. THE MATERIAL IS ENGINEERED TO NOT SABOTAGE THE DESIGN",
     "<p>LullyRest's core is built from high-density, open-cell foam.</p>"
     "<p><strong>High-density:</strong> same firmness on night sixty as night one. No softening under body heat. No flattening in the center after a few weeks.</p>"
     "<p><strong>Open-cell:</strong> airflow channels run throughout the foam instead of trapping heat against your skin. If heat is one of your migraine triggers, this is the difference between waking up in a sweat and staying cool through the night.</p>"
     "<p><strong>Zero off-gassing:</strong> the foam goes through a vacuum-baking process during manufacturing that burns off those entoxicating smells before the pillow ever reaches you. This means no smell-triggered migraine on the first night.</p>"
     "<p>The pillow ships with a ThermaFlow™ phase-change cooling cover fitted to the contoured zones. Phase-change fabric doesn't just breathe — it actively pulls heat away from your skin and redistributes it.</p>"
     + ph("Close-up cross-section of the open-cell foam showing visible airflow channels, side-by-side with a closed-cell foam cross-section for comparison. Caption: “Open-cell (left): air passes through. Closed-cell (right): heat stays trapped.”")),

    ("9. THE FIRST WEEK MIGHT FEEL STRANGE. THAT'S ACTUALLY THE POINT.",
     "<p>This is the part most pillow brands will never tell you... because it costs them returns.</p>"
     "<p>If your neck has been compensating for a bad pillow for years, those muscles won't relax overnight. They need time to release, lengthen, and adapt to the correct position.</p>"
     "<p>That process takes roughly 7 to 14 nights.</p>"
     "<p>During that window, the pillow might feel \"weird\" — too firm, too different, not what you're used to. That feeling isn't the pillow failing. It's your neck adapting to being properly supported for the first time in a long time.</p>"
     "<p>This is why judging a cervical pillow after two or three nights is the mistake almost everyone makes. The pillow didn't stop working. You just never gave your body enough time to adjust to it working correctly.</p>"
     "<p>This is also exactly why LullyRest's trial period is 60 nights, not 14 or 30. You need the full adaptation window plus enough time after it to feel the actual difference. Anything shorter, and you're testing the adjustment period, not the pillow.</p>"
     + ph("Simple timeline graphic showing Night 1–7 (“Adjustment — muscles adapting to correct position”), Night 7–14 (“Transition — tension releasing, sleep improving”), Night 14–60 (“Full benefit — pain-free mornings, clearer head”). Caption: “Your spine needs time. The trial gives it.”")),

    ("10. 60 NIGHTS. FULL REFUND. NO CATCH.",
     "<p>You've spent enough money on pillows that didn't work. You shouldn't have to gamble again.</p>"
     "<p>The LullyRest 60-Night \"Painless Morning\" Guarantee works like this: sleep on it for up to 60 nights. Give your neck the 7- to 14-day adaptation window. If your morning migraines, neck stiffness, and brain fog haven't meaningfully improved — send it back and I, Dr. Brady Menoles, see to it that you get a full refund.</p>"
     "<p><strong>What ships with every order:</strong></p>"
     "<ul>"
     "<li>The LullyRest Orthopedic Cervical Pillow — the full 4-zone dual-loft core.</li>"
     "<li>The ThermaFlow™ Phase-Change Cooling Cover — fitted to the pillow's contoured zones, actively cools instead of just breathing.</li>"
     "<li>The 5-Minute Neck Reset Protocol — a video and PDF guide with gentle stretches and exercises designed to relax the muscles at the base of your skull before bed, so the pillow's decompression starts the moment you lie down.</li>"
     "<li>The 60-Night Painless Morning Guarantee — full refund if it doesn't work. You keep the Reset Protocol either way.</li>"
     "</ul>"),
]

blocks, order = {}, []

blocks["header"] = {"type": "listicle-header", "settings": {
    "title": "I've Tried 10+ \"Cervical\" Pillows for My Morning Migraines. Here's Why They All Failed the Same Way.",
    "title_size": 44, "alignment": "left",
    "show_author_info": True,
    "author_name": "Dr. Brady Menoles, DPT",
    "author_date": "Verified Spine & Sleep Biomechanics Specialist",
}}
order.append("header")

blocks["summary"] = {"type": "listicle-summary", "settings": {"content":
    "<p>Most cervical pillows promise alignment but miss the specific nerve compression point that causes the headaches, eye pressure, and brain fog you wake up with every morning.</p>"
    "<p><strong>TL;DR:</strong> Your cervical pillow probably supports your neck in one position and compresses it in another. Here are 10 structural problems that most \"orthopedic\" pillows share — and the engineering changes that actually fix them.</p>"
    "<p>If you're reading this, you probably own what your family calls the \"pillow graveyard.\"</p>"
    "<p>A closet, a shelf, maybe an entire section under your bed filled with $40 to $200 contour pillows that felt right for a week or two — then stopped working. Memory foam. Shredded latex. Water bladders. Buckwheat. The list goes on.</p>"
    "<p>And every single one promised the same thing: <em>proper cervical alignment.</em></p>"
    "<p>Here's what I've learned after years of treating patients whose morning migraines, locked-up necks, and all-day brain fog kept coming back no matter which pillow they tried:</p>"
    "<p>Alignment was never the whole problem.</p>"
    "<p>The real issue is more specific — and until you understand it, every pillow you buy will fail for the same reason. Let me walk you through what's actually happening.</p>"}}
order.append("summary")

for i, (title, content) in enumerate(items, start=1):
    key = "item_%d" % i
    blocks[key] = {"type": "listicle-item", "settings": {"title": title, "content": content}}
    order.append(key)
    if i == 5:
        blocks["mid_cta"] = {"type": "listicle-callout-quote", "settings": {"content":
            "<p><em>The pillow engineered to solve every problem on this list — with a 60-night in-home trial so your neck has time to actually adapt.</em></p>"
            "<p><strong><a href=\"/products/lullyrest-orthopedic-cervical-pillow\">→ See How the 4-Zone Core Works</a></strong></p>"}}
        order.append("mid_cta")

blocks["final_cta"] = {"type": "listicle-callout-quote", "settings": {"content":
    "<p>You've tried alignment pillows. You've tried expensive foam. You've tried folding, stacking, switching, and starting over. The nerve compression kept coming back because no single-surface pillow could solve it.</p>"
    "<p>LullyRest is the first cervical pillow engineered with four dedicated zones — two separate height planes for back and side sleeping, recessed ear channels, and a zero-VOC open-cell core that won't collapse, overheat, or trigger a migraine.</p>"
    "<p>Try it for 60 nights. Your neck needs 7–14 to adapt. The other 46 are yours to decide.</p>"
    "<p><strong><a href=\"/products/lullyrest-orthopedic-cervical-pillow\">→ Try LullyRest Risk-Free for 60 Nights</a></strong></p>"
    "<p>Free Shipping · Free Returns · Free Exchanges</p>"}}
order.append("final_cta")

blocks["sticky_atc"] = {"type": "listicle-sticky-atc", "settings": {
    "button_text": "→ Try LullyRest Risk-Free for 60 Nights",
    "button_link": "/products/lullyrest-orthopedic-cervical-pillow",
    "show_subtext": True,
    "subtext": "Free Shipping · Free Returns · Free Exchanges",
    "sticky": True}}
order.append("sticky_atc")

blocks["footer"] = {"type": "advertorial-footer", "settings": {
    "disclaimer_text": "This page describes how the LullyRest pillow is built and what it is designed to support. "
                       "It does not claim to treat, cure or prevent any medical condition. Individual results vary. "
                       "[VERIFY] Legal review required before publish.",
    "copyright_text": "© LullyRest",
    "show_links": False}}
order.append("footer")

listicle_section = {"type": "listicle", "blocks": blocks, "block_order": order,
                     "settings": {"section_max_width": 900}}

# ---------- reviews wall (6 testimonials, verbatim) ----------
reviews = [
    ("Rachel M.", 5,
     "I have what my husband calls the pillow graveyard — seriously, 12 pillows in 3 years. The first week on LullyRest felt odd, firmer than I'm used to. By week two the morning headaches stopped. I'm on month four and I haven't woken up with that base-of-skull pressure once. I actually cried the first morning I woke up without it."),
    ("James T.", 5,
     "Software engineer, 10 hours a day at a screen. My neck was so bad I couldn't sit through a standup meeting without my arms going tingly. Tried the Dosaze, tried the Epabo, tried a $230 latex pillow from some European brand. All lasted about two weeks. LullyRest is the first one where the support actually held up. Three months in, same firmness as day one. Morning brain fog is gone."),
    ("Dr. Sarah K.", 5,
     "I'm a dental hygienist — bent over patients 8 hours a day. The neck tension was brutal and every contour pillow I tried crushed my ears during side sleeping. The ear channels on this pillow are the detail nobody else thought of. No more waking up with a throbbing ear and a TMJ flare. My chiro noticed the difference in my suboccipital tension within a month."),
    ("Marcus D.", 4,
     "Fair warning — the first 5 nights I almost returned it. Felt too firm and my neck was sore in a different way. Stuck with it because the article said to give it two weeks. By night 10, something shifted. Woke up one morning and realized I hadn't had the headache. That was six weeks ago. Only reason for 4 stars instead of 5: I wish it came in a king-size option."),
    ("Lisa R.", 5,
     "Let me just add up what I've spent on the pillow graveyard — chiropractor visits, shredded foam, buckwheat, a water pillow, two memory foam contours — easily $800+. This was $[XX] and it's the only one that didn't trigger a migraine from the smell alone AND didn't go flat in a month. The cooling cover actually works too. My husband stole my extra pillowcase."),
    ("Tom W.", 5,
     "Truck driver, 15 years on the road. Skeptic of everything. Bought it because of the 60-night trial — figured I'd return it like everything else. Night 12 I slept through without waking up at 3 AM to rub my neck. That hasn't happened in years. I just ordered a second one for my sleeper cab."),
]

rev_blocks, rev_order = {}, []
for i, (name, rating, text) in enumerate(reviews, start=1):
    key = "review_%d" % i
    rev_blocks[key] = {"type": "review", "settings": {
        "reviewer_name": name, "rating": rating,
        "show_verified_badge": True, "review_text": text}}
    rev_order.append(key)

reviews_section = {"type": "customer-reviews-carousel", "blocks": rev_blocks, "block_order": rev_order,
                    "settings": {"title_text": "FROM READERS WHO TRIED LULLYREST AFTER READING THIS ARTICLE:",
                                 "accent_text": "verified reviews"}}

page = {"sections": {"listicle": listicle_section, "reviews_carousel": reviews_section},
        "order": ["listicle", "reviews_carousel"]}

out_path = os.path.join(REPO, "templates", "page.neck-pain-listicle.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(page, f, indent=2, ensure_ascii=False)
print("wrote templates/page.neck-pain-listicle.json —", len(order), "listicle blocks +", len(rev_order), "reviews")
