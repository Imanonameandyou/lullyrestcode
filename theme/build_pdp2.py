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


if __name__ == "__main__":
    pdp_sections, pdp_order = {}, []
    # sections appended by later tasks
    out_path = os.path.join(THEME, "templates", "product.lullyrest-close.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"sections": pdp_sections, "order": pdp_order}, f, indent=2, ensure_ascii=False)
    print("wrote templates/product.lullyrest-close.json —", pdp_order)
