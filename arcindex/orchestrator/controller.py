"""
High-level orchestrator controller.

This controller provides the filesystem-backed runtime coordination needed to run
the discovery workflow from the CLI.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, MutableMapping, Optional, Tuple

from arcindex.agents import DiscoveryAgent, DiscoveryResult
from arcindex.config import RuntimeConfig, load_runtime_config
from arcindex.orchestrator.discovery import (
    DISCOVERY_CHECKLIST_PATH,
    build_elicitation_menu,
    format_discovery_questions,
    get_discovery_questionnaire,
    initialise_quality_gate,
    parse_discovery_answers,
)
from arcindex.state import WorkflowInitializationParams, WorkflowStateError, WorkflowStateStore
from arcindex.tools import (
    ElicitationMenu,
    ElicitationOption,
    QualityGateResult,
    current_timestamp,
    record_quality_gate_placeholder,
)


class OrchestratorController:
    """Wraps configuration, workflow definitions, and state management."""

    def __init__(self, runtime_config: RuntimeConfig) -> None:
        self._config = runtime_config
        self._state_store = WorkflowStateStore(
            runtime_config.state.persistence,
            runtime_config.state.workflow_template,
        )
        self._discovery_agent = DiscoveryAgent()

    def configure_run_context(
        self,
        *,
        emitter: Optional["EventEmitter"] = None,
        artifact_store: Optional["ArtifactStore"] = None,
    ) -> None:
        """
        Attach streaming and persistence infrastructure for the active run.
        """
        self._discovery_agent.bind_emitter(emitter)
        self._discovery_agent.bind_artifact_store(artifact_store)

    @classmethod
    def from_config_path(cls, config_path: Path) -> "OrchestratorController":
        """Instantiate the controller from a runtime configuration path."""
        runtime_config = load_runtime_config(config_path)
        return cls(runtime_config)

    @property
    def config(self) -> RuntimeConfig:
        """Expose the resolved runtime configuration."""
        return self._config

    def ensure_no_active_workflow(self) -> None:
        """Raise if a workflow.json already exists."""
        if self._state_store.exists():
            raise WorkflowStateError(
                "A workflow is already in progress. Use 'continue' once multi-phase "
                "support is implemented or remove the existing state."
            )

    def initialise_discovery(
        self,
        workflow_id: str,
        project_name: Optional[str],
        operation_mode: Optional[str] = None,
    ) -> Tuple[MutableMapping[str, Any], str]:
        """
        Initialise the discovery phase state and return the state plus timestamp.
        """
        operation_mode = operation_mode or self._config.elicitation.default_mode
        timestamp = current_timestamp()
        params = WorkflowInitializationParams(
            workflow_type=workflow_id,
            project_name=project_name,
            operation_mode=operation_mode,
            timestamp=timestamp,
        )
        state = self._state_store.initialize(params)
        initialise_quality_gate(state)
        self._state_store.save(state)
        return state, timestamp

    def load_state(self) -> MutableMapping[str, Any]:
        """Load the existing workflow state."""
        return self._state_store.load()

    def save_state(self, state: Mapping[str, Any]) -> None:
        """Persist the workflow state to disk."""
        self._state_store.save(state)

    def discovery_questions(self, project_name: Optional[str]) -> str:
        """Return the formatted discovery question block."""
        return format_discovery_questions(project_name)

    def discovery_questionnaire(self, project_name: Optional[str]):
        """Return the ordered questionnaire for interactive prompting."""
        return get_discovery_questionnaire(project_name)

    def parse_answers(self, raw_text: str) -> Mapping[str, str]:
        """Parse raw numbered answers supplied via file."""
        return parse_discovery_answers(raw_text)

    def persist_summary(
        self,
        state: MutableMapping[str, Any],
        answers: Mapping[str, str],
        timestamp: str,
        project_name: Optional[str],
    ) -> DiscoveryResult:
        """Persist discovery summary data and update the state."""
        result = self._discovery_agent.persist_summary(
            state,
            answers,
            self._config.state.persistence,
            project_name=project_name,
            timestamp=timestamp,
        )
        self._state_store.save(state)
        return result

    def summary_markdown(
        self,
        answers: Mapping[str, str],
        project_name: Optional[str],
    ) -> str:
        """Build the human-readable discovery summary."""
        return self._discovery_agent.build_summary_markdown(answers, project_name)

    def elicitation_menu(self) -> str:
        """Return the formatted elicitation menu."""
        return build_elicitation_menu()

    def elicitation_options(self) -> Tuple[ElicitationOption, ...]:
        """Return the elicitation options for downstream use."""
        menu = ElicitationMenu()
        return tuple(menu.build())

    def record_elicitation_history(
        self,
        state: MutableMapping[str, Any],
        selection_number: int,
        selection_label: str,
        timestamp: str,
        user_feedback: Optional[str] = None,
        applied_changes: Optional[str] = None,
    ) -> None:
        """Append an elicitation event to workflow state."""
        history = state.setdefault("elicitation_history", [])
        history.append(
            {
                "phase": "discovery",
                "timestamp": timestamp,
                "method_selected": f"{selection_number}. {selection_label}",
                "user_response": user_feedback,
                "applied_changes": applied_changes,
            }
        )
        self._state_store.save(state)

    def finalise_discovery(self, state: MutableMapping[str, Any], timestamp: str) -> None:
        """Mark the discovery phase as complete and prepare for analyst handoff."""
        project_discovery = state.setdefault("project_discovery", {})
        project_discovery["discovery_completed"] = True
        project_discovery["discovery_timestamp"] = timestamp

        elicitation_completed = state.setdefault("elicitation_completed", {})
        elicitation_completed["discovery"] = True

        completed_phases = state.setdefault("completed_phases", [])
        if "discovery" not in completed_phases:
            completed_phases.append("discovery")

        state["current_phase"] = "analyst"
        agent_context = state.setdefault("agent_context", {})
        agent_context["current_agent"] = "analyst"
        transformation_history = agent_context.setdefault("transformation_history", [])
        transformation_history.append(
            {
                "from": "discovery",
                "to": "analyst",
                "timestamp": timestamp,
                "context_passed": {"project_discovery": True},
            }
        )
        agent_context["last_transformation"] = timestamp

        record_quality_gate_placeholder(
            state,
            QualityGateResult.not_run(DISCOVERY_CHECKLIST_PATH),
            phase="discovery",
        )

        state["last_updated"] = timestamp
        self._state_store.save(state)
