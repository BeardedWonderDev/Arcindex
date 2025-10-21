"""
Client interfaces for integrating Arcindex agents with the OpenAI SDK.

These helpers encapsulate prompt construction and response handling so the core
agents can remain agnostic of the underlying transport. The implementation is
kept deliberately lightweight—production runs use the OpenAI client, while the
default factory can be swapped during tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Mapping, Optional

try:  # pragma: no cover - the OpenAI SDK may not be installed in test environments
    from openai import OpenAI
except Exception:  # pragma: no cover - fall back to a stub to keep imports happy
    OpenAI = None  # type: ignore[misc,assignment]


@dataclass
class SummaryResponse:
    """Structured response from the LLM when generating a discovery summary."""

    markdown: str
    reasoning: Optional[str] = None


@dataclass
class ElicitationResponse:
    """Structured response captured after applying an elicitation method."""

    markdown: str
    method_label: str
    notes: Optional[str] = None


class DiscoveryLLMClient:
    """
    Protocol-ish base class for discovery specific interactions.

    Concrete implementations must provide the two public methods below.  The
    interface mirrors the behaviours exercised by the discovery agent so tests
    can provide inexpensive stand-ins.
    """

    def generate_summary(
        self,
        *,
        answers: Mapping[str, str],
        project_name: Optional[str],
        workflow_type: str,
    ) -> SummaryResponse:
        raise NotImplementedError

    def apply_elicitation(
        self,
        *,
        method_label: str,
        method_instructions: str,
        current_summary: str,
        answers: Mapping[str, str],
        project_name: Optional[str],
        workflow_type: str,
    ) -> ElicitationResponse:
        raise NotImplementedError


def _render_answer_table(answers: Mapping[str, str]) -> str:
    """Render the discovery answers as markdown to provide structure to the model."""
    lines: List[str] = ["| Question Key | Response |", "|--------------|----------|"]
    for key, value in answers.items():
        sanitized = value.replace("\n", " ").strip()
        lines.append(f"| {key} | {sanitized or '*Not provided*'} |")
    return "\n".join(lines)


class OpenAIDiscoveryClient(DiscoveryLLMClient):
    """
    Thin wrapper around the OpenAI Responses API.

    The prompts lean on deterministic formatting so downstream tooling can rely
    on markdown headings that match the structured JSON persisted elsewhere.
    """

    def __init__(
        self,
        *,
        summary_model: str = "gpt-4.1-mini",
        elicitation_model: Optional[str] = None,
        client_factory: Optional[Callable[[], OpenAI]] = None,
    ) -> None:
        if OpenAI is None:  # pragma: no cover - enforced in production environments
            raise RuntimeError(
                "OpenAI SDK is required but not installed. "
                "Install the 'openai' package or inject a custom client."
            )
        self._summary_model = summary_model
        self._elicitation_model = elicitation_model or summary_model
        self._client_factory = client_factory or OpenAI

    def _client(self) -> OpenAI:
        return self._client_factory()  # type: ignore[return-value]

    def generate_summary(
        self,
        *,
        answers: Mapping[str, str],
        project_name: Optional[str],
        workflow_type: str,
    ) -> SummaryResponse:
        prompt = self._build_summary_prompt(answers, project_name, workflow_type)
        client = self._client()
        response = client.responses.create(  # type: ignore[union-attr]
            model=self._summary_model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are the Arcindex Discovery Agent. "
                        "Produce a concise, implementation-ready discovery summary in markdown. "
                        "Respect the heading structure shown in the instructions and do not invent "
                        "additional sections. Capture concrete details from the provided answers."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )
        markdown = (getattr(response, "output_text", None) or "").strip()
        if not markdown:
            # Fall back to first text block when output_text isn't populated.
            for output in getattr(response, "output", []):
                for content in getattr(output, "content", []):
                    if getattr(content, "type", None) == "output_text":
                        markdown += getattr(content, "text", "")
            markdown = markdown.strip()

        if not markdown:
            raise RuntimeError("OpenAI response did not include summary markdown.")

        return SummaryResponse(markdown=markdown)

    def apply_elicitation(
        self,
        *,
        method_label: str,
        method_instructions: str,
        current_summary: str,
        answers: Mapping[str, str],
        project_name: Optional[str],
        workflow_type: str,
    ) -> ElicitationResponse:
        prompt = self._build_elicitation_prompt(
            method_label,
            method_instructions,
            current_summary,
            answers,
            project_name,
            workflow_type,
        )
        client = self._client()
        response = client.responses.create(  # type: ignore[union-attr]
            model=self._elicitation_model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "Apply the requested elicitation method to the discovery summary. "
                        "Preserve markdown formatting, keep the original headings, and fold the "
                        "refinements directly into the summary. Provide the updated summary only."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )
        markdown = (getattr(response, "output_text", None) or "").strip()
        if not markdown:
            for output in getattr(response, "output", []):
                for content in getattr(output, "content", []):
                    if getattr(content, "type", None) == "output_text":
                        markdown += getattr(content, "text", "")
            markdown = markdown.strip()

        if not markdown:
            raise RuntimeError("OpenAI response did not include elicitation output.")

        return ElicitationResponse(markdown=markdown, method_label=method_label)

    @staticmethod
    def _build_summary_prompt(
        answers: Mapping[str, str],
        project_name: Optional[str],
        workflow_type: str,
    ) -> str:
        table = _render_answer_table(answers)
        effective_name = project_name or answers.get("project_name") or "TBD Project"
        return (
            f"Project workflow type: {workflow_type}\n"
            f"Project name: {effective_name}\n\n"
            "Discovery answers (markdown table):\n"
            f"{table}\n\n"
            "Produce markdown using the following section headings:\n"
            "- Project Name\n"
            "- Concept\n"
            "- Target Users\n"
            "- Research Status\n"
            "- Competitive Landscape\n"
            "- Market Opportunity\n"
            "- Technical Constraints\n"
            "- Integration Requirements\n"
            "- Success Criteria\n"
            "- Recommended Next Steps\n"
        )

    @staticmethod
    def _build_elicitation_prompt(
        method_label: str,
        method_instructions: str,
        current_summary: str,
        answers: Mapping[str, str],
        project_name: Optional[str],
        workflow_type: str,
    ) -> str:
        table = _render_answer_table(answers)
        effective_name = project_name or answers.get("project_name") or "TBD Project"
        return (
            f"You must apply the elicitation method '{method_label}'.\n\n"
            f"Method guidance:\n{method_instructions.strip()}\n\n"
            f"Project name: {effective_name}\n"
            f"Workflow type: {workflow_type}\n"
            "Discovery answers:\n"
            f"{table}\n\n"
            "Current discovery summary (markdown):\n"
            f"{current_summary.strip()}\n\n"
            "Return only the updated markdown summary."
        )


__all__ = [
    "DiscoveryLLMClient",
    "ElicitationResponse",
    "OpenAIDiscoveryClient",
    "SummaryResponse",
]

