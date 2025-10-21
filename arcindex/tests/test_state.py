from __future__ import annotations

import json
from pathlib import Path

import pytest

pytest.skip(
    "Legacy workflow coverage pending Codex quickstart migration (see MIGRATION-PLAN.md)",
    allow_module_level=True,
)

from arcindex.state import SUMMARY_FILENAME, STATE_FILENAME, migrate_legacy_state_to_run


def test_migrate_legacy_state_to_run(tmp_path: Path) -> None:
    legacy_dir = tmp_path / "legacy"
    run_dir = tmp_path / "runs" / "run-123"
    legacy_dir.mkdir(parents=True)

    legacy_state = legacy_dir / STATE_FILENAME
    legacy_state.write_text(json.dumps({"workflow_id": "legacy-1"}))
    legacy_summary = legacy_dir / SUMMARY_FILENAME
    legacy_summary.write_text(json.dumps({"summary": "legacy"}))

    migrated_path = migrate_legacy_state_to_run(legacy_dir, run_dir)

    assert migrated_path == run_dir / STATE_FILENAME
    assert migrated_path.exists()
    assert json.loads(migrated_path.read_text())["workflow_id"] == "legacy-1"

    migrated_summary = run_dir / SUMMARY_FILENAME
    assert migrated_summary.exists()
    assert json.loads(migrated_summary.read_text())["summary"] == "legacy"
