# Arcindex - Codex CLI Working Guide

Use this file to prime the Codex CLI before making changes in the repository. It captures the Arcindex vision, the quickstart-aligned migration strategy, and the current priorities so every session stays in sync with the latest plan.

---

## 1. Mission Overview

- **Project Name:** Arcindex (Adaptive Review & Coordination with Integrated Development Experience)
- **Vision at Completion:** Deliver a Python-first CLI that orchestrates the full software-delivery workflow (discovery -> QA) by coordinating Codex SDK agents, enforcing guardrails, and persisting artefacts for one-pass execution across multiple languages.
- **Lineage:** Builds on the BMAD Method (multi-agent planning, elicitation standards, checklist rigor) and the PRP system (context-rich implementation prompts) that informed the original CODEX implementation.
- **Goal:** Rebuild the legacy CODEX orchestration platform using the official OpenAI Codex Agents SDK quickstart patterns, keeping quality gates and multi-agent coordination while modernising the runtime.
- **Current Phase:** Phase 0 (Codex quickstart alignment and MCP bootstrap).

---

## 2. Repository Layout

| Path | Purpose | Notes |
|------|---------|-------|
| `arcindex/` | Home for the new CLI runtime, agent workflows, guardrails, and tests | Tracks quickstart structures as modules are introduced |
| `bridge/` | FastAPI and SSE bridge experiments | Will be updated after multi-agent parity lands |
| `legacy/` | Archived CODEX implementation (reference only) | Contains `.codex/`, `.bmad-core/`, docs, PRPs, test harness |
| `MIGRATION-PLAN.md` | Source of truth for the phased rebuild | Updated to mirror Codex quickstart workflows |
| `README.md` | Public-facing overview | Hold off on edits until more development is complete |

**Guardrail:** Avoid modifying `legacy/` unless a migration task explicitly calls for referencing or porting artefacts.

---

## 3. Active Objectives (Phase 0)

1. **Codex MCP Bootstrap**
   - Install quickstart-required packages (`openai`, `openai-agents`, `python-dotenv`) inside the project virtual environment.
   - Verify Node.js >=18 and confirm `npx codex --version` works.
   - Add and smoke test `scripts/codex_mcp.py`, which launches the Codex CLI MCP server exactly like the quickstart (`npx -y codex mcp`).
2. **Discovery Workflow Baseline**
   - Implement `arcindex/workflows/discovery.py` using the quickstart single-agent example.
   - Provide a thin CLI command (`arcindex discovery run`) that invokes the workflow coroutine.
   - Write an integration test confirming `Runner.run` completes and Codex MCP startup/shutdown behaves as expected.
3. **Multi-Agent Pipeline Scaffolding**
   - Port the quickstart multi-agent orchestration (orchestrator -> discovery -> analyst) into `arcindex/workflows/discovery_to_analyst.py`.
   - Ensure every agent attaches the Codex MCP server via `MCPServerStdio`.
   - Begin drafting guardrail hooks for discovery and analyst outputs, following quickstart guardrail patterns.

Reference `MIGRATION-PLAN.md` for the full roadmap through Phase 7.

---

## 4. Key Documents

- `MIGRATION-PLAN.md` - Phased plan aligned with the Codex quickstart, including code scaffolds.
- `README.md` - Public summary (avoid changes until the CLI milestones solidify).
- `legacy/docs/` - Legacy briefs, PRDs, architecture docs; source material for porting behaviour.
- `legacy/.codex/` - Legacy tasks, templates, workflows; use for understanding historical prompts.
- `legacy/.bmad-core/` - BMAD method references (checklists, agent instructions).

---

## 5. Working with Arcindex CLI

1. **Initialize the Environment**
   - Read this guide and skim `MIGRATION-PLAN.md` to confirm the current phase.
   - Activate the project virtual environment before running Python commands:
     ```bash
     python3 -m venv .venv             # run once per machine
     source .venv/bin/activate         # required every session
     python -m pip install --upgrade pip
     python -m pip install openai openai-agents python-dotenv
     ```
   - Keep the venv active for `python`, `pip`, `pytest`, and CLI interactions (`arcindex ...`). Deactivate only when the session ends (`deactivate`).
   - Ensure Node.js >=18 and the Codex CLI are available: `npx codex --version`.
2. **Start the Codex MCP Server (when required)**
   - Run `python scripts/codex_mcp.py` to launch the Codex MCP server using `MCPServerStdio`.
   - Leave the server running while local workflows execute; stop it once the session completes.
3. **Editing Guidelines**
   - Prefer `apply_patch` for single-file adjustments.
   - Note assumptions or follow-ups inline using succinct comments or TODO markers.
4. **Testing Philosophy**
   - Add unit tests alongside new workflow or guardrail modules.
   - Use integration tests to exercise `Runner.run` flows that depend on the Codex MCP server.
   - Document manual validation steps when automated coverage is not yet possible.
5. **Logging Decisions**
   - Capture rationale in PR descriptions or short notes (plan to add `docs/decisions/` once created).

---

## 6. Persona Alignment (future SDK agents)

Keep these target personas in mind when configuring instructions and handoffs:

| ID | Title | Core Responsibility |
|----|-------|---------------------|
| `orchestrator` | Arcindex Orchestrator | Manage workflow lifecycle, state persistence, guardrail routing |
| `discovery` | Discovery Guide | Elicit project context, stakeholders, goals |
| `analyst` | Requirements Analyst | Generate structured requirements and insights |
| `pm` | Product Planner | Produce PRDs, stories, acceptance criteria |
| `architect` | System Architect | Craft architecture blueprints and implementation plans |
| `prp` | PRP Author | Create implementation-ready PRPs with validation commands |
| `dev` | Development Coordinator | Coordinate execution plans and capture validation outcomes |
| `quality-gate` | Quality Gate Specialist | Run checklists, scoring, and evidence capture |
| `qa` | QA Reviewer | Perform deep quality analysis and escalate failures |
| `feedback` | Feedback Steward | Manage bidirectional feedback loops and learnings |

---

## 7. Contribution Checklist

Before finishing an Arcindex session:

- [ ] Confirmed relevant sections of `MIGRATION-PLAN.md` or this guide reflect the latest work.
- [ ] Implemented or updated quickstart-aligned scaffolding for the current phase.
- [ ] Documented new commands/tests or marked TODOs for follow-up.
- [ ] Captured blockers or open questions in hand-off notes.
