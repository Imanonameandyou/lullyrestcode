import json, os, re

THEME = os.environ["LR_THEME"]
path = os.path.join(THEME, "config", "settings_data.json")
with open(path, "r", encoding="utf-8") as f:
    raw = f.read()

# settings_data.json ships with a leading /* ... */ comment (same pattern as
# templates/product.json) -- strip it to parse, then re-prepend it on write
# so the file's own "auto-generated, don't hand-edit" header survives.
m = re.match(r"(\s*/\*.*?\*/\s*)", raw, flags=re.S)
header = m.group(1) if m else ""
data = json.loads(raw[len(header):])

cart = data["current"]["sections"]["cart-drawer"]
cart["blocks"] = {
    "cart_progress_bar": {
        "type": "cart_progress_bar",
        "settings": {
            # Free-shipping goal only. Not using product_free_amount/
            # progress_bar_free_product here -- that native "free gift" goal
            # expects the gift product to be priced $0 (see PROGRESS.md /
            # plan Global Constraints), which we deliberately did NOT do to
            # the pillowcase. Its free-gift framing is delivered via
            # cart_upsell_1 below + the real Buy-X-Get-Y discount, not this
            # progress-bar mechanic.
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
    f.write(header)
    json.dump(data, f, indent=2, ensure_ascii=False)
print("patched config/settings_data.json — cart-drawer blocks:", list(cart["blocks"].keys()))
