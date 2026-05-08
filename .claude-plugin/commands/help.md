---
description: Show help for Personal Brain - available commands and usage tips.
allowed-tools: Bash, Read
---

# Personal Brain Help

## Available Commands

| Command | Description |
|---------|-------------|
| `/search <query>` | Search across all context files |
| `/customer` | Manage customer/client profiles |
| `/venture` | Manage business venture context |
| `/context <query>` | Search all context at once |
| `/rules` | View/add coding rules |
| `/errors` | View/log error patterns and solutions |
| `/suggest` | AI suggests new patterns to add |
| `/office-hours` | Pressure-test a strategic decision |
| `/post-writer` | Draft content in your voice |
| `/reddit` | Deep Reddit research on a topic |
| `/github` | Deep GitHub research |
| `/week-retro` | Weekly retrospective |
| `/status` | Show brain stats and sync state |

## How It Works

1. **Auto-Sync**: Context syncs via git automatically
   - Session start: pulls latest from all machines
   - Session end: commits and pushes new context

2. **Routing**: The brain uses a routing table + indexes to find the right files fast
   - Read ARCHITECTURE.md for the full routing table

3. **Proactive Learning**: AI will suggest new patterns to save
   - If you keep explaining the same thing, it will notice
   - Acknowledge the pattern and it gets added to brain

## Quick Start

```bash
# Fill in your profile
edit context/preferences/profile.md

# Add a customer
copy context/customers/_TEMPLATE.md to context/customers/acme-corp.md

# Add keyword triggers
edit .claude-plugin/hooks/keyword-map.json
```
