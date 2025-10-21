from __future__ import annotations

from pathlib import Path

import pytest

pytest.skip(
    "Legacy workflow coverage pending Codex quickstart migration (see MIGRATION-PLAN.md)",
    allow_module_level=True,
)

from arcindex.orchestrator import (
    build_discovery_summary_markdown,
    format_discovery_questions,
    parse_discovery_answers,
    persist_discovery_summary,
)


def test_format_discovery_questions_includes_project_name() -> None:
    block = format_discovery_questions("Arcindex")
    assert "Arcindex" in block
    assert "📋 Discovery Questions" in block


def test_parse_discovery_answers_handles_numbered_text() -> None:
    raw = (
        "1. Arcindex\n"
        "2. Concept text\n"
        "3. Users\n"
        "4. Research\n"
        "5. Competitors\n"
        "6. Market\n"
        "7. Technical\n"
        "8. Integrations\n"
        "9. Success"
    )
    answers = parse_discovery_answers(raw)
    assert answers["project_name"] == "Arcindex"
    assert answers["project_concept"].startswith("Concept")
    assert answers["success_criteria"] == "Success"


def test_build_discovery_summary_markdown_has_fallbacks() -> None:
    answers = {"project_concept": "Concept"}
    summary = build_discovery_summary_markdown(answers, project_name=None)
    assert "Concept" in summary
    assert "Not provided" in summary  # fallback fields


def test_persist_discovery_summary_updates_state(tmp_path: Path) -> None:
    state = {"workflow_id": "arcindex-123", "workflow_type": "greenfield-discovery"}
    answers = {
        "project_name": "Arcindex",
        "project_concept": "Concept",
        "target_users": "Engineers",
        "user_research_status": "Interviews",
        "competitive_landscape": "Legacy CODEX",
        "market_opportunities": "Growing demand",
        "technical_constraints": "Python",
        "integration_requirements": "Git",
        "success_criteria": "Completion rate",
    }

    legacy_dir = tmp_path / "legacy"
    summary_path = persist_discovery_summary(
        state,
        answers,
        tmp_path,
        "2024-01-01T00:00:00Z",
        legacy_dir=legacy_dir,
    )

    assert summary_path.exists()
    legacy_summary = legacy_dir / "discovery-summary.json"
    assert legacy_summary.exists()
    project_discovery = state["project_discovery"]
    assert project_discovery["project_scope"] == "Concept"
    assert project_discovery["target_users"] == "Engineers"
    assert project_discovery["discovery_summary_path"] == str(summary_path)
