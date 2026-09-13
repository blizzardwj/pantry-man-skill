# AGENTS.md — Guide for Coding Agents

This repository is **pantry-man-skill**: a skill for AI agents to manage home pantry inventory, shopping lists, and purchase history. It follows the **Open Agent Skills specification** and must work with ANY agent (Claude Code, Cursor, Cline, Codex, Gemini CLI, etc.), not just Hermes.

## Repository Layout

```
SKILL.md                 # The skill itself (agent-facing instructions)
references/              # On-demand docs (schema, quantity benchmarks, feedback flow, ingredient knowledge)
dev/                     # Architecture proposals, development validation, regression cases, and fixtures
AGENTS.md                # Contributor instructions for coding agents
README.md                # User-facing docs (installation, usage)
IDEAS.md                 # Problems, implementation progress, and outcome/evidence links
DECISIONS.md             # Decisions, rationale, consequences, and validity/supersession
RESEARCH.md              # Research progress, evidence, candidate designs, and limitations
LICENSE                  # MIT
.gitignore               # User data and local artifact exclusions
```

`scripts/` is optional and has not been created. It may contain deterministic runtime helpers (JSON checks, quantity arithmetic, deduplication); see Hard Rule #2. `dev/` contains design documents and development-only validation and is not part of the skill distribution.

## Hard Rules

1. **Never break cross-agent compatibility.** Use `[AGENT_HOME]` as the placeholder for the agent's home directory — never hardcode `~/.hermes`, `~/.claude`, or any single agent's path. The skill must read identically for every agent.

2. **No-code core, optional scripts.** The skill's contract (SKILL.md + references) must stay pure prompt/schema — any agent must be able to use it with zero code execution. An optional `scripts/` directory may provide deterministic helpers (JSON integrity check, quantity arithmetic, dedup) that agents with a shell run for stronger guarantees; the skill must remain fully usable without them (graceful degradation). Scripts never replace LLM judgment (pairing generation, health advice).

3. **Keep instructions unambiguous.** Every operation the skill describes (read, add, remove, check, record) must be stated as a concrete step with a defined data path and schema reference. Agents execute these literally.

4. **Data files are user data, never commit them.** `pantry/data/` is gitignored — users create their own data.

## Workflow

### Documentation ownership and history
1. Use the templates and explicit stable anchors in each document. `IDEA-NNN` identifies an idea, `DEC-NNN` a decision; preserve existing `RQ-5`, `RQ-6`, `RQ-A`, and `RQ-C` research IDs. Never renumber or reuse IDs. New numeric research IDs start at RQ-7.
2. `IDEAS.md` alone owns implementation progress; `RESEARCH.md` alone owns research progress; `DECISIONS.md` alone owns decision validity. Link to the owner instead of copying its current status. Research completion, decision acceptance, implementation completion, and demonstrated effectiveness are distinct.
3. Keep current summaries separate from historical discussion. Important changes append a dated reason and evidence link in chronological order. Retain rejected/superseded conclusions and link their successors; do not rewrite history to match today's implementation.
4. Preserve original event dates; record update/backfill dates separately. Do not infer approval dates from Git timestamps. Mark retrospective summaries as such.
5. IDEAS and RESEARCH preserve existing body order and append new entries; indexes provide navigation without duplicating status. DECISIONS stays newest first. Historical proposals and decision records are development context, not runtime instructions; `SKILL.md` and its referenced contracts define current behavior.

### When you have a new idea (not yet implementing)
1. Append to `IDEAS.md` using the template at the top of the file.
2. Mark status as `idea`.
3. Only move to `planned` when the user decides to implement it.
4. Before implementation, define scope/completion criteria and link any research, decisions, and predecessor/successor ideas. Starting research does not itself authorize implementation.

### When investigating a research question
1. Create or update the linked `RESEARCH.md` entry with a research state: `open`, `investigating`, `concluded`, or `paused` (include the reason when paused or reopened).
2. Separate evidence and locatable sources from project inference and hypotheses. Record comparison criteria, alternatives, limitations, and unresolved questions.
3. Link the resulting decision; retain dated candidate designs as history. Track implementation only through the linked IDEAS entry. Small changes do not require a research entry.

### When you make a design decision
1. Record it in `DECISIONS.md` (newest first) using the template.
2. Include context, the decision, rationale, **rejected alternatives** and reasons, consequences (benefits and costs), and related idea/research or direct evidence.
3. Use decision state `proposed`, `accepted`, `superseded`, or `deprecated`. A replacement must link both ways and specify whether it replaces the entire decision or only part; keep a partially applicable decision accepted and describe the remaining scope.
4. Link the IDEAS implementation/verification entry. For historical decisions without an idea entry, link the implementation and evidence directly without introducing a second implementation-status field.

### When implementing a change
1. For agent behavior changes, update `SKILL.md` first — it is the source of truth for agent behavior. Development-documentation-only changes update their governing documents without unnecessary runtime edits.
2. If the change touches data structures, update `references/schema.md` in the same change.
3. Update `README.md` only if the change affects user-facing features or installation.
4. Set the related idea to `implementing` when work begins, then `implemented` when its scope is complete. Link implementation commits/PRs and verification results with their coverage and remaining limitations. Before a commit exists, explicitly record “current working tree / not yet committed”; add the commit link when committing, never invent a hash.
5. Test definitions are not execution evidence. If historical results cannot be found, record that gap; distinguish checks that passed from user outcomes still awaiting observation. Longer reports belong in `dev/` and are linked from IDEAS.

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
- [ ] Documentation IDs/anchors are unique and related links resolve; each state is maintained only by its owning document
- [ ] Important transitions retain dated reasons and successor links; completion records link implementation and verification evidence or explicitly state the missing evidence
