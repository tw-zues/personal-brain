#!/bin/bash
# Portable Python launcher.
#
# Picks whichever Python is actually executable on this machine. We can't
# just check PATH — Windows exposes a "python3" App Execution Alias that's
# a stub (it errors with "Python was not found"). So we probe with
# `--version` and only accept interpreters that actually respond.
#
# Usage: bash run-python.sh <script.py> [args...]

try() {
    command -v "$1" >/dev/null 2>&1 || return 1
    "$1" --version >/dev/null 2>&1 || return 1
    return 0
}

for candidate in python python3 py; do
    if try "$candidate"; then
        exec "$candidate" "$@"
    fi
done

echo "[personal-brain] no working Python interpreter found on PATH" >&2
exit 0
