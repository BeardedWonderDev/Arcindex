# Arcindex Migration Plan v3 — Agents SDK Alignment

## Preface

Arcindex is rebuilding CODEX as a Python-first command line interface that orchestrates multi-agent software delivery (discovery → QA). This plan replaces prior incremental migrations with a ground-up adoption of the OpenAI Agents SDK. **Legacy behaviour is not preserved.** Everything below assumes a clean cutover to SDK-native agents, tracing, guardrails, and tool orchestration.

Key commitments:

- Use the latest OpenAI `openai` and `openai-agents` packages for all model interactions.
- Treat the Agents SDK `Agent` + `Runner` primitives as the authoritative orchestration layer.
- Host Arcindex tools via the Model Context Protocol (MCP) so agents interact with project state through well-defined, server-backed tools.
- Persist run artefacts and documentation in Arcindex’s filesystem layout while deriving event streams from official trace data (no custom emitters).

This plan spans seven phases. Each phase yields production-quality functionality backed by tests, SDK tracing, and documentation.

---

## Phase 0 – SDK Foundations & Environment

**Objective**  
Bootstrap the repository around the OpenAI Agents SDK and MCP infrastructure.

**Tasks**
- Add dependencies: `openai>=1.40`, `openai-agents>=0.2`, `mcp>=latest`. Remove bespoke client shims.
- Introduce a top-level `arcindex_sdk` module that configures API keys, tracing (Stream/Traces API), and default models via `set_default_openai_api`.
- Implement Arcindex MCP server in `arcindex/mcp/server.py`, exposing project-aware tools:
  - `filesystem.read` / `filesystem.write` for run artefacts.
  - `elicitation.catalog` tool that returns elicitation options + prompt instructions.
  - Discovery summary persistence tool.
- Add developer docs covering environment variables, API key handling, and local MCP server launch.
- Write smoke tests that ensure the MCP server starts and responds to tool discovery.

**Exit Criteria**
- `python -m arcindex.mcp.server` launches successfully and registers tools.
- `python -m arcindex.sdk.check` verifies API configuration.
- No legacy runner or agent classes remain.

---

## Phase 1 – Discovery Agent via Agents SDK

**Objective**  
Ship the discovery workflow using SDK-native agents and the official Runner.

**Architecture**
- Define two agents in `arcindex/agents/`:
  - `orchestrator`: handles workflow lifecycle, MCP tool invocation, and documentation persistence.
  - `discovery`: generates summaries, applies elicitation methods, and writes artefacts through MCP tools.
- Configure agents with:
  - Instructions derived from legacy prompts but modernised for deterministic headings.
  - Required tools (`elicitation.catalog`, `filesystem.write`, etc.).
  - Tracing enabled by default.
- Replace CLI entrypoint with `ArcindexRunner.run_discovery(project_name, answers, elicitation_choice)` that internally:
  - Starts the MCP server.
  - Invokes `Runner.run` with the orchestrator agent.
  - Streams tokens/events through SDK callbacks directly to the CLI/bridge.
- Capture run artefacts by subscribing to Runner’s trace stream and writing to `runs/<run_id>/`:
  - Use trace metadata to populate `workflow.json`, `summary.json`, and docs under `docs/discovery/`.
- Update FastAPI bridge to call the same helper, relay trace events via SSE, and expose trace IDs for observability.

**Testing**
- CLI integration test that seeds answers, runs discovery, and asserts:
  - Runner returns `status="completed"`.
  - `docs/discovery/<run_id>.md` exists with markdown headings.
  - Trace ID is emitted.
- Bridge tests covering interactive answer submission and SSE streaming.

**Exit Criteria**
- `arcindex start …` completes discovery using SDK agents, writes docs + run artefacts, and surfaces trace IDs.
- No custom Responses API usage remains in discovery.

---

## Phase 2 – Analyst Persona & Multi-Agent Handoffs

**Objective**  
Extend the runner to transition from discovery to analyst using SDK handoffs.

**Tasks**
- Add `analyst` agent with instructions sourced from legacy content, adapted for SDK context.
- Configure orchestrator agent to emit `handoff` actions after discovery completion.
- Persist analyst artefacts via MCP filesystem tool.
- Update workflow state schema to reference trace IDs, agent outputs, and guardrail results rather than manual history arrays.
- Enhance CLI/bridge to surface phase transitions using Runner callbacks.

**Testing**
- Integration test that seeds discovery responses, triggers analyst phase, and verifies:
  - Trace log shows handoff from orchestrator to analyst.
  - Analyst artefacts saved in `runs/<run_id>/artifacts/analyst/`.
  - Quality gate guardrail invoked (see Phase 3).

**Exit Criteria**
- Analyst phase runs automatically post-discovery with artefacts persisted and trace metadata recorded.

---

## Phase 3 – Guardrails & Quality Gates

**Objective**  
Leverage SDK guardrails to enforce quality gates instead of manual placeholders.

**Tasks**
- Define guardrail callbacks using `@agents.guardrail` decorators that validate discovery/analyst outputs against checklists (ported from legacy markdown into structured JSON or YAML).
- Guardrail outcomes update `runs/<run_id>/logs/guardrails.jsonl` and runner state.
- CLI displays guardrail pass/fail status; bridge sends guardrail events in SSE stream.
- Update template docs describing guardrail expectations and remediation paths.

**Testing**
- Unit tests for each guardrail with intentionally failing inputs.
- Integration test verifying guardrail events appear in trace stream and abort run on critical failure (Runner should return `status="failed"`).

**Exit Criteria**
- Every phase uses guardrails for validation; manual `QualityGateResult.not_run` placeholders removed.

---

## Phase 4 – Product Management Agent & Artefacts

**Objective**  
Introduce PM agent with SDK-native workflows.

**Tasks**
- Add `pm` agent definition, tools (e.g., `filesystem.write`, future PRP references), and guardrails.
- Implement orchestrated fan-out if multiple PM perspectives are required (use Runner parallel execution).
- Persist PRD markdown under `docs/pm/` and JSON artefacts under run directory.
- Update CLI/bridge messaging to highlight PM outputs.

**Testing**
- Integration test covering discovery → analyst → PM run with guardrail success.
- Snapshot tests ensuring PRD headings and metadata conform to expectations.

**Exit Criteria**
- Full pipeline through PM runs via Agents SDK with artefacts and docs persisted.

---

## Phase 5 – Architecture, PRP, and Development Agents

**Objective**  
Expand to architecture planning, PRP authoring, and development coordination agents.

**Tasks**
- Define `architect`, `prp`, and `dev` agents with handoffs chained from PM phase.
- Introduce additional MCP tools as needed (e.g., repo introspection, command execution harness).
- Implement parallel fan-out (multiple architects) with SDK reduce handlers.
- Persist architecture blueprints, PRPs, and development checklists to docs + run directories.

**Testing**
- Integration suite verifying multi-agent fan-out, reduce events, and artefact persistence.
- Guardrail tests for PRP validation commands.

**Exit Criteria**
- Pipeline produces architecture plans, PRPs, and development coordination outputs using SDK agents exclusively.

---

## Phase 6 – Quality Gate & QA Agents

**Objective**  
Complete workflow with quality gate specialist and QA reviewer personas.

**Tasks**
- Add `quality_gate` and `qa` agents with guardrails enforcing evidence capture.
- Extend MCP tooling to fetch evidence artefacts, run test harness scripts, and attach logs.
- CLI exposes quality gate scoring; bridge surfaces escalations via SSE.

**Testing**
- Scenario tests covering pass/fail gates, evidence persistence, and escalations.
- Stress tests ensuring long runs stream cleanly with tracing.

**Exit Criteria**
- Full end-to-end workflow from discovery to QA runs within the SDK framework, with evidence stored under `runs/<run_id>/logs/evidence/`.

---

## Phase 7 – FastAPI Bridge & External Integrations

**Objective**  
Harden the HTTP interface and prepare for external consumer integrations.

**Tasks**
- Refactor bridge endpoints to operate purely on Runner APIs and trace IDs.
- Provide webhook or WebSocket hooks for guardrail events and artefact updates.
- Add API documentation (OpenAPI schema) and example client libraries.
- Ensure bridge supports cancelling/monitoring runs via Runner cancellation tokens.

**Testing**
- End-to-end tests simulating an external client (answer submission, cancellation, guardrail handling).
- Load tests validating SSE/WebSocket performance with long-running traces.

**Exit Criteria**
- External clients can launch, monitor, and cancel runs purely through bridge endpoints, relying on Agents SDK tracing data for observability.

---

## Cross-Cutting Concerns

- **Documentation**: Update `README.md`, developer onboarding docs, and per-phase notes to reflect SDK usage, API credentials, and MCP workflow. Provide trace troubleshooting steps.
- **State Schema**: Replace legacy `workflow.json` template with an SDK-aware document capturing `run_id`, `trace_id`, agent outputs, guardrail results, and artefact URIs.
- **Testing Strategy**: Use deterministic fixtures by swapping SDK clients with replay adapters in unit tests. Integration tests should run with the real SDK using mocked MCP backends where necessary.
- **Tool Security**: Guard MCP filesystem operations with allowlists and ensure docs/artefacts directories are the only writable locations.
- **Observability**: Integrate with OpenAI Trace viewer and emit run metadata (trace URL, guardrail summary) in CLI/bridge outputs.

---

## Conclusion

This migration abandons bespoke orchestration in favour of the OpenAI Agents SDK. Every agent interaction, guardrail, and tool invocation must flow through the SDK stack. Legacy compatibility is explicitly out of scope; new functionality, tests, and documentation should all reference SDK concepts (Agents, Runner, MCP, guardrails, tracing). Completing Phase 7 delivers a modern, maintainable Arcindex CLI aligned with the official getting started flow and ready for future multi-agent extensions. 
