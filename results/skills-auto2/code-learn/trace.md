### Human
The test suite of the `inventory` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


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

### Tool call: ls
{"path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/inventory/', '/workspace/tests/']

### Tool call: ls
{"path": "workspace/inventory"}

### Tool result
['/workspace/inventory/__init__.py', '/workspace/inventory/__pycache__/', '/workspace/inventory/export.py', '/workspace/inventory/pricing.py', '/workspace/inventory/report.py']

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/README.md", "limit": 1000}

### Tool call: ls
{"path": "workspace/tests"}

### Tool call: read_file
{"file_path": "workspace/inventory/pricing.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/inventory/report.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/inventory/export.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/inventory/__init__.py", "limit": 1000}

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 0.3.1
- initial import

### Tool result
@@ lines 1-5 of 5 @@
# inventory

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool result
['/workspace/tests/__pycache__/', '/workspace/tests/test_report.py']

### Tool result
@@ lines 1-25 of 25 @@
"""Price utilities for the inventory package."""
from decimal import Decimal


def parse_price(text):
    """Convert a price string to a Decimal.

    Supported formats:
      "$1,299.50" -> Decimal("1299.50")
      "  12 "     -> Decimal("12")
      "1299.5"    -> Decimal("1299.5")
      "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
    """
    cleaned = text.strip().replace("$", "")
    return Decimal(cleaned)


def apply_discount(price, percent):
    """Return `price` after a percentage discount.

    The result is a Decimal rounded to 2 decimal places using the
    commercial rule "round half up" (0.005 -> 0.01).
    """
    discounted = price * (100 - percent) / 100
    return discounted.quantize(Decimal("0.01"))

### Tool result
@@ lines 1-25 of 25 @@
"""Inventory reports."""
from decimal import Decimal

from .pricing import apply_discount, parse_price


def total_value(items):
    """Total value of `items` after per-item discounts.

    Each item is a dict: {"name": str, "price": str, "qty": int, "discount": percent (optional)}.
    """
    total = Decimal("0")
    for item in items:
        price = parse_price(item["price"])
        price = apply_discount(price, item.get("discount", 0))
        total += price * item["qty"]
    return total


def low_stock(items, threshold=5):
    """Names of the items whose quantity is strictly below `threshold`.

    The names are sorted alphabetically, ignoring case.
    """
    return [item["name"] for item in items if item["qty"] <= threshold]

### Tool result
@@ lines 1-12 of 12 @@
"""Export helpers."""
from .pricing import parse_price


def to_csv_row(item):
    """Format one item as a CSV row: name,price,qty (price with 2 decimals).

    A name that contains a comma or a double quote is wrapped in double quotes,
    and every double quote inside it is doubled (RFC 4180).
    """
    price = parse_price(item["price"])
    return f'{item["name"]},{price:.2f},{item["qty"]}'

### Tool result
@@ lines 1-1 @@
System reminder: File exists but has empty contents

### Tool call: read_file
{"file_path": "workspace/tests/test_report.py", "limit": 1000}

### Tool call: glob
{"pattern": "workspace/**", "path": "."}

### Tool result
@@ lines 1-32 of 32 @@
from decimal import Decimal

from inventory.export import to_csv_row
from inventory.pricing import apply_discount
from inventory.report import low_stock, total_value


def test_total_value_plain():
    items = [{"name": "pen", "price": "$2.50", "qty": 4}]
    assert total_value(items) == Decimal("10.00")


def test_total_value_thousands_separator():
    items = [{"name": "laptop", "price": "$1,299.50", "qty": 2}]
    assert total_value(items) == Decimal("2599.00")


def test_discount_rounding_half_up():
    assert apply_discount(Decimal("10.05"), 10) == Decimal("9.05")


def test_total_value_with_discount():
    items = [{"name": "desk", "price": "100.00", "qty": 1, "discount": 15}]
    assert total_value(items) == Decimal("85.00")


def test_low_stock_basic():
    assert low_stock([{"name": "pen", "qty": 2}, {"name": "ink", "qty": 9}]) == ["pen"]


def test_csv_row_plain_name():
    assert to_csv_row({"name": "pen", "price": "2.5", "qty": 4}) == "pen,2.50,4"

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/inventory/__init__.py', '/workspace/inventory/__pycache__/__init__.cpython-313.pyc', '/workspace/inventory/__pycache__/export.cpython-313.pyc', '/workspace/inventory/__pycache__/pricing.cpython-313.pyc', '/workspace/inventory/__pycache__/report.cpython-313.pyc', '/workspace/inventory/export.py', '/workspace/inventory/pricing.py', '/workspace/inventory/report.py', '/workspace/tests/__pycache__/test_report.cpython-313-pytest-9.1.1.pyc', '/workspace/tests/test_report.py']

### Tool call: edit_file
{"file_path": "workspace/inventory/pricing.py", "old_string": "from decimal import Decimal\n", "new_string": "from decimal import Decimal, ROUND_HALF_UP\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/pricing.py'

### Tool call: edit_file
{"file_path": "workspace/inventory/pricing.py", "old_string": "    cleaned = text.strip().replace(\"$\", \"\")\n    return Decimal(cleaned)\n", "new_string": "    cleaned = text.strip()\n    if cleaned.startswith(\"(\") and cleaned.endswith(\")\"):\n        cleaned = f\"-{cleaned[1:-1].strip()}\"\n    cleaned = cleaned.replace(\"$\", \"\").replace(\",\", \"\")\n    return Decimal(cleaned)\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/pricing.py'

### Tool call: edit_file
{"file_path": "workspace/inventory/pricing.py", "old_string": "    return discounted.quantize(Decimal(\"0.01\"))", "new_string": "    return discounted.quantize(Decimal(\"0.01\"), rounding=ROUND_HALF_UP)"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/pricing.py'

### Tool call: edit_file
{"file_path": "workspace/inventory/report.py", "old_string": "    return [item[\"name\"] for item in items if item[\"qty\"] <= threshold]", "new_string": "    names = [item[\"name\"] for item in items if item[\"qty\"] < threshold]\n    return sorted(names, key=str.casefold)"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/report.py'

### Tool call: edit_file
{"file_path": "workspace/inventory/export.py", "old_string": "    price = parse_price(item[\"price\"])\n    return f'{item[\"name\"]},{price:.2f},{item[\"qty\"]}'", "new_string": "    price = parse_price(item[\"price\"])\n    name = str(item[\"name\"])\n    if \",\" in name or '\"' in name:\n        name = '\"' + name.replace('\"', '\"\"') + '\"'\n    return f\"{name},{price:.2f},{item['qty']}\""}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/export.py'

### Tool call: edit_file
{"file_path": "workspace/CHANGELOG.md", "old_string": "## Unreleased\n", "new_string": "## Unreleased\n- Fix price parsing, half-up discount rounding, stock filtering and ordering, and RFC 4180 CSV name escaping.\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/CHANGELOG.md'

### Tool call: execute
{"command": "python -m pytest workspace/tests -q", "timeout": 120000}

### Tool result
Error: timeout 120000s exceeds maximum allowed (3600s).

### Tool call: execute
{"command": "python -m pytest workspace/tests -q", "timeout": 120000}

### Tool result
Error: timeout 120000s exceeds maximum allowed (3600s).

### Tool call: execute
{"command": "python -m pytest workspace/tests -q", "timeout": 120}

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

### Tool call: execute
{"command": "$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'; $env:PYTHONPATH='workspace'; python -m pytest workspace/tests -q", "timeout": 120}

### Tool result
[stderr] The filename, directory name, or volume label syntax is incorrect.

Exit code: 1
[Command failed with exit code 1]

### Tool call: execute
{"command": "python -m pytest workspace/tests -q -p no:langsmith", "timeout": 120}

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
{"command": "python -c \"import os,pytest; os.environ['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1'; raise SystemExit(pytest.main(['workspace/tests','-q']))\"", "timeout": 120}

### Tool result

=================================== ERRORS ====================================
_______________ ERROR collecting workspace/tests/test_report.py _______________
ImportError while importing test module '~\AppData\Local\Temp\lab-sandbox-7da5d3a820bf4a63b58ac46775c57b65\workspace\tests\test_report.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\Programs\Python\Python313\Lib\importlib\__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
workspace\tests\test_report.py:3: in <module>
    from inventory.export import to_csv_row
E   ModuleNotFoundError: No module named 'inventory'
=========================== short test summary info ===========================
ERROR workspace/tests/test_report.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.13s

Exit code: 2
[Command failed with exit code 2]

### Tool call: execute
{"command": "python -c \"import os,sys,pytest; os.environ['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1'; sys.path.insert(0,'workspace'); raise SystemExit(pytest.main(['workspace/tests','-q']))\"", "timeout": 120}

### Tool result
......                                                                   [100%]
6 passed in 0.04s

[Command succeeded with exit code 0]

### Assistant
Updated `workspace/inventory/pricing.py`, `workspace/inventory/report.py`, and `workspace/inventory/export.py` to match their docstrings, and recorded the fixes in `workspace/CHANGELOG.md`. The test suite passes: 6 tests passed.