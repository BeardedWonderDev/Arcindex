import pytest

from arcindex.workflows import discovery
from arcindex.workflows import discovery_to_analyst


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


@pytest.mark.asyncio
async def test_run_discovery_to_analyst_handoffs(monkeypatch):
    """Multi-agent workflow should configure orchestrator handoffs per the quickstart."""

    monkeypatch.setenv("OPENAI_API_KEY", "multi-agent-key")
    monkeypatch.setattr(discovery_to_analyst, "load_dotenv", lambda override: None)

    captured_server_kwargs = {}

    class DummyServer:
        def __init__(self, **kwargs):
            captured_server_kwargs.update(kwargs)

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

    created_agents = []

    class DummyAgent:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            self.handoffs = kwargs.get("handoffs", [])
            created_agents.append(self)

    class DummyModelSettings:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    class DummyReasoning:
        def __init__(self, effort: str):
            self.effort = effort

    captured_runner_kwargs = {}

    class DummyRunner:
        @staticmethod
        async def run(**kwargs):
            captured_runner_kwargs.update(kwargs)
            return {"status": "completed", "final_output": "done"}

    captured_api_key = {}

    def fake_set_default_openai_api(key: str) -> None:
        captured_api_key["value"] = key

    monkeypatch.setattr(discovery_to_analyst, "MCPServerStdio", DummyServer)
    monkeypatch.setattr(discovery_to_analyst, "Agent", DummyAgent)
    monkeypatch.setattr(discovery_to_analyst, "ModelSettings", DummyModelSettings)
    monkeypatch.setattr(discovery_to_analyst, "Reasoning", DummyReasoning)
    monkeypatch.setattr(discovery_to_analyst, "Runner", DummyRunner)
    monkeypatch.setattr(discovery_to_analyst, "set_default_openai_api", fake_set_default_openai_api)

    result = await discovery_to_analyst.run_discovery_to_analyst(
        task="Pipeline task",
        model="gpt-test",
        max_turns=12,
    )

    assert result["status"] == "completed"
    assert captured_api_key["value"] == "multi-agent-key"
    assert captured_server_kwargs["name"] == discovery_to_analyst.MCP_NAME
    assert captured_server_kwargs["params"] == discovery_to_analyst.MCP_PARAMS
    assert (
        captured_server_kwargs["client_session_timeout_seconds"]
        == discovery_to_analyst.MCP_SESSION_TIMEOUT_SECONDS
    )

    assert len(created_agents) == 3
    orchestrator = created_agents[2]
    discovery_agent = created_agents[0]
    analyst_agent = created_agents[1]

    assert orchestrator.kwargs["handoffs"] == [discovery_agent, analyst_agent]
    assert discovery_agent.handoffs == [orchestrator]
    assert analyst_agent.handoffs == [orchestrator]

    assert captured_runner_kwargs["agent"] is orchestrator
    assert captured_runner_kwargs["handoffs"] == [discovery_agent, analyst_agent]
    assert captured_runner_kwargs["task"] == "Pipeline task"
    assert captured_runner_kwargs["max_turns"] == 12
