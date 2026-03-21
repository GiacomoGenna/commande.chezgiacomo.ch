# CLAUDE.md — Chez Giacomo · Pâtes & Farines de Sicile

## What this project is

A standalone order form for Giacomo's artisanal pasta and Sicilian ancient grain flour business. Customers fill in the form and send their order via WhatsApp or email. No backend, no framework — just one HTML file.

---

## Deployment

- **Live URL**: https://giacomogenna.github.io/commande.chezgiacomo.ch/
- **GitHub repo**: https://github.com/giacomogenna/commande.chezgiacomo.ch
- **Main website** (not editable): https://www.chezgiacomo.ch — built on Gamma/gammahosted.com
- The Gamma site links to the GitHub Pages order form
- To deploy: commit and push `commander.html` (+ images if changed) to `main` branch

## Local preview

Open `commander.html` directly by double-clicking it in Finder. No server needed.
If a Python server is needed (e.g. for Claude Code preview tools), run:
```
python3 -c "import os,http.server,socketserver; os.chdir('/Users/giacomo/Desktop/Chez Giacomo - Pasta'); httpd=socketserver.TCPServer(('',8789),http.server.SimpleHTTPRequestHandler); httpd.serve_forever()"
```
Then open http://localhost:8789/commander.html

---

## File structure

```
commander.html                  ← The entire order form (HTML + CSS + JS in one file)
CLAUDE.md                       ← This file

# Product images used in the form
Busiata.jpg
Spaghetti.jpg
Linguine.jpg
Mezze maniche.jpg
Penne Rigate.jpg
Pappardelle.jpg
Mix farina - Pizza.jpg
Mix farina - Pane.jpg
Mix farina - Pasta.jpg
pasta artigianale Mulino Angelica.jpg   ← Used for Pack Découverte card

# Other assets / working files (not used by the form)
Pricing_Chez_Giacomo.xlsx
Commande_400kg_Chez_Giacomo.xlsx
listino prezzi PV1.pdf
Diagnostic_Lor_de_Sicile.md
serve.py                        ← Python dev server helper
[various other product/marketing photos]
```

---

## Design choices

### Colors
| Role | Hex |
|---|---|
| Primary (terracotta) | `#c2541a` |
| Dark brown (text) | `#2c1a0e` |
| Warm background | `#fdf8f3` |
| Border / dividers | `#e8ddd4` |
| Muted text | `#888`, `#999`, `#aaa` |
| WhatsApp button | `#25D366` |
| Active card highlight | `#c2541a` border + `#c2541a22` shadow |
| Pack card background | `#fff8f3` |

### Typography
- **Body / headings**: Georgia (serif) — warm, artisanal feel
- **UI elements** (labels, buttons, badges, prices): system sans-serif
- Section titles: 11px, uppercase, letter-spacing 2px, `#c2541a`
- Form field labels: 11px, uppercase, letter-spacing 1.5px, `#888`

### Layout
- Max width: 680px, centered
- Single-column mobile, 2-col grid for Prénom/Nom and NPA/Ville
- Sticky footer bar with total + send buttons
- Bottom padding 180px on main to clear sticky footer
- Breakpoint: 520px — single column, larger fonts, icon-only buttons

### UI patterns
- Product cards with circular photo (70px), name, subtitle, price, qty stepper
- Active card gets terracotta border on qty > 0
- Pack Découverte: special card with `border: 2px solid #c2541a`, "Coup de coeur" badge
- Quantity steppers: `−` / `+` buttons with `#f5ede5` background
- Discount shown inline as strikethrough price when threshold reached
- Pill-shaped checkboxes for pack mix / delivery / motivations — highlight terracotta when checked
- All form inputs use Georgia serif, `border-radius: 10px`
- Placeholder color: `#ddd` (very light, intentional)
- Input placeholders: no "ex." prefix — just the example value (e.g. "Jaime", not "ex. Jaime")

---

## Product catalogue

### Pâtes artisanales — 500 g
| Name | Bexio code | Price |
|---|---|---|
| Busiata | `PAST-BUS-500` | 7.50 CHF (6.00 dès 3) |
| Spaghetti | `PAST-SPA-500` | 7.50 CHF (6.00 dès 3) |
| Linguine | `PAST-LIN-500` | 7.50 CHF (6.00 dès 3) |
| Mezze Maniche | `PAST-MEZ-500` | 7.50 CHF (6.00 dès 3) |
| Penne Rigate | `PAST-PEN-500` | 7.50 CHF (6.00 dès 3) |
| Pappardelle | `PAST-PAP-500` | 7.50 CHF (6.00 dès 3) |

### Farines — 1 kg
| Name | Bexio code | Price |
|---|---|---|
| Mix Pizza | `MIX-PIZ-1KG` | 9.00 CHF (7.50 dès 3) |
| Mix Pain | `MIX-PAI-1KG` | 9.00 CHF (7.50 dès 3) |
| Mix Pasta | `MIX-PAT-1KG` | 9.00 CHF (7.50 dès 3) |

### Farines — 5 kg
| Name | Bexio code | Price |
|---|---|---|
| Mix Pizza | `MIX-PIZ-5KG` | 35.00 CHF |
| Mix Pain | `MIX-PAI-5KG` | 35.00 CHF |
| Mix Pasta | `MIX-PAT-5KG` | 35.00 CHF |

### Pack Découverte — 4 kg — 37.00 CHF
- Contents: Spaghetti + Pappardelle + Busiata + Penne Rigate (4×500g) + 2 Mix Farine au choix
- Customer selects 2 of 3 mix farines (max 2 enforced with `limitPackMix()`)
- Retail value: 4×7.50 + 2×9.00 = 48.00 CHF → discount of 11.00 CHF (−22.9%)
- Bexio invoice: 4 individual pâte lines + 2 farine lines + 1 discount line (`−22.9%`)

---

## Form sections (in order)

1. **Tes coordonnées** — Prénom*, Nom*, Adresse*, NPA*, Ville*, Email*, Téléphone*
2. **Mode de réception** — radio: Retrait La Neuveville / Livraison NE-Bienne / Autre (inline text)
3. **Pourquoi achètes-tu...** (optionnel) — 5 motivation checkboxes
4. Newsletter consent checkbox (required to unlock send buttons)

All fields marked `*` are required. Both send buttons disabled until: cart non-empty + all required fields filled + valid email + newsletter checkbox checked.

---

## Automation (Make.com → Bexio)

### Webhook
```
POST https://hook.eu1.make.com/vwtp69y3ro5wdjckslmsjs9h1a39scjy
```

### Payload sent on every order
```json
{
  "canal": "whatsapp|email",
  "total": 37.00,
  "lignes": ["Pack Découverte x1 — farines : Mix Pizza + Mix Pain = 37.00 CHF"],
  "lignesDetails": [
    { "type": "article", "codeBexio": "PAST-SPA-500", "nom": "Spaghetti 500 g", "quantite": 1, "prixUnitaire": 7.50, "sousTotal": 7.50 },
    { "type": "discount", "nom": "Remise Pack Découverte (-22.9%)", "montant": 11.00, "pourcentage": 22.92 }
  ],
  "client": { "prenom": "", "nom": "", "adresse": "", "npa": "", "ville": "", "email": "", "tel": "" },
  "livraison": "Retrait — La Neuveville",
  "motivations": []
}
```

- `lignes` → human-readable strings, used for WhatsApp/email message body
- `lignesDetails` → structured data for Bexio invoice positions (one object per product line)

### Make.com flow (target architecture)
1. Webhook receives order
2. Search Bexio contact by email → Router: use existing ID or create new contact
3. Create Invoice (empty, linked to contact)
4. Array Iterator on `lignesDetails`
5. Router: `type = article` → Bexio API call `POST /kb_invoice/{id}/kb_position_article` / `type = discount` → `POST /kb_invoice/{id}/kb_position_discount`

### Bexio API position endpoints
- Article: `POST /2.0/kb_invoice/{id}/kb_position_article` — body: `{ "amount": "1", "unit_price": "7.50", "text": "Spaghetti 500 g" }`
- Discount: `POST /2.0/kb_invoice/{id}/kb_position_discount` — body: `{ "value": "22.92", "is_percentual": 1, "text": "Remise Pack Découverte (-22.9%)" }`

---

## Contact info
- WhatsApp: +41 79 946 88 10
- Email: jack.genna@gmail.com
