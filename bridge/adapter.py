"""
Adapters that connect the Arcindex runner to HTTP/SSE consumers.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, MutableMapping, Optional, Tuple

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
    controller: OrchestratorController
    state: MutableMapping[str, Any]
    timestamp: str
    project_name: Optional[str]
    expected_keys: Tuple[str, ...]
    questionnaire: List[Dict[str, Any]]
    answers: Dict[str, str] = field(default_factory=dict)
    elicitation_choice: int = 1
    task: Optional[asyncio.Task[RunResult]] = None
    result: Optional[RunResult] = None
    cancelled: bool = False
    completed: bool = False

    def missing_keys(self) -> List[str]:
        return [key for key in self.expected_keys if key not in self.answers]


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
        answers: Optional[Dict[str, str]] = None,
        workflow_id: Optional[str] = None,
        operation_mode: Optional[str] = None,
        elicitation_choice: int = 1,
    ) -> Tuple[RunJob, str]:
        """Create a discovery job and, when possible, launch it immediately."""
        controller = OrchestratorController.from_config_path(self._runtime_config)
        runner = ArcindexRunner(controller)

        workflow_id = workflow_id or controller.config.system.default_workflow
        state, timestamp = controller.initialise_discovery(workflow_id, project_name, operation_mode)

        questionnaire_raw = controller.discovery_questionnaire(project_name)
        questionnaire = [
            {
                "number": question.number,
                "key": question.key,
                "prompt": prompt,
            }
            for question, prompt in questionnaire_raw
        ]
        expected_keys = tuple(question.key for question, _ in questionnaire_raw)

        merged_answers: Dict[str, str] = dict(answers or {})
        if project_name and "project_name" not in merged_answers:
            merged_answers["project_name"] = project_name

        loop = asyncio.get_running_loop()
        queue: "asyncio.Queue[Dict[str, Any]]" = asyncio.Queue()
        context = runner.create_run(
            subscribers=[_make_queue_subscriber(queue, loop)],
            emit_phase_start=False,
        )

        controller.bind_run_directory(context.artifact_store.run_directory, state)

        job = RunJob(
            run_id=context.run_id,
            runner=runner,
            context=context,
            queue=queue,
            controller=controller,
            state=state,
            timestamp=timestamp,
            project_name=project_name,
            expected_keys=expected_keys,
            questionnaire=questionnaire,
            answers=merged_answers,
            elicitation_choice=elicitation_choice,
        )

        async with self._lock:
            self._jobs[context.run_id] = job

        status = await self._launch_if_ready(job)
        return job, status

    def _on_run_complete(self, run_id: str, task: asyncio.Task[RunResult]) -> None:
        try:
            result = task.result()
        except Exception:  # pragma: no cover
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

        if job.task and job.task.done():
            await self.remove_job(run_id)
            return "completed"

        if job.task is None:
            job.queue.put_nowait({"event": "end", "status": "cancelled"})
            await self.remove_job(run_id)
            return "cancelled"

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

    async def submit_answers(
        self,
        run_id: str,
        answers: Dict[str, str],
        *,
        elicitation_choice: Optional[int] = None,
    ) -> str:
        job = await self.get_job(run_id)
        if not job:
            return "not_found"

        if job.task and job.task.done():
            return "completed"

        if elicitation_choice is not None:
            job.elicitation_choice = elicitation_choice

        job.answers.update(answers)
        job.queue.put_nowait(
            {
                "event": "answers",
                "answers": job.answers,
                "missing": job.missing_keys(),
            }
        )
        return await self._launch_if_ready(job)

    async def _launch_if_ready(self, job: RunJob) -> str:
        if job.missing_keys():
            job.queue.put_nowait(
                {
                    "event": "prompt",
                    "questions": job.questionnaire,
                    "missing": job.missing_keys(),
                }
            )
            return "pending"

        if job.task is not None:
            return "started"

        job.queue.put_nowait(
            {
                "event": "answers",
                "answers": job.answers,
                "missing": [],
            }
        )

        controller = job.controller
        state = job.state
        answers = dict(job.answers)
        project_name = job.project_name

        summary_markdown = controller.summary_markdown(answers, project_name)
        job.queue.put_nowait(
            {
                "event": "summary",
                "summary": summary_markdown,
            }
        )

        if job.elicitation_choice != 1:
            options = controller.elicitation_options()
            selected_option = next(
                (opt for opt in options if opt.number == job.elicitation_choice),
                None,
            )
            if selected_option is None:
                raise ValueError(f"Invalid elicitation selection: {job.elicitation_choice}")
            summary_markdown = controller.apply_elicitation(
                state,
                answers,
                job.elicitation_choice,
                selected_option,
                project_name,
            )
            job.queue.put_nowait(
                {
                    "event": "elicitation",
                    "method": selected_option.label,
                    "description": selected_option.description,
                    "summary": summary_markdown,
                }
            )

        async def _execute_run() -> RunResult:
            try:
                return await job.runner.complete_discovery(
                    job.context,
                    state,
                    answers,
                    job.timestamp,
                    project_name,
                )
            finally:
                job.controller = None  # help GC

        task = asyncio.create_task(_execute_run())
        job.task = task
        task.add_done_callback(lambda t, rid=job.run_id: self._on_run_complete(rid, t))
        return "started"
