---
name: enforce-test-standards
description: Use this skill to ensure that all tests adhere to the required standards and guidelines.
---
- Verify that no original test files in the tests/ directory have been modified.
- Ensure that new test files are created for any new tests.
- Check that all public functions have type annotations for parameters and return values.
- Confirm that regression tests are added in a dedicated test file for each bug fixed.
- Validate that the regression test file passes all tests.
- Record all fixes in the CHANGELOG.md under '## Unreleased'.
- Ensure that each fix entry in the CHANGELOG.md follows the specified format.
- Review the test suite for any missing or incomplete test cases.
- Ensure that all tests are executed successfully before finalizing changes.
- Document any changes made to the test structure or content.
