# Maintaining the Seer Press collections

Home, Series, Press, and the shared footer are generated from `data/series.json`.

1. Copy the current wide hero from the collection’s website into `images/series/`, using a fresh descriptive filename.
2. Add or edit a registry object. Follow the existing fields: slug, name, category, audience, tagline, description, readerHook, highlights, image, alt, width, height, website, cta, host, and press anchor.
3. Verify the official HTTPS domain against that project’s CNAME and live page. Use the configured subdomain when appropriate; Journey is `journey.i4seer.com`, Stories is `stories.i4seer.com`, and Fairies is `fairies.i4seer.com`.
4. Record the source artwork and SHA-256 in `docs/artwork-sources.json` and update `docs/link-verification.json` after live checks.
5. Run `python scripts/build_site.py`, then `python scripts/verify_site.py`. The verifier currently expects six collections; deliberately update its expected set when adding another collection.
6. Preview desktop and phone layouts. Check the artwork download, image crops, and external destination.

The publisher hub introduces collections. Full book catalogs, covers, edition URLs, publication news, and lore belong on their independent sites. Seer Stories now carries the former Standalone shelf. Keep the old bookmark redirects in the builder when maintaining the hub.
