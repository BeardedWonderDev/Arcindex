"""
Agent configuration scaffolding.

Phase 1 will introduce discovery agent bindings sourced from the legacy implementation.
"""

from .base import BaseAgent
from .discovery import DiscoveryAgent, DiscoveryResult

__all__ = [
    "BaseAgent",
    "DiscoveryAgent",
    "DiscoveryResult",
]
