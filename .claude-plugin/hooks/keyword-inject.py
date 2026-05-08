"""UserPromptSubmit hook: scan the prompt for keywords from keyword-map.json
and surface pointers to relevant context files.

Injects *pointers*, not file contents. Claude decides whether to read the
pointed-to file. This keeps the prompt lean and lets the model use judgment.
"""
from __future__ import annotations

import json
import sys

from _utils import brain_root, log, safe_exit


def load_map(root) -> dict[str, str]:
    path = root / ".claude-plugin" / "hooks" / "keyword-map.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {k.lower(): v for k, v in data.items() if not k.startswith("_")}


def main() -> None:
    try:
        raw = sys.stdin.read()
        if not raw:
            return
        payload = json.loads(raw)
        prompt = payload.get("prompt", "") or ""
        if not prompt.strip():
            return

        root = brain_root()
        keyword_map = load_map(root)
        if not keyword_map:
            return

        low = prompt.lower()
        hits: list[str] = []
        seen: set[str] = set()
        for keyword, target in keyword_map.items():
            if keyword in low and target not in seen:
                hits.append(f"- `context/{target}` (triggered by: \"{keyword}\")")
                seen.add(target)
                if len(hits) >= 5:
                    break

        if not hits:
            return

        context = (
            "=== BRAIN POINTERS (keyword-matched from your prompt) ===\n"
            "The following context files may be relevant. Read any that apply "
            "before acting — do not assume their contents.\n\n"
            + "\n".join(hits)
        )

        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context,
            }
        }))
        log("keyword-inject", f"matched {len(hits)} keywords")
    except Exception as e:
        safe_exit("keyword-inject", e)


if __name__ == "__main__":
    main()
