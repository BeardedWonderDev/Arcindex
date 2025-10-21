from __future__ import annotations

import pytest

from arcindex.agents.discovery import DiscoveryAgent
from arcindex.agents.sdk import DiscoveryLLMClient, ElicitationResponse, SummaryResponse


class _DummyDiscoveryClient(DiscoveryLLMClient):
    """Deterministic client used in tests to avoid API interactions."""

    def generate_summary(
        self,
        *,
        answers,
        project_name,
        workflow_type,
    ) -> SummaryResponse:
        effective_name = project_name or answers.get("project_name") or "Test Project"
        markdown = (
            f"# Discovery Summary for {effective_name}\n\n"
            f"- Workflow: {workflow_type}\n"
            f"- Concept: {answers.get('project_concept', 'N/A')}\n"
            f"- Target Users: {answers.get('target_users', 'N/A')}\n"
            f"- Success Criteria: {answers.get('success_criteria', 'N/A')}\n"
        )
        return SummaryResponse(markdown=markdown.strip())

    def apply_elicitation(
        self,
        *,
        method_label,
        method_instructions,
        current_summary,
        answers,
        project_name,
        workflow_type,
    ) -> ElicitationResponse:
        refined = (
            f"{current_summary.strip()}\n\n"
            f"## Elicitation Notes ({method_label})\n"
            f"{method_instructions.strip()}\n"
        )
        return ElicitationResponse(
            markdown=refined,
            method_label=method_label,
            notes=f"Applied {method_label}",
        )


@pytest.fixture(autouse=True)
def _fake_discovery_client() -> None:
    """
    Swap the discovery agent client factory with a deterministic test double.
    """
    original_factory = DiscoveryAgent.default_client_factory
    DiscoveryAgent.default_client_factory = lambda: _DummyDiscoveryClient()
    try:
        yield
    finally:
        DiscoveryAgent.default_client_factory = original_factory
