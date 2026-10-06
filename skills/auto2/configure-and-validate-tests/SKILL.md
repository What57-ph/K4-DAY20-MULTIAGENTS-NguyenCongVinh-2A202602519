---
name: configure-and-validate-tests
description: Use when test discovery or imports fail because the working directory, environment, or plugins are misconfigured.
---
- Confirm the repository root and test-directory paths before invoking the test runner.
- Check package import paths and set the project path explicitly when needed.
- Disable third-party plugin autoload only when plugin startup causes failures.
- Distinguish collection or environment errors from actual test failures.
- Rerun the intended suite after correcting invocation settings.
