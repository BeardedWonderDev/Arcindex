# Arcindex Migration Plan v4 - Codex Quickstart Alignment

## Preface

Arcindex is rebuilding CODEX as a Python-first CLI that orchestrates the full multi-agent software delivery lifecycle (discovery -> QA). This revision of the migration plan locks the program to the official OpenAI Codex "Agents SDK Quickstart," including its **Expand to a multi-agent workflow** blueprint. We will treat the quickstart code as the canonical reference: the Codex CLI is launched as the sole MCP server (`npx -y codex mcp-server`), agents are declared with the SDK's `Agent` primitives, and handoffs are orchestrated via the `Runner`. No Arcindex-specific MCP server will be created or maintained.

Key commitments:

- Install and configure the exact dependencies mandated by the quickstart (`openai`, `openai-agents`, `python-dotenv`) inside our Python virtual environment.
- Launch Codex CLI as an MCP server using `MCPServerStdio` with the quickstart's parameters (`command="npx"`, `args=["-y", "codex", "mcp-server"]`, generous session timeout).
- Model every agent, tool attachment, handoff, and runner invocation on the quickstart examples, extending them with Arcindex personas and artefact persistence only after the baseline scenario is green.
- Keep tests, documentation, and CLI wrappers focused on verifying quickstart parity before layering Arcindex features.
- Remove or quarantine legacy orchestration/runtime code as soon as the quickstart equivalents exist. Legacy modules may stay only as read-only references and must not power the CLI.

This plan spans seven phases, each producing production-grade functionality, test coverage, and documentation while remaining quickstart-compliant.

---

## Phase 0 - Environment & Codex MCP Baseline

**Objective**  
Mirror the quickstart environment verbatim so Arcindex can run Codex's MCP server and Agents SDK locally.

**Tasks**
- Activate the repo's Python virtual environment and install `openai`, `openai-agents`, and `python-dotenv` at or above the quickstart-specified versions.
- Ensure Node.js >=18 is available (per Codex CLI requirements) and verify `npx codex --version`.
- Commit the `.env` pattern used in the quickstart (`OPENAI_API_KEY`, optional `OPENAI_API_BASE_URL`), along with documentation that references `dotenv`.
- Add `scripts/codex_mcp.py`, a verbatim port of the quickstart bootstrap, to start the Codex MCP server:

```python
# scripts/codex_mcp.py
import asyncio
import os
from dotenv import load_dotenv
from agents import set_default_openai_api
from agents.mcp import MCPServerStdio

load_dotenv(override=True)
set_default_openai_api(os.getenv("OPENAI_API_KEY"))

async def main() -> None:
    async with MCPServerStdio(
        "Codex CLI",
        params={"command": "npx", "args": ["-y", "codex", "mcp-server"]},
        client_session_timeout_seconds=360000,
    ) as codex_mcp_server:
        print("Codex MCP server started.")
        await codex_mcp_server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
```

- Document the manual smoke test: run `python scripts/codex_mcp.py` and confirm "Codex MCP server started." mirrors the quickstart output.

**Exit Criteria**
- `python scripts/codex_mcp.py` starts the Codex CLI MCP server with no Arcindex-specific tooling.
- README and onboarding docs instruct contributors to follow the quickstart environment steps exactly.

---

## Phase 1 - Discovery Orchestration with Quickstart Agents

**Objective**  
Port the quickstart single-agent workflow into Arcindex, adapting instructions to our discovery persona while leaving the Codex CLI MCP attachment untouched.

**Tasks**
- Create `arcindex/workflows/discovery.py` that reuses the quickstart pattern of instantiating an `Agent` and invoking `Runner.run`. Replace the "app builder" instructions with Arcindex discovery guidance, but keep the structure and parameters intact.
- Add an initial `discovery` agent that invokes Codex MCP tools (e.g., code browsing) via the `mcp_servers` parameter exactly as shown in the quickstart.
- Route the existing `arcindex start` command through the new workflow module so the CLI only depends on Codex quickstart logic (no additional commands).
- Write an integration test that asserts `Runner.run(...).final_output` returns a non-empty summary and that Codex MCP startup/shutdown completes.

**Quickstart-derived scaffold**

```python
# arcindex/workflows/discovery.py
async def main() -> None:
    async with MCPServerStdio(
        "Codex CLI",
        params={"command": "npx", "args": ["-y", "codex", "mcp-server"]},
        client_session_timeout_seconds=360000,
    ) as codex_mcp_server:
        discovery_agent = Agent(
            name="discovery",
            instructions="You are the Arcindex discovery guide...",
            model="gpt-4.1",
            mcp_server_configs=[codex_mcp_server],
        )
        result = await Runner.run(
            agent=discovery_agent,
            task="Elicit project context for Arcindex",
            max_turns=12,
        )
        print(result.final_output)
```

**Exit Criteria**
- Running `python -m arcindex.workflows.discovery` produces discovery output via `Runner.run` and Codex MCP.
- `arcindex start` invokes the new workflow and tests confirm no custom MCP server is introduced.

---

## Phase 2 - Multi-Agent Workflow (Discovery -> Analyst)

**Objective**  
Adopt the quickstart's multi-agent example wholesale, then customize agent instructions for Arcindex discovery and analyst personas.

**Tasks**
- Add `arcindex/workflows/discovery_to_analyst.py`, starting from the quickstart's `multi_agent_workflow.py`. Modify only agent names, instructions, and handoff tasks to reflect Arcindex roles.
- Reuse quickstart concepts: a supervising orchestrator agent, downstream persona agents, explicit `result = await Runner.run(...)`, and `handoffs` arrays linking agents.
- Introduce a shared `settings = ModelSettings(...)` block and optional `Reasoning` configuration identical to the quickstart baseline.
- Ensure both `discovery` and `analyst` agents attach the Codex MCP server via `mcp_server_configs`.
- Update tests to assert orchestrated handoffs succeed (Runner status "completed"), and capture persona outputs in temporary artefact files as a post-processing step.
- Ensure `arcindex start` now invokes this multi-agent pipeline and add a placeholder `arcindex continue` command pending persistence work.

**Quickstart-aligned core**

```python
# arcindex/workflows/discovery_to_analyst.py
async def main() -> None:
    settings = ModelSettings(
        model="gpt-4.1",
        extensions=[
            WebSearchTool(),
            Reasoning(strategy=ReasoningStrategy.on, effort=ReasoningEffort.low),
        ],
    )
    async with MCPServerStdio(
        "Codex CLI",
        params={"command": "npx", "args": ["-y", "codex", "mcp-server"]},
        client_session_timeout_seconds=360000,
    ) as codex_mcp_server:
        discovery = Agent(
            name="discovery",
            instructions="Lead elicitation for Arcindex...",
            settings=settings,
            mcp_server_configs=[codex_mcp_server],
        )
        analyst = Agent(
            name="analyst",
            instructions="Transform discovery notes into structured requirements...",
            settings=settings,
            mcp_server_configs=[codex_mcp_server],
        )
        orchestrator = Agent(
            name="orchestrator",
            instructions=(
                "Coordinate agents. Ensure the discovery agent gathers context, "
                "then hand off to the analyst for structured outputs."
            ),
            settings=settings,
            handoffs=[discovery, analyst],
            mcp_server_configs=[codex_mcp_server],
        )
        result = await Runner.run(
            agent=orchestrator,
            task="Execute Arcindex discovery-to-analyst workflow.",
            handoffs=[discovery, analyst],
            max_turns=30,
        )
        print(result.final_output)
```

**Exit Criteria**
- Runner logs show orchestrator -> discovery -> analyst handoffs identical to the quickstart flow.
- `arcindex start` delegates to the multi-agent workflow and prints the orchestrator's final output.
- Artefacts capture discovery notes and analyst requirements with trace metadata recorded for later phases.

---

## Phase 3 - Guardrails & Evidence Capture

**Objective**  
Layer guardrails using the Agents SDK guardrail decorators and quickstart patterns while keeping Codex MCP as the sole tooling interface.

**Tasks**
- Port quickstart-style guardrail callbacks into `arcindex/guardrails/`. Use `@agents.guardrail` to check discovery summaries and analyst requirements.
- Wire guardrails into the `handoffs=[...]` pipeline so failed validations force `Runner.run` to return `status="failed"`.
- Persist guardrail outcomes beside the run artefacts (`runs/<run_id>/guardrails.jsonl`).
- Add unit tests covering pass/fail cases.

**Exit Criteria**
- Guardrails trigger for both personas and halt the workflow on critical violations.
- Documentation explains how guardrails align with quickstart idioms.

---

## Phase 4 - Product Management Persona

**Objective**  
Extend the quickstart multi-agent flow with a PM agent that consumes analyst output and produces PRDs.

**Tasks**
- Clone the quickstart handoff structure to add a `pm` agent after `analyst`, using identical `handoffs` wiring.
- Persist PM artefacts under `runs/<run_id>/docs/pm/` using post-run hooks (no additional MCP servers).
- Update integration tests to validate orchestrator -> discovery -> analyst -> PM progression.

**Exit Criteria**
- PM agent runs automatically after analyst with outputs saved to docs and run directories.
- Runner trace includes all three persona transitions.

---

## Phase 5 - Architecture, PRP, and Development Personas

**Objective**  
Continue chaining agents using the quickstart handoff pattern to cover architecture, PRP authoring, and development coordination.

**Tasks**
- Define `architect`, `prp`, and `dev` agents with tailored instructions but identical `settings`, `handoffs`, and `mcp_server_configs`.
- Support parallel fan-out by leveraging quickstart-style runner loops (multiple `Agent` instances added to the same `handoffs` list).
- Persist generated artefacts (architecture diagrams, PRPs, development checklists) using CLI post-processing.

**Exit Criteria**
- Multi-agent fan-out completes with consolidated artefacts and trace metadata.
- Guardrails remain active across the expanded pipeline.

---

## Phase 6 - Quality Gate & QA Personas

**Objective**  
Complete the workflow by attaching quality gate and QA reviewer agents that evaluate evidence using Codex MCP tools.

**Tasks**
- Add `quality_gate` and `qa` agents with guardrails that parse prior artefacts.
- Extend integration tests to cover pass/fail evidence scenarios and SSE-friendly trace outputs.

**Exit Criteria**
- Full discovery -> QA pipeline executes with Codex MCP, Agents SDK handoffs, and guardrails.
- Evidence artefacts stored under `runs/<run_id>/logs/evidence/`.

---

## Phase 7 - CLI Bridge & External Integrations

**Objective**  
Expose the quickstart-aligned runner via Arcindex's CLI and FastAPI bridge without altering the MCP topology.

**Tasks**
- Wrap each workflow coroutine in CLI commands (`arcindex run discovery`, `arcindex run pipeline`).
- Update the FastAPI SSE bridge to stream Runner events and trace IDs using the SDK's callbacks.
- Provide OpenAPI docs and sample client snippets that demonstrate launching the pipeline via HTTP.

**Exit Criteria**
- External clients can start, monitor, and cancel runs using the bridge while Codex MCP remains the single tool host.

---

## Cross-Cutting Concerns

- **Documentation**: Every phase must cite the relevant quickstart section and show diff snippets proving parity. Update README and developer docs after each phase.
- **Testing**: Prefer replay fixtures for unit tests; integration suites should launch the real Codex MCP server via the shared bootstrap script.
- **Artefacts**: Continue writing outputs to `runs/<run_id>/`, but never extend MCP beyond the Codex CLI server.
- **Observability**: Surface trace IDs and guardrail summaries in CLI output, mirroring quickstart logging conventions.
- **Legacy cleanup**: Tests or modules that still reference the pre-migration orchestrator must be marked with TODO/skip placeholders and scheduled for replacement. Remove the placeholders once equivalent Codex SDK coverage exists.

This roadmap keeps Arcindex on the official Agents SDK path, ensuring future quickstart updates can be adopted with minimal friction.
