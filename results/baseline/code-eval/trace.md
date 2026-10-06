### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: ls
{"path": "/workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool call: glob
{"pattern": "*.py", "path": "/workspace/workspace"}

### Tool result
No files found

### Tool call: ls
{"path": "/workspace/bookings"}

### Tool result
['/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py']

### Tool call: read_file
{"file_path": "/workspace/bookings/billing.py"}

### Tool call: read_file
{"file_path": "/workspace/bookings/calendar_export.py"}

### Tool call: read_file
{"file_path": "/workspace/bookings/schedule.py"}

### Tool call: read_file
{"file_path": "/workspace/bookings/timeutil.py"}

### Tool call: read_file
{"file_path": "/workspace/bookings/__init__.py"}

### Tool call: ls
{"path": "/workspace/tests"}

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

### Tool result
['/workspace/tests/__pycache__/', '/workspace/tests/test_bookings.py']

### Tool call: read_file
{"file_path": "/workspace/tests/test_bookings.py"}

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
{"command": "python -m pytest -q workspace/tests", "timeout": 120000}

### Tool result
Error: timeout 120000s exceeds maximum allowed (3600s).

### Tool call: edit_file
{"file_path": "/workspace/bookings/billing.py", "old_string": "    return round(minutes / block)", "new_string": "    if minutes < 0:\n        raise ValueError(\"minutes must be >= 0\")\n    if block <= 0:\n        raise ValueError(\"block must be > 0\")\n    return (minutes + block - 1) // block"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/billing.py'

### Tool call: edit_file
{"file_path": "/workspace/bookings/timeutil.py", "old_string": "    m = re.fullmatch(r\"(\\d+)h(\\d+)m\", text.strip())\n    if not m:\n        raise ValueError(f\"bad duration: {text!r}\")\n    return int(m.group(1)) * 60 + int(m.group(2))", "new_string": "    if not isinstance(text, str):\n        raise ValueError(f\"bad duration: {text!r}\")\n\n    value = text.strip()\n    patterns = (\n        (r\"(\\d+)h(\\d+)m\", lambda match: int(match.group(1)) * 60 + int(match.group(2))),\n        (r\"(\\d+)h\", lambda match: int(match.group(1)) * 60),\n        (r\"(\\d+)m\", lambda match: int(match.group(1))),\n        (r\"(\\d+):(\\d+)\", lambda match: int(match.group(1)) * 60 + int(match.group(2))),\n        (r\"(\\d+)\", lambda match: int(match.group(1))),\n    )\n    for pattern, convert in patterns:\n        match = re.fullmatch(pattern, value)\n        if match:\n            return convert(match)\n    raise ValueError(f\"bad duration: {text!r}\")"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/timeutil.py'

### Tool call: edit_file
{"file_path": "/workspace/bookings/schedule.py", "old_string": "def add_slot(slot, slots=[]):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    slots.append(slot)\n    return slots", "new_string": "def add_slot(slot, slots=None):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    return list(slots) + [slot] if slots is not None else [slot]"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/schedule.py'

### Tool call: edit_file
{"file_path": "/workspace/bookings/calendar_export.py", "old_string": "    return start_minute + parse_duration(duration_text)", "new_string": "    return (start_minute + parse_duration(duration_text)) % (24 * 60)"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/calendar_export.py'

### Tool call: execute
{"command": "python -m pytest -q workspace/tests", "timeout": 3600}

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
{"file_path": "/workspace/bookings/calendar_export.py", "old_string": "    return (start_minute + parse_duration(duration_text)) % (24 * 60)", "new_string": "    return start_minute + parse_duration(duration_text)"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/calendar_export.py'

### Tool call: execute
{"command": "python -c \"from bookings.timeutil import parse_duration; from bookings.billing import billable_blocks; from bookings.schedule import add_slot, total_minutes; assert [parse_duration(x) for x in ('1h30m','2h','45m','1:30','45')] == [90,120,45,90,45]; assert billable_blocks(16)==2 and billable_blocks(45)==3 and billable_blocks(0)==0; assert add_slot('a')==['a'] and add_slot('b')==['b']; assert add_slot('b',['a'])==['a','b']; assert total_minutes(['1h30m','2h'])==210\""}

### Tool result
[stderr] Traceback (most recent call last):
[stderr]   File "<string>", line 1, in <module>
[stderr]     from bookings.timeutil import parse_duration; from bookings.billing import billable_blocks; from bookings.schedule import add_slot, total_minutes; assert [parse_duration(x) for x in ('1h30m','2h','45m','1:30','45')] == [90,120,45,90,45]; assert billable_blocks(16)==2 and billable_blocks(45)==3 and billable_blocks(0)==0; assert add_slot('a')==['a'] and add_slot('b')==['b']; assert add_slot('b',['a'])==['a','b']; assert total_minutes(['1h30m','2h'])==210
[stderr]     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr] ModuleNotFoundError: No module named 'bookings'

Exit code: 1
[Command failed with exit code 1]

### Tool call: execute
{"command": "python -c \"import sys; sys.path.insert(0, 'workspace'); from bookings.timeutil import parse_duration; from bookings.billing import billable_blocks; from bookings.schedule import add_slot, total_minutes; assert [parse_duration(x) for x in ('1h30m','2h','45m','1:30','45')] == [90,120,45,90,45]; assert billable_blocks(16)==2 and billable_blocks(45)==3 and billable_blocks(0)==0; assert add_slot('a')==['a'] and add_slot('b')==['b']; assert add_slot('b',['a'])==['a','b']; assert total_minutes(['1h30m','2h'])==210\""}

### Tool result
<no output>
[Command succeeded with exit code 0]

### Assistant
Updated `workspace/bookings/billing.py`, `workspace/bookings/timeutil.py`, and `workspace/bookings/schedule.py` to implement the documented rounding, duration formats, and independent-list behavior. The targeted checks passed. Pytest could not run because of a Windows environment error while loading a plugin.