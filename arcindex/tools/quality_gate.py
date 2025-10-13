"""Quality gate helpers for the discovery MVP."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, MutableMapping, Optional


@dataclass
class QualityGateResult:
    """Represents the outcome of a quality gate evaluation."""

    status: str
    score: Optional[int]
    checklist: str
    mode: str
    summary: Optional[str]
    timestamp: Optional[str]

    @classmethod
    def not_run(cls, checklist: str, mode: str = "auto") -> "QualityGateResult":
        """Return a placeholder result mirroring the legacy NOT_RUN payload."""
        return cls(
            status="NOT_RUN",
            score=None,
            checklist=checklist,
            mode=mode,
            summary=None,
            timestamp=None,
        )

    def to_payload(self) -> Mapping[str, Any]:
        """Serialise the result to a dictionary compatible with workflow.json."""
        return {
            "timestamp": self.timestamp,
            "status": self.status,
            "score": self.score,
            "checklist": self.checklist,
            "mode": self.mode,
            "summary": self.summary,
            "total_items": None,
            "items_passed": None,
            "items_failed": None,
            "critical_failures": None,
            "standard_failures": None,
        }


def record_quality_gate_placeholder(
    state: MutableMapping[str, Any],
    result: QualityGateResult,
    phase: str = "discovery",
) -> None:
    """Persist a placeholder quality gate outcome into the workflow state."""
    quality_gates = state.setdefault("quality_gate_results", {})
    quality_gates[phase] = result.to_payload()


def current_timestamp() -> str:
    """Return a UTC ISO-8601 timestamp."""
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

