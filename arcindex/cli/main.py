"""
Arcindex CLI entry point.

Provides a minimal discovery workflow experience for the Phase 1 milestone.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Dict, Optional, Tuple

import click

try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.key_binding import KeyBindings

    PROMPT_TOOLKIT_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency fallback
    PROMPT_TOOLKIT_AVAILABLE = False
    PromptSession = None  # type: ignore
    KeyBindings = None  # type: ignore

from arcindex.orchestrator import OrchestratorController
from arcindex.runner import ArcindexRunner
from arcindex.tools import ElicitationOption, current_timestamp

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "runtime.yaml"


@click.group(help="Arcindex CLI. Discovery orchestration is available in this release.")
def arcindex() -> None:
    """Primary command group for Arcindex."""


@arcindex.command(help="Start a discovery workflow run.")
@click.argument("workflow_id", required=False)
@click.option("--project-name", "-p", help="Project name or working title.", type=str)
@click.option(
    "--mode",
    type=click.Choice(["interactive", "batch", "yolo"]),
    help="Override the operation mode (default is taken from the runtime config).",
)
@click.option(
    "--answers-file",
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
    help="Path to a file containing numbered discovery answers (1-9).",
)
@click.option(
    "--config",
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
    help="Path to an alternative runtime configuration file.",
)
@click.option(
    "--elicitation-choice",
    type=click.IntRange(1, 9),
    help="Non-interactive selection for the elicitation menu (defaults to 1: proceed).",
)
def start(
    workflow_id: Optional[str],
    project_name: Optional[str],
    mode: Optional[str],
    answers_file: Optional[Path],
    config: Optional[Path],
    elicitation_choice: Optional[int],
) -> None:
    """Start the discovery workflow."""
    config_path = config or DEFAULT_CONFIG_PATH
    controller = OrchestratorController.from_config_path(config_path)

    workflow_id = workflow_id or controller.config.system.default_workflow
    if workflow_id != "greenfield-discovery":
        raise click.UsageError(
            f"Workflow '{workflow_id}' is not yet supported. "
            "The discovery MVP only implements 'greenfield-discovery'."
        )

    controller.ensure_no_active_workflow()

    runner = ArcindexRunner(controller)

    operation_mode = mode or controller.config.elicitation.default_mode
    state, timestamp = controller.initialise_discovery(workflow_id, project_name, operation_mode)

    click.echo(_initialisation_message(project_name, workflow_id, operation_mode))
    click.echo()
    click.echo(controller.discovery_questions(project_name))

    answers = _load_answers(controller, project_name, answers_file)
    if not answers:
        raise click.UsageError("No discovery answers captured; aborting workflow.")

    # Ensure project name is available in the answer set
    if project_name and "project_name" not in answers:
        answers["project_name"] = project_name

    def _event_printer(event: Dict[str, object]) -> None:
        event_type = event.get("event")
        if event_type == "phase":
            phase = event.get("phase")
            status = event.get("status")
            if status == "start":
                click.echo(f"🚀 Phase '{phase}' started.")
            elif status == "end":
                click.echo(f"✅ Phase '{phase}' completed.")
        elif event_type == "artifact":
            artifact_type = event.get("artifact_type")
            path = event.get("path")
            click.echo(f"📝 Artifact saved: {artifact_type} → {path}")

    run_context = runner.create_run(subscribers=[_event_printer])
    controller.bind_run_directory(run_context.artifact_store.run_directory, state)

    summary_markdown = controller.summary_markdown(answers, project_name)

    click.echo("\n✅ Discovery answers captured.\n")
    click.echo(summary_markdown)
    click.echo()

    options = controller.elicitation_options()
    menu_text = controller.elicitation_menu()
    selection = elicitation_choice

    while True:
        click.echo(menu_text)

        if selection is None:
            selection = _prompt_elicitation_selection()
        else:
            click.echo(f"Selection: {selection}")

        if selection == 1:
            break

        selected_label = _lookup_option_label(options, selection)
        controller.record_elicitation_history(
            state,
            selection_number=selection,
            selection_label=selected_label,
            timestamp=current_timestamp(),
            user_feedback=None,
            applied_changes=None,
        )

        click.echo(
            "🔁 Discovery elicitation methods are not yet automated; summary remains unchanged."
        )
        click.echo(summary_markdown)
        selection = None

    run_result = asyncio.run(
        runner.complete_discovery(
            run_context,
            state,
            answers,
            timestamp,
            project_name,
        )
    )

    click.echo("\n✅ Discovery phase complete!")
    click.echo(f"🆔 Run ID: {run_result.run_id}")
    click.echo(f"🗂️  Discovery summary saved to {run_result.summary_path}")
    if run_result.summary_artifact:
        click.echo(f"📦  Artifact URI: {run_result.summary_artifact.uri}")
    click.echo(f"🧾 Events log written to {run_result.events_path}")
    click.echo(f"🗄️  Workflow state written to {controller.config.state.workflow_path}")


def _initialisation_message(
    project_name: Optional[str],
    workflow_id: str,
    operation_mode: str,
) -> str:
    resolved_project = project_name or "To be determined"
    return (
        "🎯 Arcindex Orchestrator Activated\n\n"
        "---\n"
        "Workflow Initialization\n\n"
        f"- Project: {resolved_project}\n"
        f"- Workflow Type: {workflow_id}\n"
        f"- Operation Mode: {operation_mode.capitalize()}\n\n"
        "---\n"
        "Available Commands\n"
        "- `arcindex start` — start a new workflow (current command)\n"
        "- `arcindex continue` — resume once multi-phase support arrives\n"
        "- `arcindex status` — inspect the workflow state (coming soon)\n"
    )


def _load_answers(
    controller: OrchestratorController,
    project_name: Optional[str],
    answers_file: Optional[Path],
) -> Dict[str, str]:
    if answers_file:
        raw = answers_file.read_text(encoding="utf-8")
        return dict(controller.parse_answers(raw))

    click.echo(
        "\nEnter responses for each question. Press ENTER to accept the answer. "
        "Use Ctrl+J to insert a newline if needed.\n"
    )
    answers: Dict[str, str] = {}
    for question, prompt in controller.discovery_questionnaire(project_name):
        click.echo(f"{question.number}. {prompt}")
        response = _prompt_answer()
        answers[question.key] = response
        click.echo()
    return answers


def _prompt_answer() -> str:
    if PROMPT_TOOLKIT_AVAILABLE:
        bindings = KeyBindings()

        @bindings.add("enter", eager=True)
        def _(event) -> None:  # type: ignore[no-redef]
            event.app.current_buffer.validate_and_handle()

        @bindings.add("c-j", eager=True)
        def _(event) -> None:  # type: ignore[no-redef]
            event.current_buffer.insert_text("\n")

        session = PromptSession(multiline=True, key_bindings=bindings)
        try:
            return session.prompt("> ").strip()
        except EOFError:
            return ""
    # Fallback: single-line prompt
    return click.prompt(">", default="", show_default=False).strip()


def _prompt_elicitation_selection() -> int:
    return click.prompt("Selection", type=click.IntRange(1, 9))


def _lookup_option_label(
    options: Tuple[ElicitationOption, ...],
    selection: int,
) -> str:
    for option in options:
        if option.number == selection:
            return option.label
    return "Proceed"


def main() -> None:
    """Invoke the CLI programmatically."""
    arcindex()


if __name__ == "__main__":
    main()
