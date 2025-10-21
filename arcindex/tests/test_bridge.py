from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

pytest.skip(
    "Legacy workflow coverage pending Codex quickstart migration (see MIGRATION-PLAN.md)",
    allow_module_level=True,
)

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
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

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
    runtime_data.setdefault("docs", {})["root"] = str(docs_dir)
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
        payload = response.json()
        run_id = payload["run_id"]
        assert payload["status"] == "started"

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


def test_bridge_questions_and_interactive_flow(tmp_path: Path) -> None:
    runtime_path = _prepare_runtime(tmp_path)
    app = create_app(runtime_path)

    with TestClient(app) as client:
        questions_resp = client.get("/discovery/questions")
        assert questions_resp.status_code == 200
        questions_payload = questions_resp.json()
        assert questions_payload["count"] == 9

        create_resp = client.post("/jobs", json={})
        assert create_resp.status_code == 202
        run_info = create_resp.json()
        assert run_info["status"] == "pending"
        run_id = run_info["run_id"]

        events = []
        with client.stream("GET", f"/events/{run_id}") as stream:
            # Process initial prompt event before submitting answers.
            line = next(stream.iter_lines())
            while line == "":
                line = next(stream.iter_lines())
            assert line.startswith("event: prompt")
            data_line = next(stream.iter_lines())
            assert data_line.startswith("data: ")
            prompt_event = json.loads(data_line[6:])
            assert prompt_event["event"] == "prompt"
            assert len(prompt_event["questions"]) == 9
            events.append(prompt_event)

            answers_payload = {
                "answers": {
                    "project_name": "Arcindex",
                    "project_concept": "Concept overview",
                    "target_users": "Engineers",
                    "user_research_status": "Interviews",
                    "competitive_landscape": "Legacy CODEX",
                    "market_opportunities": "Demand",
                    "technical_constraints": "Python",
                    "integration_requirements": "Git",
                    "success_criteria": "Adoption",
                }
            }
            update_resp = client.post(f"/jobs/{run_id}/answers", json=answers_payload)
            assert update_resp.status_code == 200
            assert update_resp.json()["status"] == "started"

            # Continue consuming the stream until completion.
            for line in stream.iter_lines():
                if not line:
                    continue
                if not line.startswith("data: "):
                    continue
                event = json.loads(line[6:])
                events.append(event)
                if event.get("event") == "end":
                    break

        assert any(evt.get("event") == "answers" for evt in events)
        assert any(evt.get("event") == "phase" and evt.get("status") == "start" for evt in events)
        assert events[-1].get("event") == "end"
