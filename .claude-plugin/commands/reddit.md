---
description: "Deep Reddit research on a topic. Pulls posts + top comments across multiple sorts, grades on 6 dimensions with exponential recency decay, writes JSON + summary."
argument-hint: "<topic> — e.g., 'ServiceTitan complaints' or 'LLM eval harness'"
allowed-tools: Bash, Read, Write, Glob, Grep
---

# /reddit — Deep Reddit Research

Pulls Reddit data on a topic to surface operator voice / lived-experience perspectives. Produces a graded JSON + committed markdown summary.

## When invoked

Pull fresh Reddit data for the topic named. Not from training knowledge. Actually run the scraper.

## Steps

### 1. Classify recency sensitivity

- **fast-moving** (apply exponential recency decay) — AI/ML/LLMs, frameworks/tools, current events, products.
- **stable** (NO recency decay) — classic algorithms, data structures, math, fundamental CS.

State: `Classified as <fast-moving|stable> because <reason>. Say "override" to flip it.`

### 2. Scrape

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/reddit_search.py" \
  --topic "<topic>" \
  --limit 200 \
  --output "${CLAUDE_PLUGIN_ROOT}/../logs/research/reddit/<timestamp>_<slug>.json"
```

### 3. Grade on six dimensions

1. **Topicality** — what % actually mention the topic meaningfully?
2. **Volume sufficiency** — <20=low, 20-100=medium, >100=high
3. **Recency coverage** — bucket into 6-month windows going back 3 years
4. **Subreddit diversity** — count unique subs, name top 5
5. **Signal posts** — top 10 ranked by engagement * recency weight
6. **Sentiment/stance breakdown** — complain / ask / recommend / other

### 4. Write summary markdown

Write to `${CLAUDE_PLUGIN_ROOT}/../context/research/reddit/<timestamp>_<slug>.md`

### 5. Report back

Give a concise version and ask if they want to:
- Pull more from a specific subreddit
- Re-run with subreddit restriction
- Fetch more comments on a specific post
- Move on

## Notes

- Reddit search caps at ~250 results per sort. Scraper mixes sorts to widen coverage.
- Rate limits: unauthenticated = ~60 req/min. Scraper sleeps 1.2s between requests.
- If topicality < 70%, recommend re-running with a subreddit restriction.
