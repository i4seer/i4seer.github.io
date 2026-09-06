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

Home, Series, and Press use `/data/series.js`. Adding a future series means adding one wide visual and one registry entry; the page structures do not need to change.
