# Portable Claude Code Skills

Skills built collaboratively with Claude that live in the brain so they're available across machines. Each skill is a self-contained folder with a `SKILL.md` plus optional companion files.

## How to install on a new machine

These are **portable definitions, not deployed installations** — consistent with the brain doctrine that "the brain IS the markdown files." To use a skill, copy its folder to the right `.claude/skills/` directory:

**For project-level use** (skill activates only inside one project):
```bash
cp -r ~/personal-brain/skills/<skill-name> <project-root>/.claude/skills/
```

**For user-level use** (skill activates in every Claude Code session):
```bash
cp -r ~/personal-brain/skills/<skill-name> ~/.claude/skills/
```

Skills load at session start. After copying, open a fresh Claude Code session in the relevant directory and the skill is registered.

## Current skills

| Skill | Purpose | Recommended install scope |
|---|---|---|
| [competitor-teardown](competitor-teardown/) | Analyze competitor websites — positioning, case study quality, deep sales-motion teardown, cross-competitor synthesis. | Project-level |
| [estimate](estimate/) | Quick project estimation from a job post or project description — phase breakdown, cost range, timeline, risks, and bid recommendation. | User-level (`~/.claude/skills/`) |
| [loop-break](loop-break/) | Breaks psychological thought loops using clinically grounded pattern interrupts. Applies to business ruts, marketing blind spots, relationship patterns, and creative blocks. | User-level (`~/.claude/skills/`) |

## Convention for adding a new skill

1. Build and test the skill in its native project (e.g., `<project>/.claude/skills/<skill>/`).
2. Once it's proven, `cp -r` the entire skill folder into `~/personal-brain/skills/`.
3. Add a row to the table above with the recommended install scope.
4. Commit + push the brain.

The skill's content (SKILL.md, companion files, scripts, templates) lives here as the canonical source. The deployed copy in `<project>/.claude/skills/` or `~/.claude/skills/` is a working copy — re-sync from the brain when updating across machines.
