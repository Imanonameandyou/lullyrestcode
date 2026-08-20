# LullyRest — Bonus / Gift-With-Purchase Products

Physical bonuses attached to the offer tiers in `../research/OFFER.md`. Selection rationale: every bonus must service a specific belief or objection from `../research/BELIEF_CHAIN.md` / `../research/AUDIENCE.md`. Anything that's just "sleep swag" gets cut — `../brand/BRAND_GUIDE.md` names the mass bedding industry's filler marketing as our antagonist, so filler bonuses actively undercut positioning.

All products are created **DRAFT** per `../CLAUDE.md` rule 3.

## Shipping now (tier 1–2)

| Product | SKU | Perceived value | Est. landed | Services |
|---|---|---|---|---|
| LullyRest Cooling Migraine Wrap | `LR-CMW-001` | $29 | ~$3 | The ice-pack horror story in `VOICE_OF_CUSTOMER.md` |
| LullyRest Contoured Blackout Sleep Mask | `LR-CBM-001` | $24 | ~$2 | Photophobia; orbital pressure pain |
| LullyRest Filtered Sleep Earplugs | `LR-FSE-001` | $19 | ~$1 | Belief #3's "eight uninterrupted hours" |

## Held for phase 2

| Product | Why held |
|---|---|
| Magnesium glycinate | Ingestible supplement — needs GMP sourcing, Supplement Facts panel, FDA disclaimer, structure-function claim review, and a "consult your doctor" line (this avatar is frequently on triptans / muscle relaxants). Best *mechanism* fit of all bonuses — acts on the same suboccipital tissue the pillow does — but a different sourcing track. Do not gate launch on it. |

## Cut

| Product | Why |
|---|---|
| Cooling bedsheets | Services no belief in the chain. Sizing matrix (4 sizes x colors), $25–40 landed, real shipping weight, exchange overhead — more COGS than the other four combined. Also redundant against the ThermaFlow™ cooling cover already promised on the core unit. |

## Tier structure

Delivered via Elixir's `quantity_break` section, already present in `theme/` templates/product.lullyrest.json.

- **1 pillow — $149** → Cooling Migraine Wrap + 5-Minute Craniocervical Reset Protocol
- **2 pillows — $249** → + Blackout Sleep Mask + Filtered Earplugs *("The Night Kit")*
- **3 / Full Reset — $329** → + magnesium, once compliance clears

Rationale: one free hero bonus at every tier keeps the clinical frame intact; the rest pull AOV instead of being given away at entry. This is our answer to Dosaze's BOGO without inheriting their discount mechanic, which `OFFER.md` explicitly warns against.

## Open

- [ ] **Do returned orders keep the bonuses?** "Keep everything" strengthens the 60-night risk reversal but costs ~$6/return across tier 1–2.
- [ ] Trademark symbols — `OFFER.md` already uses `ThermaFlow™`. None of these names are registered marks yet; don't ship a ™ on anything unfiled.
- [ ] Suppliers not yet sourced for any bonus.

## Copy note

All descriptions are mechanism-led per `BRAND_GUIDE.md` voice rules — no "cloud-like" / "luxurious" bedding language, numbers set in Space Mono where the theme allows. Every claim below is a **product-design** claim, not a medical one.
