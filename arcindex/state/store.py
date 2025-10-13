"""
Workflow state persistence utilities.

This module replaces the legacy `state-manager.md` behavior with Python code that
creates and maintains `workflow.json`.
"""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, MutableMapping, Optional

STATE_FILENAME = "workflow.json"


class WorkflowStateError(RuntimeError):
    """Base exception for workflow state operations."""


class WorkflowStateNotInitialized(WorkflowStateError):
    """Raised when workflow.json has not been created yet."""


@dataclass
class WorkflowInitializationParams:
    """Parameters required to create a new workflow state file."""

    workflow_type: str
    project_name: Optional[str]
    operation_mode: str
    timestamp: str


class WorkflowStateStore:
    """Read/write access to the workflow state JSON file."""

    def __init__(self, state_dir: Path, template_path: Path) -> None:
        self._state_dir = state_dir
        self._template_path = template_path
        self._state_path = state_dir / STATE_FILENAME

    @property
    def path(self) -> Path:
        """Return the location of the workflow state file."""
        return self._state_path

    def exists(self) -> bool:
        """True if a workflow state file already exists."""
        return self._state_path.exists()

    def load(self) -> MutableMapping[str, Any]:
        """Load the workflow state."""
        if not self.exists():
            raise WorkflowStateNotInitialized(
                "Workflow state has not been initialized yet."
            )
        with self._state_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def save(self, state: Mapping[str, Any]) -> None:
        """Persist the workflow state."""
        self._state_dir.mkdir(parents=True, exist_ok=True)
        with self._state_path.open("w", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2, sort_keys=True)

    def initialize(self, params: WorkflowInitializationParams) -> MutableMapping[str, Any]:
        """
        Create a new workflow state file from the template.

        The template is cloned and populated with discovery defaults that match
        the legacy system's expectations.
        """
        template_state = self._load_template()
        state = self._apply_initial_values(template_state, params)
        self.save(state)
        return state

    def update_last_modified(self, state: MutableMapping[str, Any], timestamp: str) -> None:
        """Update the last-updated timestamp for the state in-memory and on disk."""
        state["last_updated"] = timestamp
        self.save(state)

    def _load_template(self) -> MutableMapping[str, Any]:
        with self._template_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _apply_initial_values(
        self,
        template: Mapping[str, Any],
        params: WorkflowInitializationParams,
    ) -> MutableMapping[str, Any]:
        state = deepcopy(template)

        state["workflow_id"] = f"arcindex-{params.timestamp}"
        state["workflow_type"] = params.workflow_type
        state["project_name"] = params.project_name
        state["current_phase"] = "discovery"
        state["completed_phases"] = []
        state["operation_mode"] = params.operation_mode
        state["mode_initialized_at"] = params.timestamp
        state["started_at"] = params.timestamp
        state["last_updated"] = params.timestamp
        state["status"] = "active"

        self._initialise_project_discovery(state, params)
        self._initialise_agent_context(state, params)
        self._initialise_elicitation(state)
        self._ensure_defaults(state)

        return state

    @staticmethod
    def _initialise_project_discovery(
        state: MutableMapping[str, Any],
        params: WorkflowInitializationParams,
    ) -> None:
        discovery = state.setdefault("project_discovery", {})
        discovery.update(
            {
                "project_name": params.project_name,
                "project_concept": None,
                "existing_inputs": None,
                "discovery_timestamp": params.timestamp,
                "discovery_completed": False,
                "discovery_summary_path": None,
                "project_scope": None,
                "target_users": None,
                "user_research_status": None,
                "competitive_landscape": None,
                "market_opportunities": None,
                "technical_constraints": None,
                "integration_requirements": None,
                "success_criteria": None,
                "business_goals": None,
            }
        )

    @staticmethod
    def _initialise_agent_context(
        state: MutableMapping[str, Any],
        params: WorkflowInitializationParams,
    ) -> None:
        agent_context = state.setdefault("agent_context", {})
        agent_context["current_agent"] = "discovery"
        agent_context["transformation_history"] = []
        agent_context["last_transformation"] = params.timestamp

    @staticmethod
    def _initialise_elicitation(state: MutableMapping[str, Any]) -> None:
        el_required = state.setdefault(
            "elicitation_required",
            {
                "discovery": True,
                "analyst": True,
                "pm": True,
                "architect": True,
                "prp_creator": True,
                "dev": False,
                "qa": False,
            },
        )
        el_required.setdefault("discovery", True)

        el_completed = state.setdefault(
            "elicitation_completed",
            {
                "discovery": False,
                "analyst": False,
                "pm": False,
                "architect": False,
                "prp_creator": False,
                "dev": False,
                "qa": False,
            },
        )
        el_completed["discovery"] = False

        state.setdefault("elicitation_history", [])

    @staticmethod
    def _ensure_defaults(state: MutableMapping[str, Any]) -> None:
        state.setdefault("documents", {})
        state.setdefault("context_checkpoints", [])
        state.setdefault("validation_results", {})
        state.setdefault(
            "quality_gate_results",
            {"discovery": None, "analyst": None, "pm": None, "architect": None, "prp": None},
        )
        state.setdefault("quality_scores", {})
        state.setdefault(
            "validation_evidence",
            {
                "discovery": [],
                "analyst": [],
                "pm": [],
                "architect": [],
                "prp": [],
            },
        )
        state.setdefault("violation_log", [])
        state.setdefault("feedback_requests", [])
        state.setdefault("failure_escalations", [])
        state.setdefault("epic_learnings", {"current_epic": None, "learnings": []})
        state.setdefault("execution_reports", [])
