# Arcindex — Codex CLI Working Guide

Use this file to prime Codex CLI before taking actions in the repository. It summarizes the current vision (Arcindex), architecture plans, and in-progress migration work so every session can hit the ground running.

---

## 1. Mission Overview

- **Project Name:** Arcindex (Adaptive Review & Coordination with Integrated Development Experience)
- **Vision at Completion:** A self-contained CLI that orchestrates end-to-end software delivery by coordinating specialized agents (discovery → QA), capturing elicitation inputs, enforcing evidence-based quality gates, and generating implementation-ready artifacts that enable one-pass execution across multiple languages.
- **Lineage:** Builds on the BMAD Method (multi-agent planning, elicitation standards, checklist rigor) and the PRP system (context-rich implementation prompts) that informed the original CODEX implementation.
- **Goal:** Rebuild the legacy CODEX orchestration platform as a Python CLI powered by the OpenAI Codex SDK, preserving quality gates, elicitation, and multi-agent workflow coordination while modernizing the runtime and SDK abstraction.
- **Current Phase:** Migration Phase 0 (scaffolding `arcindex/`, Python environment, tooling baseline). Discovery orchestrator work begins in Phase 1.

---

## 2. Repository Layout

| Path | Purpose | Notes |
|------|---------|-------|
| `arcindex/` | Future home of the new CLI runtime, orchestrator, agents, tools, configs, tests | Mostly scaffolding during Phase 0 |
| `legacy/` | Archived CODEX implementation (reference only) | Contains `.codex/`, `.bmad-core/`, docs, PRPs, test harness |
| `MIGRATION-PLAN.md` | Source of truth for phased rebuild | Review before scoping tasks |
| `README.md` | Public-facing overview updated for Arcindex | Mirrors legacy structure with new status |
| `.github/` | Issue/PR templates, workflows (legacy copies live in `legacy/.github`) | Adjust as migration matures |

**Guardrail:** Avoid modifying `legacy/` unless a migration task explicitly calls for referencing or porting artifacts.

---

## 3. Active Objectives (Phase 0 → Phase 1)

1. **Bootstrap SDK Structure**
   - Create skeleton modules: `orchestrator/`, `agents/`, `tools/`, `resources/`, `config/`, `tests/`.
   - Add placeholder `__init__.py` files and package scaffolding.
2. **Environment & Tooling**
   - Define `requirements.txt` / `pyproject.toml`.
   - Add lint/test scripts (e.g., `make lint`, `make test`).
3. **Discovery Orchestrator Prep**
   - Draft workflow config stubs for `greenfield-discovery`.
   - Identify legacy templates/checklists needed for Phase 1 port.
4. **Documentation Hooks**
   - Keep README, MIGRATION-PLAN, and this guide in sync with completed items.

Reference `MIGRATION-PLAN.md` for the full roadmap through Phase 7.

---

## 4. Key Documents & Where to Look

- `MIGRATION-PLAN.md` — phased implementation plan (primary reference).
- `README.md` — up-to-date project description and expectations.
- `legacy/docs/` — legacy briefs, PRDs, architecture docs; useful when porting behavior.
- `legacy/.codex/` — legacy tasks, templates, workflows; source material for SDK translation.
- `legacy/.bmad-core/` — BMAD method references (checklists, agent instructions).

---

## 5. Working with Arcindex CLI

1. **Initialize Session**
   - Read this file.
   - Skim `MIGRATION-PLAN.md` for phase-specific details.
   - Confirm target phase in README’s roadmap table.

2. **When Editing**
   - Prefer `apply_patch` for single-file edits.
   - Note any assumptions or TODOs inline (Markdown comments, Python `TODO`).

3. **When Porting Legacy Artifacts**
   - Extract intent, not literal markdown.
   - Adapt structures for Python modules, YAML configs, or JSON state as appropriate.

4. **Testing Philosophy**
   - Create lightweight unit tests as you build out `arcindex/`.
   - Use `arcindex/test-harness/scripts/run-test.sh` to spin up disposable sandboxes for manual validation.
   - End-to-end harness will be reintroduced once discovery orchestrator is running.

5. **Logging Decisions**
   - Capture rationale in PR descriptions or short design notes (`docs/decisions/` once created).

---

## 6. Persona Alignment (for future SDK agents)

These are the target personas the SDK will expose; keep them in mind as you define configs:

| ID | Title | Core Responsibility |
|----|-------|---------------------|
| `orchestrator` | Arcindex Orchestrator | Manage workflow lifecycle, state persistence |
| `discovery` | Discovery Guide | Elicit project context, stakeholders, goals |
| `analyst` | Requirements Analyst | Generate structured requirements and insights |
| `pm` | Product Planner | Produce PRDs, stories, acceptance criteria |
| `architect` | System Architect | Craft architecture blueprints, epic-specific plans |
| `prp` | PRP Author | Create implementation-ready PRPs with validation commands |
| `dev` | Development Coordinator | Orchestrate validation levels, capture execution learnings |
| `quality-gate` | Quality Gate Specialist | Run checklists, scoring, evidence capture |
| `qa` | QA Reviewer | Deep quality analysis, failure escalation |
| `feedback` | Feedback Steward | Manage bi-directional feedback loops and learnings |

---

## 7. Contribution Checklist

Before finishing an Arcindex CLI session:

- [ ] Updated or confirmed relevant sections of README / migration plan / this guide.
- [ ] Added or adjusted SDK scaffolding according to the active phase.
- [ ] Documented new commands/tests or left TODO markers for follow-up.
- [ ] Mentioned any blockers or open questions in your hand-off notes.
