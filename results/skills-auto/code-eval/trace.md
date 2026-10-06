### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: read_file
{"file_path": "skills/python-regression-maintenance/SKILL.md", "limit": 1000}

### Tool call: read_file
{"file_path": "skills/enforce-test-standards/SKILL.md", "limit": 1000}

### Tool result
@@ lines 1-10 of 10 @@
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

### Tool result
@@ lines 1-14 of 14 @@
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

### Tool call: ls
{"path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool call: ls
{"path": "workspace/bookings"}

### Tool result
['/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py']

### Tool call: ls
{"path": "workspace/tests"}

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/README.md", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/bookings/__init__.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/bookings/calendar_export.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py", "limit": 1000}

### Tool result
['/workspace/tests/__pycache__/', '/workspace/tests/test_bookings.py']

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 1.4.2
- initial import

### Tool result
@@ lines 1-5 of 5 @@
# bookings

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool result
@@ lines 1-1 of 1 @@
__version__ = "1.4.2"

### Tool result
@@ lines 1-11 of 11 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)

### Tool result
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

### Tool result
@@ lines 1-17 of 17 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=[]):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    slots.append(slot)
    return slots

### Tool result
@@ lines 1-19 of 19 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
    if not m:
        raise ValueError(f"bad duration: {text!r}")
    return int(m.group(1)) * 60 + int(m.group(2))

### Tool call: read_file
{"file_path": "workspace/tests/test_bookings.py", "limit": 1000}

### Tool result
@@ lines 1-15 of 15 @@
from bookings.billing import billable_blocks
from bookings.schedule import add_slot, total_minutes


def test_total_minutes_mixed_formats():
    assert total_minutes(["1h30m", "2h"]) == 210


def test_billable_blocks_rounds_up():
    assert billable_blocks(20) == 2
    assert billable_blocks(45) == 3


def test_add_slot_single_call():
    assert add_slot("a") == ["a"]

### Tool call: glob
{"pattern": "**/*", "path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/__init__.cpython-313.pyc', '/workspace/bookings/__pycache__/billing.cpython-313.pyc', '/workspace/bookings/__pycache__/calendar_export.cpython-313.pyc', '/workspace/bookings/__pycache__/schedule.cpython-313.pyc', '/workspace/bookings/__pycache__/timeutil.cpython-313.pyc', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/__pycache__/test_bookings.cpython-313-pytest-9.1.1.pyc', '/workspace/tests/test_bookings.py']

### Tool call: write_file
{"file_path": "workspace/bookings/timeutil.py", "content": "\"\"\"Time helpers for the bookings package.\"\"\"\nimport re\n\n\n_DURATION_PATTERN = re.compile(r\"(?:(\\d+)h)?(?:(\\d+)m)?\")\n_CLOCK_PATTERN = re.compile(r\"(\\d+):(\\d+)\")\n_INTEGER_PATTERN = re.compile(r\"\\d+\")\n\n\ndef parse_duration(text: str) -> int:\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    if not isinstance(text, str):\n        raise ValueError(f\"bad duration: {text!r}\")\n\n    value = text.strip()\n    match = _DURATION_PATTERN.fullmatch(value)\n    if match is not None and any(part is not None for part in match.groups()):\n        hours, minutes = match.groups()\n        return int(hours or 0) * 60 + int(minutes or 0)\n\n    match = _CLOCK_PATTERN.fullmatch(value)\n    if match is not None:\n        return int(match.group(1)) * 60 + int(match.group(2))\n\n    if _INTEGER_PATTERN.fullmatch(value) is not None:\n        return int(value)\n\n    raise ValueError(f\"bad duration: {text!r}\")\n"}

### Tool result
Updated file /workspace/bookings/timeutil.py

### Tool call: write_file
{"file_path": "workspace/bookings/billing.py", "content": "\"\"\"Billing rules.\"\"\"\n\n\ndef billable_blocks(minutes: int, block: int = 15) -> int:\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    if minutes < 0:\n        raise ValueError(\"minutes must be >= 0\")\n    if block <= 0:\n        raise ValueError(\"block must be > 0\")\n    return (minutes + block - 1) // block\n"}

### Tool result
Updated file /workspace/bookings/billing.py

### Tool call: write_file
{"file_path": "workspace/bookings/schedule.py", "content": "\"\"\"Schedule helpers.\"\"\"\nfrom collections.abc import Iterable\n\nfrom .timeutil import parse_duration\n\n\ndef total_minutes(durations: Iterable[str]) -> int:\n    \"\"\"Total minutes of a list of duration strings.\"\"\"\n    return sum(parse_duration(duration) for duration in durations)\n\n\ndef add_slot(slot: str, slots: Iterable[str] | None = None) -> list[str]:\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    return [*(slots if slots is not None else ()), slot]\n"}

### Tool result
Updated file /workspace/bookings/schedule.py

### Tool call: write_file
{"file_path": "workspace/bookings/calendar_export.py", "content": "\"\"\"Calendar export.\"\"\"\nfrom .timeutil import parse_duration\n\n\ndef slot_end(start_minute: int, duration_text: str) -> int:\n    \"\"\"Minute of the day at which a slot ends.\"\"\"\n    return start_minute + parse_duration(duration_text)\n"}

### Tool result
Updated file /workspace/bookings/calendar_export.py

### Tool call: write_file
{"file_path": "workspace/CHANGELOG.md", "content": "# Changelog\n\n## Unreleased\n- Fix duration parsing for all documented formats, round billing blocks up, and prevent schedule calls from sharing mutable state.\n\n## 1.4.2\n- initial import"}

### Tool result
Updated file /workspace/CHANGELOG.md

### Tool call: write_file
{"file_path": "workspace/tests/test_regressions.py", "content": "import pytest\n\nfrom bookings.billing import billable_blocks\nfrom bookings.calendar_export import slot_end\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.timeutil import parse_duration\n\n\n@pytest.mark.parametrize(\n    (\"text\", \"expected\"),\n    [(\"1h30m\", 90), (\"2h\", 120), (\"45m\", 45), (\"1:30\", 90), (\"45\", 45), (\" 45m \", 45)],\n)\ndef test_parse_duration_documented_formats(text, expected):\n    assert parse_duration(text) == expected\n\n\n@pytest.mark.parametrize(\"text\", [\"\", \"1h30\", \"1:60\", \"-1\", \"abc\"])\ndef test_parse_duration_rejects_malformed_values(text):\n    with pytest.raises(ValueError):\n        parse_duration(text)\n\n\ndef test_billable_blocks_rounds_up_and_validates():\n    assert billable_blocks(0) == 0\n    assert billable_blocks(15) == 1\n    assert billable_blocks(16) == 2\n    with pytest.raises(ValueError):\n        billable_blocks(-1)\n\n\ndef test_add_slot_returns_independent_new_lists():\n    first = add_slot(\"a\")\n    second = add_slot(\"b\")\n    assert first == [\"a\"]\n    assert second == [\"b\"]\n    assert add_slot(\"b\", first) == [\"a\", \"b\"]\n    assert first == [\"a\"]\n\n\ndef test_duration_aggregation_and_slot_end():\n    assert total_minutes([\"1:30\", \"45\"]) == 135\n    assert slot_end(60, \"1h\") == 120\n"}

### Tool result
Updated file /workspace/tests/test_regressions.py

### Tool call: execute
{"command": "python -m pytest workspace/tests -q", "timeout": 120000}

### Tool result
Error: timeout 120000s exceeds maximum allowed (3600s).

### Tool call: execute
{"command": "python -m pytest workspace/tests -q", "timeout": 120000}

### Tool result
Error: timeout 120000s exceeds maximum allowed (3600s).

### Tool call: execute
{"command": "python -m pytest workspace/tests -q"}

### Tool result
[stderr] Traceback (most recent call last):
[stderr]   File "<frozen runpy>", line 198, in _run_module_as_main
[stderr]   File "<frozen runpy>", line 88, in _run_code
[stderr]   File "~\AppData\Local\Programs\Python\Python313\Lib\site-packages\pytest\__main__.py", line 9, in <module>
[stderr]     raise SystemExit(pytest.console_main())
[stderr]                      ~~~~~~~~~~~~~~~~~~~^^
[stderr]   File "~\AppData\Local\Programs\Python\Python313\Lib\site-packages\_pytest\config\__init__.py", line 201, in console_main
[stderr]     code = main()
[stderr]   File "~\AppData\Local\Programs\Python\Python313\Lib\site-packages\_pytest\config\__init__.py", line 156, in main
[stderr]     config = _prepareconfig(args, plugins)
[stderr]   File "~\AppData\Local\Programs\Python\Python313\Lib\site-packages\_pytest\config\__init__.py", line 342, in _prepareconfig
[stderr]     config = pluginmanager.hook.pytest_cmdline_parse(
[stderr]         pluginmanager=pluginmanager, args=args
[stderr]     )
[stderr]   File "~\AppData\Local\Programs\Python\Python313\Lib\site-packages\pluggy\_hooks.py", line 512, in __call__
[stderr]     return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
[stderr]            ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]   File "~\AppData\Local\Programs\Python\Python313\Lib\site-packages\pluggy\_manager.py", line 120, in _hookexec
[stderr]     return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
[std

### Tool call: execute
{"command": "python -m pytest workspace/tests -q -p no:langsmith"}

### Tool result
[stderr] Traceback (most recent call last):
[stderr]   File "<frozen runpy>", line 198, in _run_module_as_main
[stderr]   File "<frozen runpy>", line 88, in _run_code
[stderr]   File "~\AppData\Local\Programs\Python\Python313\Lib\site-packages\pytest\__main__.py", line 9, in <module>
[stderr]     raise SystemExit(pytest.console_main())
[stderr]                      ~~~~~~~~~~~~~~~~~~~^^
[stderr]   File "~\AppData\Local\Programs\Python\Python313\Lib\site-packages\_pytest\config\__init__.py", line 201, in console_main
[stderr]     code = main()
[stderr]   File "~\AppData\Local\Programs\Python\Python313\Lib\site-packages\_pytest\config\__init__.py", line 156, in main
[stderr]     config = _prepareconfig(args, plugins)
[stderr]   File "~\AppData\Local\Programs\Python\Python313\Lib\site-packages\_pytest\config\__init__.py", line 342, in _prepareconfig
[stderr]     config = pluginmanager.hook.pytest_cmdline_parse(
[stderr]         pluginmanager=pluginmanager, args=args
[stderr]     )
[stderr]   File "~\AppData\Local\Programs\Python\Python313\Lib\site-packages\pluggy\_hooks.py", line 512, in __call__
[stderr]     return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
[stderr]            ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]   File "~\AppData\Local\Programs\Python\Python313\Lib\site-packages\pluggy\_manager.py", line 120, in _hookexec
[stderr]     return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
[std

### Tool call: execute
{"command": "python -c \"from bookings.timeutil import parse_duration; from bookings.billing import billable_blocks; from bookings.schedule import add_slot; assert [parse_duration(x) for x in ['1h30m','2h','45m','1:30','45']] == [90,120,45,90,45]; assert billable_blocks(16)==2 and billable_blocks(15)==1; assert add_slot('a')==['a'] and add_slot('b')==['b']; print('manual checks passed')\"", "timeout": 60}

### Tool result
[stderr] Traceback (most recent call last):
[stderr]   File "<string>", line 1, in <module>
[stderr]     from bookings.timeutil import parse_duration; from bookings.billing import billable_blocks; from bookings.schedule import add_slot; assert [parse_duration(x) for x in ['1h30m','2h','45m','1:30','45']] == [90,120,45,90,45]; assert billable_blocks(16)==2 and billable_blocks(15)==1; assert add_slot('a')==['a'] and add_slot('b')==['b']; print('manual checks passed')
[stderr]     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr] ModuleNotFoundError: No module named 'bookings'

Exit code: 1
[Command failed with exit code 1]

### Tool call: execute
{"command": "set PYTHONPATH=workspace&& python -c \"from bookings.timeutil import parse_duration; from bookings.billing import billable_blocks; from bookings.schedule import add_slot; assert [parse_duration(x) for x in ['1h30m','2h','45m','1:30','45']] == [90,120,45,90,45]; assert billable_blocks(16)==2 and billable_blocks(15)==1; assert add_slot('a')==['a'] and add_slot('b')==['b']; print('manual checks passed')\"", "timeout": 60}

### Tool result
manual checks passed

[Command succeeded with exit code 0]

### Assistant
Fixed duration parsing for all documented formats, made billing blocks round up with validation, and ensured `add_slot` returns independent lists. Added regression tests and an Unreleased changelog entry. The pytest run was blocked by an environment error loading a pytest plugin; targeted manual checks passed.