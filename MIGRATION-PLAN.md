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
  - New SDK implementation (to be scaffolded under `codex-sdk/`)

---

## 2. Target Architecture Overview

- **Interface:** CLI-based runner built with Python (`click` or `argparse`).
- **Core components:**
  - `codex-sdk/orchestrator/`: workflow controller (`controller.py`, `state.py`).
  - `codex-sdk/agents/`: per-persona assistant configs (YAML/JSON).
  - `codex-sdk/tools/`: SDK function-call implementations for reusable tasks.
  - `codex-sdk/resources/`: templates, checklists, elicitation methods.
  - `codex-sdk/config/`: workflow definitions (`config/workflows/`) and runtime settings.
  - `codex-sdk/tests/`: harness adapters and unit/integration tests.
- **State management:** JSON store (initially) mirroring legacy `workflow.json`, with future option to migrate to DB or vector store.
- **Test harness:** Update existing scripts to call the new CLI; reuse result comparison patterns.

---

## 3. Migration Phases

### Phase 0 – Foundations

1. Scaffold the new directory structure under `codex-sdk/`.
2. Set up Python environment (`pyproject.toml` / `requirements.txt`) and lint/test tooling.
3. Draft initial runtime config (`codex-sdk/config/runtime.yaml`) and workflow stub (`codex-sdk/config/workflows/greenfield-discovery.json`).

### Phase 1 – Minimal Orchestrator (Discovery Only)

1. Implement orchestrator core:
   - Load workflow config and state snapshot.
   - Register discovery assistant with the Codex SDK.
   - Handle tool calls and basic elicitation flow.
2. Port “project discovery” tools (document creation, elicitation options) from legacy tasks into `codex-sdk/tools/`.
3. Create CLI entry point (`codex-sdk/cli.py`) that starts a discovery run.
4. Write smoke tests covering discovery end-to-end via the CLI.

### Phase 2 – Analyst Phase Integration

1. Add analyst assistant definition and templates.
2. Extend workflow config to include discovery→analyst handoff with gating.
3. Enhance orchestrator to manage multi-phase state, enforce elicitation, and log violations.
4. Update tests to validate both phases and ensure documents match golden fixtures.

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
- Add unit tests per tool in `codex-sdk/tests/tools/` and integration tests per workflow in `codex-sdk/tests/workflows/`.
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

1. Create `codex-sdk/` scaffold with empty orchestrator, agents, tools, config, tests.
2. Establish Python environment and initial dependency list.
3. Migrate discovery assets (templates, checklists) from `legacy/` into `codex-sdk/resources/`.
4. Implement minimal orchestrator loop and discovery assistant registration.

