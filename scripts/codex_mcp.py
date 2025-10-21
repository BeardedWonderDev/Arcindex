"""
Codex MCP bootstrap script aligned with the official Agents SDK quickstart.

Running this module launches the Codex CLI as a Model Context Protocol server
so local workflows can attach to it via the OpenAI Agents SDK.
"""

from __future__ import annotations

import asyncio
import os
from typing import Final

from dotenv import load_dotenv

from agents import set_default_openai_api
from agents.mcp import MCPServerStdio

MCP_NAME: Final[str] = "Codex CLI"
MCP_PARAMS: Final[dict[str, object]] = {
    "command": "npx",
    "args": ["-y", "codex", "mcp"],
}
MCP_SESSION_TIMEOUT_SECONDS: Final[int] = 360_000


def configure_openai() -> None:
    """Load environment variables and configure API defaults for the SDK."""
    load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Create a .env file as described in "
            "the Agents SDK quickstart before launching Codex MCP."
        )
    set_default_openai_api(api_key)


async def main() -> None:
    """Start the Codex CLI MCP server and keep it alive until the process exits."""
    configure_openai()
    async with MCPServerStdio(
        name=MCP_NAME,
        params=MCP_PARAMS,
        client_session_timeout_seconds=MCP_SESSION_TIMEOUT_SECONDS,
    ) as codex_mcp_server:
        print("Codex MCP server started.")
        await codex_mcp_server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
