import asyncio

import pytest

codex_mcp = pytest.importorskip("scripts.codex_mcp")


def test_mcp_params_match_quickstart():
    """Ensure the Codex MCP launch parameters mirror the quickstart guidance."""
    assert codex_mcp.MCP_NAME == "Codex CLI"
    assert codex_mcp.MCP_PARAMS == {"command": "npx", "args": ["-y", "codex", "mcp-server"]}
    assert codex_mcp.MCP_SESSION_TIMEOUT_SECONDS == 360_000


def test_main_starts_stubbed_mcp_server(monkeypatch):
    """Running main should configure the API and wait on the MCP server."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    captured_kwargs = {}

    class DummyServer:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        def __init__(self, **kwargs):
            captured_kwargs.update(kwargs)

    monkeypatch.setattr(codex_mcp, "MCPServerStdio", DummyServer)

    class DummyEvent:
        def __init__(self):
            captured_kwargs["event_created"] = True

        async def wait(self):
            captured_kwargs["event_wait_called"] = True

    monkeypatch.setattr(codex_mcp.asyncio, "Event", DummyEvent)

    printed = []
    monkeypatch.setattr(codex_mcp.__builtins__, "print", lambda message: printed.append(message))

    asyncio.run(codex_mcp.main())

    assert printed == ["Codex MCP server started."]
    assert captured_kwargs["name"] == codex_mcp.MCP_NAME
    assert captured_kwargs["params"] == codex_mcp.MCP_PARAMS
    assert (
        captured_kwargs["client_session_timeout_seconds"]
        == codex_mcp.MCP_SESSION_TIMEOUT_SECONDS
    )
    assert captured_kwargs.get("event_created")
    assert captured_kwargs.get("event_wait_called")


def test_main_requires_api_key(monkeypatch):
    """OPENAI_API_KEY must be present before launching the MCP server."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(RuntimeError):
        asyncio.run(codex_mcp.main())
