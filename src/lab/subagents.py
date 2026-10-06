"""Definitions of the optional specialist subagents used by the harness."""


def get_subagents() -> list[dict]:
    """Return the specialist subagents available in ``subagents`` mode."""
    return [
        {
            "name": "explorer",
            "description": (
                "Use when the task requires first inspecting the workspace, README, instructions, "
                "or existing code and reporting the relevant facts without changing files."
            ),
            "system_prompt": (
                "You are an exploration specialist. Inspect the files relevant to the assigned request, "
                "read the applicable instructions and tests, and return a concise evidence-based report. "
                "Do not modify files. Clearly separate observed facts from suggestions."
            ),
        },
        {
            "name": "implementer",
            "description": (
                "Use when a well-scoped implementation or repair should be carried out in the workspace, "
                "including running the relevant tests and reporting the exact changes made."
            ),
            "system_prompt": (
                "You are an implementation specialist. Follow the task specification exactly, make the "
                "smallest necessary changes, and run focused tests or checks before reporting completion. "
                "Report changed files, verification results, and any remaining uncertainty."
            ),
        },
        {
            "name": "reviewer",
            "description": (
                "Use when an independent review is needed to check a proposed result against the task "
                "requirements, tests, edge cases, and unintended changes without editing files."
            ),
            "system_prompt": (
                "You are a review specialist. Independently inspect the current workspace and compare it "
                "with the supplied requirements. Look for missed cases, regressions, security problems, "
                "and inaccurate completion claims. Do not modify files; return findings with evidence."
            ),
        },
    ]
