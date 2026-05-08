---
description: "View or add coding rules - things AI should never do, preferences, and feedback."
argument-hint: "view | add <rule>"
allowed-tools: Bash, Read, Write, Edit
---

# Coding Rules Manager

View and manage the rules for how AI should behave when coding with you.

## View Current Rules

```bash
cat "${CLAUDE_PLUGIN_ROOT}/context/preferences/coding-rules.md"
```

**IMPORTANT**: Read this file at the start of coding sessions to avoid repeating mistakes.

## Add a New Rule

When told "stop doing X" or "never do Y again", add it to the rules file:

1. Open `${CLAUDE_PLUGIN_ROOT}/context/preferences/coding-rules.md`
2. Add under the appropriate section with this format:

```markdown
### [Today's Date] - [Short Description]
**What you did**: [Describe the behavior]
**Why it's bad**: [Why it's a problem]
**Instead**: [What to do instead]
```

3. Save and it will auto-sync to all machines

## Rule Categories

| Section | Purpose |
|---------|---------|
| NEVER DO THESE | Hard rules - violations are unacceptable |
| THINGS TO STOP DOING | Bad habits to correct |
| PREFERENCES | Soft preferences for style/approach |
| THINGS YOU DO WELL | Positive feedback to reinforce |

## Auto-Load

This file should be checked at the start of every coding session to avoid repeating past mistakes.
