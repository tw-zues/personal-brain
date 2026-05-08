# Personal Brain

Persistent context for AI sessions. Markdown + git. Works on any machine, any AI tool that can read files.

## What This Is

A folder of markdown files containing everything an AI session needs to work with you without re-explaining context every time:

- Who you are (identity, role, voice, preferences)
- What you're building (ventures, active projects, customers)
- How you work (rules, anti-patterns, style)
- What's been tried (project history, dead experiments, wins)
- Reference material (research, competitive analysis, best practices)

The brain is the markdown files. Everything else is a disposable consumer.

## Quick Start

```bash
# 1. Fork this repo on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/personal-brain.git ~/personal-brain

# 2. Fill in your profile
#    Edit context/preferences/profile.md with your info
#    Edit context/preferences/writing-style.md with your voice

# 3. Register the plugin with Claude Code
cp ~/personal-brain/bootstrap/claude-settings.json.template ~/.claude/settings.json
#    (edit pluginDirs path if you cloned elsewhere)

# 4. Start Claude Code — brain auto-loads
```

See `SETUP.md` for the full walkthrough.

## How To Use It (For Any AI Session)

**On every session, in this order:**

1. Read `CLAUDE.md` — session behavior directive
2. Read `ARCHITECTURE.md` — system design + routing table (which files to read for which task)
3. Match the current task to the routing table
4. Read the relevant `_INDEX.md` files
5. Read only the specific files the task needs

**Critical:** read the actual markdown files. Do not use built-in memory tools, scratchpad summaries, or AI-managed memory features to reconstruct what's already in the files. The files are the source of truth.

## Directory Structure

```
personal-brain/
├── CLAUDE.md              <- Session behavior. Read first.
├── ARCHITECTURE.md        <- Routing table + system design. Read second.
├── README.md              <- This file.
├── SETUP.md               <- New-machine setup walkthrough.
├── bootstrap/             <- Templates for per-machine config (settings.json).
├── .claude-plugin/        <- Plugin scaffold: hooks, slash commands, scripts.
├── context/
│   ├── _inbox.md          <- Unsorted captures. Review and file periodically.
│   ├── customers/         <- One file per client/prospect.
│   ├── history/           <- Synthesized patterns from your past.
│   ├── preferences/       <- Identity, voice, rules.
│   ├── projects/          <- Active campaigns, analyses, experiments.
│   ├── research/          <- Market data, competitive intel.
│   └── ventures/          <- Business entity profiles.
├── skills/                <- Portable Claude Code skill definitions.
└── logs/                  <- Hook logs (gitignored).
```

Every `context/` subdirectory has an `_INDEX.md` file describing its contents. Read the index before opening files in that directory.

## How Sync Works

1. **Session start:** `git pull` to get the latest brain from any other machine
2. **Session end:** `git commit && push` to save new context

If using the Claude Code plugin, hooks handle sync automatically (`sync-start.sh` and `sync-stop.sh`).

If running manually: just `git pull` before working and `git push` when done.

## What To Do With New Information

When the AI learns something worth saving:

| Type | File it in |
|------|------------|
| Specific company or person | `context/customers/{name}.md` |
| Active initiative | `context/projects/{name}.md` |
| Your identity, style, or rules | `context/preferences/{topic}.md` |
| Business entity | `context/ventures/{name}.md` |
| Market data / competitors | `context/research/{topic}.md` |
| Pattern from your past | `context/history/{topic}.md` |
| Doesn't fit any room | Stage in `context/_inbox.md`, ask where it belongs |

After filing, update the directory's `_INDEX.md`.

## Anti-Patterns (Things AI Should NOT Do)

- Do not use built-in memory palace, scratchpad, or AI-managed memory tools to "remember" things that should be in the brain. Write them to the brain instead.
- Do not construct summaries of the brain in conversation context. Read the actual files when you need them.
- Do not ignore the routing table and scan all files. Use the routing table to load only what the task needs.
- Do not create a new top-level directory without asking first.
- Do not skip reading `CLAUDE.md` and `ARCHITECTURE.md` at session start.

## Customizing

This is a template. Make it yours:

1. **Fill in your profile** — `context/preferences/profile.md`
2. **Add your writing style** — `context/preferences/writing-style.md`
3. **Add your first customer** — copy `context/customers/_TEMPLATE.md`
4. **Add your first venture** — copy `context/ventures/_TEMPLATE.md`
5. **Customize the routing table** — edit `ARCHITECTURE.md` to match your work
6. **Add keyword triggers** — edit `.claude-plugin/hooks/keyword-map.json`
7. **Add slash commands** — create new `.md` files in `.claude-plugin/commands/`

## License

MIT
