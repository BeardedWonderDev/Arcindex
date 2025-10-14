"""
Dataclass models describing Arcindex runtime events.

These event payloads align with the Phase 1 streaming contract outlined in the
migration plan. Each event provides a ``to_dict`` helper that removes ``None``
values so the payloads can be serialized directly as NDJSON records or SSE data.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, ClassVar, Dict, Mapping, MutableMapping, Optional


@dataclass
class BaseEvent:
    """
    Shared fields across all events.

    ``seq`` is optional so callers can override the sequence if they need to
    replay historical events. The emitter will assign one when omitted.
    """

    run_id: str
    ts: str
    seq: Optional[int] = field(default=None, init=False)

    event: ClassVar[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a JSON-safe dictionary."""
        data = asdict(self)
        data["event"] = self.event
        return {key: value for key, value in data.items() if value is not None}


@dataclass
class PhaseEvent(BaseEvent):
    """Lifecycle signal indicating a phase started or ended."""

    event: ClassVar[str] = "phase"
    phase: str
    status: str  # start | end
    meta: Optional[Mapping[str, Any]] = None


@dataclass
class TokenEvent(BaseEvent):
    """Token stream emitted from an agent."""

    event: ClassVar[str] = "token"
    agent: str
    channel: str  # stdout | stderr | thought
    text: str


@dataclass
class ToolEvent(BaseEvent):
    """Tool invocation lifecycle emitted by agents."""

    event: ClassVar[str] = "tool"
    name: str
    status: str  # call | result | error
    args: Mapping[str, Any] = field(default_factory=dict)
    agent: Optional[str] = None
    duration_ms: Optional[int] = None
    details: Optional[Mapping[str, Any]] = None


@dataclass
class ArtifactEvent(BaseEvent):
    """Notification that an artifact has been persisted."""

    event: ClassVar[str] = "artifact"
    artifact_type: str
    path: str
    sha256: str
    phase: Optional[str] = None
    agent: Optional[str] = None
    uri: Optional[str] = None
    mime_type: Optional[str] = None
    metadata: Optional[Mapping[str, Any]] = None


@dataclass
class ReduceEvent(BaseEvent):
    """Fan-in lifecycle for merged outputs."""

    event: ClassVar[str] = "reduce"
    node: str
    status: str  # start | done | error
    inputs: Optional[int] = None
    result_ref: Optional[str] = None
    details: Optional[Mapping[str, Any]] = None


@dataclass
class ErrorEvent(BaseEvent):
    """Failure signal emitted by runner, agents, or tooling."""

    event: ClassVar[str] = "error"
    where: str  # executor | agent | tool | system
    message: str
    retryable: bool
    details: Optional[Mapping[str, Any]] = None


@dataclass
class EndEvent(BaseEvent):
    """Terminal run status."""

    event: ClassVar[str] = "end"
    status: str  # ok | partial | error | cancelled
    elapsed_ms: Optional[int] = None
    summary: Optional[MutableMapping[str, Any]] = None
