from __future__ import annotations

from click.testing import CliRunner

from arcindex.cli import arcindex
from arcindex.cli import main as cli_main


def test_cli_start_invokes_quickstart(monkeypatch):
    """Ensure `arcindex start` delegates to the Codex quickstart workflow."""

    class DummyResult:
        def __init__(self) -> None:
            self.final_output = "Codex workflow completed"

    captured_kwargs = {}

    async def fake_run(**kwargs):
        captured_kwargs.update(kwargs)
        return DummyResult()

    monkeypatch.setattr(
        cli_main.workflow,
        "run_discovery_to_analyst",
        fake_run,
    )

    runner = CliRunner()
    result = runner.invoke(
        arcindex,
        ["start", "--task", "Custom task", "--model", "gpt-test", "--max-turns", "10"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output
    assert "Codex workflow completed" in result.output
    assert captured_kwargs["task"] == "Custom task"
    assert captured_kwargs["model"] == "gpt-test"
    assert captured_kwargs["max_turns"] == 10


def test_cli_continue_placeholder():
    """`arcindex continue` should remind contributors that persistence is pending."""
    runner = CliRunner()
    result = runner.invoke(arcindex, ["continue"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    assert "not yet implemented" in result.output.lower()
