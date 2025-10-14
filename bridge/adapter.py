"""
Adapters that connect the Arcindex runner to HTTP/SSE consumers.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from arcindex.orchestrator import OrchestratorController
from arcindex.runner import ArcindexRunner, RunContext, RunResult


def _sse_frame(event: Dict[str, Any]) -> str:
    """Render an event payload as an SSE frame."""
    return f"event: {event.get('event', 'message')}\ndata: {json.dumps(event)}\n\n"


def _make_queue_subscriber(queue: "asyncio.Queue[Dict[str, Any]]", loop: asyncio.AbstractEventLoop):
    def _subscriber(payload: Dict[str, Any]) -> None:
        loop.call_soon_threadsafe(queue.put_nowait, payload)

    return _subscriber


@dataclass
class RunJob:
    """Holds context for an active run."""

    run_id: str
    runner: ArcindexRunner
    context: RunContext
    queue: "asyncio.Queue[Dict[str, Any]]"
    task: asyncio.Task[RunResult]
    controller: OrchestratorController
    result: Optional[RunResult] = None
    cancelled: bool = False
    subscribers: Iterable[Any] = field(default_factory=tuple)
    completed: bool = False


class RunJobManager:
    """Manage active Arcindex runs for the HTTP bridge."""

    def __init__(self, runtime_config: Path) -> None:
        self._runtime_config = runtime_config
        self._jobs: Dict[str, RunJob] = {}
        self._lock = asyncio.Lock()

    async def start_job(
        self,
        *,
        project_name: Optional[str],
        answers: Dict[str, str],
        workflow_id: Optional[str] = None,
        operation_mode: Optional[str] = None,
        elicitation_choice: int = 1,
    ) -> RunJob:
        """Start a discovery run and stream events to a queue."""
        controller = OrchestratorController.from_config_path(self._runtime_config)
        runner = ArcindexRunner(controller)

        workflow_id = workflow_id or controller.config.system.default_workflow
        state, timestamp = controller.initialise_discovery(workflow_id, project_name, operation_mode)

        if project_name and "project_name" not in answers:
            answers["project_name"] = project_name

        loop = asyncio.get_running_loop()
        queue: "asyncio.Queue[Dict[str, Any]]" = asyncio.Queue()
        context = runner.create_run(subscribers=[_make_queue_subscriber(queue, loop)])

        controller.bind_run_directory(context.artifact_store.run_directory, state)
        controller.summary_markdown(answers, project_name)

        if elicitation_choice != 1:
            options = controller.elicitation_options()
            selected_label = next((opt.label for opt in options if opt.number == elicitation_choice), None)
            if selected_label:
                controller.record_elicitation_history(
                    state,
                    selection_number=elicitation_choice,
                    selection_label=selected_label,
                    timestamp=timestamp,
                    user_feedback=None,
                    applied_changes=None,
                )

        async def _execute_run() -> RunResult:
            try:
                result = await runner.complete_discovery(
                    context,
                    state,
                    answers,
                    timestamp,
                    project_name,
                )
                return result
            finally:
                controller = None  # help GC

        task = asyncio.create_task(_execute_run())
        job = RunJob(
            run_id=context.run_id,
            runner=runner,
            context=context,
            queue=queue,
            task=task,
            controller=controller,
        )
        task.add_done_callback(lambda t, rid=context.run_id: self._on_run_complete(rid, t))
        async with self._lock:
            self._jobs[context.run_id] = job
        return job

    def _on_run_complete(self, run_id: str, task: asyncio.Task[RunResult]) -> None:
        try:
            result = task.result()
        except Exception:  # pragma: no cover - result handled by callers
            result = None
        job = self._jobs.get(run_id)
        if job:
            job.result = result
            job.completed = True

    async def get_job(self, run_id: str) -> Optional[RunJob]:
        async with self._lock:
            return self._jobs.get(run_id)

    async def remove_job(self, run_id: str) -> None:
        async with self._lock:
            self._jobs.pop(run_id, None)

    async def cancel_run(self, run_id: str) -> str:
        job = await self.get_job(run_id)
        if not job:
            return "not_found"

        if job.task.done():
            await self.remove_job(run_id)
            return "completed"

        job.runner.cancel()
        job.cancelled = True
        await job.task
        await self.remove_job(run_id)
        return "cancelling"

    async def stream_events(self, run_id: str):
        job = await self.get_job(run_id)
        if not job:
            return None

        async def _generator():
            try:
                while True:
                    event = await job.queue.get()
                    yield _sse_frame(event)
                    if event.get("event") == "end":
                        break
            finally:
                pass

        return _generator()
