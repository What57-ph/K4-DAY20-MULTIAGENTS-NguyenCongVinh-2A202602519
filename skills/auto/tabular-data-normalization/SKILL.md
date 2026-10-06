---
name: tabular-data-normalization
description: Use when analyzing messy tabular data and producing normalized summaries or cleaned datasets.
---
- Inspect the input schema and count all data rows before filtering or deduplicating.
- Identify duplicates by the appropriate entity key and retain one record per distinct entity according to a consistent rule.
- Exclude records with unknown amounts where required, and distinguish input row counts from usable entity counts.
- Parse timestamps carefully, resolve time zones, and emit the required UTC representation.
- Normalize categorical values to the specified canonical spellings.
- Convert monetary values to integer minor units using decimal-safe arithmetic rather than binary floating point.
- Include required provenance and row-count metadata in the summary.
- Validate output schemas, row counts, formats, and monetary types before finishing.
