# Personal Brain — System Architecture

**Created:** YYYY-MM-DD
**Last verified:** YYYY-MM-DD

---

## Purpose

This brain exists to give every AI session deep context beyond the prompt. The measure of success: when you type a prompt, the session already knows enough to avoid wrong assumptions.

Every file in this brain exists to eliminate a category of guessing.

---

## Design Doctrine

### 1. The brain IS the markdown files. Everything else is a disposable consumer.

Markdown + git is the most durable format in computing. If Claude Code dies, Obsidian dies, or any tool built on top of this brain dies, the brain itself is unchanged. Any tool that reads these files is a consumer, not a dependency.

**Corollary:** Never restructure the brain to accommodate a specific tool. Tools adapt to the brain, not the other way around.

### 2. Tool independence above all.

No paid services. No databases. No runtime dependencies. No APIs required to read the brain. A human with a text editor and a folder can use this brain. An LLM with file-read access can use this brain. That's the only requirement, forever.

### 3. The brain scales by growing, never by migrating.

New information = new files or updated files. Never a migration to a new system. The folder structure and conventions handle 50 files and 5,000 files the same way, because every directory has an index and every file has metadata.

### 4. Context injection is the primary job.

The brain is optimized for **retrieval** — quickly identifying and loading the right 3-8 files for any given task. Storage is already solved (markdown). The hard problem is: which files does this session need?

---

## Context Routing — The Librarian

**How retrieval works:** Read this routing table first. Match the task to the right rooms. Read each room's `_INDEX.md` to find the specific files. Read only what the task needs. Never scan all files.

| If the task involves... | Start here | Then check if needed |
|---|---|---|
| A specific client or prospect | `customers/{name}.md` | `ventures/` for capabilities |
| Writing copy or content | `preferences/writing-style.md` | The specific project in `projects/` |
| Business positioning or pitching | `ventures/{name}.md` | `customers/` for proof points, `projects/case-studies/` |
| A new campaign or initiative | Active files in `projects/` + `research/` | `history/` for what's been tried |
| An RFP or proposal | `ventures/{name}.md` + `projects/case-studies/` | `customers/` for relevant past work |
| How you think or make decisions | `preferences/profile.md` | `history/thinking-patterns.md` |
| Writing in your voice | `preferences/writing-style.md` | `history/` for communication patterns |
| Pipeline, deals, or CRM status | Relevant files in `projects/` | `customers/` for the specific deal |
| What's been tried before | `history/` files | `projects/` for experiment results |
| Brain architecture or maintenance | This file (`ARCHITECTURE.md`) | `CLAUDE.md` for session behavior |
| Something not in the table | Read `_INDEX.md` files in likely directories | Ask if nothing matches |

**Fallback rule:** If unsure which room, read the `_INDEX.md` of the 2 most likely directories. If still unsure, ask rather than scanning everything.

---

## Folder Structure

```
personal-brain/
├── ARCHITECTURE.md          <- You are here. System design, routing, conventions.
├── CLAUDE.md                <- Session behavior: what to do on every session.
├── README.md                <- Public-facing repo description.
├── context/
│   ├── _inbox.md            <- Unsorted captures. Review and file periodically.
│   ├── customers/           <- One file per client/prospect. Active relationships.
│   │   ├── _INDEX.md        <- Room description. Read before opening files.
│   │   ├── _archived/       <- Retired client files (historical, not active).
│   │   └── {name}.md
│   ├── history/             <- Reference material from past. Rarely changes.
│   │   ├── _INDEX.md
│   │   └── {topic}.md
│   ├── preferences/         <- Your identity, style, rules. Durable.
│   │   ├── _INDEX.md
│   │   └── {topic}.md
│   ├── projects/            <- Active and recent work. Changes frequently.
│   │   ├── _INDEX.md
│   │   ├── _archived/       <- Completed or abandoned projects.
│   │   ├── case-studies/    <- Proof points. Rarely changes.
│   │   └── {project}.md
│   ├── research/            <- Market data, competitive intel. Load on demand.
│   │   ├── _INDEX.md
│   │   └── {topic}.md
│   └── ventures/            <- Business entities you operate.
│       ├── _INDEX.md
│       └── {entity}.md
```

### Room Descriptions

| Directory | What it holds | When to read | Staleness risk |
|---|---|---|---|
| `customers/` | One file per named client/prospect. Deal status, contacts, history. | When the task names a company or person | High — deal statuses change fast |
| `history/` | Synthesized patterns from your past. Thinking patterns, communication style, business history. | When the task benefits from historical context | Low — patterns are durable |
| `preferences/` | Your identity, writing style, coding rules. | Almost always — these are the "always-load" files | Very low — identity and style are stable |
| `projects/` | Active campaigns, analyses, experiments, case studies. | When working on a specific initiative | Medium — active projects evolve |
| `research/` | Market research, competitive analysis, tool/repo evaluations. | When evaluating a market, offer, or tool | Medium — markets shift |
| `ventures/` | Business entity profiles. Company info, team, differentiators. | When positioning, pitching, or writing about your business | Low — company identity is stable |

---

## The Index System

Every directory has an `_INDEX.md` file. This is the "room description on the door" — an LLM reads it before opening any files in the directory.

### Index Format
```
# {Directory Name} — Index

**Last updated:** YYYY-MM-DD

## Active Files
- **filename.md** — One-line description. (Last verified: YYYY-MM-DD)

## Archived
- **_archived/old-file.md** — Why archived. (Archived: YYYY-MM-DD)
```

### Index Maintenance
- When adding a file to a directory, add it to the index.
- When archiving a file, move its entry to the Archived section.
- When updating a file significantly, update its one-line description.
- Indexes are the cheapest thing to regenerate — if one gets stale, rebuild it from the directory contents.

---

## File Conventions

### Naming
- Lowercase, hyphen-separated: `acme-corp.md`
- Descriptive enough to identify content from the filename alone
- Prefix with `_` for system files: `_INDEX.md`, `_TEMPLATE.md`, `_archived/`

### Required Headers (for files with factual claims)
```
**Created:** YYYY-MM-DD
**Last verified:** YYYY-MM-DD
```

### Source/Confidence Tagging

Not all information is equally trustworthy. When writing or updating a file, tag claims with their source so future sessions know how much weight to give them.

| Tag | Meaning | Example |
|---|---|---|
| `(source: direct)` | Said explicitly in conversation | "No closed deals from cold email" |
| `(source: API pull, YYYY-MM-DD)` | Pulled from a live API | Campaign metrics, deal counts |
| `(source: synthesized)` | Extracted from conversation history by AI | Thinking patterns, business history |
| `(source: inferred)` | AI analysis or interpretation, not directly stated | "Highest-engagement unconverted prospect" |
| `(source: external research)` | From web search, competitor analysis, market data | TAM estimates, competitor pricing |

**When to tag:**
- Always tag when a specific fact could be wrong and the error would matter
- Don't tag obvious stable facts (your name, company address, team roles)
- Don't tag every sentence — tag the claims that a future session might rely on for a decision

**How to use tags when reading:**
- `direct` = trust it unless clearly outdated
- `API pull` = trust it, but check the date — data decays
- `synthesized` = treat as best-available, but verify if acting on it
- `inferred` = treat as a hypothesis, not a fact — verify before relying on it
- `external research` = check the date and whether the market has shifted

### When to Create a New File vs. Update Existing
- **New file:** A genuinely new entity (new client, new project, new research topic)
- **Update existing:** New information about an existing entity (deal status change, new contact, revised metrics)
- **Never:** Create a file for a one-off fact. Put it in the relevant existing file or `_inbox.md`.

### When to Archive
- Move to `_archived/` when: project is completed/abandoned, client relationship is dormant for 6+ months, research is superseded by newer work
- Never delete. Archived files are still searchable when someone specifically needs historical context.
- Update the directory's `_INDEX.md` when archiving (move from Active to Archived section).

---

## Data Freshness

### The Convention
Every file with factual claims has `Created` and `Last verified` date headers.

### The Rules
1. **When you modify a file with fresh data:** bump `Last verified` to today's date.
2. **When starting a session:** if a file you're relying on has `Last verified` older than 60 days AND contains metrics, deal statuses, or market claims, flag it before using it.
3. **Preferences and style docs don't go stale this way** — identity and voice are stable.
4. **Git log is the backup:** `git log --format="%ai" -1 -- <file>` gives last modification date, but modification != verification.

---

## Filing Rules — Where Does New Information Go?

When new information arrives, follow this decision tree:

| # | If it's about... | File it in... |
|---|---|---|
| 1 | A specific company or person | `customers/{name}.md` (new file if new entity) |
| 2 | An active initiative with a start/end | `projects/{name}.md` |
| 3 | Your identity, style, or preferences | `preferences/{topic}.md` |
| 4 | A business entity you operate | `ventures/{name}.md` |
| 5 | Market data, competitors, or external research | `research/{topic}.md` |
| 6 | Historical synthesis (patterns from past data) | `history/{topic}.md` |
| 7 | Doesn't fit any room | **STOP and ask immediately.** Do not silently file it. Say what the information is, why it doesn't fit existing rooms, and propose options (new room, refile into existing, or drop it). Stage in `context/_inbox.md` only after deciding. Never create a new directory without explicit approval. |

**After filing:** add the file to the directory's `_INDEX.md`.

---

## Hook System (Claude Code Plugin)

The brain uses Claude Code's hook system for automatic sync and context injection.

All hooks live under `.claude-plugin/hooks/`. Claude Code loads them automatically when the brain is listed in the user's `pluginDirs`.

| File | Event | Purpose |
|---|---|---|
| `sync-start.sh` | SessionStart | `git pull` the latest brain from GitHub before session begins |
| `load-brain.py` | SessionStart | Inject core directive (`CLAUDE.md`) + `context/` file index |
| `keyword-inject.py` | UserPromptSubmit | Match prompt text against `keyword-map.json` and surface file pointers |
| `keyword-map.json` | (data) | Keyword to context file path lookup |
| `capture.py` | Stop | Scan last user message for memory triggers; append to `_inbox.md` |
| `sync-stop.sh` | Stop, PreCompact | If anything changed, commit + pull-rebase + push to GitHub |
| `_utils.py` | (shared) | Portable brain-root resolution and silent logging |

### Inbox Pattern
Auto-capture writes ONLY to `context/_inbox.md`, never into the structured tree. The inbox is a staging area. Trigger phrases: `remember`, `save this`, `note that`, `from now on`, `always`, `never`, `stop doing`, `don't`, `fyi`, `important:`, `for the record`, `add to my brain`.

### Failure Behavior
Every hook exits `0` on any error. A broken hook must never block the session. Errors go to `logs/<hookname>.log` (gitignored).

---

## Portability

This brain is platform-agnostic by design:

- **CLAUDE.md** contains Claude Code-specific session behavior. Rename to SYSTEM.md or BOOTSTRAP.md for another platform.
- **ARCHITECTURE.md** (this file) is platform-agnostic. Any LLM can follow the routing table and index system.
- **All content files** are standard markdown. No tool-specific formatting, no proprietary frontmatter, no database dependencies.
- **To switch platforms:** copy the folder, rename CLAUDE.md, done.

### To install on a new machine
1. `git clone https://github.com/YOUR_USERNAME/personal-brain.git ~/personal-brain`
2. Add that path to `pluginDirs` in `~/.claude/settings.json`
3. Ensure `python3`, `git`, and `bash` are on PATH
4. Start Claude Code. First SessionStart does `git pull`, loads brain, running.

**No hardcoded paths anywhere.** All hook scripts resolve root via `$CLAUDE_PLUGIN_ROOT` with script-relative fallback.

---

## Extending

- **Add a keyword-triggered context pointer:** edit `.claude-plugin/hooks/keyword-map.json`
- **Add a memory trigger phrase:** edit the `TRIGGERS` regex in `capture.py`
- **Add a new hook event:** add a script under `.claude-plugin/hooks/`, register in `hooks.json`, use `_utils.brain_root()` for paths
- **Add a new routing row:** edit the Context Routing table above
- **Add a new directory:** create the directory, add `_INDEX.md`, add a row to the Room Descriptions table

Keep hooks **idempotent** and **fast** (< 1 second). A slow Stop hook delays every turn.
