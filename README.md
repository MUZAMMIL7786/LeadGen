# wakilz — AI Sales Qualification & Lead Generation

> **Enterprise-grade conversational AI** that qualifies leads, books meetings, and automates your B2B sales pipeline — 24/7.

[![Live Site](https://img.shields.io/badge/Live%20Site-wakilz-22c55e?style=flat-square)](https://wakilz.com)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

---

## Overview

This repository contains the source code for the **wakilz** B2B SaaS landing page — a high-conversion page showcasing AI-powered lead qualification and sales automation services.

### Key Features
- 🤖 **Animated AI chat demo** — live conversation simulation in the hero section
- 🔗 **18 native integrations** — arc diagram with popup modal (HubSpot, Salesforce, Slack, Zapier, and more)
- 🌙 **Dark / Light mode** — persisted via `localStorage`
- 📱 **Fully responsive** — mobile-first layout
- ⚡ **Zero dependencies** — pure HTML, CSS & vanilla JS

---

## Project Structure

```
wakilz-leadgen/
├── assets/
│   ├── icons/
│   │   └── integrations/       # SVG brand icons for all 18 integrations
│   ├── images/                 # Photos & raster assets
│   └── fonts/                  # Local web fonts (if any)
├── scripts/                    # Dev & maintenance scripts (PowerShell)
│   ├── download_svgs.ps1       # Downloads SVG icons from Simple Icons CDN
│   ├── download_missing.ps1    # Fallback for icons not found on CDN
│   ├── update_paths.ps1        # Updates asset paths after restructuring
│   └── restructure.ps1         # One-time folder restructure script
├── .gitignore
├── CNAME                       # GitHub Pages custom domain
├── index.html                  # Main (and only) page — all CSS & JS inline
├── README.md
└── sitemap.xml                 # SEO sitemap
```

---

## Integrations Supported

| CRM & Sales | Messaging | Automation | Support & More |
|---|---|---|---|
| HubSpot | Slack | Zapier | Zendesk |
| Salesforce | Microsoft Teams | Make | Calendly |
| Pipedrive | WhatsApp | Airtable | Intercom |
| | Twilio | | Mailchimp |
| | | | ActiveCampaign |
| | | | Notion / Stripe |

---

## Getting Started

This is a **static site** — no build step required.

```bash
# Clone the repo
git clone https://github.com/your-username/LeadGen.git
cd LeadGen

# Open locally (any method)
start index.html          # Windows
open index.html           # macOS
```

Or serve with any static file server:

```bash
npx serve .
# → http://localhost:3000
```

---

## Deployment

The site is deployed via **GitHub Pages** with a custom domain configured in `CNAME`.

```bash
git add .
git commit -m "feat: update landing page"
git push origin main
# → Auto-deploys via GitHub Pages
```

---

## Scripts

All maintenance scripts are in `scripts/` and require PowerShell:

| Script | Purpose |
|---|---|
| `download_svgs.ps1` | Batch-downloads SVG icons from Simple Icons CDN |
| `download_missing.ps1` | Creates fallback SVGs for icons not available on CDN |
| `update_paths.ps1` | Updates all asset `src` paths in `index.html` |
| `restructure.ps1` | One-time script used to create the current folder layout |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Markup | Semantic HTML5 |
| Styling | Vanilla CSS (custom properties, CSS Grid, Flexbox) |
| Scripting | Vanilla JavaScript (ES6+) |
| Fonts | Inter — Google Fonts |
| Icons | Simple Icons (SVG) |
| Hosting | GitHub Pages |
| Chat Widget | Voiceflow |

---

## License

MIT © wakilz. See [LICENSE](LICENSE) for details.