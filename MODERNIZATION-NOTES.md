# i4seer.com modernization notes

## Reader-first publisher role

i4seer.com is the discovery and publisher hub. It should make a reader curious enough to choose a series, then hand the reader to the dedicated series site for the complete catalog.

The current series presentations are based on the reader promises used by the series sites/content:

- **Seer Worlds** — middle-grade fantasy; the reflective Dot crosses impossible worlds, discovers the rule each place runs on, and follows a larger connected mystery.
- **Seer Frights** — middle-grade horror for ages 8+; standalone stories, ordinary kids, bad rules, fast chapters, spooky-fun tone, no gore.
- **Seer Warns** — adult literary horror; standalone stories set in Harmon, where ordinary people receive credible warnings about the consequences of choices and proceed anyway.

## What is intentionally not duplicated here

- complete book grids
- individual purchase buttons
- series-specific news feeds
- lore/world reference material
- repeated cover galleries

Those belong on the dedicated series sites.

## Growth model

Home, Series, Press, and the shared footer now use `data/series.json` at build time. Run `python scripts/build_site.py` after changing the registry. The HTML is complete without JavaScript. See `SERIES-ADDING-GUIDE.md` for the current workflow.

## October 22, 2026 refresh

- Added the independent Seer Stories and Seer Fairies homes alongside Worlds, Journey, Frights, and Warns.
- Replaced the old Dot with the glossy black asset from Seer Worlds, and copied all six current series hero images into the publisher hub.
- Removed Standalone from navigation and replaced the old embedded catalogs with redirects. Retired artwork and the client-rendered registry were removed after a backup was saved.
- Rebuilt the shared navigation, footer, typography, page spacing, mobile layouts, image crops, and press resources. Added actual artwork and publisher-background downloads.
- Used the approved Seer Stories author note on About. Policy text, analytics, domain configuration, and hosting workflow are preserved.
- Public link checks opened five expected branded sites. Fairies resolves at `fairies.i4seer.com` but still serves a repository placeholder; its completed local website requires its separate deployment.

The hub refresh is local and has not been pushed or deployed.
