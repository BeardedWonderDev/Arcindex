"""
Discovery workflow helpers.

These utilities mirror the behavior described in the legacy discovery agent instructions.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, MutableMapping, Optional, Sequence, Tuple

from arcindex.tools import ElicitationMenu, QualityGateResult, record_quality_gate_placeholder

DISCOVERY_CHECKLIST_PATH = "legacy/.codex/checklists/discovery-quality-gate.md"


@dataclass(frozen=True)
class DiscoveryQuestion:
    """Represents a discovery question in the order defined by the legacy agent."""

    number: int
    key: str
    prompt: str
    skip_if_project_name_known: bool = False


QUESTIONS: Sequence[DiscoveryQuestion] = (
    DiscoveryQuestion(
        1,
        "project_name",
        "Project Name/Working Title",
        skip_if_project_name_known=True,
    ),
    DiscoveryQuestion(
        2,
        "project_concept",
        (
            "Brief Project Concept: What are you building with {project_name}? "
            "Describe the core problem you're solving, who will use it, and the primary functionality. "
            "(2-3 paragraphs)"
        ),
    ),
    DiscoveryQuestion(
        3,
        "target_users",
        (
            "Target Users & Pain Points: Who are your target users, and what specific pain points or "
            "challenges are they currently experiencing that this project addresses? "
            "What makes these pain points significant enough to warrant this solution?"
        ),
    ),
    DiscoveryQuestion(
        4,
        "user_research_status",
        (
            "User Research Status: What user research has been conducted so far (interviews, surveys, "
            "market analysis)? If none yet, what research do you plan to conduct, and how will you validate "
            "user needs before building?"
        ),
    ),
    DiscoveryQuestion(
        5,
        "competitive_landscape",
        (
            "Competitive Landscape: Who are the main competitors or alternative solutions in this space? "
            "What are their key strengths and weaknesses? How will your solution differentiate itself "
            "from existing options?"
        ),
    ),
    DiscoveryQuestion(
        6,
        "market_opportunities",
        (
            "Market Opportunity: What market trends, gaps, or opportunities is this project addressing? "
            "Why is now the right time to build this solution? What evidence supports the market demand?"
        ),
    ),
    DiscoveryQuestion(
        7,
        "technical_constraints",
        (
            "Technical Platform & Language: What are the must-have technical constraints for this project? "
            "Specify target platform(s) (iOS, Android, Web, Backend Service, etc.), required programming "
            "languages, and any framework preferences or organizational standards that must be followed."
        ),
    ),
    DiscoveryQuestion(
        8,
        "integration_requirements",
        (
            "Integration Requirements: What existing systems, APIs, or third-party services must this project "
            "integrate with? Are there any authentication, data format, or protocol requirements for these "
            "integrations?"
        ),
    ),
    DiscoveryQuestion(
        9,
        "success_criteria",
        (
            "Success Criteria & Constraints: How will you measure success for this project? "
            "What are the critical success factors, timeline constraints, budget considerations, and any other "
            "limitations (regulatory, compliance, organizational) that will shape the solution?"
        ),
    ),
)

_QUESTION_BY_NUMBER = {question.number: question for question in QUESTIONS}
_QUESTION_BY_KEY = {question.key: question for question in QUESTIONS}
_ANSWER_SPLIT_PATTERN = re.compile(r"^\s*(\d+)[\).\-\:]\s*", re.MULTILINE)


def format_discovery_questions(project_name: Optional[str]) -> str:
    """
    Return the prompt block containing discovery questions.

    The formatting matches the legacy discovery agent, including emoji headers.
    """
    questions = _build_question_lines(project_name)
    question_text = "\n".join(questions)
    return (
        "📋 Discovery Questions\n\n"
        "Please provide answers to the following:\n\n"
        f"{question_text}\n\n"
        "Please provide comprehensive answers to all questions."
    )


def _build_question_lines(project_name: Optional[str]) -> List[str]:
    substitute_name = project_name or "this project"
    lines: List[str] = []
    for question in QUESTIONS:
        if question.skip_if_project_name_known and project_name:
            continue
        text = question.prompt.format(project_name=substitute_name)
        lines.append(f"{question.number}. {text}")
    return lines


def get_discovery_questionnaire(
    project_name: Optional[str],
) -> List[Tuple[DiscoveryQuestion, str]]:
    """Return the ordered list of discovery questions with rendered prompts."""
    substitute_name = project_name or "this project"
    items: List[Tuple[DiscoveryQuestion, str]] = []
    for question in QUESTIONS:
        if question.skip_if_project_name_known and project_name:
            continue
        items.append((question, question.prompt.format(project_name=substitute_name)))
    return items


def parse_discovery_answers(raw_text: str) -> Dict[str, str]:
    """
    Parse numbered discovery answers into a keyed dictionary.

    The parser assumes answers start with `1.` ... `9.` but gracefully ignores missing entries.
    """
    text = raw_text.strip()
    if not text:
        return {}

    parts = _ANSWER_SPLIT_PATTERN.split(text)
    if not parts:
        return {}

    # The split produces ["", "1", "Answer", "2", "Answer", ...]
    if parts[0] == "":
        parts = parts[1:]

    answers: Dict[str, str] = {}
    for index in range(0, len(parts), 2):
        try:
            number = int(parts[index])
        except (ValueError, IndexError):
            continue
        try:
            value = parts[index + 1].strip()
        except IndexError:
            value = ""
        question = _QUESTION_BY_NUMBER.get(number)
        if question:
            answers[question.key] = value
    return answers


def build_discovery_summary_markdown(
    answers: Mapping[str, str],
    project_name: Optional[str],
) -> str:
    """Create a markdown summary block for the discovery phase."""
    effective_name = project_name or answers.get("project_name") or "TBD"
    lines = [
        "📋 Discovery Summary",
        "",
        f"- **Project Name:** {effective_name}",
        f"- **Concept:** {_fallback(answers.get('project_concept'))}",
        f"- **Target Users:** {_fallback(answers.get('target_users'))}",
        f"- **Research Status:** {_fallback(answers.get('user_research_status'))}",
        f"- **Competitive Landscape:** {_fallback(answers.get('competitive_landscape'))}",
        f"- **Market Opportunity:** {_fallback(answers.get('market_opportunities'))}",
        f"- **Technical Constraints:** {_fallback(answers.get('technical_constraints'))}",
        f"- **Integration Requirements:** {_fallback(answers.get('integration_requirements'))}",
        f"- **Success Criteria:** {_fallback(answers.get('success_criteria'))}",
    ]
    return "\n".join(lines)


def persist_discovery_summary(
    state: MutableMapping[str, Any],
    answers: Mapping[str, str],
    state_dir: Path,
    timestamp: str,
) -> Path:
    """
    Persist discovery insights to a JSON file and update the workflow state.

    Returns the path to the saved summary file.
    """
    summary_data = _build_summary_payload(state, answers, timestamp)
    state_dir.mkdir(parents=True, exist_ok=True)
    summary_path = state_dir / "discovery-summary.json"
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary_data, handle, indent=2, sort_keys=True)

    project_discovery = state.setdefault("project_discovery", {})
    project_discovery.update(
        {
            "project_scope": summary_data["project_scope"]["content"],
            "target_users": summary_data["target_users"]["content"],
            "user_research_status": summary_data["user_research_status"]["content"],
            "competitive_landscape": summary_data["competitive_landscape"]["content"],
            "market_opportunities": summary_data["market_opportunities"]["content"],
            "technical_constraints": summary_data["technical_constraints"]["content"],
            "integration_requirements": summary_data["integration_requirements"]["content"],
            "success_criteria": summary_data["success_criteria"]["content"],
            "business_goals": summary_data["business_goals"]["content"],
            "discovery_summary_path": str(summary_path),
            "discovery_completed": False,
            "discovery_timestamp": timestamp,
        }
    )
    if answers.get("project_name"):
        project_discovery["project_name"] = answers["project_name"]
    if answers.get("project_concept"):
        project_discovery["project_concept"] = answers["project_concept"]

    return summary_path


def initialise_quality_gate(state: MutableMapping[str, Any]) -> None:
    """
    Ensure the discovery quality gate has a placeholder entry to mirror legacy behavior.
    """
    record_quality_gate_placeholder(
        state,
        QualityGateResult.not_run(DISCOVERY_CHECKLIST_PATH),
        phase="discovery",
    )


def build_elicitation_menu() -> str:
    """Return a formatted elicitation options block."""
    return ElicitationMenu().format()


def _build_summary_payload(
    state: Mapping[str, Any],
    answers: Mapping[str, str],
    timestamp: str,
) -> Mapping[str, Any]:
    workflow_id = state.get("workflow_id")
    workflow_type = state.get("workflow_type")
    return {
        "project_scope": _summary_entry(
            answers.get("project_concept"),
            question="2",
        ),
        "target_users": _summary_entry(
            answers.get("target_users"),
            items=_bulletize(answers.get("target_users")),
            question="3",
        ),
        "user_research_status": _summary_entry(
            answers.get("user_research_status"),
            question="4",
        ),
        "competitive_landscape": _summary_entry(
            answers.get("competitive_landscape"),
            question="5",
        ),
        "market_opportunities": _summary_entry(
            answers.get("market_opportunities"),
            question="6",
        ),
        "technical_constraints": _summary_entry(
            answers.get("technical_constraints"),
            question="7",
        ),
        "integration_requirements": _summary_entry(
            answers.get("integration_requirements"),
            items=_bulletize(answers.get("integration_requirements")),
            question="8",
        ),
        "success_criteria": _summary_entry(
            answers.get("success_criteria"),
            items=_bulletize(answers.get("success_criteria")),
            question="9",
        ),
        "business_goals": _summary_entry(
            _extract_business_goals(answers),
        ),
        "discovery_metadata": {
            "timestamp": timestamp,
            "workflow_id": workflow_id,
            "workflow_type": workflow_type,
            "questions_answered": len(answers),
            "elicitation_rounds": 0,
        },
    }


def _summary_entry(
    content: Optional[str],
    *,
    items: Optional[Sequence[str]] = None,
    question: Optional[str] = None,
) -> Mapping[str, Any]:
    return {
        "content": content,
        "items": list(items or []),
        "source_question": question,
    }


def _bulletize(value: Optional[str]) -> List[str]:
    if not value:
        return []
    items: List[str] = []
    for line in value.splitlines():
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")):
            items.append(stripped[2:].strip())
        elif stripped:
            items.append(stripped)
    return items


def _extract_business_goals(answers: Mapping[str, str]) -> Optional[str]:
    goals = [
        answers.get("market_opportunities"),
        answers.get("success_criteria"),
    ]
    filtered = [goal for goal in goals if goal]
    if not filtered:
        return None
    return "\n\n".join(filtered)


def _fallback(value: Optional[str]) -> str:
    return value if value else "Not provided"
