"""
FastAPI bridge exposing Arcindex runs over HTTP.
"""

from .app import create_app

__all__ = ["create_app"]
