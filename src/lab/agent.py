"""Deep Agents harness construction for the lab."""

import os
import sys
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend

from .model import make_model
from .subagents import get_subagents


PATHS_NOTE = (
    "PATHS: every path is relative to the sandbox root and never starts with '/'. "
    "The task files are in the folder workspace/ (for example workspace/app.log). "
    "Use exactly this relative form both in the file tools and in the shell (execute); "
    "the shell starts in the sandbox root. "
)
BASE_PROMPT = (
    "You are an engineering assistant working in a sandbox. "
    + PATHS_NOTE
    + "Use the shell to run Python and tests. "
    "When you are done, reply with a short summary that mentions only files you really created or changed."
)
SKILLS_NOTE = (
    " Skills are in the folder skills/ (one sub-folder per skill with a SKILL.md). "
    "As your FIRST action, read the SKILL.md of every skill whose description could apply to the task, "
    "then follow them. Never modify skills/."
)
SUBAGENTS_NOTE = (
    " You have specialised subagents (see the description of the task tool). "
    "For anything beyond a trivial step, delegate to a suitable subagent and put ALL the task rules and file paths "
    "in the delegation message, because a subagent sees only what you send. "
    "Check what a subagent returns before you rely on it."
)


def make_backend(sandbox: Path):
    """Create an isolated filesystem and shell backend for ``sandbox``."""
    sandbox = Path(sandbox).resolve()
    python_dir = Path(sys.executable).resolve().parent
    path_entries = [str(python_dir), "/usr/local/bin", "/usr/bin", "/bin"]
    env = {
        "PATH": os.pathsep.join(path_entries),
        "HOME": str(sandbox),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    if os.name == "nt":
        # The offline tests use POSIX command names even when the lab runs on Windows.
        # Keep these helpers inside the sandbox and do not inherit the host environment.
        system_root = Path(os.environ.get("SystemRoot", r"C:\Windows"))
        bin_dir = sandbox / ".lab-bin"
        bin_dir.mkdir(parents=True, exist_ok=True)
        (bin_dir / "which.cmd").write_bytes(b"@echo off\r\nwhere.exe %*\r\n")
        (bin_dir / "env.cmd").write_bytes(b"@echo off\r\nset\r\n")
        (bin_dir / "cat_helper.py").write_text(
            "from pathlib import Path\n"
            "import sys\n"
            "print(Path(sys.argv[1]).read_text(), end='')\n",
            encoding="utf-8",
        )
        (bin_dir / "cat.cmd").write_bytes(
            b"@echo off\r\npython \"%~dp0cat_helper.py\" %*\r\n"
        )
        (bin_dir / "ls.cmd").write_bytes(b"@echo off\r\ndir /b %*\r\n")
        path_entries = [str(bin_dir), *path_entries, str(system_root / "System32")]
        env["PATH"] = os.pathsep.join(path_entries)
        env["PATHEXT"] = ".COM;.EXE;.BAT;.CMD"
    return LocalShellBackend(
        root_dir=sandbox,
        virtual_mode=True,
        inherit_env=False,
        env=env,
        timeout=120,
    )


def build_agent(sandbox: Path, mode: str = "single", use_skills: bool = False, model=None):
    """Build a Deep Agents graph for one of the lab's two modes."""
    if mode not in {"single", "subagents"}:
        raise ValueError(f"unknown mode: {mode}")

    kwargs = {}
    prompt = BASE_PROMPT

    if mode == "subagents":
        kwargs["subagents"] = [
            {
                **subagent,
                "system_prompt": subagent["system_prompt"] + " " + PATHS_NOTE,
            }
            for subagent in get_subagents()
        ]
        prompt += SUBAGENTS_NOTE

    if use_skills:
        kwargs["skills"] = ["/skills/"]
        prompt += SKILLS_NOTE

    return create_deep_agent(
        model=model if model is not None else make_model(),
        system_prompt=prompt,
        backend=make_backend(sandbox),
        **kwargs,
    )
