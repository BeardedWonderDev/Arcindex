# Arcindex Migration Plan v2 — Full Context

## Preface

Arcindex is rebuilding the legacy CODEX orchestration platform into a Python-based CLI that coordinates multiple specialized AI agents (discovery, analyst, product management, architecture, PRP authoring, development coordination, QA). The destination system must deliver deterministic, artifact-first workflows that honour the BMAD method and Product Requirement Prompt (PRP) discipline. This plan merges the original seven-phase roadmap with a concrete architecture modernization that introduces:

- A structured event pipeline designed for Server-Sent Events (SSE) streaming.
- A run-scoped persistence model (`runs/<run_id>/…`) that stores immutable artifacts, workflow state snapshots, and append-only logs.
- An asynchronous runner capable of parallel fan-out/fan-in and cooperative cancellation.
- A FastAPI bridge exposing `POST /jobs`, `GET /events/{run_id}` (SSE), and `POST /cancel/{run_id}` endpoints so other interfaces (web, voice, batch automation) can consume Arcindex runs.

Everything below is self-contained; no prior knowledge of earlier plans is assumed.

---

## Architecture Overview

- **Runner & Task Graph**  
  Arcindex will orchestrate workflows through an asynchronous runner (`arcindex/runner/runner.py`) backed by graph primitives (`arcindex/runner/graph.py`). The runner emits phase lifecycle events, supports fan-out/fan-in for parallel agents, enforces retry budgets, and honours cancellation requests via an internal `asyncio.Event`.

- **Agent Layer**  
  Each persona (discovery, analyst, PM, architect, PRP, dev, QA) subclasses a shared `BaseAgent` that wraps the OpenAI Agents/SDK client. BaseAgent streams model tokens, tool invocations, and artifacts through the event emitter, persists outputs via the artifact store, and exposes typed results back to the runner.

- **Event Pipeline**  
  An `EventEmitter` provides two sinks: (1) in-process subscribers (CLI renderer, bridge adapter, metrics collectors) and (2) an append-only NDJSON log at `runs/<run_id>/logs/events.ndjson`. Events follow a unified schema for seven types: `phase`, `token`, `tool`, `artifact`, `reduce`, `error`, `end`. Every event includes `run_id`, ISO8601 timestamp `ts`, and monotonically increasing `seq` for streaming order guarantees.

- **Persistence Layout**  
  Each run receives an immutable directory tree:
  ```
  runs/<run_id>/
    workflow.json          # state snapshot at time of write
    summary.json           # final run roll-up
    artifacts/<phase>/<agent>/<artifact_type>.json|.md|files/...
    logs/events.ndjson     # every emitted event (SSE-compatible)
    logs/tool/<agent>-<tool>.log
    logs/metrics.jsonl     # derived metrics (phase duration, token rate, tool latency)
  ```
  The artifact store computes sha256 checksums for every file and returns URI-style references (`arc://runs/<run_id>/artifacts/...`) that downstream consumers can resolve.

- **CLI Experience**  
  The CLI (`arcindex/cli/main.py`) is a thin wrapper over the runner: it streams token events with throttled display, prints phase/quality-gate updates, surfaces artifact paths at completion, and returns exit codes (0 success, 10 partial with retryable issues, 20 failure). Legacy entry points (`arcindex/cli.py`, test harness scripts) remain intact by forwarding imports.

- **Bridge Service**  
  A lightweight FastAPI app (`bridge/app.py`) exposes:
  - `POST /jobs` — enqueue or start a run; responds with `{run_id, status}`.
  - `GET /events/{run_id}` — Server-Sent Events stream that forwards all events until `end`.
  - `POST /cancel/{run_id}` — cooperative cancellation with acknowledgement (`cancelling`, `not_found`, `completed`).
  The bridge keeps per-run asyncio queues to buffer events for slow subscribers, and drains those queues when cancellation or completion occurs.

- **Configuration & Limits**  
  Runtime config (`arcindex/config/runtime.py`) will expose model defaults, artifact root, parallelism caps per phase, timeouts, and retry limits. Environment overrides (dotenv) give operators control without code changes.

- **Testing Strategy**  
  Each phase introduces unit, contract, and integration tests:
  - Dataclass serialization and SSE framing tests for events.
  - Artifact store tests verifying sha paths and immutability.
  - Runner tests using fake agents to assert event ordering, cancellation, and retry semantics.
  - Integration tests for end-to-end runs (discovery only in Phase 1, expanding as new phases land).
  - SSE bridge tests using FastAPI TestClient to validate streaming behaviour under normal and slow-consumer conditions.

### System Contracts and Semantics

- **Event Fields (Representative)**  
  - `phase`: `{event:"phase", phase:"discovery", status:"start|end", run_id, ts, seq?, meta?}`  
  - `token`: `{event:"token", agent:"analyst", seq:0…n, channel:"stdout|stderr|thought", text:"...", run_id, ts}`  
  - `tool`: `{event:"tool", name:"repo.search", status:"call|result|error", args:{}, duration_ms?, agent, run_id, ts}`  
  - `artifact`: `{event:"artifact", artifact_type:"discovery_summary", phase, agent, path, sha256, metadata?, run_id, ts}`  
  - `reduce`: `{event:"reduce", node:"analyst_merge", inputs:3, status:"start|done|error", result_ref?, run_id, ts}`  
  - `error`: `{event:"error", where:"executor|agent|tool", message, retryable:true|false, details?, run_id, ts}`  
  - `end`: `{event:"end", status:"ok|error|cancelled|partial", elapsed_ms, summary?, run_id, ts}`

- **REST & SSE APIs**  
  - `POST /jobs`: body `{plan:{...}, options:{run_id?, labels?, priority?, parallelism_overrides?}}`, returns `202` with `{run_id, status:"queued|started"}` or errors (`409` conflict, `422` validation, `500` start failure).  
  - `GET /events/{run_id}`: requires `Accept: text/event-stream`; streams `event:`/`data:` frames until completion; errors `404` (unknown run), `410` (archived), `503` (bridge unavailable).  
  - `POST /cancel/{run_id}`: optional `{reason}` body; returns `{run_id, status:"cancelling|not_found|completed"}`; errors `404`, `409`, `500`.

- **Cancellation Semantics**  
  Cancellation propagates via the runner’s `asyncio.Event`. Agents check for cancellation between tool calls and token batches. When triggered, the runner emits `error` (`retryable:false`, `message:"cancelled"`) followed by `end` with status `cancelled`; SSE queues flush remaining events and close.

- **Security & Deployment Posture**  
  Default deployments assume the CLI runs locally (no auth). When the bridge is deployed, it should sit behind an existing reverse proxy that handles authentication/authorization. Bridge containers mount the host `runs/` directory for persistence; systemd or Docker Compose scripts keep the service minimal.

- **Stretch Goals (Post Phase 7)**  
  Add a simple web dashboard that consumes SSE streams, integrate a job queue (RQ/Celery) if concurrency requirements spike, and explore multi-channel delivery (email, voice) using the same event contracts.

---

## Phase 0 – Foundations (In cleanup)

**Purpose**  
Stand up the initial Python package, runtime configuration, discovery MVP, and contributor tooling so the CLI can run end-to-end today.

**Completed work**
- `arcindex/` package with discovery-only CLI entry point (`arcindex start …`).
- File-based state store writing `arcindex/state/workflow.json`.
- Discovery helpers for questions, elicitation menu, and quality gate placeholders.
- Test harness (`arcindex/test-harness/scripts/run-test.sh`) to spin up disposable sandboxes.
- Core documentation: README, MIGRATION-PLAN, AGENTS guide.

**Outstanding cleanup (Immediate focus)**
1. **Fix newline handling bug in CLI**  
   Current `PromptSession` key bindings block ENTER from submitting answers when multi-line input is enabled; the intended Shift+Enter combo fails and the prompt becomes unusable. Update the binding logic so ENTER submits and Shift+Enter inserts a newline, mirroring legacy behavior. Confirm the fallback (no prompt_toolkit) still works.
2. **Regression test Phase 0 discovery flow**  
   Run manual and automated tests to ensure the CLI collects all nine discovery answers, writes `workflow.json`, and generates `discovery-summary.json` without interaction glitches. Update the test harness instructions and verification checklist to include the newline test case.
3. **Documentation refresh**  
   Note the CLI input fix and testing expectations in README/AGENTS so contributors know Phase 0 is stable before Phase 1 begins. Record remaining Phase 1 targets in this plan for transparency.

**Exit condition**  
Discovery workflow runs successfully via CLI with correct input handling, state persists in `arcindex/state`, documentation highlights the stabilized MVP, and all Phase 0 smoke tests pass.

---

## Phase 1 – Discovery Orchestrator Parity With Modern Runtime

**Objective**  
Preserve the current discovery experience while rebuilding the runtime to support streaming events, per-run storage, and future parallelism.

1. **Structured Events and Emitter**
   - Implement `arcindex/events/model.py` with event dataclasses (`phase`, `token`, `tool`, `artifact`, `reduce`, `error`, `end`).
   - Build `arcindex/events/emitter.py` to fan events to in-proc subscribers and append them to `runs/<run_id>/logs/events.ndjson`, formatting output for SSE clients.

2. **Run-Scoped Artifact Store**
   - Add `arcindex/artifacts/store.py` that writes JSON/Markdown/binary artifacts to `runs/<run_id>/artifacts/<phase>/<agent>/…`, computes sha256 hashes, and returns URI-style references.
   - Update `WorkflowStateStore` to persist snapshots in the run directory while migrating legacy `arcindex/state` data via a helper script and integration test.

3. **BaseAgent Wrapper for OpenAI Agents/SDK**
   - Encapsulate stream handling, tool-call translation, artifact persistence, and cancellation in `arcindex/agents/base.py`.
   - Refactor the discovery agent to inherit from BaseAgent and rely on the streaming flow.
   - Cover with replay-based unit tests that simulate OpenAI SDK responses.

4. **Runner Skeleton With Cancellation**
   - Introduce `arcindex/runner/graph.py` for async fan-out/fan-in primitives and cooperative cancel signals.
   - Implement `arcindex/runner/runner.py` to generate run IDs, emit phase events, invoke discovery via BaseAgent, listen for cancel requests, and emit `end` events.

5. **CLI Event Integration**
   - Move CLI entry to `arcindex/cli/main.py`, leave `arcindex/cli.py` as a shim for compatibility.
   - Subscribe to the emitter to display live token streams, artifact summaries, and proper exit codes (0 success, 10 partial, 20 failure).
   - Update CLI smoke tests and documentation to reflect run-scoped artifacts.

6. **FastAPI Bridge**
   - Build `bridge/app.py` with:
     - `POST /jobs` to launch runs via the runner.
     - `GET /events/{run_id}` to stream events over SSE.
     - `POST /cancel/{run_id}` to trigger cooperative cancellation.
   - Use `bridge/adapter.py` to connect runner output to per-run asyncio queues.
   - Provide integration tests validating the SSE stream with a sample discovery run.

7. **Tooling Updates**
   - Refresh harness scripts and docs to point at run directories and explain how to inspect events/artifacts.
   - Ensure unit/integration tests cover the entire event + artifact pipeline.

**Exit condition**  
Running `arcindex start …` generates a unique run directory under `runs/<run_id>/`, streams events to CLI and bridge clients, persists artifacts/logs, and passes all new tests.

---

## Phase 2 – Analyst Phase + Multi-Agent Fan-Out

**Objective**  
Port the analyst persona, wire the runner for phase-to-phase handoffs, and exercise parallel analysts with reduce events.

- Port analyst instructions, templates, and quality gates into the new codebase.
- Extend workflow state to track analyst documents, elicitation history, and validation results.
- Implement analyst fan-out in `runner/graph.py` with corresponding `reduce` events.
- Persist analyst artifacts via the artifact store and emit events per output.
- Update CLI/bridge to show phase transitions and artifact summaries.
- Add an integration test covering discovery→analyst run verifying events, state, and artifacts.

**Exit condition**  
Analyst phase runs automatically after discovery, optional parallel analysts merge via reduce events, and artifact/state snapshots mirror expectations.

---

## Phase 3 – Product Management Phase (PRD Generation)

**Objective**  
Introduce the PM persona, ensure PRD artifacts and quality gates flow through the system.

- Port PM templates and checklists from legacy.
- Update workflow schema to include PRD outputs, acceptance criteria, and scores.
- Ensure runner enforces PM quality gates before advancing.
- Emit artifact/tool events for PRD creation and validation commands.
- Provide golden fixtures and regression tests for PRD content and event logs.

**Exit condition**  
Discovery→analyst→PM pipeline produces PRDs, records gate results, and enforces BMAD elicitation requirements.

---

## Phase 4 – Architecture Phase (Epic-Aware Planning)

**Objective**  
Add architecture persona outputs, including epic-aware fan-out, and ensure artifacts integrate into the event stream.

- Port architecture instructions, epic-aware templates, and checklists.
- Implement parallel architecture tasks with reduce events capturing merged outputs.
- Persist architecture assets and emit artifact events with SHA references.
- Update CLI/bridge messaging to emphasize architecture deliverables.

**Exit condition**  
Architecture documents exist per run, reduce events capture aggregation, and quality gates enforce readiness for PRP authoring.

---

## Phase 5 – PRP Creation & Development Coordination

**Objective**  
Integrate PRP creator and development coordinator roles, including validation command execution and retry handling.

- Port enhanced PRP templates and zero-knowledge validation rules.
- Add development coordinator agent executing validation commands; emit `tool` events for each command with duration and status.
- Configure runner retry policies (backoff, caps) and ensure errors are tagged retryable/fatal in event stream.
- Persist PRP and validation artifacts under run directories.

**Exit condition**  
PRP documents and validation logs exist for each run, retries behave predictably, and `end` events reflect success/partial/failure accurately.

---

## Phase 6 – QA Persona & Automated Quality Gates

**Objective**  
Bring QA reviewer automation online, collecting evidence and final scores.

- Port QA checklists, escalation rules, and reporting templates.
- Emit QA-specific artifact events (reports, evidence attachments).
- Enforce QA completion before emitting `end` status `ok`; capture partial/error states otherwise.
- Add an integration test verifying QA failure path produces `error` event and `partial` end status.

**Exit condition**  
QA phase runs, artifacts/evidence are stored, and final event statuses align with QA outcomes.

---

## Phase 7 – Regression Harness, Documentation, Release Prep

**Objective**  
Stabilize APIs, expand documentation, and prepare for packaging/deployment.

- Publish JSON Schemas for events/artifacts with contract tests.
- Enhance test harness to record golden runs for regression comparison.
- Update README, MIGRATION PLAN, AGENTS, and add detailed design notes under `docs/decisions/`.
- Package CLI (wheel/pipx) and containerize FastAPI bridge with persistent volumes for runs.
- Document deployment playbooks and observability setup (metrics from events).

**Exit condition**  
Schemas locked down, documentation reflects full workflow, packages/containers build successfully, and regression harness can replay complete runs.

---

## Continuous Workstreams (Span Multiple Phases)

- **Observability & Metrics**  
  Derive metrics (phase duration, token rate, tool latency) from events and write to `runs/<run_id>/logs/metrics.jsonl`. Plan dashboards/alerting once the bridge is operational.

- **Risk Management**  
  - **SDK Streaming Changes**: keep BaseAgent under replay-based tests and a versioned interface to absorb OpenAI SDK updates.  
  - **Parallelism Contention**: expose parallelism limits in config, throttle phases on constrained environments, and add chaos tests as fan-out increases.  
  - **Flaky External Tools**: wrap tool invocations with strict timeouts and classify results as retryable vs fatal; emit detailed `tool` events for observability.  
  - **State Drift**: enforce append-only artifact writes and immutable run directories; provide migration tooling when layouts change.  
  - **Back-Pressure on SSE**: bound per-run queues, emit heartbeats, and close connections gracefully when consumers lag.

- **Documentation Discipline**  
  Update README, MIGRATION PLAN, and AGENTS after each phase. Capture architectural decisions and trade-offs in `docs/decisions/`.

---

## Immediate Focus (Right now)

1. **Harden the FastAPI bridge** — add SSE back-pressure protections/heartbeats, document concurrency limits, and provide optional auth/config toggles so external consumers can rely on the service.
2. **Restore live discovery inference** — wire the BaseAgent-backed discovery persona to the OpenAI SDK (prompt catalog, streaming tokens/artifacts, replay-based tests, configuration hooks for credentials/models).
3. **Publish interaction contracts** — ship the bridge/event API reference (schemas, prompt/answer lifecycle, curl examples) and capture the legacy→run directory migration guidance in docs.
4. **Expand coverage & observability stubs** — add interactive bridge tests, BaseAgent replay coverage, harness updates, and drop placeholders for `metrics.jsonl` generation/monitoring so Phase 1 exit criteria are satisfied.

With these remaining tasks complete, Phase 1 will deliver full discovery parity on the modern runtime and a production-ready interface for downstream clients.
