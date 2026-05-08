"""Stop hook: scan the last user message for explicit memory signals and
append them to context/_inbox.md for review.

Design decisions:
- Inbox pattern: captured entries land in _inbox.md, NOT directly in the
  structured context/ tree. This prevents auto-capture from silently
  polluting curated files. The inbox is reviewed and entries are filed properly.
- Trigger-phrase only: we only capture when the user's last message
  contains an explicit memory signal ("remember", "save this", "from now
  on", "don't", "never", etc). Cuts noise dramatically.
- No LLM calls: pure regex. Deterministic, free, fast.
- Never blocks the session: any error exits 0.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

from _utils import brain_root, log, safe_exit

TRIGGERS = re.compile(
    r"\b("
    r"remember(?:\s+(?:this|that))?"
    r"|save\s+(?:this|that|it|for\s+later)"
    r"|note\s+(?:this|that)"
    r"|from\s+now\s+on"
    r"|always\b"
    r"|never\b"
    r"|stop\s+(?:doing|using)"
    r"|don'?t\b"
    r"|fyi\b"
    r"|important:"
    r"|for\s+the\s+record"
    r"|add\s+to\s+(?:my\s+)?brain"
    r")\b",
    re.IGNORECASE,
)


def read_transcript(path: str) -> list[dict]:
    out: list[dict] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def extract_user_text(entry: dict) -> str:
    """Pull plain text out of a transcript entry, tolerating schema variants."""
    msg = entry.get("message") if isinstance(entry.get("message"), dict) else entry
    content = msg.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
            elif isinstance(item, str):
                parts.append(item)
        return "\n".join(parts)
    return ""


def last_user_message(transcript: list[dict]) -> str:
    for entry in reversed(transcript):
        role = entry.get("type") or entry.get("role")
        if role == "user" or (isinstance(entry.get("message"), dict) and entry["message"].get("role") == "user"):
            text = extract_user_text(entry)
            if text and not text.startswith("<") and "tool_result" not in text[:50]:
                return text
    return ""


def main() -> None:
    try:
        raw = sys.stdin.read()
        if not raw:
            return
        payload = json.loads(raw)
        transcript_path = payload.get("transcript_path", "")
        if not transcript_path or not Path(transcript_path).exists():
            log("capture", f"no transcript at {transcript_path!r}")
            return

        transcript = read_transcript(transcript_path)
        text = last_user_message(transcript).strip()
        if not text:
            return

        if not TRIGGERS.search(text):
            return

        root = brain_root()
        inbox = root / "context" / "_inbox.md"
        inbox.parent.mkdir(parents=True, exist_ok=True)

        if not inbox.exists():
            inbox.write_text(
                "# Memory Inbox\n\n"
                "Auto-captured entries from conversations where the user signaled intent\n"
                "to remember something. Review and file into the structured context/ tree,\n"
                "then delete from here.\n",
                encoding="utf-8",
            )

        entry = (
            f"\n---\n"
            f"## {datetime.now().isoformat(timespec='seconds')}\n\n"
            f"> {text.strip()[:2000]}\n"
        )
        with open(inbox, "a", encoding="utf-8") as f:
            f.write(entry)

        log("capture", f"wrote {len(text)} chars to _inbox.md")
    except Exception as e:
        safe_exit("capture", e)


if __name__ == "__main__":
    main()
