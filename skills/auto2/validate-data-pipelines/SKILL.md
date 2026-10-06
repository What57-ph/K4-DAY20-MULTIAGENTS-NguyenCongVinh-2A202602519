---
name: validate-data-pipelines
description: Use when transforming tabular data or logs into structured summaries and output files.
---
- Read the output schema and transformation rules before processing records.
- Preserve source row counts separately from deduplicated record counts.
- Define deduplication keys and missing-value handling explicitly.
- Normalize timestamps to UTC and categorical values to the required canonical form.
- Represent monetary values in the required exact unit; avoid floating-point arithmetic.
- Apply all filters before aggregating, and verify boundaries use the required timezone.
- Sort output records by every specified key.
- Recompute summary counts from the final output and assert they agree.
- Validate required metadata, field names, value types, and output formatting.
- Use short scripts or structured parsing for inspection; avoid fragile shell quoting.
=== END===
