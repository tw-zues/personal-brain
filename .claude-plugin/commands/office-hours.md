---
description: "Pressure-test a strategic decision before committing. Forces questions, surfaces assumptions, names risks. Use before big moves."
argument-hint: "<decision> — e.g., 'launch the partnership program' or 'kill the email campaign'"
allowed-tools: Read, Write, Glob, Grep
---

# /office-hours — Strategic Decision Pressure-Test

Interrogate a decision before making it. This is the anti-agreeableness mode.

## Purpose

This command forces a decision into the open by making you answer specific, uncomfortable questions.

## Context to Load First

Whatever's relevant to the decision. Typical pulls:
- `context/projects/` — relevant active projects
- `context/history/` — has this been explored before?
- `context/ventures/` — does this align with positioning?
- `context/preferences/profile.md` — does this align with values and goals?

## The Interrogation

Ask these in order. Don't let vague answers slide. Push back.

### 1. The Goal Test
- What specifically are you trying to achieve?
- What would "this worked" look like in 30 days? 90 days?
- How will you know if it didn't?

### 2. The History Test
- Have you tried a version of this before? (Check brain.)
- If yes, what was different then? What's different now?
- Is this a re-run of a dead experiment or genuinely new?

### 3. The Assumption Test
- What are you assuming about the audience / market / capacity?
- Which of those assumptions are verified vs. hoped-for?
- What's the cheapest way to test the weakest assumption?

### 4. The Capacity Test
- Who's doing the work?
- What does this displace? (Opportunity cost.)
- Realistic hours/week sustained over the first 60 days?

### 5. The Commercial Test
- What's the expected revenue / outcome if it works?
- What's the cost if it doesn't?
- What's the ratio — is the upside worth the downside?

### 6. The Kill Criteria Test
- What metric or signal tells you to stop?
- When would you review and decide to kill?
- Will you actually kill it, or keep it on life support?

## Output Format

After answering, synthesize:

```
DECISION: [restate the decision]

WHAT HOLDS UP:
- [things with strong evidence]

WHAT'S THIN:
- [assumptions that could fail]

KILL CRITERIA:
- [specific measurable signal]
- [review date]

RECOMMENDATION: [commit / kill / modify before committing]
```

## The Anti-Agreeableness Standard

If the answers don't hold up, say so. The value of this command is in the friction, not the approval. Do NOT end with "great plan, let's ship it" unless the plan genuinely holds up under pressure.
