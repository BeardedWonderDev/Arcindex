from __future__ import annotations

import json
from pathlib import Path

from arcindex.artifacts import ArtifactStore


def test_write_text_artifact(tmp_path: Path) -> None:
    runs_root = tmp_path / "runs"
    store = ArtifactStore(run_id="run-001", runs_root=runs_root)

    record = store.write_text(
        "discovery_summary",
        "# Summary\ncontent",
        phase="discovery",
        agent="discovery",
        extension=".md",
    )

    expected_path = runs_root / "run-001" / "artifacts" / "discovery" / "discovery" / "discovery_summary.md"
    assert record.path == expected_path
    assert record.path.exists()
    assert record.sha256
    assert record.uri == "arc://runs/run-001/artifacts/discovery/discovery/discovery_summary.md"
    assert record.mime_type == "text/markdown"

    assert record.path.read_text(encoding="utf-8") == "# Summary\ncontent"


def test_write_json_artifact(tmp_path: Path) -> None:
    store = ArtifactStore(run_id="run-xyz", runs_root=tmp_path / "runs")
    payload = {"foo": "bar", "nested": {"value": 1}}

    record = store.write_json(
        "workflow_state",
        payload,
        phase="system",
        agent=None,
    )

    expected_path = tmp_path / "runs" / "run-xyz" / "artifacts" / "system" / "workflow_state.json"
    assert record.path == expected_path
    assert record.mime_type == "application/json"

    reloaded = json.loads(record.path.read_text(encoding="utf-8"))
    assert reloaded == payload
