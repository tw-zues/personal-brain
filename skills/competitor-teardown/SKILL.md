---
name: competitor-teardown
description: "Analyze competitor websites to learn what's working in the field and figure out how to stand out positively. Produces structured per-competitor analyses + cross-competitor synthesis. Posture is learn-and-borrow, not attack."
allowed-tools:
  - WebFetch
  - WebSearch
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Agent
---

# Competitor Teardown

Analyze competitor websites to extract positioning, case study quality, sales motion, and differentiators. Output is markdown files — no PDFs, no battle cards.

## When to trigger

- User provides one or more competitor URLs
- User says "teardown this site" / "analyze this shop" / "what does X do that we don't"
- User asks comparison questions

## Companion files (load when running an analysis)

- `dimensions.md` — full scoring rubric for all 8 dimensions, with the deep Sales Motion treatment. **Read this before starting any analysis.**
- `output-template.md` — per-competitor and synthesis markdown skeletons. **Read this before writing any output file.**

## Methodology (per competitor)

For each competitor URL, run four passes:

1. **Crawl pass** — `WebFetch` pages in this order:
   - Homepage
   - Services / Offerings / What we do
   - Case studies / Work / Portfolio (index + 2-3 individual case studies)
   - Blog (index + 3 most recent posts)
   - Pricing (if exists)
   - About / Team
   - Footer (industries, certifications, locations)

2. **Extract pass** — pull structured data into the 9-dimension schema in `dimensions.md`. **Sales Motion (#5) gets a 6-sub-dimension deep dive.**

3. **Score pass** — assign 0-3 per dimension/sub-dimension with **evidence quotes** and confidence tags:
   - `[Confirmed]` — directly stated on their site
   - `[Estimated]` — strong inference from copy/structure
   - `[Inferred]` — best guess from indirect signal

4. **Synthesize pass** — write the per-competitor file using the template in `output-template.md`.

### When a site is unreachable

Do not write a partial analysis file. Report the failure and ask whether to skip, retry, or have content pasted manually.

## Cross-competitor synthesis

After 3+ competitors are analyzed, automatically run a synthesis pass. Re-run when 2+ new competitors are added.

## Critical rules

- **Every claim needs evidence.** Quote the source language. No vibes.
- **Every claim gets a confidence tag.** `[Confirmed]` / `[Estimated]` / `[Inferred]`.
- **Always check for IP-ownership / "you own the code" language** under dimension 6.
- **Posture: learn, don't attack.** Frame analyses as "what's working here that we can borrow" and "how to stand out positively." Never write adversarial copy.
