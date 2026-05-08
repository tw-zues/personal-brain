---
description: "Suggest a new pattern or context category to add to the brain."
argument-hint: "<pattern description>"
allowed-tools: Bash, Read, Write, Edit
---

# Pattern Suggestion

When you notice a pattern that should be saved but doesn't fit existing categories, use this command to suggest it.

## When to Suggest

Proactively identify patterns like:
- **Repeated context** you keep having to re-explain
- **New client/project** that deserves its own file
- **Recurring errors** that should be logged
- **Preferences** you keep stating
- **New category** that would be useful

## How to Suggest

Present the suggestion:

```
PATTERN DETECTED

**What I noticed**: [describe the pattern]
**Suggested category**: [where it should go, or suggest a new category]
**Why it matters**: [how this will save time]

Should I add this to your brain?
- Yes, add it to [location]
- No, skip it
- Create a new category for this
```

## If Approved

1. **Existing category**: Add to the appropriate file in `context/`
2. **New category**:
   - Create `context/<new-category>/` directory
   - Create `_INDEX.md` with the standard format
   - Create `_TEMPLATE.md` with appropriate structure
   - Create the first entry
   - Optionally add a new command in `.claude-plugin/commands/`

## Examples of Patterns to Catch

- "You keep asking me about my tech stack preferences"
- "This is the third time I've explained our deployment process"
- "You made this same database error last week"
- "Every project I work on uses these same libraries"
- "I always want commits formatted this way"
