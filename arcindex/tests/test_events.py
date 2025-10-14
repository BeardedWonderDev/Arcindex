from __future__ import annotations

import json
from pathlib import Path
from typing import List

from arcindex.events import EventEmitter, PhaseEvent


def test_event_emitter_writes_ndjson_and_notifies_subscribers(tmp_path: Path) -> None:
    runs_root = tmp_path / "runs"
    emitter = EventEmitter(run_id="run-123", runs_root=runs_root)

    received: List[dict] = []
    emitter.subscribe(received.append)

    event = PhaseEvent(run_id="run-ignored", ts="2025-10-14T12:00:00Z", phase="discovery", status="start")
    payload = emitter.emit(event)

    assert payload["event"] == "phase"
    assert payload["phase"] == "discovery"
    assert payload["seq"] == 0
    # run_id is enforced by the emitter
    assert payload["run_id"] == "run-123"

    assert received == [payload]

    events_path = runs_root / "run-123" / "logs" / "events.ndjson"
    assert events_path.exists()

    contents = events_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(contents) == 1
    reloaded = json.loads(contents[0])
    assert reloaded == payload


def test_event_emitter_unsubscribe(tmp_path: Path) -> None:
    emitter = EventEmitter(run_id="run-abc", runs_root=tmp_path / "runs")
    received: List[dict] = []
    unsubscribe = emitter.subscribe(received.append)
    unsubscribe()

    emitter.emit(PhaseEvent(run_id="ignored", ts="2025-10-14T12:00:00Z", phase="discovery", status="start"))
    assert received == []
