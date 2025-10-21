import pytest

codex_mcp = pytest.importorskip("scripts.codex_mcp")


def test_mcp_params_match_quickstart():
    """Ensure the Codex MCP launch parameters mirror the quickstart guidance."""
    assert codex_mcp.MCP_NAME == "Codex CLI"
    assert codex_mcp.MCP_PARAMS == {"command": "npx", "args": ["-y", "codex", "mcp"]}
    assert codex_mcp.MCP_SESSION_TIMEOUT_SECONDS == 360_000


@pytest.mark.asyncio
async def test_main_starts_stubbed_mcp_server(monkeypatch):
    """Running main should configure the API and wait on the MCP server."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    captured_kwargs = {}

    class DummyServer:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def wait_closed(self):
            captured_kwargs["wait_closed_called"] = True

        def __init__(self, **kwargs):
            captured_kwargs.update(kwargs)

    monkeypatch.setattr(codex_mcp, "MCPServerStdio", DummyServer)

    printed = []
    monkeypatch.setattr(codex_mcp, "print", lambda message: printed.append(message))

    await codex_mcp.main()

    assert printed == ["Codex MCP server started."]
    assert captured_kwargs["name"] == codex_mcp.MCP_NAME
    assert captured_kwargs["params"] == codex_mcp.MCP_PARAMS
    assert (
        captured_kwargs["client_session_timeout_seconds"]
        == codex_mcp.MCP_SESSION_TIMEOUT_SECONDS
    )
    assert captured_kwargs.get("wait_closed_called")


@pytest.mark.asyncio
async def test_main_requires_api_key(monkeypatch):
    """OPENAI_API_KEY must be present before launching the MCP server."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(RuntimeError):
        await codex_mcp.main()
