---
description: "Weekly retrospective. Reviews what happened this week across active projects and campaigns. Proposes brain updates so learnings don't drift."
argument-hint: "<optional: specific focus area> — leave blank for full retro"
allowed-tools: Bash, Read, Write, Glob, Grep
---

# /week-retro — Weekly Retrospective

A structured review of the week. Prevents context drift and ensures the brain stays current.

## Context to Load First

1. `context/projects/_INDEX.md` — what's active
2. `context/history/_INDEX.md` — recent additions
3. Git log for the last 7 days: `git log --since="7 days ago" --oneline` in the brain repo

## The Retro Structure

Walk through these questions. Record answers. Save updates.

### 1. What Shipped This Week
- Things published, launched, sent, completed
- Pull real data where available

### 2. What Got Signal
- Anything that worked unexpectedly well?
- Any engagement or traction you didn't expect?

### 3. What Bombed
- Anything that went nowhere?
- Does anything need to be killed?

### 4. What Changed in Your Thinking
- Any strategy pivots this week?
- Any new angles to test?

### 5. What's Stuck
- Anything being circled on without closure?
- Any decision being avoided?
- Flag for `/office-hours` if it needs forcing.

### 6. Who's Owed a Follow-Up
- Warm leads who haven't heard back
- Partners mid-conversation
- Commitments made that haven't landed

## Output Format

```
WEEK OF [dates]

SHIPPED:
- [specific items with metrics]

SIGNAL:
- [what worked + why]

DEAD / TO KILL:
- [what's bombing + recommendation]

PIVOTS IN THINKING:
- [changes this week]

STUCK:
- [things needing decision]

FOLLOW-UPS OWED:
- [name — last touch — suggested next step]

BRAIN UPDATES TO MAKE:
- [file to update]: [what to change]
- [new file to create]: [purpose]
```

## After the Retro

Propose specific brain updates. Don't make them without approval. Present as:

> "Should I update [file] with [change]?"
