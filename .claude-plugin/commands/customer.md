---
description: "Manage customer/client context - add, view, or update customer profiles for instant recall."
argument-hint: "add <name> | view <name> | list"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Customer/Client Context Manager

Store and retrieve context about your customers and clients.

## Commands

### Add a new customer
Create a new file at `${CLAUDE_PLUGIN_ROOT}/context/customers/<name>.md` using the template at `${CLAUDE_PLUGIN_ROOT}/context/customers/_TEMPLATE.md`.

After creating, add an entry to `${CLAUDE_PLUGIN_ROOT}/context/customers/_INDEX.md`.

### View a customer
```bash
cat "${CLAUDE_PLUGIN_ROOT}/context/customers/<name>.md"
```

### List all customers
```bash
ls -la "${CLAUDE_PLUGIN_ROOT}/context/customers/"
```

### Search across customers
```bash
grep -r "<query>" "${CLAUDE_PLUGIN_ROOT}/context/customers/"
```

## Auto-Sync
Customer context files auto-sync via git. Changes on any machine propagate to all others.
