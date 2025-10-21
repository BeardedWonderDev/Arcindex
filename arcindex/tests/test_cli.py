from __future__ import annotations

import json
import re
import shutil
import textwrap
from pathlib import Path

import yaml
from click.testing import CliRunner

from arcindex.cli import arcindex
from arcindex.cli import main as cli_main


def test_cli_start_smoke(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    workflows_dir = config_dir / "workflows"
    state_dir = tmp_path / "state"
    runs_dir = tmp_path / "runs"
    config_dir.mkdir()
    workflows_dir.mkdir()
    state_dir.mkdir()
    runs_dir.mkdir()
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    template_src = Path("arcindex/state/workflow_template.json")
    template_dst = state_dir / "workflow_template.json"
    shutil.copy(template_src, template_dst)

    workflow_src = Path("arcindex/config/workflows/greenfield-discovery.json")
    shutil.copy(workflow_src, workflows_dir / "greenfield-discovery.json")

    runtime_data = yaml.safe_load(Path("arcindex/config/runtime.yaml").read_text())
    runtime_data["workflows"]["directory"] = "./workflows"
    runtime_data["state"]["persistence"] = str(state_dir)
    runtime_data["state"]["workflow_template"] = str(template_dst)
    runtime_data.setdefault("runs", {})["root"] = str(runs_dir)
    runtime_data.setdefault("docs", {})["root"] = str(docs_dir)
    runtime_data["elicitation"]["methods_source"] = str(
        Path("arcindex/resources/elicitation-methods.md").resolve()
    )

    runtime_path = config_dir / "runtime.yaml"
    runtime_path.write_text(yaml.safe_dump(runtime_data, sort_keys=False))

    answers_file = tmp_path / "answers.txt"
    answers_file.write_text(
        textwrap.dedent(
            """
            1. Arcindex
            2. Concept overview
            3. Engineering leads and product managers
            4. Interviews with internal users; beta program planned
            5. Legacy CODEX scripts and ad-hoc tooling
            6. Increasing demand for orchestrated AI workflows
            7. Python CLI, JSON state files, reusable SDK bindings
            8. Git, optional OpenAI SDK integrations
            9. Success measured by workflow completion rate and onboarding time
            """
        ).strip()
    )

    runner = CliRunner()
    result = runner.invoke(
        arcindex,
        [
            "start",
            "--project-name",
            "Arcindex",
            "--answers-file",
            str(answers_file),
            "--elicitation-choice",
            "1",
            "--config",
            str(runtime_path),
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output
    assert "Discovery phase complete" in result.output

    run_id_match = re.search(r"Run ID: ([0-9a-f]{32})", result.output)
    assert run_id_match, result.output
    run_id = run_id_match.group(1)

    workflow_path = state_dir / "workflow.json"
    assert workflow_path.exists()
    workflow = json.loads(workflow_path.read_text())
    assert workflow["current_phase"] == "analyst"
    assert workflow["project_discovery"]["project_name"] == "Arcindex"

    run_state_path = runs_dir / run_id / "workflow.json"
    assert run_state_path.exists()
    run_summary_path = runs_dir / run_id / "discovery-summary.json"
    assert run_summary_path.exists()
    legacy_summary = state_dir / "discovery-summary.json"
    assert legacy_summary.exists()

    events_path = runs_dir / run_id / "logs" / "events.ndjson"
    assert events_path.exists()
    assert events_path.read_text(encoding="utf-8").strip()

    docs_summary_path = docs_dir / "discovery" / f"{workflow['workflow_id']}-summary.md"
    assert docs_summary_path.exists()
    contents = docs_summary_path.read_text(encoding="utf-8")
    assert "Discovery Summary" in contents


def test_cli_discovery_run_quickstart(monkeypatch):
    """Ensure the quickstart-aligned CLI command invokes the workflow coroutine."""

    class DummyResult:
        def __init__(self) -> None:
            self.final_output = "Quickstart discovery summary"

    captured_kwargs = {}

    async def fake_run_discovery(**kwargs):
        captured_kwargs.update(kwargs)
        return DummyResult()

    monkeypatch.setattr(cli_main.discovery_workflow, "run_discovery", fake_run_discovery)

    runner = CliRunner()
    result = runner.invoke(
        arcindex,
        ["discovery", "run", "--task", "Custom task", "--model", "gpt-test", "--max-turns", "3"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output
    assert "Quickstart discovery summary" in result.output
    assert captured_kwargs["task"] == "Custom task"
    assert captured_kwargs["model"] == "gpt-test"
    assert captured_kwargs["max_turns"] == 3
