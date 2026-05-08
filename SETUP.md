# Setup On A New Machine

Goal: 100% identical brain experience on every machine you use Claude Code from.

This file is the authoritative bootstrap. If you only want to understand what the brain is, read `README.md` first.

---

## What You're Reproducing

The full experience on a working machine consists of these layers:

| Layer | What it does | Where it lives | How it gets to a new machine |
|---|---|---|---|
| **Brain repo** | All persistent context (markdown files) | `~/personal-brain/` | `git clone` |
| **Plugin registration** | Tells Claude Code to load the brain plugin | `~/.claude/settings.json` (per-machine) | Manual copy from `bootstrap/claude-settings.json.template` |
| **Plugin hooks** | SessionStart sync + context inject, UserPromptSubmit reminders, Stop capture + push | `.claude-plugin/hooks/` | Travels with the brain repo |
| **Slash commands** | `/search`, `/customer`, `/venture`, etc. | `.claude-plugin/commands/` | Travels with the brain repo |
| **Skills** (e.g. loop-break) | Portable Claude Code skills | `skills/<skill>/` | Travels with the brain, copy to `.claude/skills/` to activate |
| **Runtime requirements** | python3, git, bash on PATH | System | Install per machine |

What does NOT travel automatically:
- `~/.claude/settings.json` itself (per-machine config)
- Project-specific `.claude/projects/<name>/memory/` directories (per-machine, per-project Claude Code memory)
- Python interpreter and git binary (per-machine system)

---

## Step-By-Step Setup

### Step 1 — Verify prerequisites

You need these installed and on PATH:

```bash
git --version       # Any modern version
python3 --version   # 3.8+
bash --version      # Any
```

On Windows, Git Bash provides bash. On macOS/Linux, bash is built in.

---

### Step 2 — Clone the brain

Pick a stable home. Recommended: `~/personal-brain`.

```bash
git clone https://github.com/YOUR_USERNAME/personal-brain.git ~/personal-brain
cd ~/personal-brain
```

Verify the clone:

```bash
ls
# Expect: ARCHITECTURE.md  CLAUDE.md  README.md  SETUP.md  bootstrap  context  logs  skills
```

If the clone fails on auth, configure your git credentials for GitHub first.

---

### Step 3 — Configure Claude Code to load the brain plugin

This is the critical step. Without it, none of the brain's hooks fire.

**Copy the template:**

```bash
cp ~/personal-brain/bootstrap/claude-settings.json.template ~/.claude/settings.json
```

If `~/.claude/settings.json` already exists, merge the keys manually instead of overwriting.

**Edit `~/.claude/settings.json` and update `pluginDirs`** to match where you cloned the brain. Use forward slashes everywhere (Windows accepts them) or escape backslashes:

```json
{
  "pluginDirs": [
    "C:/Users/YourName/personal-brain"
  ],
  "effortLevel": "high"
}
```

Save the file. Restart Claude Code for the plugin to load.

---

### Step 4 — Fill in your profile

Before the brain can be useful, it needs to know who you are:

1. Edit `context/preferences/profile.md` — your identity, role, goals, values
2. Edit `context/preferences/writing-style.md` — your voice, tone, anti-patterns
3. Optionally add your first venture, customer, or project using the `_TEMPLATE.md` files

---

### Step 5 — Verify the plugin loaded

Start a fresh Claude Code session in any directory. Then ask Claude:

> Read CLAUDE.md and ARCHITECTURE.md from my brain. Then summarize: who am I and what does this brain contain?

You should get back a response based on the profile you filled in.

Also verify the auto-injected reminder fires. Type any prompt and look for the system message starting with `LOAD-BEARING INFERENCE CHECK`. If you see it, the UserPromptSubmit hook is working.

If neither verification works:
- Check `~/.claude/settings.json` has the correct `pluginDirs` path
- Check `~/personal-brain/logs/load-brain.log` and `sync-start.log` for hook errors
- Confirm python3, git, bash are on PATH

---

### Step 6 — Wire the brain into other projects

When you open Claude Code in a non-brain directory (e.g. `~/myproject/`), the SessionStart hook still fires (because it's plugin-scoped, not project-scoped). The brain context loads regardless of working directory.

Optional: add a project-level `CLAUDE.md` in each working project that gives Claude project-specific orientation on top of the brain.

---

### Step 7 — Understand the indexing setup

This is how Claude finds the right files for any task. Three layers, all auto-loaded by the SessionStart hook.

**Layer 1: The routing table (in `ARCHITECTURE.md`)**

Maps task types to starting directories. Claude's first-pass librarian. Read once at session start, used to route every prompt.

**Layer 2: Per-directory `_INDEX.md` files**

Every `context/` subdirectory has an `_INDEX.md` listing its files with one-line descriptions and freshness dates. The `load-brain.py` hook concatenates ALL `_INDEX.md` files at session start and injects them.

**Layer 3: Keyword-triggered context pointers (`keyword-map.json` + `keyword-inject.py`)**

When you submit a prompt, `keyword-inject.py` matches your prompt text against the map and surfaces relevant file paths inline.

To see what keywords exist:

```bash
cat ~/personal-brain/.claude-plugin/hooks/keyword-map.json
```

To add a new keyword trigger: edit `keyword-map.json` and add a `"keyword": "context/path/to/file.md"` entry.

**What auto-injects vs. what Claude pulls on demand**

| Auto-injected at SessionStart | Pulled by Claude on demand |
|---|---|
| `CLAUDE.md` (session behavior) | Specific files matched to the task |
| Routing table from `ARCHITECTURE.md` | Files referenced by `_INDEX.md` entries |
| All `_INDEX.md` files (concatenated) | Files surfaced via keyword-inject |
| Flat file listing (fallback) | Anything Claude looks up explicitly |

So at session start, Claude has the MAP but not the territory. It pulls the territory (specific markdown files) only as the conversation needs it. This keeps the context window clean.

---

### Step 8 — Daily use

| When | What happens |
|---|---|
| Start of session | `sync-start.sh` runs `git pull` to get latest from any other machine |
| Start of session | `load-brain.py` injects CLAUDE.md, the routing table, and all `_INDEX.md` files |
| Every prompt you send | `ask-over-assume-reminder.json` injects the load-bearing inference check |
| Every prompt you send | `keyword-inject.py` matches your prompt against `keyword-map.json` and surfaces relevant context files |
| End of session | `capture.py` scans for trigger phrases ("remember," "save this," etc.) and appends to `_inbox.md` |
| End of session | `sync-stop.sh` commits any changes and pushes to GitHub |

You don't run any of this manually. It's all automatic once Step 3 is done.

---

## Updating Across Machines

When you change the brain on one machine:

```bash
cd ~/personal-brain
git add .
git commit -m "Updated X"
git push
```

(The Stop hook does this automatically if anything changed during the session.)

On any other machine, before your next session:

```bash
cd ~/personal-brain
git pull
```

(The SessionStart hook does this automatically.)

---

## Troubleshooting

### "Claude isn't using brain context"

Most likely cause: the plugin isn't loading.

1. Check `~/.claude/settings.json` exists and has `pluginDirs` pointing to your brain location
2. Check `~/personal-brain/logs/load-brain.log` — if empty or missing, the SessionStart hook isn't firing
3. Run the SessionStart hook manually to see errors:
   ```bash
   bash ~/personal-brain/.claude-plugin/hooks/sync-start.sh
   bash ~/personal-brain/.claude-plugin/hooks/run-python.sh ~/personal-brain/.claude-plugin/hooks/load-brain.py
   ```
4. Restart Claude Code

### "The load-bearing inference check isn't firing"

1. Confirm `.claude-plugin/hooks/ask-over-assume-reminder.json` exists
2. Confirm `.claude-plugin/hooks/hooks.json` lists it under `UserPromptSubmit`
3. If your `~/.claude/settings.json` has its OWN UserPromptSubmit hook, they may conflict

### "Sync isn't working"

- Check `~/personal-brain/logs/sync-start.log` and `sync-stop.log`
- Verify git credentials work: `cd ~/personal-brain && git pull` and `git push` manually
- Make sure `python3`, `git`, `bash` are on PATH

### "Claude is trying to use built-in memory tools instead of the brain"

Tell it: "Stop. Read the markdown files in `~/personal-brain`. Don't use any built-in memory or scratchpad tools." This is documented as an anti-pattern in `CLAUDE.md` but some sessions still try to fall back to internal memory.

### "Slash commands aren't working"

Check `.claude-plugin/commands/` — if they aren't showing up:
- Plugin isn't loading (see above)
- Restart Claude Code after updating settings.json

---

## What If The Brain Repo Goes Down?

The brain is just markdown files. If GitHub is down, all tooling fails, or any tool breaks:

- The folder still exists on disk
- You can read every file with any text editor
- You can re-explain context to any AI manually using the files as reference
- Nothing is locked into a proprietary format

This is by design. See `ARCHITECTURE.md` Design Doctrine.
