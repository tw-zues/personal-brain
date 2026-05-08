"""SessionStart hook: inject the core directive, routing table, and directory indexes.

On every session start, the brain injects:
1. CLAUDE.md — session behavior rules
2. The routing table from ARCHITECTURE.md — the "librarian" that maps tasks to files
3. All _INDEX.md files — room descriptions for every directory
4. A flat file listing as fallback

This means every session starts knowing WHERE to look, not just WHAT exists.

Portable: discovers the brain root via CLAUDE_PLUGIN_ROOT or script-relative
fallback. No hardcoded user paths.
"""
from __future__ import annotations

import json
import re
import sys

from _utils import brain_root, log, safe_exit


def extract_routing_table(architecture_path) -> str:
    """Extract the Context Routing section from ARCHITECTURE.md."""
    if not architecture_path.exists():
        return ""
    text = architecture_path.read_text(encoding="utf-8")
    # Extract from "## Context Routing" to the next "## " heading
    match = re.search(
        r"(## Context Routing.*?)(?=\n## |\Z)",
        text,
        re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def collect_indexes(context_dir) -> str:
    """Read all _INDEX.md files and concatenate them."""
    if not context_dir.exists():
        return ""
    parts = []
    for idx_path in sorted(context_dir.rglob("_INDEX.md")):
        rel = idx_path.relative_to(context_dir).as_posix()
        content = idx_path.read_text(encoding="utf-8").strip()
        parts.append(f"--- {rel} ---\n{content}")
    return "\n\n".join(parts)


def main() -> None:
    try:
        root = brain_root()
        directive_path = root / "CLAUDE.md"
        architecture_path = root / "ARCHITECTURE.md"
        context_dir = root / "context"

        # 1. Core directive
        directive = directive_path.read_text(encoding="utf-8") if directive_path.exists() else ""

        # 2. Routing table (the librarian)
        routing = extract_routing_table(architecture_path)

        # 3. All directory indexes (room descriptions)
        indexes = collect_indexes(context_dir)

        # 4. Flat file listing (fallback)
        files: list[str] = []
        if context_dir.exists():
            for p in sorted(context_dir.rglob("*")):
                if p.is_file() and not p.name.startswith("."):
                    rel = p.relative_to(context_dir).as_posix()
                    files.append(rel)

        context = (
            "=== BRAIN CORE DIRECTIVE ===\n"
            + directive
            + "\n\n=== CONTEXT ROUTING (use this to find the right files) ===\n"
            + routing
            + "\n\n=== DIRECTORY INDEXES (room descriptions) ===\n"
            + indexes
            + "\n\n=== ALL FILES (fallback — prefer routing table + indexes above) ===\n"
            + "\n".join(files)
        )

        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context,
            }
        }))
        log("load-brain", f"loaded {len(files)} context files, routing table, and {indexes.count('_INDEX.md')} indexes from {root}")
    except Exception as e:
        safe_exit("load-brain", e)


if __name__ == "__main__":
    main()
