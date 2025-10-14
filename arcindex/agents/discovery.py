"""
Discovery persona agent built on top of the BaseAgent abstraction.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, MutableMapping, Optional

from arcindex.agents.base import BaseAgent
from arcindex.artifacts import ArtifactRecord
from arcindex.tools import current_timestamp


@dataclass
class DiscoveryResult:
    """Structured result from the discovery agent."""

    summary_markdown: str
    summary_path: Path
    summary_artifact: Optional[ArtifactRecord]


class DiscoveryAgent(BaseAgent):
    """Generate and persist discovery summaries."""

    def __init__(self, *, phase: str = "discovery", **kwargs) -> None:
        super().__init__("discovery", **kwargs)
        self._phase = phase

    def build_summary_markdown(
        self,
        answers: Mapping[str, str],
        project_name: Optional[str],
    ) -> str:
        """Return the human-readable summary for the provided answers."""
        from arcindex.orchestrator.discovery import build_discovery_summary_markdown

        summary = build_discovery_summary_markdown(answers, project_name)
        self.stream_text(summary)
        return summary

    def persist_summary(
        self,
        state: MutableMapping[str, object],
        answers: Mapping[str, str],
        state_dir: Path,
        project_name: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> DiscoveryResult:
        """
        Persist discovery outputs to disk and, when available, the artifact store.
        """
        from arcindex.orchestrator.discovery import (
            build_discovery_summary_markdown,
            persist_discovery_summary,
        )

        ts = timestamp or current_timestamp()
        summary_path = persist_discovery_summary(state, answers, state_dir, ts)

        # Store a markdown version for downstream consumption.
        summary_markdown = build_discovery_summary_markdown(answers, project_name)
        artifact_record = self.persist_markdown(
            "discovery_summary",
            summary_markdown,
            phase=self._phase,
            metadata={"source": "discovery", "format": "markdown"},
        )

        return DiscoveryResult(
            summary_markdown=summary_markdown,
            summary_path=summary_path,
            summary_artifact=artifact_record,
        )
