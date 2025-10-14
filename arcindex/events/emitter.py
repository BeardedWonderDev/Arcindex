"""
Event emitter that fans out runtime events and persists them as NDJSON.
"""

from __future__ import annotations

import json
from pathlib import Path
from threading import RLock
from typing import Callable, Dict, List, Optional

from .model import BaseEvent

EventSubscriber = Callable[[Dict[str, object]], None]


class EventEmitter:
    """
    Emit structured events for a single run.

    The emitter fans events to in-process subscribers and appends a compact
    NDJSON record to ``runs/<run_id>/logs/events.ndjson``. Sequence numbers are
    auto-incremented unless provided explicitly on the event payload.
    """

    def __init__(self, run_id: str, runs_root: Path) -> None:
        self._run_id = run_id
        self._runs_root = runs_root
        self._subscribers: List[EventSubscriber] = []
        self._lock = RLock()
        self._sequence = 0

        self._events_path = self._prepare_event_log()

    @property
    def run_id(self) -> str:
        """Return the emitter's run identifier."""
        return self._run_id

    @property
    def events_path(self) -> Path:
        """Location of the NDJSON event log."""
        return self._events_path

    def subscribe(self, subscriber: EventSubscriber) -> Callable[[], None]:
        """
        Register a subscriber callable.

        Returns a callable that, when invoked, removes the subscriber.
        """
        with self._lock:
            self._subscribers.append(subscriber)

        def _unsubscribe() -> None:
            with self._lock:
                try:
                    self._subscribers.remove(subscriber)
                except ValueError:
                    pass

        return _unsubscribe

    def emit(self, event: BaseEvent) -> Dict[str, object]:
        """
        Emit an event to all subscribers and append it to the NDJSON log.

        Returns the serialised payload for convenience and testing.
        """
        with self._lock:
            payload = event.to_dict()
            payload["run_id"] = self._run_id  # ensure downstream invariants
            seq = payload.get("seq")
            if seq is None:
                seq = self._sequence
                payload["seq"] = seq
                event.seq = seq
            self._sequence = max(self._sequence + 1, seq + 1)

            self._append(payload)
            subscribers = tuple(self._subscribers)

        for subscriber in subscribers:
            subscriber(payload)

        return payload

    def _prepare_event_log(self) -> Path:
        run_dir = self._runs_root / self._run_id
        logs_dir = run_dir / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        events_path = logs_dir / "events.ndjson"
        if not events_path.exists():
            events_path.touch()
        return events_path

    def _append(self, payload: Dict[str, object]) -> None:
        with self._events_path.open("a", encoding="utf-8") as handle:
            json.dump(payload, handle, separators=(",", ":"))
            handle.write("\n")
