---
description: "Manage business venture context - add, view, or update venture profiles for strategic recall."
argument-hint: "add <name> | view <name> | list"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Business Venture Context Manager

Store and retrieve context about your business ventures and projects.

## Commands

### Add a new venture
Create a new file at `${CLAUDE_PLUGIN_ROOT}/context/ventures/<name>.md` using the template at `${CLAUDE_PLUGIN_ROOT}/context/ventures/_TEMPLATE.md`.

After creating, add an entry to `${CLAUDE_PLUGIN_ROOT}/context/ventures/_INDEX.md`.

### View a venture
```bash
cat "${CLAUDE_PLUGIN_ROOT}/context/ventures/<name>.md"
```

### List all ventures
```bash
ls -la "${CLAUDE_PLUGIN_ROOT}/context/ventures/"
```

### Search across ventures
```bash
grep -r "<query>" "${CLAUDE_PLUGIN_ROOT}/context/ventures/"
```

## Auto-Sync
Venture context files auto-sync via git. Strategic context available on all machines.
