"""
CLI package shim that re-exports the primary command group.
"""

from .main import arcindex, main, start

__all__ = ["arcindex", "start", "main"]
