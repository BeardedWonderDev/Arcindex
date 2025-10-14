from __future__ import annotations

import asyncio
import json
import shutil
from pathlib import Path

import yaml

from arcindex.orchestrator import OrchestratorController
from arcindex.runner import ArcindexRunner


def _prepare_controller(tmp_path: Path) -> OrchestratorController:
    config_dir = tmp_path / "config"
    workflows_dir = config_dir / "workflows"
    state_dir = tmp_path / "state"
    runs_dir = tmp_path / "runs"
    config_dir.mkdir()
    workflows_dir.mkdir()
    state_dir.mkdir()
    runs_dir.mkdir()

    template_src = Path("arcindex/state/workflow_template.json")
    template_dst = state_dir / "workflow_template.json"
    shutil.copy(template_src, template_dst)

    workflow_src = Path("arcindex/config/workflows/greenfield-discovery.json")
    shutil.copy(workflow_src, workflows_dir / "greenfield-discovery.json")

    runtime_data = yaml.safe_load(Path("arcindex/config/runtime.yaml").read_text())
    runtime_data.setdefault("workflows", {})["directory"] = "./workflows"
    runtime_data.setdefault("state", {})["persistence"] = str(state_dir)
    runtime_data["state"]["workflow_template"] = str(template_dst)
    runtime_data.setdefault("runs", {})["root"] = str(runs_dir)
    runtime_data.setdefault("elicitation", {})["methods_source"] = str(
        Path("arcindex/resources/elicitation-methods.md").resolve()
    )

    runtime_path = config_dir / "runtime.yaml"
    runtime_path.write_text(yaml.safe_dump(runtime_data, sort_keys=False))

    return OrchestratorController.from_config_path(runtime_path)


def test_runner_complete_discovery_emits_events(tmp_path: Path) -> None:
    controller = _prepare_controller(tmp_path)
    runner = ArcindexRunner(controller)

    state, timestamp = controller.initialise_discovery(
        "greenfield-discovery",
        project_name="Arcindex",
        operation_mode=controller.config.elicitation.default_mode,
    )

    answers = {
        "project_name": "Arcindex",
        "project_concept": "Concept",
        "target_users": "Engineers",
        "user_research_status": "Interviews",
        "competitive_landscape": "Legacy",
        "market_opportunities": "Demand",
        "technical_constraints": "Python",
        "integration_requirements": "Git",
        "success_criteria": "Adoption",
    }

    events: list[dict] = []
    context = runner.create_run(subscribers=[events.append])
    controller.bind_run_directory(context.artifact_store.run_directory, state)
    # Generate summary (streams token events if subscribers care).
    controller.summary_markdown(answers, "Arcindex")

    result = asyncio.run(
        runner.complete_discovery(
            context,
            state,
            answers,
            timestamp,
            "Arcindex",
        )
    )

    assert result.status == "ok"
    assert result.summary_path.exists()
    if result.summary_artifact:
        assert result.summary_artifact.path.exists()

    workflow = json.loads(controller.config.state.workflow_path.read_text())
    assert workflow["current_phase"] == "analyst"

    run_state_path = context.artifact_store.run_directory / "workflow.json"
    assert run_state_path.exists()
    run_summary = context.artifact_store.run_directory / "discovery-summary.json"
    assert run_summary.exists()

    event_types = {event["event"] for event in events}
    assert {"phase", "artifact", "end"}.issubset(event_types)

    events_log = result.events_path
    assert events_log.exists()
    lines = events_log.read_text(encoding="utf-8").strip().splitlines()
    assert lines, "Expected events to be recorded"
