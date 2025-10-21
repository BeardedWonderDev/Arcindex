"""Arcindex CLI entry point aligned with the Codex Agents SDK quickstart."""

from __future__ import annotations

import asyncio

import click

from arcindex.workflows import discovery_to_analyst as workflow


@click.group(help="Arcindex CLI orchestrating Codex Agents SDK workflows.")
def arcindex() -> None:
    """Primary command group for Arcindex."""


@arcindex.command(help="Start a new Arcindex workflow run using Codex quickstart agents.")
@click.option(
    "--task",
    default=workflow.DEFAULT_DISCOVERY_TO_ANALYST_TASK,
    show_default=True,
    help="High-level task description provided to the orchestrator agent.",
)
@click.option(
    "--model",
    default=workflow.DEFAULT_MODEL,
    show_default=True,
    help="Model identifier shared across orchestrator, discovery, and analyst agents.",
)
@click.option(
    "--max-turns",
    default=24,
    show_default=True,
    type=click.IntRange(1, 120),
    help="Maximum number of turns the runner may execute for this workflow.",
)
def start(task: str, model: str, max_turns: int) -> None:
    """
    Launch the orchestrated discovery-to-analyst workflow via the Codex Agents SDK.
    """
    click.echo("🚀 Starting Arcindex workflow using Codex Agents SDK ...")
    result = asyncio.run(
        workflow.run_discovery_to_analyst(
            task=task,
            model=model,
            max_turns=max_turns,
        )
    )
    click.echo("\n✅ Workflow completed.")
    click.echo(result.final_output)
    click.echo(
        "\nℹ️  TODO: Persist workflow state and artefacts to support context retention across runs."
    )


@arcindex.command(name="continue", help="Resume a paused workflow run (placeholder).")
def continue_() -> None:
    """
    Placeholder for resuming workflows once multi-run persistence is implemented.
    """
    click.echo(
        "⏸️  `arcindex continue` is not yet implemented. "
        "TODO: restore workflow context once run persistence and guardrails migrate to Codex SDK."
    )


def main() -> None:
    """Console script entry point."""
    arcindex()


__all__ = ["arcindex", "start", "continue_", "main"]
