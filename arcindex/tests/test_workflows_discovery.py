import pytest

from arcindex.workflows import discovery


@pytest.mark.asyncio
async def test_run_discovery_wires_codex_mcp(monkeypatch):
    """The quickstart discovery workflow should attach the Codex MCP server and call the runner."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(discovery, "load_dotenv", lambda override: None)

    captured_server_kwargs = {}
    created_servers = []

    class DummyServer:
        def __init__(self, **kwargs):
            captured_server_kwargs.update(kwargs)

        async def __aenter__(self):
            created_servers.append(self)
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

    captured_agent_kwargs = {}

    class DummyAgent:
        def __init__(self, **kwargs):
            captured_agent_kwargs.update(kwargs)
            captured_agent_kwargs["instance"] = self

    captured_runner_kwargs = {}

    class DummyRunner:
        @staticmethod
        async def run(**kwargs):
            captured_runner_kwargs.update(kwargs)
            return {"status": "completed"}

    captured_api_key = {}

    def fake_set_default_openai_api(key: str) -> None:
        captured_api_key["value"] = key

    monkeypatch.setattr(discovery, "MCPServerStdio", DummyServer)
    monkeypatch.setattr(discovery, "Agent", DummyAgent)
    monkeypatch.setattr(discovery, "Runner", DummyRunner)
    monkeypatch.setattr(discovery, "set_default_openai_api", fake_set_default_openai_api)

    result = await discovery.run_discovery(
        task="Test task",
        model="gpt-test",
        max_turns=5,
        instructions="Instruction text",
    )

    assert result == {"status": "completed"}
    assert captured_api_key["value"] == "test-key"
    assert captured_server_kwargs["name"] == discovery.MCP_NAME
    assert captured_server_kwargs["params"] == discovery.MCP_PARAMS
    assert (
        captured_server_kwargs["client_session_timeout_seconds"]
        == discovery.MCP_SESSION_TIMEOUT_SECONDS
    )
    assert captured_agent_kwargs["name"] == "discovery"
    assert captured_agent_kwargs["instructions"] == "Instruction text"
    assert captured_agent_kwargs["model"] == "gpt-test"
    assert captured_agent_kwargs["mcp_servers"] == created_servers
    assert captured_runner_kwargs["task"] == "Test task"
    assert captured_runner_kwargs["max_turns"] == 5
    assert captured_runner_kwargs["agent"] is captured_agent_kwargs["instance"]
