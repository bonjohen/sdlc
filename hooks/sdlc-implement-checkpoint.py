#!/usr/bin/env python3
"""
UserPromptSubmit hook: creates the implement checkpoint (sentinel file)
when /sdlc implement is detected in the user's prompt.

The sentinel activates the pre-implement-status-guard.py hook, which blocks
source file edits when no task is marked 'Started'. This hook ensures the
sentinel is created reliably — not dependent on the agent following prompt
instructions.

Logic:
    1. Check prompt for /sdlc implement patterns
    2. If sentinel exists for this project → keep it (already active)
    3. If no sdlc/docs/final.plan.md → skip (not an SDLC project)
    4. Find the active phase plan (first with Open tasks)
    5. Create sentinel at ~/.claude/state/sdlc-implement.json
    6. Print confirmation (injected as agent context)

Always exits 0 (augments, never blocks).
"""
import glob
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Force UTF-8 stdout (Windows default cp1252 mangles non-ASCII)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# --- Read prompt from stdin ---------------------------------------------------

try:
    payload = json.load(sys.stdin)
except (json.JSONDecodeError, ValueError):
    sys.exit(0)

prompt = (payload.get("prompt") or "").strip()
if not prompt:
    sys.exit(0)

# --- Detect /sdlc implement --------------------------------------------------
# Match: "/sdlc implement", "sdlc implement" (from skill dispatcher expansion)
if not re.search(r"\bsdlc\s+implement\b", prompt, re.IGNORECASE):
    sys.exit(0)

# --- Check this is an SDLC project -------------------------------------------

project_root = os.getcwd().replace("\\", "/")
master_plan = os.path.join(project_root, "sdlc", "docs", "final.plan.md")
if not os.path.isfile(master_plan):
    sys.exit(0)  # Not an SDLC project — nothing to checkpoint

# --- Check existing sentinel --------------------------------------------------

sentinel_path = Path.home() / ".claude" / "state" / "sdlc-implement.json"

if sentinel_path.exists():
    try:
        with open(sentinel_path, "r", encoding="utf-8") as f:
            existing = json.load(f)
        existing_root = existing.get("project_root", "").replace("\\", "/").rstrip("/")
        if existing_root == project_root.rstrip("/"):
            # Sentinel exists for this project — still valid, report it
            phase_plan = existing.get("phase_plan", "unknown")
            print(
                f"[implement-checkpoint] Sentinel active for this project.\n"
                f"  Phase plan: {phase_plan}\n"
                f"  The pre-implement-status-guard hook is enforcing Started-before-edit."
            )
            sys.exit(0)
        # Sentinel is for a different project — overwrite below
    except (json.JSONDecodeError, ValueError, OSError):
        pass  # Corrupted sentinel — overwrite

# --- Find active phase plan ---------------------------------------------------

plan_dir = os.path.join(project_root, "sdlc", "plan")
phase_plan_rel = None

if os.path.isdir(plan_dir):
    pattern = os.path.join(plan_dir, "phase*", "plan.md")
    phase_files = sorted(glob.glob(pattern))

    for pf in phase_files:
        try:
            with open(pf, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError:
            continue

        # Check task table for any Open task (the only reliable signal —
        # frontmatter status can be stale after phase completion)
        if re.search(r"\|\s*Open\s*\|", content):
            phase_plan_rel = os.path.relpath(pf, project_root).replace("\\", "/")
            break

if not phase_plan_rel:
    # No open phase found. Could be fully complete, or plan uses Started tasks.
    # Scan for Started tasks as fallback.
    if os.path.isdir(plan_dir):
        for pf in sorted(glob.glob(os.path.join(plan_dir, "phase*", "plan.md"))):
            try:
                with open(pf, "r", encoding="utf-8") as f:
                    content = f.read()
                if re.search(r"\|\s*Started\s*\|", content):
                    phase_plan_rel = os.path.relpath(pf, project_root).replace("\\", "/")
                    break
            except OSError:
                continue

if not phase_plan_rel:
    # Still nothing — use the master plan path as a fallback. The implement
    # prompt will determine the actual phase on its own.
    phase_plan_rel = "sdlc/docs/final.plan.md"

# --- Create sentinel ----------------------------------------------------------

sentinel_data = {
    "project_root": project_root,
    "phase_plan": phase_plan_rel,
    "started_at": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
}

sentinel_path.parent.mkdir(parents=True, exist_ok=True)
try:
    with open(sentinel_path, "w", encoding="utf-8") as f:
        json.dump(sentinel_data, f, indent=2)
except OSError as e:
    print(f"[implement-checkpoint] WARNING: Could not create sentinel: {e}")
    sys.exit(0)

print(
    f"[implement-checkpoint] Created checkpoint for {project_root}\n"
    f"  Phase plan: {phase_plan_rel}\n"
    f"  Sentinel: {sentinel_path}\n"
    f"  The pre-implement-status-guard hook is now active.\n"
    f"  Source file edits will be blocked unless a task is marked Started."
)

sys.exit(0)
