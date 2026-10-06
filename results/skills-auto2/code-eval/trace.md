### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: ls
{"path": "skills"}

### Tool result
['/skills/configure-and-validate-tests/', '/skills/preserve-tests-and-log-fixes/', '/skills/validate-data-pipelines/']

### Tool call: read_file
{"file_path": "skills/configure-and-validate-tests/SKILL.md", "limit": 1000}

### Tool result
@@ lines 1-9 of 9 @@
---
name: configure-and-validate-tests
description: Use when test discovery or imports fail because the working directory, environment, or plugins are misconfigured.
---
- Confirm the repository root and test-directory paths before invoking the test runner.
- Check package import paths and set the project path explicitly when needed.
- Disable third-party plugin autoload only when plugin startup causes failures.
- Distinguish collection or environment errors from actual test failures.
- Rerun the intended suite after correcting invocation settings.

### Tool call: read_file
{"file_path": "skills/preserve-tests-and-log-fixes/SKILL.md", "limit": 1000}

### Tool result
@@ lines 1-8 of 8 @@
---
name: preserve-tests-and-log-fixes
description: Use when modifying a codebase with existing tests and a required changelog convention.
---
- Inspect repository instructions and changelog format before editing.
- Treat existing test files as read-only; add new tests separately when needed.
- Record every fix under the required changelog heading and bullet format.
- Run the relevant tests after implementation and report the result.

### Tool call: read_file
{"file_path": "skills/validate-data-pipelines/SKILL.md", "limit": 1000}

### Tool result
@@ lines 1-15 of 15 @@
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

### Tool call: ls
{"path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool call: ls
{"path": "workspace/bookings"}

### Tool result
['/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py']

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/README.md", "limit": 1000}

### Tool call: ls
{"path": "workspace/tests"}

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/bookings/calendar_export.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/bookings/__init__.py", "limit": 1000}

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
['/workspace/tests/__pycache__/', '/workspace/tests/test_bookings.py']

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

### Tool result
@@ lines 1-1 of 1 @@
__version__ = "1.4.2"

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

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q", "timeout": 120000}

### Tool result
Error: timeout 120000s exceeds maximum allowed (3600s).

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q", "timeout": 3600}

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

### Tool call: edit_file
{"file_path": "workspace/bookings/billing.py", "old_string": "    return round(minutes / block)\n", "new_string": "    if minutes < 0:\n        raise ValueError(\"minutes must be >= 0\")\n    if block <= 0:\n        raise ValueError(\"block must be > 0\")\n    return (minutes + block - 1) // block\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/billing.py'

### Tool call: edit_file
{"file_path": "workspace/bookings/schedule.py", "old_string": "def add_slot(slot, slots=[]):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    slots.append(slot)\n    return slots\n", "new_string": "def add_slot(slot, slots=None):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    result = [] if slots is None else list(slots)\n    result.append(slot)\n    return result\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/schedule.py'

### Tool call: write_file
{"file_path": "workspace/bookings/timeutil.py", "content": "\"\"\"Time helpers for the bookings package.\"\"\"\nimport re\n\n\n_DURATION_RE = re.compile(r\"(?:(\\d+)h)?(?:(\\d+)m)?\\Z\")\n_CLOCK_RE = re.compile(r\"(\\d+):(\\d+)\\Z\")\n_INTEGER_RE = re.compile(r\"\\d+\\Z\")\n\n\ndef parse_duration(text):\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    if not isinstance(text, str):\n        raise ValueError(f\"bad duration: {text!r}\")\n\n    value = text.strip()\n    match = _DURATION_RE.fullmatch(value)\n    if match and any(part is not None for part in match.groups()):\n        hours = int(match.group(1) or 0)\n        minutes = int(match.group(2) or 0)\n        return hours * 60 + minutes\n\n    match = _CLOCK_RE.fullmatch(value)\n    if match:\n        return int(match.group(1)) * 60 + int(match.group(2))\n\n    if _INTEGER_RE.fullmatch(value):\n        return int(value)\n\n    raise ValueError(f\"bad duration: {text!r}\")\n"}

### Tool result
Updated file /workspace/bookings/timeutil.py

### Tool call: edit_file
{"file_path": "workspace/CHANGELOG.md", "old_string": "## Unreleased\n", "new_string": "## Unreleased\n- Corrected duration parsing, billable-block rounding and validation, and slot list isolation.\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/CHANGELOG.md'

### Tool call: execute
{"command": "cd workspace && set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 && python -m pytest tests -q", "timeout": 3600}

### Tool result
...                                                                      [100%]
3 passed in 0.04s

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && python -c \"from bookings.timeutil import parse_duration; from bookings.billing import billable_blocks; from bookings.schedule import add_slot; assert [parse_duration(x) for x in ('1h30m','2h','45m','1:30','45',' 1h ')] == [90,120,45,90,45,60]; assert billable_blocks(16)==2 and billable_blocks(0)==0; a=add_slot('a'); b=add_slot('b'); assert (a,b)==(['a'],['b']); assert add_slot('x',['y'])==['y','x']; print('edge checks passed')\""}

### Tool result
edge checks passed

[Command succeeded with exit code 0]

### Assistant
Updated `bookings/billing.py`, `bookings/schedule.py`, and `bookings/timeutil.py` to match their docstrings, including rounding up, rejecting negative minutes, isolating slot lists, and supporting all documented duration formats. Recorded the fixes in `CHANGELOG.md`.

The test suite passed: **3 passed**.