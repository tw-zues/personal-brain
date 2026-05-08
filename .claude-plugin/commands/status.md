---
description: Show brain status - file counts, directory sizes, and sync state.
allowed-tools: Bash, Read
---

# Brain Status

Show the current state of the brain.

## Usage

Check git sync status and file counts:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && echo "=== Git Status ===" && git status && echo "" && echo "=== Recent Commits ===" && git log --oneline -5 && echo "" && echo "=== File Counts ===" && find context/ -name "*.md" -not -path "*/_archived/*" | wc -l && echo "total context files"
```

Break down by directory:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && for dir in context/*/; do echo "$(find "$dir" -name "*.md" -not -path "*/_archived/*" 2>/dev/null | wc -l) files in $dir"; done
```

This shows:
- Git sync state (clean / dirty / ahead / behind)
- Recent sync history
- Total context files per directory
