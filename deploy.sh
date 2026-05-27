#!/usr/bin/env bash
# Deploy SDLC skill files to ~/.claude/skills/sdlc/
# Copies skill/ directory contents and hooks to their installed locations.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_TARGET="$HOME/.claude/skills/sdlc"
HOOKS_TARGET="$HOME/.claude/hooks"

echo "Deploying SDLC skill from $SCRIPT_DIR"

# --- Skill files ---
mkdir -p "$SKILL_TARGET/skill"
cp "$SCRIPT_DIR/skill/SKILL.md" "$SKILL_TARGET/SKILL.md"
cp "$SCRIPT_DIR/skill/"*.md "$SKILL_TARGET/skill/"
echo "  Skill files -> $SKILL_TARGET/"

# --- Hooks ---
mkdir -p "$HOOKS_TARGET"
for hook in sdlc-implement-checkpoint.py pre-implement-status-guard.py; do
    if [ -f "$HOOKS_TARGET/$hook" ]; then
        cp "$HOOKS_TARGET/$hook" "$HOOKS_TARGET/$hook.bak"
    fi
    cp "$SCRIPT_DIR/hooks/$hook" "$HOOKS_TARGET/$hook"
done
echo "  Hooks -> $HOOKS_TARGET/"

# --- Clean stale layout (sdlc/prompts/ from earlier deploys) ---
if [ -d "$SKILL_TARGET/sdlc/prompts" ]; then
    rm -rf "$SKILL_TARGET/sdlc"
    echo "  Cleaned stale sdlc/prompts/ layout"
fi

echo "Done. New sessions will pick up the changes."
