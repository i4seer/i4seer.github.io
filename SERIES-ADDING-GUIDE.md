# Adding a New Series to i4seer.com

The public Home, Series, and Press series presentations are generated from one registry:

`/data/series.js`

To add a series:

1. Add one wide series image under `/images/series/` (roughly 16:9 to 2:1 works well).
2. Add one object to `window.SEER_SERIES` in `/data/series.js` with:
   - `slug`
   - `name`
   - `category`
   - `audience`
   - `tagline`
   - `description`
   - `readerHook`
   - `highlights` (four short reader-facing promises)
   - `image`
   - `website`
   - `cta`
   - optional `press` anchor
3. If editorial cover downloads should be hosted on i4seer.com, add a compact `<details>` block to `/press/index.html`. Do not add cover grids to Home or Series.
4. The top navigation and footer do not need to change.

## Site ownership model

- **i4seer.com**: publisher identity, compelling series discovery, author/company information, press resources.
- **Dedicated series sites**: complete book catalog, covers, purchase links, series news, lore, and reader content.

The reader-facing series blocks are intentionally data-driven, so additional series flow into the same layouts without a redesign.
