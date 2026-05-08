#!/bin/bash
# Personal Brain - Start Hook
# Pulls latest memories from git before session starts.
# Logs failures to logs/sync-start.log (gitignored) rather than silently
# swallowing them — silent failure was previously masking real problems.

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$(realpath "$0")")")}"
LOG_DIR="$PLUGIN_ROOT/logs"
LOG="$LOG_DIR/sync-start.log"
mkdir -p "$LOG_DIR"

timestamp() { date +"%Y-%m-%d %H:%M:%S"; }
logline()   { echo "$(timestamp) $1" >> "$LOG"; }

cd "$PLUGIN_ROOT" || { logline "cd failed: $PLUGIN_ROOT"; exit 0; }

# Stash any local changes (shouldn't happen, but just in case).
if git stash push -m "sync-start auto-stash" 2>>"$LOG" >/dev/null; then
    STASHED=1
else
    STASHED=0
fi

# Pull latest from remote — try main then master.
if git pull --ff-only origin main 2>>"$LOG" >>"$LOG"; then
    logline "pulled origin/main"
elif git pull --ff-only origin master 2>>"$LOG" >>"$LOG"; then
    logline "pulled origin/master"
else
    logline "pull failed (network? auth? diverged?)"
fi

# Restore stash if we made one.
if [[ "$STASHED" -eq 1 ]]; then
    git stash pop 2>>"$LOG" >/dev/null || logline "stash pop failed — stash retained"
fi

echo "Brain loaded."
exit 0
