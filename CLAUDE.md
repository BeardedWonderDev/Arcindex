# Claude Project Guidelines

## AI Workflow Artifact Policy

**When analyzing artifacts:** Read `.claude/artifact-policy-reference.md` for complete rules.

**Ultra-quick rules:**
- `.codex/**` → KEEP (product code)
- `docs/**`, `PRPs/**`, `.bmad-core/**` → REMOVE (artifacts)
- Root docs (README, ROADMAP, etc.) → KEEP
- Uncertain? → Read detailed reference

**Two workflows:**
- `@claude-artifacts` → Full PR analysis (ai-artifact-cleanup.yml)
- `@claude keep/remove X` → Learning responses (claude.yml)

## Core Principles

**Beta Development Philosophy (Pre-v0.1.0):**

- **Fix-forward** — No backwards compatibility; remove deprecated code immediately
- **Detailed errors over graceful failures** — Identify and fix issues fast
- **Break things to improve them** — Rapid iteration, embrace breaking changes
- **Continuous improvement** — Learn from mistakes, iterate quickly
- **KISS** — Keep workflows simple and readable
- **DRY when appropriate** — Reuse patterns, but not prematurely
- **YAGNI** — Don't implement features that aren't needed yet
- **Clear over clever** — Workflows should be obvious, not optimized for brevity
- **Validate early** — Use quality gates to catch issues at phase boundaries
- **Document decisions** — Track architectural choices in ROADMAP.md
- **One source of truth** — `.codex/` is product code; everything else is artifacts

**For detailed development guidance:** `.claude/development-reference.md`

## Project Context

**CODEX** - AI Agent Workflow System (Pre-v0.1.0, 85% complete)
**Product Code:** `.codex/` directory only (agents, workflows, tasks, state, checklists)

## Documentation

- **Development Reference:** `.claude/development-reference.md` (for Claude Code)
- **Artifact Policy:** `.claude/artifact-policy-reference.md`
- **Contributors:** `CONTRIBUTING.md` (for humans)
- **User Guide:** `CODEX-User-Guide.md`
- **Workflow Guide:** `CODEX-Workflow-Guide.md`
