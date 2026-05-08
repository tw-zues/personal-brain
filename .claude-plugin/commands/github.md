---
description: "Deep GitHub research: find public repos that solve a stated problem. Pulls 100+ repos by stars, deep-dives READMEs + top issues on the best candidates, grades results."
argument-hint: "<problem or topic> — e.g., 'python retry decorator' or 'open-source LLM eval harness'"
allowed-tools: Bash, Read, Write, Glob, Grep
---

# /github — Deep GitHub Research

Surface public repos that solve a problem. Pull fresh data from the GitHub API, not training knowledge.

## Steps

### 1. Classify recency sensitivity

- **fast-moving** (penalize stale repos) — AI/ML/LLM tooling, new frameworks.
- **stable** (accept older repos) — classic algorithms, stable utility libs.

State: `Classified as <fast-moving|stable> because <reason>. Say "override" to flip it.`

### 2. Scrape

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/github_search.py" \
  --topic "<topic>" \
  --min-repos 100 \
  --deep 10 \
  --output "${CLAUDE_PLUGIN_ROOT}/../logs/research/github/<timestamp>_<slug>.json"
```

### 3. Grade

1. **Relevance** — how many actually solve the stated problem?
2. **Activity filter** — compute activity score with recency decay for fast-moving topics
3. **Top candidates (5-10)** — rank by stars * activity * relevance. Include: repo URL, stars, last commit, 1-2 sentence gist, notable issues, honest verdict
4. **Gaps surfaced** — recurring unsolved pain across repos

### 4. Write summary markdown

Write to `${CLAUDE_PLUGIN_ROOT}/../context/research/github/<timestamp>_<slug>.md`

### 5. Report

Top 3-5 candidates with honest verdict. Ask if they want:
- Deep-dive on a specific repo
- Re-search with refined query
- Focus on specific language/tag
- Move on

## Notes

- `GITHUB_TOKEN` env var enables 5000 req/hr (vs 60 unauthenticated) and deeper dives.
- GitHub returns max 1000 results per query. Scraper pulls up to first 100 by star rank.
