#!/bin/bash
# Personal Brain - Stop Hook
# Commits and pushes to git. Logs failures to logs/sync-stop.log.

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$(realpath "$0")")")}"
REPO_ROOT="$PLUGIN_ROOT"
LOG_DIR="$PLUGIN_ROOT/logs"
LOG="$LOG_DIR/sync-stop.log"
mkdir -p "$LOG_DIR"

timestamp() { date +"%Y-%m-%d %H:%M:%S"; }
logline()   { echo "$(timestamp) $1" >> "$LOG"; }

cd "$REPO_ROOT" || { logline "cd failed: $REPO_ROOT"; exit 0; }

# Only act if there are changes.
if [[ -z $(git status --porcelain 2>/dev/null) ]]; then
    exit 0
fi

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
MACHINE=$(hostname)

git add -A 2>>"$LOG" || { logline "git add failed"; exit 0; }

if ! git commit -m "brain-sync: $MACHINE @ $TIMESTAMP" --no-verify 2>>"$LOG"; then
    logline "git commit failed (nothing to commit? hook blocked?)"
    exit 0
fi

# Rebase-pull to resolve any divergence (last write wins).
if ! git pull --rebase origin main 2>>"$LOG" >>"$LOG" \
  && ! git pull --rebase origin master 2>>"$LOG" >>"$LOG"; then
    logline "rebase-pull failed — local commit exists but may diverge"
fi

if ! git push origin main 2>>"$LOG" >>"$LOG" \
  && ! git push origin master 2>>"$LOG" >>"$LOG"; then
    logline "push failed — commit is local only until next successful sync"
fi

logline "synced: $MACHINE @ $TIMESTAMP"
echo "Brain synced."
exit 0
