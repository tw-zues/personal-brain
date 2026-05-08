---
description: "View or log error patterns - track bugs made and solutions found."
argument-hint: "view | add <error>"
allowed-tools: Bash, Read, Write, Edit
---

# Error Patterns Manager

Track errors made and how they were fixed, so they don't repeat.

## View Error Patterns

```bash
cat "${CLAUDE_PLUGIN_ROOT}/context/preferences/error-patterns.md"
```

**IMPORTANT**: Check this file when debugging to see if it's a known pattern.

## Log a New Error

When an error is fixed, add it to the log:

1. Open `${CLAUDE_PLUGIN_ROOT}/context/preferences/error-patterns.md`
2. Add under "## ERROR LOG" with this format:

```markdown
### [Today's Date] - [Error Type/Description]
**Error**: The actual error message or behavior
**Root Cause**: Why it happened
**Solution**: How it was fixed
**Prevention**: How to avoid this in the future
**Files Affected**: Which files/patterns to watch
```

## Search Past Errors

```bash
grep -i "<error keyword>" "${CLAUDE_PLUGIN_ROOT}/context/preferences/error-patterns.md"
```

## When to Use This

1. **Before debugging**: Check if it's a known pattern
2. **After fixing**: Log the error so it doesn't repeat
3. **When stuck**: Review common mistakes section
