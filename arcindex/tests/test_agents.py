from __future__ import annotations

from pathlib import Path

from arcindex.agents import DiscoveryAgent
from arcindex.artifacts import ArtifactStore


def test_discovery_agent_persist_summary_with_artifact(tmp_path: Path) -> None:
    runs_root = tmp_path / "runs"
    store = ArtifactStore(run_id="run-test", runs_root=runs_root)
    agent = DiscoveryAgent(artifact_store=store)
    state_dir = store.run_directory
    legacy_dir = tmp_path / "legacy-state"

    state = {"workflow_id": "arcindex-1", "workflow_type": "greenfield-discovery"}
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

    result = agent.persist_summary(
        state,
        answers,
        state_dir,
        project_name="Arcindex",
        timestamp="2025-10-14T00:00:00Z",
        legacy_dir=legacy_dir,
    )

    assert result.summary_markdown.startswith("📋 Discovery Summary")
    assert result.summary_path.exists()
    assert state["project_discovery"]["project_scope"] == "Concept"

    artifact = result.summary_artifact
    assert artifact is not None
    expected_artifact_path = runs_root / "run-test" / "artifacts" / "discovery" / "discovery" / "discovery_summary.md"
    assert artifact.path == expected_artifact_path
    assert artifact.path.exists()
    assert artifact.path.read_text(encoding="utf-8").startswith("📋 Discovery Summary")
    legacy_summary = legacy_dir / "discovery-summary.json"
    assert legacy_summary.exists()
