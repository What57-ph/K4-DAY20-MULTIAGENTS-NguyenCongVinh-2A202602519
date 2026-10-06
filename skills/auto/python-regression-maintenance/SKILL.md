---
name: python-regression-maintenance
description: Use when fixing bugs in a Python package that must satisfy repository rules and preserve existing tests.
---
- Inspect the package, public APIs, existing tests, and project-specific conventions before editing.
- Leave original test files unchanged; add new tests when needed.
- Add type annotations to every parameter and return value of each public function.
- Add a focused regression test for every bug fixed, covering expected behavior and relevant edge cases.
- Record each fix under the changelog’s unreleased heading using the required bullet format.
- Run the full test suite and verify the new tests and changelog entries are present.
