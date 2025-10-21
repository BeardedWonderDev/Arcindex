"""
Discovery persona agent built on top of the BaseAgent abstraction.

Phase 1 originally synthesised summaries locally.  The agent now delegates
summary generation and elicitation to the OpenAI Agent SDK so the migration
can rely on true model output instead of deterministic templates.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, MutableMapping, Optional

from arcindex.agents.base import BaseAgent
from arcindex.artifacts import ArtifactRecord
from arcindex.tools import current_timestamp
from arcindex.tools.elicitation import get_elicitation_method_details

from .sdk import (
    DiscoveryLLMClient,
    ElicitationResponse,
    OpenAIDiscoveryClient,
    SummaryResponse,
)


@dataclass
class DiscoveryResult:
    """Structured result from the discovery agent."""

    summary_markdown: str
    summary_path: Path
    summary_artifact: Optional[ArtifactRecord]
    docs_markdown_path: Optional[Path] = None


class DiscoveryAgent(BaseAgent):
    """Generate and persist discovery summaries via the Agent SDK."""

    default_client_factory = OpenAIDiscoveryClient

    def __init__(
        self,
        *,
        phase: str = "discovery",
        client: Optional[DiscoveryLLMClient] = None,
        **kwargs,
    ) -> None:
        super().__init__("discovery", **kwargs)
        self._phase = phase
        self._client: DiscoveryLLMClient = client or self.default_client_factory()
        self._cached_summary: Optional[str] = None
        self._cached_answers: Optional[Mapping[str, str]] = None
        self._cached_project_name: Optional[str] = None
        self._cached_workflow_type: str = "greenfield-discovery"
        self._cached_timestamp: Optional[str] = None

    # ------------------------------------------------------------------#
    # Summary generation and persistence
    # ------------------------------------------------------------------#

    def build_summary_markdown(
        self,
        answers: Mapping[str, str],
        project_name: Optional[str],
        *,
        workflow_type: str,
    ) -> str:
        """
        Return the human-readable summary for the provided answers.

        The content is generated through the Agent SDK and cached so later steps
        (elicitation and persistence) can reuse it without incurring new calls.
        """
        summary = self.generate_summary(answers, project_name, workflow_type=workflow_type)
        return summary

    def persist_summary(
        self,
        state: MutableMapping[str, object],
        answers: Mapping[str, str],
        state_dir: Path,
        project_name: Optional[str] = None,
        timestamp: Optional[str] = None,
        legacy_dir: Optional[Path] = None,
        docs_root: Optional[Path] = None,
    ) -> DiscoveryResult:
        """
        Persist discovery outputs to disk and, when available, the artifact store.
        """
        from arcindex.orchestrator.discovery import (
            build_discovery_summary_markdown,
            persist_discovery_summary,
        )

        workflow_type = state.get("workflow_type", "greenfield-discovery")
        if self._cached_summary is None:
            self.generate_summary(answers, project_name, workflow_type=workflow_type)

        ts = timestamp or self._cached_timestamp or current_timestamp()
        summary_path = persist_discovery_summary(
            state,
            answers,
            state_dir,
            ts,
            legacy_dir=legacy_dir,
        )

        summary_markdown = self._cached_summary
        if summary_markdown is None:
            # Safeguard: fall back to legacy builder if the SDK call failed.
            summary_markdown = build_discovery_summary_markdown(answers, project_name)

        docs_markdown_path: Optional[Path] = None
        if docs_root is not None:
            docs_markdown_path = self._write_docs_markdown(
                docs_root,
                summary_markdown,
                workflow_id=str(state.get("workflow_id", "")),
                timestamp=ts,
            )

        artifact_record = self.persist_markdown(
            "discovery_summary",
            summary_markdown,
            phase=self._phase,
            metadata={"source": "discovery", "format": "markdown"},
        )

        project_discovery = state.setdefault("project_discovery", {})
        if docs_markdown_path is not None:
            project_discovery["discovery_summary_markdown_path"] = str(docs_markdown_path)

        return DiscoveryResult(
            summary_markdown=summary_markdown,
            summary_path=summary_path,
            summary_artifact=artifact_record,
            docs_markdown_path=docs_markdown_path,
        )

    # ------------------------------------------------------------------#
    # Agent SDK helpers
    # ------------------------------------------------------------------#

    def generate_summary(
        self,
        answers: Mapping[str, str],
        project_name: Optional[str],
        *,
        workflow_type: str,
    ) -> str:
        response = self._client.generate_summary(
            answers=answers,
            project_name=project_name,
            workflow_type=workflow_type,
        )
        self._cache_summary(response, answers, project_name, workflow_type)
        self.stream_text(response.markdown)
        return response.markdown

    def apply_elicitation_method(
        self,
        *,
        method_label: str,
        answers: Mapping[str, str],
        project_name: Optional[str],
        workflow_type: str,
    ) -> ElicitationResponse:
        if self._cached_summary is None:
            self.generate_summary(answers, project_name, workflow_type=workflow_type)

        instructions = get_elicitation_method_details(method_label)
        response = self._client.apply_elicitation(
            method_label=method_label,
            method_instructions=instructions,
            current_summary=self._cached_summary or "",
            answers=answers,
            project_name=project_name,
            workflow_type=workflow_type,
        )
        self._cached_summary = response.markdown
        self._cached_answers = answers
        self._cached_project_name = project_name
        self.stream_text(response.markdown)
        return response

    def _cache_summary(
        self,
        response: SummaryResponse,
        answers: Mapping[str, str],
        project_name: Optional[str],
        workflow_type: str,
    ) -> None:
        self._cached_summary = response.markdown
        self._cached_answers = answers
        self._cached_project_name = project_name
        self._cached_workflow_type = workflow_type
        self._cached_timestamp = current_timestamp()

    def _write_docs_markdown(
        self,
        docs_root: Path,
        markdown: str,
        *,
        workflow_id: str,
        timestamp: str,
    ) -> Path:
        """
        Persist the AI generated markdown to the repository docs directory.
        """
        safe_workflow = workflow_id or f"arcindex-{timestamp}"
        docs_dir = docs_root / "discovery"
        docs_dir.mkdir(parents=True, exist_ok=True)
        doc_path = docs_dir / f"{safe_workflow}-summary.md"
        doc_path.write_text(markdown, encoding="utf-8")
        return doc_path


__all__ = ["DiscoveryAgent", "DiscoveryResult"]

