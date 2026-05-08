"""Shared helpers for Personal Brain hooks.

Keeps path resolution and logging consistent across hooks so they behave
identically on every machine. All hooks must fail silently (exit 0) — a
broken hook must never block the session.
"""
from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path


def brain_root() -> Path:
    """Resolve the brain root directory.

    Order: CLAUDE_PLUGIN_ROOT env var (set by Claude Code when the plugin
    loads) → script-relative fallback (this file lives at
    .claude-plugin/hooks/_utils.py, so parents[2] is the repo root).
    """
    env = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env:
        p = Path(env)
        if p.exists():
            return p
    return Path(__file__).resolve().parents[2]


def log(hook: str, msg: str) -> None:
    """Append a timestamped line to logs/<hook>.log.

    Silent on failure — logging must never break a hook.
    """
    try:
        root = brain_root()
        logs = root / "logs"
        logs.mkdir(parents=True, exist_ok=True)
        line = f"{datetime.now().isoformat(timespec='seconds')} {msg}\n"
        with open(logs / f"{hook}.log", "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass


def safe_exit(hook: str, err: BaseException | None = None) -> None:
    """Always exit 0. Log the error if one was given."""
    if err is not None:
        log(hook, f"ERROR {type(err).__name__}: {err}")
        sys.stderr.write(f"[{hook}] {err}\n")
    sys.exit(0)
