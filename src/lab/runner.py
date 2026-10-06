"""Run tasks, collect measurements, grade workspaces, and write traces."""

import argparse
import json
import shutil
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from langchain_core.callbacks import UsageMetadataCallbackHandler
from langchain_core.messages import AIMessage, ToolMessage

from .agent import build_agent
from .grading import grade
from .tasks import ROOT, get_task, hash_dir, list_tasks, prepare_sandbox


CONDITIONS = {
    "baseline": {"mode": "single", "skills_dir": None},
    "subagents": {"mode": "subagents", "skills_dir": None},
    "skills-auto": {"mode": "single", "skills_dir": "skills/auto"},
}

# Data tasks may need more graph steps than the original 60-step default when
# the model has to inspect a larger CSV and produce both output files.
DEFAULT_RECURSION_LIMIT = 160


def render_trace(messages) -> str:
    """Convert the main agent's messages into a bounded Markdown trace."""
    home = str(Path.home())

    def clean(text) -> str:
        return str(text).replace(home, "~")[:1500]

    parts = []
    for m in messages:
        if isinstance(m, AIMessage):
            if m.content:
                parts.append(f"### Assistant\n{clean(m.content)}")
            for tc in m.tool_calls:
                parts.append(f"### Tool call: {tc['name']}\n{clean(json.dumps(tc['args'], ensure_ascii=False))}")
        elif isinstance(m, ToolMessage):
            parts.append(f"### Tool result\n{clean(m.content)}")
        else:
            parts.append(f"### {m.type.capitalize()}\n{clean(m.content)}")
    return "\n\n".join(parts)


def _tool_calls(messages):
    return [
        tool_call
        for message in messages
        if isinstance(message, AIMessage)
        for tool_call in message.tool_calls
    ]


def _skill_names(calls):
    names = set()
    for call in calls:
        if call.get("name") != "read_file":
            continue
        file_path = str(call.get("args", {}).get("file_path", ""))
        parts = file_path.replace("\\", "/").split("/")
        try:
            index = parts.index("skills")
        except ValueError:
            continue
        if index + 1 < len(parts) and parts[index + 1]:
            names.add(parts[index + 1])
    return names


def _usage_totals(usage):
    totals = {"input": 0, "output": 0, "total": 0}
    for metadata in usage.usage_metadata.values():
        totals["input"] += metadata.get("input_tokens", 0)
        totals["output"] += metadata.get("output_tokens", 0)
        totals["total"] += metadata.get("total_tokens", 0)
    return totals


def _make_sandbox() -> Path:
    """Create a writable temporary sandbox, with a local fallback for restricted hosts."""
    try:
        candidate = Path(tempfile.gettempdir()) / f"lab-sandbox-{uuid.uuid4().hex}"
        candidate.mkdir()
        probe = candidate / ".probe"
        probe.mkdir()
        probe.rmdir()
        return candidate
    except (OSError, PermissionError):
        if "candidate" in locals():
            shutil.rmtree(candidate, ignore_errors=True)
        candidate = ROOT / f".lab-sandbox-{uuid.uuid4().hex}"
        candidate.mkdir()
        return candidate


def run_task(
    task_id: str,
    condition: str,
    results_dir="results",
    model=None,
    recursion_limit: int = DEFAULT_RECURSION_LIMIT,
) -> dict:
    """Run one task in a temporary sandbox and persist its complete record."""
    if condition not in CONDITIONS:
        raise KeyError(f"unknown condition: {condition}")

    cfg = CONDITIONS[condition]
    task = get_task(task_id)
    output_dir = Path(results_dir) / condition / task_id
    output_dir.mkdir(parents=True, exist_ok=True)
    skills_dir = ROOT / cfg["skills_dir"] if cfg["skills_dir"] else None
    sandbox = _make_sandbox()
    record = {
        "task": task.id,
        "condition": condition,
        "role": task.role,
        "error": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    messages = []
    usage = UsageMetadataCallbackHandler()
    skills_before = hash_dir(sandbox / "skills")

    try:
        prepare_sandbox(task, sandbox, skills_dir)
        skills_before = hash_dir(sandbox / "skills")
        record["skills_sha256"] = skills_before
        agent = build_agent(
            sandbox,
            mode=cfg["mode"],
            use_skills=skills_dir is not None,
            model=model,
        )

        started = time.perf_counter()
        try:
            result = agent.invoke(
                {"messages": [{"role": "user", "content": task.instruction}]},
                config={"callbacks": [usage], "recursion_limit": recursion_limit},
            )
            messages = result.get("messages", [])
            if messages:
                final_message = messages[-1].content
            else:
                final_message = ""
        except Exception as exc:  # noqa: BLE001
            record["error"] = f"{type(exc).__name__}: {exc}"
            final_message = ""

        record["seconds"] = round(time.perf_counter() - started, 1)
        record["tokens"] = _usage_totals(usage)
        calls = _tool_calls(messages)
        record["tool_calls"] = len(calls)
        record["subagent_calls"] = sum(call.get("name") == "task" for call in calls)
        record["skills_read"] = len(_skill_names(calls))
        record["skills_modified"] = hash_dir(sandbox / "skills") != skills_before
        record["final_message"] = final_message

        grading = grade(task, sandbox / "workspace")
        record.update({
            "score": grading.get("score", 0.0),
            "passed": grading.get("passed", 0),
            "total": grading.get("total", 0),
            "checks": grading.get("checks", []),
        })
    except Exception as exc:  # noqa: BLE001
        if record["error"] is None:
            record["error"] = f"{type(exc).__name__}: {exc}"
        record.setdefault("seconds", 0.0)
        record.setdefault("tokens", {"input": 0, "output": 0, "total": 0})
        record.setdefault("tool_calls", 0)
        record.setdefault("subagent_calls", 0)
        record.setdefault("skills_read", 0)
        record.setdefault("skills_modified", False)
        record.setdefault("final_message", "")
        record.setdefault("score", 0.0)
        record.setdefault("passed", 0)
        record.setdefault("total", 0)
        record.setdefault("checks", [])
    finally:
        record.setdefault("skills_sha256", skills_before)
        (output_dir / "trace.md").write_text(render_trace(messages), encoding="utf-8")
        shutil.rmtree(sandbox, ignore_errors=True)

    (output_dir / "run.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return record


def main(argv=None):
    """Command-line interface for running one or more tasks."""
    ap = argparse.ArgumentParser(description="Run tasks under one condition.")
    ap.add_argument("--condition", required=True, choices=sorted(CONDITIONS))
    ap.add_argument("--tasks", nargs="+", default=["all"], help="task ids, or 'all', 'learn', 'eval'")
    ap.add_argument("--results", default="results")
    ap.add_argument("--recursion-limit", type=int, default=DEFAULT_RECURSION_LIMIT)
    args = ap.parse_args(argv)
    if args.tasks == ["all"]:
        ids = [t.id for t in list_tasks()]
    elif args.tasks in (["learn"], ["eval"]):
        ids = [t.id for t in list_tasks(args.tasks[0])]
    else:
        ids = args.tasks
    for tid in ids:
        try:
            r = run_task(tid, args.condition, args.results, recursion_limit=args.recursion_limit)
        except Exception as exc:  # noqa: BLE001
            print(f"{args.condition:13s} {tid:11s} CRASH {type(exc).__name__}: {exc}", flush=True)
            continue
        print(
            f"{args.condition:13s} {tid:11s} score={r['passed']}/{r['total']} "
            f"tokens={r['tokens']['total']} calls={r['tool_calls']} {r['seconds']}s"
            + (f" ERROR={r['error']}" if r["error"] else ""),
            flush=True,
        )


if __name__ == "__main__":
    main()
