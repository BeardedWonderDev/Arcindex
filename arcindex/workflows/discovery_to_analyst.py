"""
Multi-agent discovery-to-analyst workflow aligned with the Codex Agents SDK quickstart.

The module mirrors the structure in the "Expand to a multi-agent workflow" section of the
Codex quickstart, pared down to Arcindex's orchestrator, discovery, and analyst personas.
"""

from __future__ import annotations

import os
from typing import Any, Dict

from dotenv import load_dotenv

from scripts.codex_mcp import MCP_NAME, MCP_PARAMS, MCP_SESSION_TIMEOUT_SECONDS

try:
    from agents import Agent, ModelSettings, Runner, set_default_openai_api
    from agents.mcp import MCPServerStdio
    from openai.types.shared import Reasoning
except ImportError as import_error:  # pragma: no cover - dependency guard
    Agent = None  # type: ignore[assignment]
    ModelSettings = None  # type: ignore[assignment]
    Runner = None  # type: ignore[assignment]
    set_default_openai_api = None  # type: ignore[assignment]
    MCPServerStdio = None  # type: ignore[assignment]
    Reasoning = None  # type: ignore[assignment]
    _AGENTS_IMPORT_ERROR = import_error
else:  # pragma: no cover - import guard fallback
    _AGENTS_IMPORT_ERROR = None

DEFAULT_DISCOVERY_TO_ANALYST_TASK: str = (
    "Coordinate discovery and analyst personas for Arcindex. "
    "Gather project context, produce a structured discovery summary, "
    "and translate it into analyst-ready requirements."
)

DEFAULT_MODEL: str = "gpt-4.1"

DISCOVERY_INSTRUCTIONS: str = (
    "You are the Arcindex discovery agent. Elicit and summarise the key context, "
    "stakeholders, constraints, and success criteria for the provided task. "
    "Write a concise markdown summary with headings: Overview, Stakeholders, Goals, "
    "Risks, Open Questions. When complete, hand off to the analyst."
)

ANALYST_INSTRUCTIONS: str = (
    "You are the Arcindex analyst. Using the discovery summary and any attachments, "
    "produce structured requirements ready for downstream planning. "
    "Output markdown with sections: Requirements Overview, Functional Requirements, "
    "Non-Functional Requirements, Acceptance Criteria, Follow-up Questions."
)

ORCHESTRATOR_INSTRUCTIONS: str = (
    "You are the Arcindex orchestrator. Create the plan, capture key artefacts, "
    "and coordinate handoffs between discovery and analyst agents. "
    "Ensure discovery completes before analyst work begins. "
    "Summarise final outputs and confirm completion."
)


def _ensure_agents_sdk_available() -> None:
    if None in {Agent, ModelSettings, Runner, set_default_openai_api, MCPServerStdio}:
        raise RuntimeError(
            "OpenAI Agents SDK is not installed. Install `openai-agents` as described "
            "in the Codex quickstart before running the multi-agent workflow."
        ) from _AGENTS_IMPORT_ERROR


def _configure_openai_from_env() -> None:
    _ensure_agents_sdk_available()
    load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Ensure the .env file follows the Codex quickstart instructions."
        )
    assert set_default_openai_api is not None  # for static type checkers
    set_default_openai_api(api_key)


async def run_discovery_to_analyst(
    task: str = DEFAULT_DISCOVERY_TO_ANALYST_TASK,
    *,
    model: str = DEFAULT_MODEL,
    max_turns: int = 24,
    discovery_instructions: str = DISCOVERY_INSTRUCTIONS,
    analyst_instructions: str = ANALYST_INSTRUCTIONS,
    orchestrator_instructions: str = ORCHESTRATOR_INSTRUCTIONS,
    orchestrator_model_settings: Dict[str, Any] | None = None,
):
    """
    Execute the multi-agent workflow and return the runner result.

    The workflow launches Codex MCP, instantiates Arcindex personas, and orchestrates
    handoffs via the Agents SDK Runner, closely mirroring the Codex quickstart sample.
    """
    _configure_openai_from_env()

    async with MCPServerStdio(
        name=MCP_NAME,
        params=MCP_PARAMS,
        client_session_timeout_seconds=MCP_SESSION_TIMEOUT_SECONDS,
    ) as codex_mcp_server:
        discovery_agent = Agent(
            name="discovery",
            instructions=discovery_instructions,
            model=model,
            mcp_servers=[codex_mcp_server],
        )
        analyst_agent = Agent(
            name="analyst",
            instructions=analyst_instructions,
            model=model,
            mcp_servers=[codex_mcp_server],
        )

        if orchestrator_model_settings is None:
            if Reasoning is not None:
                model_settings = ModelSettings(reasoning=Reasoning(effort="medium"))  # type: ignore[call-arg]
            else:  # pragma: no cover - fallback when Reasoning class is unavailable
                model_settings = ModelSettings()
        else:
            model_settings = ModelSettings(**orchestrator_model_settings)  # type: ignore[arg-type]

        orchestrator_agent = Agent(
            name="orchestrator",
            instructions=orchestrator_instructions,
            model=model,
            model_settings=model_settings,
            handoffs=[discovery_agent, analyst_agent],
            mcp_servers=[codex_mcp_server],
        )

        discovery_agent.handoffs = [orchestrator_agent]
        analyst_agent.handoffs = [orchestrator_agent]

        result = await Runner.run(
            agent=orchestrator_agent,
            task=task,
            max_turns=max_turns,
            handoffs=[discovery_agent, analyst_agent],
        )
        return result


def run_discovery_to_analyst_sync(
    task: str = DEFAULT_DISCOVERY_TO_ANALYST_TASK,
    *,
    model: str = DEFAULT_MODEL,
    max_turns: int = 24,
    discovery_instructions: str = DISCOVERY_INSTRUCTIONS,
    analyst_instructions: str = ANALYST_INSTRUCTIONS,
    orchestrator_instructions: str = ORCHESTRATOR_INSTRUCTIONS,
    orchestrator_model_settings: Dict[str, Any] | None = None,
):
    """Convenience wrapper for synchronous callers such as CLI commands."""
    import asyncio

    return asyncio.run(
        run_discovery_to_analyst(
            task=task,
            model=model,
            max_turns=max_turns,
            discovery_instructions=discovery_instructions,
            analyst_instructions=analyst_instructions,
            orchestrator_instructions=orchestrator_instructions,
            orchestrator_model_settings=orchestrator_model_settings,
        )
    )
