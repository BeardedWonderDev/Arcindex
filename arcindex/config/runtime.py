"""
Runtime configuration loading utilities for Arcindex.

The loader mirrors the structure of the legacy CODEX configuration while
producing convenient Python objects with resolved filesystem paths.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional

import yaml


@dataclass
class SystemSettings:
    """Top-level system configuration."""

    version: str
    default_workflow: str


@dataclass
class WorkflowsSettings:
    """Workflow configuration metadata."""

    directory: Path


@dataclass
class StateSettings:
    """State persistence configuration."""

    persistence: Path
    workflow_template: Path

    @property
    def workflow_path(self) -> Path:
        """Location of the runtime workflow state file."""
        return self.persistence / "workflow.json"


@dataclass
class ElicitationSettings:
    """Elicitation configuration."""

    default_mode: str
    methods_source: Optional[Path]


@dataclass
class RunsSettings:
    """Run directory configuration."""

    root: Path


@dataclass
class DocsSettings:
    """Documentation output configuration."""

    root: Path


@dataclass
class RuntimeConfig:
    """Resolved runtime configuration."""

    root: Path
    system: SystemSettings
    workflows: WorkflowsSettings
    state: StateSettings
    runs: RunsSettings
    elicitation: ElicitationSettings
    docs: DocsSettings


def load_runtime_config(path: Path) -> RuntimeConfig:
    """
    Load the runtime configuration from a YAML file.

    Paths in the YAML document are interpreted relative to the file location.
    """
    data = _read_yaml(path)
    base = path.parent

    system = _parse_system_settings(data.get("system", {}))
    workflows = _parse_workflows_settings(base, data.get("workflows", {}))
    state = _parse_state_settings(base, data.get("state", {}))
    runs = _parse_runs_settings(base, data.get("runs", {}))
    elicitation = _parse_elicitation_settings(base, data.get("elicitation", {}))
    docs = _parse_docs_settings(base, data.get("docs", {}))

    return RuntimeConfig(
        root=base,
        system=system,
        workflows=workflows,
        state=state,
        runs=runs,
        elicitation=elicitation,
        docs=docs,
    )


def _read_yaml(path: Path) -> Mapping[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}
        if not isinstance(loaded, Mapping):
            msg = f"Runtime config at {path} must contain a mapping."
            raise ValueError(msg)
        return loaded


def _parse_system_settings(data: Mapping[str, Any]) -> SystemSettings:
    version = str(data.get("version", "0.0.0"))
    default_workflow = str(data.get("default_workflow", "greenfield-discovery"))
    return SystemSettings(version=version, default_workflow=default_workflow)


def _parse_workflows_settings(base: Path, data: Mapping[str, Any]) -> WorkflowsSettings:
    directory = data.get("directory")
    if directory is None:
        msg = "Runtime config must define workflows.directory."
        raise ValueError(msg)
    workflow_dir = (base / str(directory)).resolve()
    return WorkflowsSettings(directory=workflow_dir)


def _parse_state_settings(base: Path, data: Mapping[str, Any]) -> StateSettings:
    persistence = data.get("persistence")
    template = data.get("workflow_template")

    if persistence is None or template is None:
        msg = "Runtime config must define state.persistence and state.workflow_template."
        raise ValueError(msg)

    persistence_path = (base / str(persistence)).resolve()
    template_path = (base / str(template)).resolve()

    return StateSettings(persistence=persistence_path, workflow_template=template_path)


def _parse_elicitation_settings(base: Path, data: Mapping[str, Any]) -> ElicitationSettings:
    default_mode = str(data.get("default_mode", "interactive"))
    methods_source = data.get("methods_source")
    methods_path: Optional[Path]
    if methods_source is None:
        methods_path = None
    else:
        methods_path = (base / str(methods_source)).resolve()
    return ElicitationSettings(default_mode=default_mode, methods_source=methods_path)


def _parse_runs_settings(base: Path, data: Mapping[str, Any]) -> RunsSettings:
    root = data.get("root")
    if root is None:
        msg = "Runtime config must define runs.root."
        raise ValueError(msg)
    runs_root = (base / str(root)).resolve()
    return RunsSettings(root=runs_root)


def _parse_docs_settings(base: Path, data: Mapping[str, Any]) -> DocsSettings:
    root = data.get("root", "../docs")
    docs_root = (base / str(root)).resolve()
    return DocsSettings(root=docs_root)
