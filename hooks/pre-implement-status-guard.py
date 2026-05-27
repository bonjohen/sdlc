#!/usr/bin/env python3
"""
PreToolUse hook (Edit/Write matcher): blocks source file edits when no task
is marked 'Started' in the active phase plan.

This hook is only active when the sentinel file exists — meaning /sdlc implement
is in progress. Outside of implement mode, it does nothing.

Sentinel: ~/.claude/state/sdlc-implement.json

Sentinel lifecycle (managed by the implement prompt, not this hook):
    - Created when /sdlc implement starts (contains project_root, phase_plan, started_at)
    - Updated when advancing to the next phase (phase_plan field changes)
    - Deleted when all phases complete, single-phase stop, or clean stop
    - Orphaned if the session crashes — next /sdlc implement overwrites it

To disable enforcement at any time:
    rm ~/.claude/state/sdlc-implement.json

Decision tree:
    1. Parse stdin JSON          → on failure: exit 0 (fail open)
    2. Extract file_path         → missing: exit 0
    3. Normalize path            → backslashes to forward slashes, absolute
    4. Plan file check           → matches plan patterns: exit 0 (always allow)
    5. Read sentinel             → missing or malformed: exit 0 (not in implement mode)
    6. Project membership check  → file outside project_root: exit 0
    7. Parse phase plan table    → parse failure: exit 0 (fail open)
    8. Any task Started?         → YES: exit 0; NO: exit 2 (block)

Exit codes:
    0 -> allow the edit/write
    2 -> BLOCK (no task is Started in the active phase plan)
"""
import json
import os
import sys
from pathlib import Path


def normalize_path(p):
    """Normalize a file path: backslashes to forward slashes, resolve to absolute."""
    # Replace backslashes with forward slashes
    p = p.replace("\\", "/")
    # Handle Git Bash style /c/ prefixes → C:/
    if len(p) >= 3 and p[0] == "/" and p[1].isalpha() and p[2] == "/":
        p = p[1].upper() + ":/" + p[3:]
    # Resolve to absolute
    try:
        p = str(Path(p).resolve()).replace("\\", "/")
    except (OSError, ValueError):
        pass
    return p


def is_plan_file(path):
    """Check if the path is a plan file that should always be allowed."""
    # Normalize for matching
    p = path.replace("\\", "/")
    parts = p.split("/")
    # Pattern: */plan/phase*/plan.md
    for i in range(len(parts) - 1):
        if parts[i] == "plan" and i + 1 < len(parts) and parts[i + 1].startswith("phase"):
            if i + 2 < len(parts) and parts[i + 2] == "plan.md":
                return True
    # Pattern: */docs/final.plan.md
    if len(parts) >= 2 and parts[-2] == "docs" and parts[-1] == "final.plan.md":
        return True
    # Pattern: */docs/draft.*.md
    if len(parts) >= 2 and parts[-2] == "docs" and parts[-1].startswith("draft.") and parts[-1].endswith(".md"):
        return True
    return False


def has_started_task(plan_path):
    """Parse the task table in a plan file and check for any 'Started' status.

    Returns True if any task has Status = 'Started', or if parsing fails (fail open).
    """
    try:
        with open(plan_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except (OSError, IOError):
        return True  # fail open

    if not lines:
        return True  # empty file, fail open

    status_col_index = None
    in_table = False
    skip_separator = False

    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            # Not a table row — reset table state
            in_table = False
            status_col_index = None
            skip_separator = False
            continue

        cells = [c.strip() for c in stripped.split("|")]
        # split("|") on "|a|b|c|" gives ['', 'a', 'b', 'c', '']
        # Remove empty leading/trailing from split
        if cells and cells[0] == "":
            cells = cells[1:]
        if cells and cells[-1] == "":
            cells = cells[:-1]

        if not in_table:
            # Check if this is a header row with a Status column
            for i, cell in enumerate(cells):
                if cell.lower() == "status":
                    status_col_index = i
                    in_table = True
                    skip_separator = True
                    break
            continue

        if skip_separator:
            # Skip the separator row (|---|---|...)
            skip_separator = False
            continue

        # Data row — check status column
        if status_col_index is not None and status_col_index < len(cells):
            val = cells[status_col_index].strip().lower()
            if val == "started":
                return True

    return False  # No Started task found


def main():
    # Step 1: Parse stdin JSON
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)  # fail open

    # Step 2: Extract file_path from tool_input
    tool_input = payload.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)  # no file path, nothing to guard

    # Step 3: Normalize path
    file_path = normalize_path(file_path)

    # Step 4: Plan file check — always allow plan file edits
    if is_plan_file(file_path):
        sys.exit(0)

    # Step 5: Read sentinel
    sentinel_path = Path.home() / ".claude" / "state" / "sdlc-implement.json"
    if not sentinel_path.exists():
        sys.exit(0)  # not in implement mode

    try:
        with open(sentinel_path, "r", encoding="utf-8") as f:
            sentinel = json.load(f)
    except (json.JSONDecodeError, ValueError, OSError):
        sys.exit(0)  # malformed sentinel, fail open

    project_root = sentinel.get("project_root", "")
    phase_plan = sentinel.get("phase_plan", "")

    if not project_root or not phase_plan:
        sys.exit(0)  # incomplete sentinel, fail open

    # Step 6: Project membership check
    project_root = normalize_path(project_root)
    if not file_path.startswith(project_root.rstrip("/") + "/"):
        sys.exit(0)  # different project

    # Step 7: Read phase plan and parse task table
    plan_full_path = os.path.join(project_root, phase_plan).replace("\\", "/")
    if not os.path.isfile(plan_full_path):
        sys.exit(0)  # plan file not found, fail open

    # Step 8: Check for Started tasks
    if has_started_task(plan_full_path):
        sys.exit(0)  # at least one task is Started — allow

    # No Started task found — BLOCK
    sys.stderr.write(
        "BLOCKED: No task is marked 'Started' in the active phase plan.\n"
        "\n"
        "The implement workflow requires updating the phase plan BEFORE editing\n"
        "source files. Mark the next task as 'Started' in:\n"
        f"    {project_root}/{phase_plan}\n"
        "\n"
        "Then retry this edit. This hook enforces US-005 from the user requirements.\n"
        "\n"
        "To disable this hook (not recommended during /sdlc implement):\n"
        "    rm ~/.claude/state/sdlc-implement.json\n"
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
