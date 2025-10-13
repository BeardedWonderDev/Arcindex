<!-- Powered by CODEX™ Core -->

# Execute Quality Gate Task

## Purpose

Orchestrate the execution of quality gate checklists for any phase transition in the CODEX workflow. This task ensures that deliverables meet quality standards before progression, supporting one-pass implementation success by validating completeness, clarity, and implementation-readiness.

## Overview

Quality gates are critical validation points that determine whether phase outputs are ready for the next stage. This task:

- **Loads** phase-specific quality gate checklists
- **Executes** validation based on operation mode (interactive/batch/yolo)
- **Calculates** quality scores using standardized rubric
- **Records** results in state management system
- **Blocks** or allows phase progression based on validation status

## Inputs

```yaml
inputs:
  phase:
    type: string
    required: true
    values: [discovery, analyst, pm, architect, prp]
    description: "Phase being validated"

  document:
    type: string
    required: true
    description: "Primary document to validate (e.g., prd.md, architecture.md, prp.md)"

  mode:
    type: string
    required: false
    values: [interactive, batch, yolo]
    description: "Execution mode - defaults to workflow.json operation_mode"

  checklist_path:
    type: string
    required: false
    description: "Override default checklist path"
    default: ".codex/checklists/{phase}-quality-gate.md"
```

## Execution Steps

### Step 1: Load and Parse Checklist

**Purpose:** Load the phase-specific quality gate checklist and parse its structure.

**Process:**

```pseudocode
FUNCTION load_checklist(phase, checklist_path):
    # Determine checklist path
    IF checklist_path is provided:
        path = checklist_path
    ELSE:
        path = f".codex/checklists/{phase}-quality-gate.md"

    # Verify checklist exists
    IF NOT file_exists(path):
        ERROR: "Quality gate checklist not found at {path}"
        HALT_EXECUTION

    # Read checklist content
    content = read_file(path)

    # Parse checklist structure
    checklist = parse_checklist_structure(content)

    # Extract metadata
    checklist.phase = phase
    checklist.llm_instructions = extract_llm_instructions(content)
    checklist.sections = extract_sections(content)

    RETURN checklist

FUNCTION parse_checklist_structure(content):
    structure = {
        "title": extract_title(content),
        "initialization_instructions": extract_between("[[LLM: INITIALIZATION", "]]"),
        "sections": [],
        "critical_items": [],
        "standard_items": []
    }

    # Parse sections (## headers)
    FOR each section_match IN find_all(r"^## \d+\.", content):
        section = {
            "section_id": extract_section_number(section_match),
            "section_title": extract_section_title(section_match),
            "llm_guidance": extract_llm_guidance(section_match),
            "subsections": [],
            "items": []
        }

        # Parse subsections (### headers)
        FOR each subsection IN find_subsections(section):
            subsection_data = {
                "subsection_id": extract_subsection_number(subsection),
                "subsection_title": extract_subsection_title(subsection),
                "items": []
            }

            # Parse checklist items (- [ ] or - ⚠️ [ ])
            FOR each item IN find_items(subsection):
                item_data = {
                    "text": extract_item_text(item),
                    "critical": item.startswith("⚠️"),
                    "evidence_required": extract_evidence_requirement(item),
                    "passed": null,
                    "evidence": "",
                    "notes": "",
                    "conditional": extract_conditional_marker(item)  # e.g., [[FRONTEND ONLY]]
                }

                subsection_data.items.append(item_data)

                IF item_data.critical:
                    structure.critical_items.append(item_data)
                ELSE:
                    structure.standard_items.append(item_data)

            section.subsections.append(subsection_data)

        structure.sections.append(section)

    RETURN structure
```

**Output:** Structured checklist object with parsed sections, items, and metadata.

---

### Step 2: Determine Operation Mode

**Purpose:** Determine which execution mode to use for validation.

**Process:**

```pseudocode
FUNCTION determine_mode(provided_mode):
    # Check if mode provided as parameter
    IF provided_mode is not null:
        mode = provided_mode
    ELSE:
        # Read from workflow state
        state = read_workflow_state()
        mode = state.operation_mode

    # If still not set, prompt user
    IF mode is null OR mode not in [interactive, batch, yolo]:
        DISPLAY: "Quality Gate Execution Mode Selection"
        DISPLAY: ""
        DISPLAY: "Choose how to execute the quality gate validation:"
        DISPLAY: ""
        DISPLAY: "1. Interactive - Section-by-section review with evidence collection"
        DISPLAY: "   • Review each section before proceeding to next"
        DISPLAY: "   • Collect specific evidence for each item"
        DISPLAY: "   • User confirms findings at each step"
        DISPLAY: "   • RECOMMENDED for first-time phase transitions"
        DISPLAY: ""
        DISPLAY: "2. Batch - Complete analysis with comprehensive report"
        DISPLAY: "   • Analyze entire document against all criteria"
        DISPLAY: "   • Present complete findings at end"
        DISPLAY: "   • User reviews final report"
        DISPLAY: "   • RECOMMENDED for experienced users"
        DISPLAY: ""
        DISPLAY: "3. YOLO - Skip validation (not recommended)"
        DISPLAY: "   • Bypass all quality checks"
        DISPLAY: "   • Logs violation to workflow.json"
        DISPLAY: "   • Automatically marks as APPROVED"
        DISPLAY: "   • ⚠️ USE ONLY when deadline-driven or prototyping"
        DISPLAY: ""

        mode = prompt_user("Select mode (1-3): ")

        # Convert numeric input
        IF mode == "1": mode = "interactive"
        ELSE IF mode == "2": mode = "batch"
        ELSE IF mode == "3": mode = "yolo"

        # Update workflow state with mode
        update_workflow_state({"operation_mode": mode})

    RETURN mode
```

**Output:** Validated operation mode (interactive|batch|yolo).

---

### Step 3: Execute Validation by Mode

**Purpose:** Execute validation according to selected mode.

#### Mode 3a: Interactive Mode

```pseudocode
FUNCTION execute_interactive_mode(checklist, document):
    results = initialize_results_structure()

    DISPLAY: "=== INTERACTIVE QUALITY GATE VALIDATION ==="
    DISPLAY: f"Phase: {checklist.phase}"
    DISPLAY: f"Document: {document}"
    DISPLAY: f"Checklist: {checklist.title}"
    DISPLAY: ""

    # Present initialization instructions
    DISPLAY: checklist.initialization_instructions
    DISPLAY: ""
    DISPLAY: "Press ENTER to begin validation..."
    WAIT_FOR_USER()

    # Iterate through sections
    FOR section IN checklist.sections:
        DISPLAY: ""
        DISPLAY: "=" * 80
        DISPLAY: f"SECTION {section.section_id}: {section.section_title}"
        DISPLAY: "=" * 80
        DISPLAY: ""

        # Display LLM guidance for section
        IF section.llm_guidance:
            DISPLAY: "LLM GUIDANCE:"
            DISPLAY: section.llm_guidance
            DISPLAY: ""

        section_results = {
            "section_id": section.section_id,
            "section_title": section.section_title,
            "items_total": 0,
            "items_passed": 0,
            "items_failed": 0,
            "items_skipped": 0,
            "evidence": []
        }

        # Iterate through subsections
        FOR subsection IN section.subsections:
            DISPLAY: f"--- {subsection.subsection_id} {subsection.subsection_title} ---"
            DISPLAY: ""

            # Iterate through items
            FOR item IN subsection.items:
                # Check for conditional skip logic
                IF should_skip_item(item):
                    item.passed = "skipped"
                    section_results.items_skipped += 1
                    CONTINUE

                section_results.items_total += 1

                # Display item
                marker = "⚠️ CRITICAL" IF item.critical ELSE "•"
                DISPLAY: f"{marker} {item.text}"

                # Display evidence requirement
                IF item.evidence_required:
                    DISPLAY: f"  Evidence Required: {item.evidence_required}"

                DISPLAY: ""

                # Collect evidence
                DISPLAY: "Evidence (cite specific document section/line):"
                evidence = prompt_user("> ")

                # Ask for pass/fail
                DISPLAY: "Status: (p)ass, (f)ail, (s)kip"
                status = prompt_user("> ")

                # Optional notes
                DISPLAY: "Additional notes (optional):"
                notes = prompt_user("> ")

                # Record results
                item.evidence = evidence
                item.notes = notes

                IF status == "p":
                    item.passed = true
                    section_results.items_passed += 1
                ELSE IF status == "f":
                    item.passed = false
                    section_results.items_failed += 1
                ELSE IF status == "s":
                    item.passed = "skipped"
                    section_results.items_skipped += 1

                section_results.evidence.append({
                    "item": item.text,
                    "passed": item.passed,
                    "critical": item.critical,
                    "evidence": evidence,
                    "notes": notes
                })

                DISPLAY: ""

        # Section summary
        DISPLAY: ""
        DISPLAY: f"--- SECTION {section.section_id} SUMMARY ---"
        DISPLAY: f"Passed: {section_results.items_passed}/{section_results.items_total}"
        DISPLAY: f"Failed: {section_results.items_failed}/{section_results.items_total}"
        DISPLAY: f"Skipped: {section_results.items_skipped}"

        pass_rate = (section_results.items_passed / section_results.items_total * 100) IF section_results.items_total > 0 ELSE 0
        DISPLAY: f"Pass Rate: {pass_rate:.1f}%"
        DISPLAY: ""

        # User confirmation before next section
        DISPLAY: "Review complete. Continue to next section? (y/n)"
        IF prompt_user("> ") != "y":
            DISPLAY: "Validation paused. Would you like to:"
            DISPLAY: "1. Resume from next section"
            DISPLAY: "2. Save progress and exit"
            DISPLAY: "3. Discard and restart"
            choice = prompt_user("> ")

            IF choice == "2":
                save_partial_results(results)
                EXIT
            ELSE IF choice == "3":
                RETURN null

        results.sections.append(section_results)

    RETURN results
```

#### Mode 3b: Batch Mode

```pseudocode
FUNCTION execute_batch_mode(checklist, document):
    results = initialize_results_structure()

    DISPLAY: "=== BATCH QUALITY GATE VALIDATION ==="
    DISPLAY: f"Phase: {checklist.phase}"
    DISPLAY: f"Document: {document}"
    DISPLAY: ""
    DISPLAY: "Analyzing document against quality criteria..."
    DISPLAY: ""

    # Read target document
    document_content = read_file(document)

    # Iterate through all sections silently
    FOR section IN checklist.sections:
        section_results = {
            "section_id": section.section_id,
            "section_title": section.section_title,
            "items_total": 0,
            "items_passed": 0,
            "items_failed": 0,
            "items_skipped": 0,
            "evidence": []
        }

        # Iterate through subsections
        FOR subsection IN section.subsections:
            # Iterate through items
            FOR item IN subsection.items:
                # Check for conditional skip logic
                IF should_skip_item(item):
                    item.passed = "skipped"
                    section_results.items_skipped += 1
                    CONTINUE

                section_results.items_total += 1

                # Automatically analyze document for evidence
                analysis = analyze_item_against_document(
                    item=item,
                    document=document_content,
                    section_context=section.llm_guidance
                )

                item.passed = analysis.passed
                item.evidence = analysis.evidence
                item.notes = analysis.notes

                IF item.passed:
                    section_results.items_passed += 1
                ELSE:
                    section_results.items_failed += 1

                section_results.evidence.append({
                    "item": item.text,
                    "passed": item.passed,
                    "critical": item.critical,
                    "evidence": item.evidence,
                    "notes": item.notes
                })

        results.sections.append(section_results)

    RETURN results

FUNCTION analyze_item_against_document(item, document, section_context):
    # Use LLM to analyze document for evidence of item satisfaction

    prompt = f"""
    Analyze the following document to determine if it satisfies this quality gate item.

    ITEM: {item.text}
    EVIDENCE REQUIRED: {item.evidence_required}
    SECTION CONTEXT: {section_context}

    DOCUMENT:
    {document}

    Provide:
    1. PASSED: true/false
    2. EVIDENCE: Specific citation from document (section title, line numbers, or quote)
    3. NOTES: Brief explanation of why item passed or failed

    Be strict but fair. If evidence is weak or implicit, mark as failed.
    """

    # Execute LLM analysis (this would use actual LLM call in implementation)
    analysis_result = llm_analyze(prompt)

    RETURN {
        "passed": analysis_result.passed,
        "evidence": analysis_result.evidence,
        "notes": analysis_result.notes
    }
```

#### Mode 3c: YOLO Mode

```pseudocode
FUNCTION execute_yolo_mode(checklist, document):
    DISPLAY: "⚠️ YOLO MODE ACTIVATED - SKIPPING VALIDATION ⚠️"
    DISPLAY: ""
    DISPLAY: "Quality gate validation has been bypassed."
    DISPLAY: "This violation will be logged to workflow.json"
    DISPLAY: ""

    # Log violation
    violation = {
        "timestamp": current_iso_timestamp(),
        "phase": checklist.phase,
        "violation_type": "quality_gate_skipped",
        "mode": "yolo",
        "checklist": f"{checklist.phase}-quality-gate.md",
        "document": document,
        "reason": "User chose YOLO mode - validation bypassed",
        "severity": "high"
    }

    log_violation_to_workflow(violation)

    # Create minimal results structure
    results = {
        "phase": checklist.phase,
        "checklist": f"{checklist.phase}-quality-gate.md",
        "timestamp": current_iso_timestamp(),
        "mode": "yolo",
        "overall_status": "APPROVED",
        "overall_score": "N/A",
        "violation_logged": true,
        "sections": [],
        "recommendations": [
            {
                "priority": "high",
                "action": "Complete quality gate validation before production deployment",
                "rationale": "YOLO mode bypasses critical quality checks"
            }
        ]
    }

    RETURN results
```

---

### Step 4: Calculate Quality Score

**Purpose:** Calculate overall quality score based on validation results.

**Process:**

```pseudocode
FUNCTION calculate_quality_score(results):
    # Skip scoring for YOLO mode
    IF results.mode == "yolo":
        RETURN results  # Already set to APPROVED with N/A score

    # Count failures by type
    critical_failures = 0
    standard_failures = 0
    total_items = 0
    items_passed = 0
    items_failed = 0
    items_skipped = 0

    FOR section IN results.sections:
        FOR evidence_item IN section.evidence:
            IF evidence_item.passed == "skipped":
                items_skipped += 1
                CONTINUE

            total_items += 1

            IF evidence_item.passed == true:
                items_passed += 1
            ELSE:
                items_failed += 1

                IF evidence_item.critical:
                    critical_failures += 1
                ELSE:
                    standard_failures += 1

    # Calculate score using rubric:
    # Score = 100 - (10 × critical_failures) - (5 × standard_failures)
    score = 100 - (10 * critical_failures) - (5 * standard_failures)

    # Clamp score to 0-100 range
    score = max(0, min(100, score))

    # Determine status based on score
    IF score >= 90:
        status = "APPROVED"
    ELSE IF score >= 70:
        status = "CONDITIONAL"
    ELSE:
        status = "REJECTED"

    # Update results
    results.overall_score = score
    results.overall_status = status
    results.total_items = total_items
    results.items_passed = items_passed
    results.items_failed = items_failed
    results.items_skipped = items_skipped
    results.critical_failures = critical_failures
    results.standard_failures = standard_failures

    RETURN results
```

**Scoring Reference:**

| Failure Type | Point Deduction | Rationale |
|--------------|----------------|-----------|
| Critical (⚠️) | -10 points | Blocks one-pass implementation success |
| Standard | -5 points | Degrades quality but not blocking |
| Skipped (N/A) | 0 points | Not applicable to project |

**Status Thresholds:**

| Score Range | Status | Meaning |
|-------------|--------|---------|
| 90-100 | APPROVED | High quality, ready to proceed |
| 70-89 | CONDITIONAL | Acceptable with minor issues, review recommendations |
| 0-69 | REJECTED | Too many gaps, must address failures |

---

### Step 5: Generate Recommendations

**Purpose:** Generate actionable recommendations based on validation failures.

**Process:**

```pseudocode
FUNCTION generate_recommendations(results):
    recommendations = []

    # Critical failures - HIGH priority
    FOR section IN results.sections:
        FOR item IN section.evidence:
            IF item.passed == false AND item.critical:
                recommendations.append({
                    "priority": "high",
                    "action": f"Address critical item: {item.item}",
                    "rationale": "Critical items block one-pass implementation success",
                    "section": section.section_title,
                    "evidence_gap": item.notes
                })

    # Standard failures by section - MEDIUM priority
    section_failure_counts = {}
    FOR section IN results.sections:
        failures = count(item WHERE item.passed == false AND NOT item.critical FOR item IN section.evidence)
        IF failures > 0:
            section_failure_counts[section.section_title] = failures

    # Prioritize sections with most failures
    FOR section_title, failure_count IN sort_by_value_desc(section_failure_counts):
        IF failure_count >= 3:  # Multiple failures in section
            recommendations.append({
                "priority": "medium",
                "action": f"Review and strengthen {section_title}",
                "rationale": f"{failure_count} items failed in this section",
                "section": section_title
            })

    # Overall status recommendations
    IF results.overall_status == "REJECTED":
        recommendations.insert(0, {
            "priority": "high",
            "action": "Conduct comprehensive document revision",
            "rationale": f"Overall score {results.overall_score} is below acceptable threshold (70)",
            "required": true
        })
    ELSE IF results.overall_status == "CONDITIONAL":
        recommendations.append({
            "priority": "medium",
            "action": "Address failed items before final implementation",
            "rationale": f"Score {results.overall_score} is acceptable but has gaps",
            "required": false
        })

    # Pattern-based recommendations
    IF results.critical_failures > 0:
        recommendations.append({
            "priority": "high",
            "action": f"Fix {results.critical_failures} critical validation failures",
            "rationale": "Critical items are non-negotiable for quality",
            "required": true
        })

    results.recommendations = recommendations
    RETURN results
```

---

### Step 6: Save Results

**Purpose:** Persist validation results to state management system.

**Process:**

```pseudocode
FUNCTION save_validation_results(results):
    # Generate timestamp-based filename
    timestamp = current_iso_timestamp().replace(":", "-")  # Filesystem-safe
    results_filename = f".codex/state/quality-gate-{results.phase}-{timestamp}.json"

    # Ensure state directory exists
    ensure_directory_exists(".codex/state")

    # Write results to JSON file
    write_json_file(results_filename, results)

    DISPLAY: f"✓ Validation results saved to: {results_filename}"

    # Update workflow.json
    update_workflow_state(results)

    RETURN results_filename

FUNCTION update_workflow_state(results):
    # Read current workflow state
    workflow_path = ".codex/state/workflow.json"

    IF NOT file_exists(workflow_path):
        # Initialize workflow state using state-manager task
        EXECUTE_TASK("state-manager.md", action="initialize")

    state = read_json_file(workflow_path)

    # Update quality_gate_results
    IF "quality_gate_results" NOT IN state:
        state.quality_gate_results = {}

    state.quality_gate_results[results.phase] = {
        "timestamp": results.timestamp,
        "status": results.overall_status,
        "score": results.overall_score,
        "checklist": results.checklist,
        "mode": results.mode,
        "summary": generate_one_line_summary(results)
    }

    # Update quality_scores
    IF "quality_scores" NOT IN state:
        state.quality_scores = {}

    IF results.overall_score != "N/A":
        state.quality_scores[results.phase] = results.overall_score

    # Update last_updated
    state.last_updated = current_iso_timestamp()

    # Write updated state
    write_json_file(workflow_path, state)

    DISPLAY: f"✓ Workflow state updated with quality gate results"

FUNCTION generate_one_line_summary(results):
    IF results.mode == "yolo":
        RETURN "Validation skipped (YOLO mode)"

    IF results.overall_status == "APPROVED":
        RETURN f"Approved with score {results.overall_score}/100 ({results.items_passed}/{results.total_items} passed)"
    ELSE IF results.overall_status == "CONDITIONAL":
        RETURN f"Conditional approval ({results.overall_score}/100) - {results.items_failed} items need review"
    ELSE:
        RETURN f"Rejected ({results.overall_score}/100) - {results.critical_failures} critical, {results.standard_failures} standard failures"
```

**Results File Schema:**

```json
{
  "phase": "pm",
  "checklist": "pm-quality-gate.md",
  "timestamp": "2025-10-07T15:30:00Z",
  "mode": "interactive",
  "overall_status": "APPROVED",
  "overall_score": 95,
  "total_items": 40,
  "items_passed": 38,
  "items_failed": 2,
  "items_skipped": 5,
  "critical_failures": 0,
  "standard_failures": 2,
  "sections": [
    {
      "section_id": "1",
      "section_title": "PROBLEM DEFINITION & CONTEXT",
      "items_total": 15,
      "items_passed": 14,
      "items_failed": 1,
      "items_skipped": 2,
      "evidence": [
        {
          "item": "Clear articulation of the problem being solved",
          "passed": true,
          "critical": true,
          "evidence": "PRD Section 1.1 'Problem Statement' clearly defines user pain point of manual data entry",
          "notes": "Well-articulated with specific examples"
        },
        {
          "item": "Quantification of problem impact (metrics, scale, frequency)",
          "passed": false,
          "critical": false,
          "evidence": "PRD mentions 'many users' but lacks specific numbers",
          "notes": "Should include estimated number of affected users or frequency of problem"
        }
      ]
    }
  ],
  "recommendations": [
    {
      "priority": "medium",
      "action": "Add quantitative metrics to problem impact section",
      "rationale": "Specific numbers help validate business value and prioritization",
      "section": "PROBLEM DEFINITION & CONTEXT"
    }
  ]
}
```

**Workflow.json Update:**

```json
{
  "quality_gate_results": {
    "pm": {
      "timestamp": "2025-10-07T15:30:00Z",
      "status": "APPROVED",
      "score": 95,
      "checklist": "pm-quality-gate.md",
      "mode": "interactive",
      "summary": "Approved with score 95/100 (38/40 passed)"
    }
  },
  "quality_scores": {
    "pm": 95
  }
}
```

---

### Step 7: Present Comprehensive Report

**Purpose:** Generate and display final validation report.

**Process:**

```pseudocode
FUNCTION present_validation_report(results):
    DISPLAY: ""
    DISPLAY: "=" * 80
    DISPLAY: "QUALITY GATE VALIDATION REPORT"
    DISPLAY: "=" * 80
    DISPLAY: ""

    # Header
    DISPLAY: f"Phase: {results.phase.upper()}"
    DISPLAY: f"Checklist: {results.checklist}"
    DISPLAY: f"Validation Mode: {results.mode.upper()}"
    DISPLAY: f"Timestamp: {results.timestamp}"
    DISPLAY: ""

    # Overall Status
    status_symbol = "✓" IF results.overall_status == "APPROVED" ELSE "⚠" IF results.overall_status == "CONDITIONAL" ELSE "✗"
    DISPLAY: f"{status_symbol} OVERALL STATUS: {results.overall_status}"

    IF results.overall_score != "N/A":
        DISPLAY: f"   Quality Score: {results.overall_score}/100"
    DISPLAY: ""

    # Statistics
    DISPLAY: "VALIDATION STATISTICS:"
    DISPLAY: f"  Total Items:       {results.total_items}"
    DISPLAY: f"  Items Passed:      {results.items_passed} ({results.items_passed/results.total_items*100:.1f}%)"
    DISPLAY: f"  Items Failed:      {results.items_failed}"
    DISPLAY: f"  Items Skipped:     {results.items_skipped}"
    DISPLAY: ""

    IF results.mode != "yolo":
        DISPLAY: f"  Critical Failures: {results.critical_failures} (-{results.critical_failures * 10} points)"
        DISPLAY: f"  Standard Failures: {results.standard_failures} (-{results.standard_failures * 5} points)"
        DISPLAY: ""

    # Section Breakdown
    DISPLAY: "SECTION BREAKDOWN:"
    DISPLAY: ""

    FOR section IN results.sections:
        pass_rate = (section.items_passed / section.items_total * 100) IF section.items_total > 0 ELSE 0
        status_icon = "✓" IF pass_rate == 100 ELSE "⚠" IF pass_rate >= 70 ELSE "✗"

        DISPLAY: f"{status_icon} Section {section.section_id}: {section.section_title}"
        DISPLAY: f"   Passed: {section.items_passed}/{section.items_total} ({pass_rate:.1f}%)"

        IF section.items_failed > 0:
            DISPLAY: f"   Failed Items:"
            FOR item IN section.evidence:
                IF item.passed == false:
                    marker = "⚠️ CRITICAL" IF item.critical ELSE "•"
                    DISPLAY: f"     {marker} {item.item}"
                    IF item.notes:
                        DISPLAY: f"       Reason: {item.notes}"
        DISPLAY: ""

    # Recommendations
    IF length(results.recommendations) > 0:
        DISPLAY: "RECOMMENDATIONS:"
        DISPLAY: ""

        # Group by priority
        high_priority = filter(r WHERE r.priority == "high" FOR r IN results.recommendations)
        medium_priority = filter(r WHERE r.priority == "medium" FOR r IN results.recommendations)
        low_priority = filter(r WHERE r.priority == "low" FOR r IN results.recommendations)

        IF length(high_priority) > 0:
            DISPLAY: "  HIGH PRIORITY:"
            FOR rec IN high_priority:
                DISPLAY: f"    • {rec.action}"
                DISPLAY: f"      Rationale: {rec.rationale}"
            DISPLAY: ""

        IF length(medium_priority) > 0:
            DISPLAY: "  MEDIUM PRIORITY:"
            FOR rec IN medium_priority:
                DISPLAY: f"    • {rec.action}"
                DISPLAY: f"      Rationale: {rec.rationale}"
            DISPLAY: ""

        IF length(low_priority) > 0:
            DISPLAY: "  LOW PRIORITY:"
            FOR rec IN low_priority:
                DISPLAY: f"    • {rec.action}"
                DISPLAY: f"      Rationale: {rec.rationale}"
            DISPLAY: ""

    # Next Steps
    DISPLAY: "NEXT STEPS:"
    DISPLAY: ""

    IF results.overall_status == "APPROVED":
        DISPLAY: "  ✓ Quality gate passed - ready to proceed to next phase"
        DISPLAY: f"  ✓ Results saved to: quality-gate-{results.phase}-*.json"
    ELSE IF results.overall_status == "CONDITIONAL":
        DISPLAY: "  ⚠ Quality gate conditionally passed"
        DISPLAY: "  ⚠ Review recommendations before proceeding"
        DISPLAY: "  • Consider addressing failed items"
        DISPLAY: "  • Re-run validation after improvements (optional)"
    ELSE:  # REJECTED
        DISPLAY: "  ✗ Quality gate FAILED - must address issues before proceeding"
        DISPLAY: "  ✗ Review critical failures (marked with ⚠️)"
        DISPLAY: "  • Revise document to address gaps"
        DISPLAY: "  • Re-run validation after revisions"

    DISPLAY: ""
    DISPLAY: "=" * 80
```

---

## Helper Functions

### Conditional Skip Logic

```pseudocode
FUNCTION should_skip_item(item):
    # Extract conditional markers from item text
    conditionals = extract_conditionals(item.text)

    IF length(conditionals) == 0:
        RETURN false  # No conditionals, don't skip

    # Check project type from workflow.json
    state = read_workflow_state()
    project_type = state.project_metadata.type  # e.g., "frontend", "backend", "fullstack"

    FOR conditional IN conditionals:
        IF conditional == "[[FRONTEND ONLY]]" AND project_type != "frontend" AND project_type != "fullstack":
            RETURN true

        IF conditional == "[[BACKEND ONLY]]" AND project_type != "backend" AND project_type != "fullstack":
            RETURN true

        IF conditional == "[[MOBILE ONLY]]" AND project_type != "mobile":
            RETURN true

        IF conditional == "[[WEB ONLY]]" AND project_type != "web":
            RETURN true

    RETURN false

FUNCTION extract_conditionals(text):
    # Find all [[...]] markers
    pattern = r"\[\[([^\]]+)\]\]"
    matches = regex_find_all(pattern, text)
    RETURN matches
```

---

## Error Handling

### Missing Checklist

```pseudocode
IF checklist file does NOT exist:
    ERROR: "Quality gate checklist not found"
    DISPLAY: f"Expected checklist at: .codex/checklists/{phase}-quality-gate.md"
    DISPLAY: ""
    DISPLAY: "Available checklists:"
    FOR file IN list_files(".codex/checklists/*-quality-gate.md"):
        DISPLAY: f"  • {file}"
    DISPLAY: ""
    HALT_EXECUTION
```

### Missing Document

```pseudocode
IF target document does NOT exist:
    ERROR: "Target document not found for validation"
    DISPLAY: f"Expected document at: {document}"
    DISPLAY: ""
    DISPLAY: "Quality gate validation requires the phase deliverable document."
    DISPLAY: "Please ensure the document exists before running validation."
    DISPLAY: ""

    # Suggest phase-specific document names
    IF phase == "analyst":
        DISPLAY: "Expected: docs/project-brief.md"
    ELSE IF phase == "pm":
        DISPLAY: "Expected: docs/prd.md"
    ELSE IF phase == "architect":
        DISPLAY: "Expected: docs/architecture.md"
    ELSE IF phase == "prp":
        DISPLAY: "Expected: docs/prp.md or prp/*.md"

    HALT_EXECUTION
```

### Invalid Mode

```pseudocode
IF mode NOT IN [interactive, batch, yolo]:
    WARN: f"Invalid operation mode: {mode}"
    DISPLAY: "Defaulting to interactive mode"
    mode = "interactive"
```

### Weak Evidence

```pseudocode
# During batch mode analysis
IF evidence_confidence < 0.7:
    item.passed = false
    item.notes = "Evidence is weak or implicit - explicit documentation required"
```

### Corrupted State

```pseudocode
TRY:
    state = read_json_file(".codex/state/workflow.json")
EXCEPT JSONDecodeError:
    ERROR: "Workflow state file is corrupted"
    DISPLAY: "Attempting to recover from backup..."

    IF file_exists(".codex/state/workflow.json.bak"):
        copy_file(".codex/state/workflow.json.bak", ".codex/state/workflow.json")
        state = read_json_file(".codex/state/workflow.json")
        DISPLAY: "✓ Recovered from backup"
    ELSE:
        DISPLAY: "No backup found - initializing new workflow state"
        EXECUTE_TASK("state-manager.md", action="initialize")
        state = read_json_file(".codex/state/workflow.json")
```

---

## Integration Points

### Called By

1. **Quality Gate Agents** (`.codex/agents/quality-gate.md`)
   - `/validate-discovery` command
   - `/validate-analyst` command
   - `/validate-pm` command
   - `/validate-architect` command
   - `/validate-prp` command

2. **Workflow Orchestrators**
   - Phase transition logic
   - Automated validation at checkpoints

3. **Validation Gate Task** (`.codex/tasks/validation-gate.md`)
   - Level 0 integration for elicitation validation
   - Phase transition enforcement

### Dependencies

1. **Quality Gate Checklists**
   - `.codex/checklists/discovery-quality-gate.md`
   - `.codex/checklists/analyst-quality-gate.md`
   - `.codex/checklists/pm-quality-gate.md`
   - `.codex/checklists/architect-quality-gate.md`
   - `.codex/checklists/prp-quality-gate.md`

2. **State Management**
   - `.codex/state/workflow.json` - Current workflow state
   - `.codex/tasks/state-manager.md` - State initialization and recovery

3. **Templates**
   - Phase-specific templates for reference validation

4. **Scoring Rubric**
   - `.codex/data/quality-scoring-rubric.md` - Detailed scoring methodology

---

## Usage Examples

### Example 1: Interactive PM Quality Gate

```bash
# Invoked by quality-gate agent
/validate-pm

# Agent executes:
execute-quality-gate(
  phase="pm",
  document="docs/prd.md",
  mode="interactive"
)

# User walks through each section interactively
# Provides evidence for each item
# Receives comprehensive report at end
# Results saved to .codex/state/quality-gate-pm-2025-10-07T15-30-00Z.json
```

### Example 2: Batch PRP Validation

```bash
# User specifies batch mode
/validate-prp --mode=batch

# Agent executes:
execute-quality-gate(
  phase="prp",
  document="docs/prp.md",
  mode="batch"
)

# LLM analyzes entire document automatically
# Presents comprehensive report at end
# User reviews and confirms
```

### Example 3: YOLO Mode for Prototyping

```bash
# User in rapid prototyping mode
/validate-architect --mode=yolo

# Agent executes:
execute-quality-gate(
  phase="architect",
  document="docs/architecture.md",
  mode="yolo"
)

# Validation skipped
# Violation logged to workflow.json
# Automatically marked APPROVED
# User warned about skipped validation
```

---

## Complete Execution Flow

```
┌─────────────────────────────────────────────────┐
│ 1. Load Checklist                               │
│    • Read {phase}-quality-gate.md               │
│    • Parse sections and items                   │
│    • Identify critical items                    │
└────────────────┬────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────┐
│ 2. Determine Mode                               │
│    • Check provided mode parameter              │
│    • Read workflow.json operation_mode          │
│    • Prompt user if not set                     │
└────────────────┬────────────────────────────────┘
                 ▼
         ┌───────┴───────┐
         ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ Interactive │  │    Batch    │  │    YOLO     │
│    Mode     │  │    Mode     │  │    Mode     │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       │                │                │
       ▼                ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ Section by  │  │  Analyze    │  │ Skip all    │
│ Section     │  │  Document   │  │ validation  │
│ • Collect   │  │  • Auto     │  │ • Log       │
│   evidence  │  │   evidence  │  │   violation │
│ • User      │  │  • Silent   │  │ • Mark      │
│   confirms  │  │   analysis  │  │   APPROVED  │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────┬───────┴────────┬───────┘
                ▼                │
┌─────────────────────────────────────────────────┐
│ 4. Calculate Quality Score                      │
│    • Count critical vs standard failures        │
│    • Apply scoring rubric                       │
│    • Determine status (APPROVED/CONDITIONAL/    │
│      REJECTED)                                  │
└────────────────┬────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────┐
│ 5. Generate Recommendations                     │
│    • Prioritize by failure type                 │
│    • Create actionable guidance                 │
│    • Include section-specific advice            │
└────────────────┬────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────┐
│ 6. Save Results                                 │
│    • quality-gate-{phase}-{timestamp}.json      │
│    • Update workflow.json                       │
│    • Backup previous state                      │
└────────────────┬────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────┐
│ 7. Present Report                               │
│    • Overall status and score                   │
│    • Section breakdown                          │
│    • Recommendations                            │
│    • Next steps                                 │
└─────────────────────────────────────────────────┘
```

---

## Quality Assurance Notes

### For LLM Execution

When executing this task as an LLM:

1. **Read Phase Context First**
   - Load the checklist initialization instructions
   - Understand phase-specific validation philosophy
   - Review what "success" means for this phase

2. **Be Evidence-Based**
   - Always cite specific document sections
   - Quote relevant text when available
   - Don't assume - verify with actual content

3. **Critical Items Are Non-Negotiable**
   - ⚠️ markers indicate blocking issues
   - A single critical failure can justify REJECTED status
   - Focus extra scrutiny on critical items

4. **Context Completeness Matters**
   - In PRP validation, verify all file paths exist
   - Check that references are specific, not generic
   - Ensure validation commands are executable

5. **User Experience**
   - In interactive mode, provide clear guidance
   - Don't overwhelm with details - stay focused
   - Confirm understanding before moving forward

6. **Scoring Accuracy**
   - Double-check failure counts
   - Verify score calculation
   - Ensure status aligns with thresholds

---

## Related Documentation

- **Quality Gate Checklists:** `.codex/checklists/*-quality-gate.md`
- **Scoring Rubric:** `.codex/data/quality-scoring-rubric.md` (if exists)
- **State Manager:** `.codex/tasks/state-manager.md`
- **Validation Gate:** `.codex/tasks/validation-gate.md`
- **Execute Checklist:** `.bmad-core/tasks/execute-checklist.md` (reference pattern)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-07 | Initial implementation based on PRP Task 7 requirements |

---

<!-- Powered by CODEX™ Core -->
