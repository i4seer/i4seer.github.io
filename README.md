# i4Seer · Seer Press

The publisher hub at `www.i4seer.com`. Each of the six collections has its own independent website. This repository introduces the collections, author, and press resources; book catalogs and edition links live on the collection sites.

Run `python scripts/build_site.py` to regenerate the HTML, sitemap, press background text, and legacy redirects. Run `python scripts/verify_site.py` to validate the generated output. No third-party Python packages are needed for these commands. Preview locally with `python -m http.server 8773` from this folder.

The site is static and already includes its generated pages. The retained GitHub Pages workflow publishes the repository root when changes are pushed to `main`. This refresh did not push or deploy changes.

## Main files

- `data/series.json`: names, summaries, images, audience labels, reading-order notes, and official websites.
- `data/legal-pages.json`: preserved policy page content. Changes to policy wording require a separate deliberate content review.
- `scripts/build_site.py`: shared page templates and editorial copy.
- `style.css`, `site.js`: responsive theme and mobile navigation. All series content works without JavaScript.
- `docs/artwork-sources.json`: exact current hero sources and asset hashes.
- `docs/link-verification.json`: checked domains and the Fairies live-site caveat.

The glossy black Dot is copied directly from the current Seer Worlds site. Series images are copied from the latest local series homepages, with content hashes on rendered asset URLs. Fonts are local EB Garamond files supplied with the book projects. Existing Plausible analytics, CNAME, hosting workflow, favicon, and security headers are retained.

Retired `/standalone/` and `/series/seer-fairies/` pages now redirect to Stories and Fairies. `/books/` continues to redirect to the collection directory. HTML redirects work on GitHub Pages; 301 rules are also retained in the Azure static hosting configuration. Redirect routes are excluded from the sitemap.

Verified October 22, 2026: Stories, Journey, Worlds, Frights, and Warns open the expected public sites. `fairies.i4seer.com` resolves but still serves a repository placeholder; the finished `C:/SEERFAIRIES_WEB` site needs its separate deployment.
