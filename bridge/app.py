"""
FastAPI application exposing Arcindex runs via HTTP and SSE.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from .adapter import RunJobManager
from arcindex.orchestrator import OrchestratorController


class BridgeSettings(BaseModel):
    """Runtime settings for the bridge."""

    runtime_config: Path = Field(..., description="Path to the Arcindex runtime configuration YAML.")


class JobRequest(BaseModel):
    """Payload for creating a discovery job."""

    project_name: Optional[str] = None
    answers: Optional[Dict[str, str]] = None
    workflow_id: Optional[str] = None
    operation_mode: Optional[str] = None
    elicitation_choice: int = 1


class AnswerUpdate(BaseModel):
    """Incremental answer submission payload."""

    answers: Dict[str, str]
    elicitation_choice: Optional[int] = None


def _default_runtime_config() -> Path:
    return Path(__file__).resolve().parent.parent / "arcindex" / "config" / "runtime.yaml"


def create_app(runtime_config_path: Optional[Path] = None) -> FastAPI:
    """Construct the FastAPI application."""
    runtime_config_path = runtime_config_path or _default_runtime_config()
    app = FastAPI(title="Arcindex Bridge", version="0.1.0")
    settings = BridgeSettings(runtime_config=runtime_config_path)
    manager = RunJobManager(settings.runtime_config)

    def get_manager() -> RunJobManager:
        return manager

    @app.get("/discovery/questions")
    async def list_questions() -> Dict[str, object]:
        controller = OrchestratorController.from_config_path(settings.runtime_config)
        questionnaire = controller.discovery_questionnaire(None)
        questions = [
            {
                "number": question.number,
                "key": question.key,
                "prompt": prompt,
            }
            for question, prompt in questionnaire
        ]
        return {"questions": questions, "count": len(questions)}

    @app.post("/jobs", status_code=status.HTTP_202_ACCEPTED)
    async def create_job(request: JobRequest, mgr: RunJobManager = Depends(get_manager)):
        job, status_value = await mgr.start_job(
            project_name=request.project_name,
            answers=dict(request.answers or {}),
            workflow_id=request.workflow_id,
            operation_mode=request.operation_mode,
            elicitation_choice=request.elicitation_choice,
        )
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={"run_id": job.run_id, "status": status_value},
        )

    @app.post("/jobs/{run_id}/answers")
    async def submit_answers(
        run_id: str,
        payload: AnswerUpdate,
        mgr: RunJobManager = Depends(get_manager),
    ):
        status_value = await mgr.submit_answers(
            run_id,
            dict(payload.answers),
            elicitation_choice=payload.elicitation_choice,
        )
        if status_value == "not_found":
            raise HTTPException(status_code=404, detail="Run not found")
        return {"run_id": run_id, "status": status_value}

    @app.get("/events/{run_id}")
    async def stream_events(run_id: str, request: Request, mgr: RunJobManager = Depends(get_manager)):
        generator = await mgr.stream_events(run_id)
        if generator is None:
            raise HTTPException(status_code=404, detail="Run not found")

        return StreamingResponse(
            generator,
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache"},
        )

    @app.post("/cancel/{run_id}")
    async def cancel_run(run_id: str, mgr: RunJobManager = Depends(get_manager)):
        status_value = await mgr.cancel_run(run_id)
        if status_value == "not_found":
            raise HTTPException(status_code=404, detail="Run not found")
        return {"run_id": run_id, "status": status_value}

    return app
