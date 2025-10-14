# Arcindex — Codex CLI Working Guide

Use this file to prime Codex CLI before taking actions in the repository. It summarizes the current vision (Arcindex), architecture plans, and in-progress migration work so every session can hit the ground running.

---

## 1. Mission Overview

- **Project Name:** Arcindex (Adaptive Review & Coordination with Integrated Development Experience)
- **Vision at Completion:** A self-contained CLI that orchestrates end-to-end software delivery by coordinating specialized agents (discovery → QA), capturing elicitation inputs, enforcing evidence-based quality gates, and generating implementation-ready artifacts that enable one-pass execution across multiple languages.
- **Lineage:** Builds on the BMAD Method (multi-agent planning, elicitation standards, checklist rigor) and the PRP system (context-rich implementation prompts) that informed the original CODEX implementation.
- **Goal:** Rebuild the legacy CODEX orchestration platform as a Python CLI powered by the OpenAI Codex SDK, preserving quality gates, elicitation, and multi-agent workflow coordination while modernizing the runtime and SDK abstraction.
- **Current Phase:** Phase 1 (discovery orchestrator parity – event/agent runtime overhaul).

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

## 3. Active Objectives (Phase 1)

1. **Event & Artifact Infrastructure**
   - Implement the Phase 1 event emitter and artifact store so discovery runs write to `runs/<run_id>/`.
   - Update workflow/state persistence to operate against run-scoped directories.
2. **Discovery Agent Modernization**
   - Port the legacy discovery prompt into the new BaseAgent, generating summaries via the Codex SDK.
   - Migrate `advanced-elicitation.md` and the method catalog so menu selections transform the summary.
3. **Runner & Streaming CLI**
   - Build the asynchronous runner skeleton and hook CLI output to the event stream.
   - Prepare the SSE bridge adapter (FastAPI) so external clients can subscribe once discovery parity is verified.

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
   - Activate the project virtual environment (`source .venv/bin/activate`) so CLI commands and tests run against the repo-managed Python toolchain.

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
