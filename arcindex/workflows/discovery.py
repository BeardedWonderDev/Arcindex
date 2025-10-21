"""
Quickstart-aligned discovery workflow using the OpenAI Agents SDK.

This module mirrors the single-agent example from the Codex Agents SDK
quickstart, adapted with Arcindex-specific instructions and defaults.
"""

from __future__ import annotations

import os
from agents import Agent, Runner, set_default_openai_api
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv

from scripts.codex_mcp import (
    MCP_NAME,
    MCP_PARAMS,
    MCP_SESSION_TIMEOUT_SECONDS,
)

DEFAULT_DISCOVERY_TASK: str = "Lead the Arcindex discovery workflow and capture a concise summary."
DEFAULT_DISCOVERY_INSTRUCTIONS: str = (
    "You are the Arcindex discovery guide. Gather the core context, stakeholders, "
    "risks, and goals needed to kick off the multi-agent workflow. Deliver a tight "
    "markdown summary with clear headings ready for analyst handoff."
)
DEFAULT_MODEL: str = "gpt-4.1"


def _configure_openai_from_env() -> None:
    load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Ensure the .env file follows the Codex quickstart instructions."
        )
    set_default_openai_api(api_key)


async def run_discovery(
    task: str = DEFAULT_DISCOVERY_TASK,
    *,
    model: str = DEFAULT_MODEL,
    max_turns: int = 12,
    instructions: str = DEFAULT_DISCOVERY_INSTRUCTIONS,
):
    """
    Execute the Codex quickstart discovery workflow and return the Runner result.
    """
    _configure_openai_from_env()

    async with MCPServerStdio(
        name=MCP_NAME,
        params=MCP_PARAMS,
        client_session_timeout_seconds=MCP_SESSION_TIMEOUT_SECONDS,
    ) as codex_mcp_server:
        discovery_agent = Agent(
            name="discovery",
            instructions=instructions,
            model=model,
            mcp_servers=[codex_mcp_server],
        )
        result = await Runner.run(
            agent=discovery_agent,
            task=task,
            max_turns=max_turns,
        )
        return result


def run_discovery_sync(
    task: str = DEFAULT_DISCOVERY_TASK,
    *,
    model: str = DEFAULT_MODEL,
    max_turns: int = 12,
    instructions: str = DEFAULT_DISCOVERY_INSTRUCTIONS,
):
    """Convenience wrapper for synchronous contexts such as the CLI."""
    import asyncio

    return asyncio.run(
        run_discovery(
            task=task,
            model=model,
            max_turns=max_turns,
            instructions=instructions,
        )
    )
