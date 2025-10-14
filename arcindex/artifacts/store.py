"""
Run-scoped artifact storage utilities.

Artifacts are written beneath ``runs/<run_id>/artifacts/...`` and referenced via
``arc://`` URIs so downstream consumers can resolve them without guessing paths.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping, MutableMapping, Optional, Union


@dataclass(frozen=True)
class ArtifactRecord:
    """Represents a persisted artifact."""

    artifact_type: str
    path: Path
    uri: str
    sha256: str
    phase: Optional[str]
    agent: Optional[str]
    mime_type: Optional[str]
    metadata: Optional[Mapping[str, Any]]

    def to_event_payload(self) -> MutableMapping[str, Any]:
        """
        Convert this record into a payload suitable for an artifact event.
        """
        payload: MutableMapping[str, Any] = {
            "artifact_type": self.artifact_type,
            "path": str(self.path),
            "sha256": self.sha256,
        }
        if self.phase:
            payload["phase"] = self.phase
        if self.agent:
            payload["agent"] = self.agent
        if self.uri:
            payload["uri"] = self.uri
        if self.mime_type:
            payload["mime_type"] = self.mime_type
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


class ArtifactStore:
    """
    Persist artifacts for a single run.

    ``runs_root`` should point to the directory containing ``runs/<run_id>``.
    The store will create the run directory on demand.
    """

    def __init__(self, run_id: str, runs_root: Path) -> None:
        self._run_id = run_id
        self._runs_root = runs_root
        self._run_dir = self._prepare_run_directory()

    @property
    def run_directory(self) -> Path:
        """Absolute path to the run directory."""
        return self._run_dir

    def write_text(
        self,
        artifact_type: str,
        content: str,
        *,
        phase: Optional[str] = None,
        agent: Optional[str] = None,
        extension: str = ".md",
        encoding: str = "utf-8",
        mime_type: Optional[str] = None,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> ArtifactRecord:
        """Write a text artifact."""
        data = content.encode(encoding)
        return self._write_bytes(
            artifact_type,
            data,
            phase=phase,
            agent=agent,
            extension=extension,
            mime_type=mime_type or "text/markdown",
            metadata=metadata,
        )

    def write_json(
        self,
        artifact_type: str,
        document: Union[Mapping[str, Any], Any],
        *,
        phase: Optional[str] = None,
        agent: Optional[str] = None,
        metadata: Optional[Mapping[str, Any]] = None,
        sort_keys: bool = True,
    ) -> ArtifactRecord:
        """Write a JSON artifact."""
        text = json.dumps(document, indent=2, sort_keys=sort_keys)
        return self._write_bytes(
            artifact_type,
            text.encode("utf-8"),
            phase=phase,
            agent=agent,
            extension=".json",
            mime_type="application/json",
            metadata=metadata,
        )

    def write_bytes(
        self,
        artifact_type: str,
        blob: bytes,
        *,
        phase: Optional[str] = None,
        agent: Optional[str] = None,
        extension: str,
        mime_type: Optional[str] = None,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> ArtifactRecord:
        """Write arbitrary binary data to the store."""
        return self._write_bytes(
            artifact_type,
            blob,
            phase=phase,
            agent=agent,
            extension=extension,
            mime_type=mime_type,
            metadata=metadata,
        )

    def _write_bytes(
        self,
        artifact_type: str,
        blob: bytes,
        *,
        phase: Optional[str],
        agent: Optional[str],
        extension: str,
        mime_type: Optional[str],
        metadata: Optional[Mapping[str, Any]],
    ) -> ArtifactRecord:
        rel_path = self._resolve_relative_path(artifact_type, extension, phase, agent)
        abs_path = self._run_dir / rel_path
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        with abs_path.open("wb") as handle:
            handle.write(blob)

        checksum = sha256(blob).hexdigest()
        uri = f"arc://runs/{self._run_id}/{rel_path.as_posix()}"
        return ArtifactRecord(
            artifact_type=artifact_type,
            path=abs_path,
            uri=uri,
            sha256=checksum,
            phase=phase,
            agent=agent,
            mime_type=mime_type,
            metadata=metadata,
        )

    def _prepare_run_directory(self) -> Path:
        run_dir = self._runs_root / self._run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "artifacts").mkdir(exist_ok=True)
        (run_dir / "logs").mkdir(exist_ok=True)
        return run_dir

    @staticmethod
    def _normalize_component(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        sanitized = value.strip().replace(" ", "-")
        return sanitized or None

    def _resolve_relative_path(
        self,
        artifact_type: str,
        extension: str,
        phase: Optional[str],
        agent: Optional[str],
    ) -> Path:
        components = ["artifacts"]
        norm_phase = self._normalize_component(phase)
        norm_agent = self._normalize_component(agent)
        if norm_phase:
            components.append(norm_phase)
        if norm_agent:
            components.append(norm_agent)

        filename = f"{artifact_type}{extension}"
        return Path(os.path.join(*components, filename))
