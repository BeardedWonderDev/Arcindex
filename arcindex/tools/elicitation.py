"""
Advanced elicitation menu utilities.

This module captures the legacy requirement that option 1 must always be a proceed
action while the remaining options provide reflective techniques for improving content.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

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
_METHODS_PATH = Path(__file__).resolve().parent.parent / "resources" / "elicitation-methods.md"


@dataclass(frozen=True)
class ElicitationOption:
    """Represents a single elicitation option shown to the user."""

    number: int
    label: str
    description: Optional[str] = None

    def as_line(self) -> str:
        """Render the option as a numbered menu line."""
        return f"{self.number}. {self.label}"


class ElicitationMenu:
    """Constructs and formats advanced elicitation menus."""

    def __init__(self, methods: Sequence[str] | None = None) -> None:
        self._methods = list(methods or DEFAULT_METHODS)

    def build(self) -> List[ElicitationOption]:
        """Return a list of menu options adhering to the 1–9 convention."""
        options: List[ElicitationOption] = [
            ElicitationOption(1, PROCEED_LABEL, "Move forward without further refinement.")
        ]
        registry = _load_method_details()
        for index, method in enumerate(self._selected_methods(), start=2):
            options.append(
                ElicitationOption(
                    index,
                    method,
                    registry.get(method, "Apply the selected elicitation technique."),
                )
            )
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


@lru_cache(maxsize=1)
def _load_method_details() -> Dict[str, str]:
    """
    Parse the elicitation methods markdown into a mapping of label -> guidance text.
    """
    details: Dict[str, str] = {}
    if not _METHODS_PATH.exists():
        return details

    current_label: Optional[str] = None
    current_lines: List[str] = []
    for raw_line in _METHODS_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("**") and line.endswith("**"):
            if current_label and current_lines:
                details[current_label] = "\n".join(current_lines).strip()
            current_label = line.strip("* ")
            current_lines = []
            continue

        if line.startswith("##"):
            # Section heading – flush any accumulated block.
            if current_label and current_lines:
                details[current_label] = "\n".join(current_lines).strip()
            current_label = None
            current_lines = []
            continue

        if current_label:
            current_lines.append(raw_line)

    if current_label and current_lines:
        details[current_label] = "\n".join(current_lines).strip()

    return details


def get_elicitation_method_details(label: str) -> str:
    """Return detailed instructions for the provided elicitation method."""
    registry = _load_method_details()
    if label == PROCEED_LABEL:
        return "No additional elicitation requested; proceed to the next phase."
    return registry.get(label, "Apply the selected elicitation technique to refine the summary.")


__all__ = [
    "ElicitationMenu",
    "ElicitationOption",
    "PROCEED_LABEL",
    "get_elicitation_method_details",
]
