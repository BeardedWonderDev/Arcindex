"""
Advanced elicitation menu utilities.

This module captures the legacy requirement that option 1 must always be a proceed
action while the remaining options provide reflective techniques for improving content.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

# Core methods pulled from the legacy elicitation catalog; this subset keeps the
# discovery MVP focused while maintaining the familiar experience.
DEFAULT_METHODS: Sequence[str] = (
    "Expand or Contract for Audience",
    "Critique and Refine",
    "Identify Potential Risks and Unforeseen Issues",
    "Assess Alignment with Overall Goals",
    "Tree of Thoughts Deep Dive",
    "Stakeholder Round Table",
    "Self-Consistency Validation",
    "ReWOO (Reasoning Without Observation)",
)

PROCEED_LABEL = "Proceed to next phase"


@dataclass(frozen=True)
class ElicitationOption:
    """Represents a single elicitation option shown to the user."""

    number: int
    label: str

    def as_line(self) -> str:
        """Render the option as a numbered menu line."""
        return f"{self.number}. {self.label}"


class ElicitationMenu:
    """Constructs and formats advanced elicitation menus."""

    def __init__(self, methods: Sequence[str] | None = None) -> None:
        self._methods = list(methods or DEFAULT_METHODS)

    def build(self) -> List[ElicitationOption]:
        """Return a list of menu options adhering to the 1–9 convention."""
        options: List[ElicitationOption] = [ElicitationOption(1, PROCEED_LABEL)]
        for index, method in enumerate(self._selected_methods(), start=2):
            options.append(ElicitationOption(index, method))
        return options

    def format(self, options: Iterable[ElicitationOption] | None = None) -> str:
        """Format the menu for display to the user."""
        opts = list(options or self.build())
        lines = [
            "**Advanced Elicitation Options**",
            "Select 1-9 or type your feedback:",
            "",
        ]
        lines.extend(option.as_line() for option in opts)
        return "\n".join(lines)

    def _selected_methods(self) -> List[str]:
        """Ensure the menu only contains eight discovery-appropriate options."""
        if len(self._methods) >= 8:
            return list(self._methods[:8])
        padded = list(self._methods)
        while len(padded) < 8:
            padded.append("Assess Alignment with Overall Goals")
        return padded

