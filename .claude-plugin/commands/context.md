---
description: "Quick context lookup - search across all customers, ventures, and projects at once."
argument-hint: "<search query>"
allowed-tools: Bash, Read, Glob, Grep
---

# Quick Context Search

Search across ALL context files (customers, ventures, projects) at once.

## Usage

```bash
grep -ri "<query>" "${CLAUDE_PLUGIN_ROOT}/context/"
```

Or for more detailed results, read matching files:

```bash
# Find files mentioning the query
grep -rl "<query>" "${CLAUDE_PLUGIN_ROOT}/context/"

# Then read the relevant ones
cat "${CLAUDE_PLUGIN_ROOT}/context/<type>/<name>.md"
```

## Context Types

| Type | Location | Command |
|------|----------|---------|
| Customers/Clients | `context/customers/` | `/customer` |
| Business Ventures | `context/ventures/` | `/venture` |
| Projects | `context/projects/` | direct file access |
| Research | `context/research/` | direct file access |
| Preferences | `context/preferences/` | `/rules` for coding rules |

## Examples

- "What do I know about Acme Corp?" -> search customers
- "What's the status of my SaaS idea?" -> search ventures
- "Authentication decisions" -> search all context
