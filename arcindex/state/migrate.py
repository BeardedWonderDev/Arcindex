"""Helpers for migrating legacy workflow state into run directories."""

from __future__ import annotations

import shutil
from pathlib import Path

from .store import STATE_FILENAME, SUMMARY_FILENAME, WorkflowStateNotInitialized


def migrate_legacy_state_to_run(legacy_dir: Path, run_dir: Path) -> Path:
    """
    Copy legacy workflow state and summary into the run directory.

    Returns the path to the migrated ``workflow.json``.
    """

    legacy_state = legacy_dir / STATE_FILENAME
    if not legacy_state.exists():
        raise WorkflowStateNotInitialized("Legacy workflow state does not exist.")

    run_dir.mkdir(parents=True, exist_ok=True)
    target_state = run_dir / STATE_FILENAME
    shutil.copy2(legacy_state, target_state)

    legacy_summary = legacy_dir / SUMMARY_FILENAME
    if legacy_summary.exists():
        shutil.copy2(legacy_summary, run_dir / SUMMARY_FILENAME)

    return target_state
