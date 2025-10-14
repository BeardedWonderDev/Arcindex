"""
Lightweight primitives supporting Arcindex runner execution graphs.
"""

from __future__ import annotations

import asyncio


class CancellationError(RuntimeError):
    """Raised when a run is cancelled."""


class CancellationToken:
    """Async-aware cancellation helper."""

    def __init__(self) -> None:
        self._event = asyncio.Event()

    def cancel(self) -> None:
        """Trigger cancellation."""
        self._event.set()

    def is_cancelled(self) -> bool:
        """Return True if cancellation has been requested."""
        return self._event.is_set()

    async def wait(self) -> None:
        """Await cancellation."""
        await self._event.wait()
