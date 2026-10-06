---
name: structured-log-triage
description: Use when parsing application logs into a structured error report with normalized fields and aggregates.
---
- Parse entries while preserving their timestamps, service names, severity, messages, and repeat counts.
- Associate continuation or traceback lines with the correct preceding entry and extract exception details consistently.
- Normalize service names to the required lowercase separator convention.
- Filter to the requested severity levels and compute aggregates from the same retained entries.
- Sort errors by the specified fields and ascending order before serialization.
- Include all required top-level schema and generator metadata.
- Validate the serialized output against the requested schema and ordering rules.
