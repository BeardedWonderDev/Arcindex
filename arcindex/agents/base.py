"""
Common agent utilities for Arcindex personas.
"""

from __future__ import annotations

from typing import Optional

from arcindex.artifacts import ArtifactRecord, ArtifactStore
from arcindex.events import ArtifactEvent, EventEmitter, TokenEvent
from arcindex.tools import current_timestamp


class BaseAgent:
    """
    Base implementation for persona agents.

    Agents interact with the event emitter and artifact store when they are
    provided; otherwise the helpers become no-ops so legacy flows continue to
    operate until the runner wiring lands.
    """

    def __init__(
        self,
        name: str,
        *,
        emitter: Optional[EventEmitter] = None,
        artifact_store: Optional[ArtifactStore] = None,
    ) -> None:
        self.name = name
        self._emitter = emitter
        self._artifact_store = artifact_store

    @property
    def emitter(self) -> Optional[EventEmitter]:
        """Return the configured emitter."""
        return self._emitter

    @property
    def artifact_store(self) -> Optional[ArtifactStore]:
        """Return the configured artifact store."""
        return self._artifact_store

    def bind_emitter(self, emitter: Optional[EventEmitter]) -> None:
        """Attach an event emitter."""
        self._emitter = emitter

    def bind_artifact_store(self, store: Optional[ArtifactStore]) -> None:
        """Attach an artifact store."""
        self._artifact_store = store

    def stream_text(self, text: str, channel: str = "stdout") -> None:
        """Emit a token event for the given text if streaming is available."""
        if not self._emitter:
            return
        event = TokenEvent(
            run_id=self._emitter.run_id,
            ts=current_timestamp(),
            agent=self.name,
            channel=channel,
            text=text,
        )
        self._emitter.emit(event)

    def record_artifact(self, record: ArtifactRecord) -> None:
        """Emit an artifact event for the provided record."""
        if not self._emitter:
            return
        event = ArtifactEvent(
            run_id=self._emitter.run_id,
            ts=current_timestamp(),
            artifact_type=record.artifact_type,
            path=str(record.path),
            sha256=record.sha256,
            phase=record.phase,
            agent=record.agent or self.name,
            uri=record.uri,
            mime_type=record.mime_type,
            metadata=record.metadata,
        )
        self._emitter.emit(event)

    def persist_markdown(
        self,
        artifact_type: str,
        content: str,
        *,
        phase: Optional[str] = None,
        agent: Optional[str] = None,
        extension: str = ".md",
        metadata: Optional[dict] = None,
    ) -> Optional[ArtifactRecord]:
        """
        Persist a markdown artifact through the attached store.

        Returns the created record when available, otherwise ``None``.
        """
        if not self._artifact_store:
            return None
        record = self._artifact_store.write_text(
            artifact_type,
            content,
            phase=phase,
            agent=agent or self.name,
            extension=extension,
            metadata=metadata,
        )
        self.record_artifact(record)
        return record

    def persist_json(
        self,
        artifact_type: str,
        document,
        *,
        phase: Optional[str] = None,
        agent: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> Optional[ArtifactRecord]:
        """
        Persist a JSON artifact through the attached store.
        """
        if not self._artifact_store:
            return None
        record = self._artifact_store.write_json(
            artifact_type,
            document,
            phase=phase,
            agent=agent or self.name,
            metadata=metadata,
        )
        self.record_artifact(record)
        return record
