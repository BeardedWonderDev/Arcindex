"""
Arcindex runner skeleton for Phase 1.
"""

from __future__ import annotations

import asyncio
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable, Mapping, MutableMapping, Optional, Tuple

from arcindex.agents import DiscoveryResult
from arcindex.artifacts import ArtifactRecord, ArtifactStore
from arcindex.events import ArtifactEvent, EndEvent, EventEmitter, EventSubscriber, PhaseEvent
from arcindex.events.model import ErrorEvent
from arcindex.tools import current_timestamp

from .graph import CancellationError, CancellationToken


@dataclass
class RunContext:
    """Holds per-run infrastructure."""

    run_id: str
    started_at: Optional[str]
    emitter: EventEmitter
    artifact_store: ArtifactStore
    events_path: Path
    phase_started: bool = False
    _unsubscribe: Tuple[Callable[[], None], ...] = field(default_factory=tuple)

    def close(self) -> None:
        """Detach any subscribers registered for this run."""
        for unsubscribe in self._unsubscribe:
            unsubscribe()


@dataclass
class RunResult:
    """Represents the outcome of a discovery run."""

    run_id: str
    status: str
    started_at: str
    completed_at: str
    elapsed_ms: int
    summary_markdown: str
    summary_path: Path
    summary_artifact: Optional[ArtifactRecord]
    docs_markdown_path: Optional[Path]
    events_path: Path


class ArcindexRunner:
    """Coordinates discovery execution for Phase 1."""

    def __init__(self, controller) -> None:
        self._controller = controller
        self._cancel_token = CancellationToken()

    def cancel(self) -> None:
        """Request cancellation of the active run."""
        self._cancel_token.cancel()

    def create_run(
        self,
        subscribers: Iterable[EventSubscriber] = (),
        *,
        emit_phase_start: bool = True,
    ) -> RunContext:
        """
        Prepare run infrastructure and emit initial phase start event.
        """
        run_id = uuid.uuid4().hex
        runs_root = self._controller.config.runs.root

        emitter = EventEmitter(run_id, runs_root)
        artifact_store = ArtifactStore(run_id, runs_root)
        unsubscribers = tuple(emitter.subscribe(sub) for sub in subscribers)

        self._controller.configure_run_context(emitter=emitter, artifact_store=artifact_store)

        started_at: Optional[str] = None
        phase_started = False
        if emit_phase_start:
            started_at = current_timestamp()
            emitter.emit(
                PhaseEvent(
                    run_id=run_id,
                    ts=started_at,
                    phase="discovery",
                    status="start",
                )
            )
            phase_started = True

        return RunContext(
            run_id=run_id,
            started_at=started_at,
            emitter=emitter,
            artifact_store=artifact_store,
            events_path=emitter.events_path,
            phase_started=phase_started,
            _unsubscribe=unsubscribers,
        )

    async def complete_discovery(
        self,
        context: RunContext,
        state: MutableMapping[str, object],
        answers: Mapping[str, str],
        timestamp: str,
        project_name: Optional[str],
    ) -> RunResult:
        """
        Persist discovery artifacts, finalise workflow state, and emit terminal events.
        """
        if not context.phase_started:
            context.started_at = current_timestamp()
            context.emitter.emit(
                PhaseEvent(
                    run_id=context.run_id,
                    ts=context.started_at,
                    phase="discovery",
                    status="start",
                )
            )
            context.phase_started = True

        start_perf = time.perf_counter()
        try:
            self._ensure_not_cancelled()
            discovery_result = self._controller.persist_summary(
                state,
                answers,
                timestamp,
                project_name,
            )

            self._ensure_not_cancelled()
            completed_at = current_timestamp()
            self._controller.finalise_discovery(state, completed_at)

            elapsed_ms = int((time.perf_counter() - start_perf) * 1000)
            context.emitter.emit(
                PhaseEvent(
                    run_id=context.run_id,
                    ts=completed_at,
                    phase="discovery",
                    status="end",
                )
            )
            self._emit_artifact_event(context, discovery_result.summary_artifact)

            context.emitter.emit(
                EndEvent(
                    run_id=context.run_id,
                    ts=completed_at,
                    status="ok",
                    elapsed_ms=elapsed_ms,
                    summary={
                        "summary_path": str(discovery_result.summary_path),
                        "artifact_uri": (
                            discovery_result.summary_artifact.uri
                            if discovery_result.summary_artifact
                            else None
                        ),
                        "docs_markdown_path": (
                            str(discovery_result.docs_markdown_path)
                            if discovery_result.docs_markdown_path
                            else None
                        ),
                    },
                )
            )

            return RunResult(
                run_id=context.run_id,
                status="ok",
                started_at=context.started_at or completed_at,
                completed_at=completed_at,
                elapsed_ms=elapsed_ms,
                summary_markdown=discovery_result.summary_markdown,
                summary_path=discovery_result.summary_path,
                summary_artifact=discovery_result.summary_artifact,
                docs_markdown_path=discovery_result.docs_markdown_path,
                events_path=context.events_path,
            )
        except CancellationError:
            completed_at = current_timestamp()
            context.emitter.emit(
                EndEvent(
                    run_id=context.run_id,
                    ts=completed_at,
                    status="cancelled",
                )
            )
            raise
        except Exception as exc:
            completed_at = current_timestamp()
            context.emitter.emit(
                ErrorEvent(
                    run_id=context.run_id,
                    ts=completed_at,
                    where="runner",
                    message=str(exc),
                    retryable=False,
                )
            )
            context.emitter.emit(
                EndEvent(
                    run_id=context.run_id,
                    ts=completed_at,
                    status="error",
                )
            )
            raise
        finally:
            context.close()

    def _ensure_not_cancelled(self) -> None:
        if self._cancel_token.is_cancelled():
            raise CancellationError()

    def _emit_artifact_event(self, context: RunContext, record: Optional[ArtifactRecord]) -> None:
        if not record:
            return
        context.emitter.emit(
            ArtifactEvent(
                run_id=context.run_id,
                ts=current_timestamp(),
                artifact_type=record.artifact_type,
                path=str(record.path),
                sha256=record.sha256,
                phase="discovery",
                agent=record.agent,
                uri=record.uri,
                mime_type=record.mime_type,
                metadata=record.metadata,
            )
        )
