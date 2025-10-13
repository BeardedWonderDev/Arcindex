# CODEX SDK Migration Plan

This document captures the end-to-end plan for porting CODEX from the legacy Claude Code implementation (now in `legacy/`) to a new system built on the OpenAI Codex SDK.

- **Last updated:** 2024-xx-xx
- **Maintainer:** _TBD_
- **Current status:** Restructure complete; SDK implementation not yet started

---

## 1. Repository Restructure (Completed)

- Move all legacy assets under `legacy/`:
  - `legacy/.codex`, `legacy/.bmad-core`, `legacy/.claude`
  - `legacy/PRPs`, `legacy/docs`, `legacy/test-fixtures`
  - `legacy/bin`, `legacy/lib`, `legacy/node_modules`, `legacy/package*.json`
  - Legacy documentation (`legacy/CHANGELOG.md`, `legacy/CODEX-User-Guide.md`, etc.)
  - Legacy GitHub workflows (`legacy/.github/workflows/`)
- Keep repo root clean for the new SDK:
  - `.git/`, `.github/` (issue templates), `.gitignore`, `.npmignore`
  - `LICENSE`, `README.md`
  - New SDK implementation (to be scaffolded under `arcindex/`)

---

## 2. Target Architecture Overview

- **Interface:** CLI-based runner built with Python (`click` or `argparse`).
- **Core components:**
  - `arcindex/orchestrator/`: workflow controller (`controller.py`, `state.py`).
  - `arcindex/agents/`: per-persona assistant configs (YAML/JSON).
  - `arcindex/tools/`: SDK function-call implementations for reusable tasks.
  - `arcindex/resources/`: templates, checklists, elicitation methods.
  - `arcindex/config/`: workflow definitions (`config/workflows/`) and runtime settings.
  - `arcindex/tests/`: harness adapters and unit/integration tests.
- **State management:** JSON store (initially) mirroring legacy `workflow.json`, with future option to migrate to DB or vector store.
- **Test harness:** Update existing scripts to call the new CLI; reuse result comparison patterns.

---

## 3. Migration Phases

### Phase 0 – Foundations

1. Scaffold the new directory structure under `arcindex/`.
2. Set up Python environment (`pyproject.toml` / `requirements.txt`) and lint/test tooling.
3. Draft initial runtime config (`arcindex/config/runtime.yaml`) and workflow stub (`arcindex/config/workflows/greenfield-discovery.json`).
4. Provide a lightweight test harness (`arcindex/test-harness/`) to spin up isolated workspaces for manual validation.

### Phase 1 – Minimal Orchestrator (Discovery Only)

1. Implement orchestrator core:
   - Load workflow config and runtime state snapshot.
   - Register the discovery assistant with the Codex SDK.
   - Mirror legacy `/codex start` behavior (verbatim question display, menu echo) using the output-handling rules from `legacy/.codex/tasks/protocols/workflow-start.md`.
   - Handle tool calls and basic elicitation flow, respecting interactive/batch/yolo modes.
2. Recreate discovery state management:
   - Port the logic from `legacy/.codex/tasks/state-manager.md` so the Python runtime can initialize and update `workflow.json` based on the template in `legacy/.codex/state/workflow.json.template`.
   - Persist discovery summaries via a new module equivalent to `legacy/.codex/tasks/persist-discovery-summary.md`, writing the same nine-field schema to `arcindex/state/discovery-summary.json`.
3. Port discovery tooling into the SDK:
   - Implement advanced elicitation menus (option 1 = proceed, 1–9 numbering) using `legacy/.codex/tasks/advanced-elicitation.md` plus the methods catalog in `legacy/.codex/data/elicitation-methods.md`.
   - Bring forward any discovery-specific tasks or helpers referenced by the agent definition.
4. Create CLI entry point (`arcindex/cli.py`) that exposes `start`/`continue` commands and enforces the same UX contract described in the legacy orchestrator (`legacy/.codex/agents/orchestrator.md`).
5. Introduce a lightweight quality gate runner capable of executing `legacy/.codex/checklists/discovery-quality-gate.md` against the new state files.
6. Write smoke tests covering discovery end-to-end via the CLI, including fixtures that compare discovery summaries against legacy outputs.

### Phase 2 – Analyst Phase Integration

1. Add analyst assistant definition and templates.
2. Extend workflow config to include discovery→analyst handoff with gating.
3. Enhance orchestrator to manage multi-phase state, enforce elicitation, and log violations.
4. Update tests to validate both phases and ensure documents match golden fixtures.

### Legacy Reference Alignment (Phase 0–1)

- Reuse BMAD orchestration patterns (`legacy/.bmad-core/agents/bmad-orchestrator.md`) to shape CLI help output, numbered menu presentation, and transformation affordances.
- Cross-check SDK document tooling against BMAD’s template workflow (`legacy/.bmad-core/tasks/create-doc.md`) to keep elicitation, rationale, and permission handling consistent.
- Preserve document and shard expectations called out in `legacy/.bmad-core/core-config.yaml` so later phases can reason over PRD/architecture file locations without rework.
- Treat BMAD knowledge base assets (`legacy/.bmad-core/data/`) as the source for expanded elicitation or guidance features once the discovery MVP is stable.

### Phase 3 – Product Management Phase

1. Port PM assistant and PRD creation tools.
2. Integrate PM-specific quality gates and templates.
3. Persist multi-document outputs and confirm workflow progression.
4. Expand tests for PRD generation and gating logic.

### Phase 4 – Architecture Phase

1. Introduce architect assistant with epic-aware workflow support.
2. Convert architecture templates and tasks.
3. Implement epic-based conditionals and pattern checks in orchestrator.
4. Build regression tests for architecture outputs.

### Phase 5 – PRP Creation & Development Coordination

1. Port PRP Creator assistant with ultrathink planning tools.
2. Add development coordinator assistant; implement validation levels (syntax→system) as tools.
3. Capture execution learnings and quality logs in state store.
4. Extend harness tests to cover implementation planning and validation flow.

### Phase 6 – QA & Quality Gate Automation

1. Add QA assistant and quality gate checklists/tools.
2. Wire quality gate enforcement into orchestrator.
3. Generate QA reports and link to execution learnings.
4. Complete end-to-end harness run from discovery through QA.

### Phase 7 – Regression & Documentation

1. Finalize CLI help/documentation.
2. Rewrite README and user guides to describe the new system.
3. Archive or retire redundant legacy docs after parity confirmed.
4. Tag initial SDK-based release (v0.1.0 or similar).

---

## 4. Testing & Validation Strategy

- Update `.codex/test-harness/` scripts (when migrated) to call the new CLI.
- Maintain golden copies of generated docs to compare against legacy outputs during each phase.
- Add unit tests per tool in `arcindex/tests/tools/` and integration tests per workflow in `arcindex/tests/workflows/`.
- Track KPIs (validation scores, elicitation compliance) by parsing state snapshots in tests.

---

## 5. Interface Decision

- Proceed with CLI interface first—lower engineering effort, direct compatibility with existing automation, easy to drive locally or in CI.
- Revisit web UI after SDK parity if user experience warrants it (separate epic).

---

## 6. Open Questions

- Final state backend: continue with JSON files or move to SQLite/Redis?
- Authentication/authorization for CLI usage (if sharing across teams).
- Versioning strategy for assistant instructions (auto-upsert vs. manual control).
- Post-port documentation format (single README vs. multi-doc set).

---

## 7. Next Actions

1. Catalogue analyst assistant prompts, templates, and quality gates from the legacy system for Phase 2 porting.
2. Design the multi-phase state extensions required for discovery→analyst handoff (elicitation history, document tracking, gating).
3. Prototype analyst workflow definitions under `arcindex/config/workflows/` and align CLI ergonomics for transitioning phases.
4. Expand the test suite with fixtures that validate analyst outputs against golden references once the phase lands.
