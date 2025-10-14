from __future__ import annotations

import json
import shutil
import textwrap
from pathlib import Path

import yaml
from fastapi.testclient import TestClient

from bridge import create_app


def _prepare_runtime(tmp_path: Path) -> Path:
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
    return runtime_path


def test_bridge_streams_events(tmp_path: Path) -> None:
    runtime_path = _prepare_runtime(tmp_path)
    app = create_app(runtime_path)

    answers = {
        "project_name": "Arcindex",
        "project_concept": "Concept overview",
        "target_users": "Engineers",
        "user_research_status": "Interviews",
        "competitive_landscape": "Legacy CODEX scripts",
        "market_opportunities": "Demand for orchestrated workflows",
        "technical_constraints": "Python CLI",
        "integration_requirements": "Git integrations",
        "success_criteria": "Completion rate",
    }

    with TestClient(app) as client:
        response = client.post(
            "/jobs",
            json={
                "project_name": "Arcindex",
                "answers": answers,
                "workflow_id": "greenfield-discovery",
            },
        )
        assert response.status_code == 202, response.text
        run_id = response.json()["run_id"]

        events = []
        with client.stream("GET", f"/events/{run_id}") as stream:
            for line in stream.iter_lines():
                if not line:
                    continue
                if line.startswith("data: "):
                    event = json.loads(line[6:])
                    events.append(event)
                    if event.get("event") == "end":
                        break

        assert any(evt.get("event") == "phase" and evt.get("status") == "start" for evt in events)
        assert any(evt.get("event") == "artifact" for evt in events)
        assert events[-1].get("event") == "end"

        cancel_response = client.post(f"/cancel/{run_id}")
        assert cancel_response.status_code == 200
        assert cancel_response.json()["status"] in {"completed", "cancelling"}
