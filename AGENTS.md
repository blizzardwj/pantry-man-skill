# AGENTS.md — Guide for Coding Agents

This repository is **pantry-man-skill**: a skill for AI agents to manage home pantry inventory, shopping lists, and purchase history. It follows the **Open Agent Skills specification** and must work with ANY agent (Claude Code, Cursor, Cline, Codex, Gemini CLI, etc.), not just Hermes.

## Repository Layout

```
SKILL.md                 # The skill itself (agent-facing instructions)
references/schema.md     # JSON data schemas (pantry.json, shopping.json, history)
README.md                # User-facing docs (installation, usage)
IDEAS.md                 # Idea backlog — NOT-YET-implemented ideas
DECISIONS.md             # Decision record — every design decision + rationale
LICENSE                  # MIT
```

## Hard Rules

1. **Never break cross-agent compatibility.** Use `[AGENT_HOME]` as the placeholder for the agent's home directory — never hardcode `~/.hermes`, `~/.claude`, or any single agent's path. The skill must read identically for every agent.

2. **No code, no scripts.** This is a prompt/instruction skill. Changes should be to instructions and schemas, not executable code. If you think code is needed, record it as an idea in `IDEAS.md` first and discuss before implementing.

3. **Keep instructions unambiguous.** Every operation the skill describes (read, add, remove, check, record) must be stated as a concrete step with a defined data path and schema reference. Agents execute these literally.

4. **Data files are user data, never commit them.** `pantry/data/` is gitignored — users create their own data.

## Workflow

### When you have a new idea (not yet implementing)
1. Append to `IDEAS.md` using the template at the top of the file.
2. Mark status as `idea`.
3. Only move to `planned` when the user decides to implement it.

### When you make a design decision
1. Record it in `DECISIONS.md` (newest first) using the template.
2. Include: the decision, the rationale, and **rejected alternatives** with why they were rejected.
3. Reference the implementing commit if applicable.

### When implementing a change
1. Update `SKILL.md` first — it is the source of truth for agent behavior.
2. If the change touches data structures, update `references/schema.md` in the same change.
3. Update `README.md` only if the change affects user-facing features or installation.
4. Mark the related idea in `IDEAS.md` as `implemented` and link the commit.

### Dropped ideas
Do NOT delete dropped ideas from `IDEAS.md`. Mark them `dropped` with the reason — they tell future agents which paths are dead ends.

## Commit Conventions

Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` — new agent-facing capability in SKILL.md
- `docs:` — documentation (README, AGENTS.md, IDEAS.md, DECISIONS.md, schema docs)
- `chore:` — housekeeping (gitignore, CI, config)

Keep the subject concise; add a body explaining the **why** when it's not obvious from the diff.

## Verification Checklist (before declaring a change done)

- [ ] SKILL.md frontmatter intact (`name: pantry-man`, `description` accurate)
- [ ] All file paths referenced in SKILL.md match actual files (e.g., `references/schema.md`)
- [ ] Schema changes are reflected in both SKILL.md and `references/schema.md`
- [ ] No agent-specific paths or commands introduced (check for `~/.hermes`, `~/.claude`, `cron add`, etc.)
- [ ] IDEAS.md statuses are up to date; DECISIONS.md has an entry for this change if it was a design decision
