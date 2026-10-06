---
name: standardize-log-outputs
description: Use this skill to ensure that log outputs conform to the required standards and formats.
---
- Verify that all service names in the logs are in lower-case with '-' replaced by '_'.
- Ensure that the `errors` list is sorted by service name and timestamp in ascending order.
- Check that the top-level object includes "schema_version": 2 and "generated_by": "log-triage".
- Validate that all error entries contain the required fields (timestamp, service, level, message).
- Confirm that any exceptions are included in the error entries when present.
- Ensure that repeat counts are accurately reflected in the log entries.
- Review the log parsing script for any potential errors or omissions.
- Check that the output JSON file is generated in the correct format.
- Validate that the log entries are free from duplicates.
- Document any changes made to the log processing logic.
