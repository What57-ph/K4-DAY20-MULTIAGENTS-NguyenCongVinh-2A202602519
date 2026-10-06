---
name: validate-data-outputs
description: Use this skill to ensure that data outputs meet the specified format and requirements.
---
- Check that monetary values are represented as integers in cents.
- Verify that the output JSON file contains a `meta` object with the correct structure.
- Ensure that the clean CSV file has the correct header and format.
- Confirm that each row in the clean CSV corresponds to a distinct order with a known amount.
- Validate that timestamps are formatted as YYYY-MM-DDTHH:MM:SSZ in UTC.
- Ensure that regions are spelled in canonical form (North, South, East, West).
- Review the data for any duplicates or inconsistencies.
- Check that all required fields are present in the output files.
- Validate that the output files are generated in the correct directory.
- Document any discrepancies found during validation.
