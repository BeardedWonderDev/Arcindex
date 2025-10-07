# Analyst Quality Gate Checklist

This checklist validates the project-brief.md output before transitioning to the PM phase. It ensures complete business analysis and sufficient context for Product Requirements Document (PRD) creation.

[[LLM: INITIALIZATION INSTRUCTIONS - ANALYST QUALITY GATE

Before proceeding with this checklist, ensure you have access to:

1. **docs/project-brief.md** - The Project Brief document
2. **project-brief-template.yaml** - Template structure reference
3. **.codex/state/discovery-summary.json** - Discovery phase context
4. **.codex/state/workflow.json** - Current workflow state

IMPORTANT: The project brief bridges discovery insights and PRD creation. Incomplete analysis cascades to poor requirements and failed implementation.

PROJECT TYPE:
CODEX focuses on greenfield projects. Skip any brownfield-specific validations.

VALIDATION APPROACH:

1. **Evidence-Based** - Cite specific project-brief.md sections proving each requirement
2. **Discovery-Aligned** - Verify answers connect to discovery-summary.json findings
3. **Business-Focused** - Ensure business value and stakeholder needs are clear
4. **PM-Ready** - Sufficient context for PM to create detailed PRD without gaps

EXECUTION MODE:
Ask the user which mode to use:

- **Interactive** - Review section by section, collect evidence, confirm before next section
- **Batch** - Complete full analysis, present comprehensive report at end
- **YOLO** - Skip validation (logs violation to workflow.json)

For interactive/batch modes:
- Collect specific evidence for each item (cite project-brief.md sections/lines)
- Mark items as ⚠️ CRITICAL or standard
- Calculate score: 100 - (10 × critical_fails) - (5 × standard_fails)
- Determine status: APPROVED (90-100), CONDITIONAL (70-89), REJECTED (0-69)

After validation, save results to:
- `.codex/state/quality-gate-analyst-{timestamp}.json`
- Update `workflow.json` quality_gate_results

See: `.codex/data/quality-scoring-rubric.md` for detailed scoring methodology]]

## 1. REQUIREMENTS DEPTH

[[LLM: Requirements depth ensures PM has comprehensive understanding to create detailed PRD. Validate that discovery questions were fully addressed with business context, not just technical specs.

Evidence requirement: Cite project-brief.md sections proving completeness]]

### 1.1 Discovery Question Coverage

- ⚠️ [ ] All discovery questions addressed in project brief
  - Evidence: "Cite project-brief.md sections covering problem, users, goals, constraints from discovery-summary.json"
  - Validate: No discovery findings ignored or omitted
  - Check: Cross-reference discovery-summary.json to ensure all key points incorporated

- ⚠️ [ ] Technical requirements are specific and testable
  - Evidence: "Cite technical constraints section with measurable requirements"
  - NOT OK: "System should be fast and scalable"
  - OK: "API response time <200ms for 95th percentile, support 1000 concurrent users"

- [ ] Non-functional requirements defined
  - Evidence: "Cite performance, security, reliability, or quality attributes"
  - Examples: Uptime targets, data protection standards, accessibility compliance

- [ ] Integration points identified with specificity
  - Evidence: "Cite external systems, APIs, or services with integration details"
  - Validate: Each integration has purpose and technical approach documented

- [ ] Constraints documented with rationale
  - Evidence: "Cite technical/business constraints section with reasons why constraints exist"
  - Examples: "Must use AWS (existing infrastructure)", "Budget limit $50k (startup stage)"

- [ ] Assumptions clearly stated and validated
  - Evidence: "Cite key assumptions section with validation approach"
  - Validate: Critical assumptions flagged for validation during PM/architecture phases

- [ ] Dependencies mapped with impact analysis
  - Evidence: "Cite project dependencies section identifying prerequisites and blockers"
  - Validate: Both technical and business dependencies documented

## 2. TEMPLATE COMPLETENESS

[[LLM: Template completeness ensures standardized structure for downstream phases. The analyst must fully populate project-brief-template.yaml sections including BMAD enhancements.

CRITICAL: Verify 4 BMAD-restored sections present (user research, competitive analysis, success metrics, constraints)]]

### 2.1 Core Template Sections

- ⚠️ [ ] All required project-brief sections present
  - Evidence: "Verify sections: project_overview, problem_statement, target_users, business_goals, scope_boundaries, constraints_assumptions, risk_assessment, next_steps"
  - Validate: No template sections skipped or placeholder content

- ⚠️ [ ] User research section complete (BMAD enhancement)
  - Evidence: "Cite user research section with target users, pain points, user needs, personas"
  - Source: Restored from BMAD Week 2 based on discovery findings
  - Validate: Connects to discovery user research or explains research plan

- ⚠️ [ ] Competitive analysis section complete (BMAD enhancement)
  - Evidence: "Cite competitive landscape section with existing solutions, competitive advantages, market positioning"
  - Source: Restored from BMAD based on discovery competitive analysis
  - Validate: At least 2-3 competitors analyzed with differentiation strategy

- [ ] Success metrics section complete (BMAD enhancement)
  - Evidence: "Cite business goals section with KPIs, success timeline, measurable objectives"
  - Source: Restored from BMAD success criteria
  - Validate: Metrics are SMART (Specific, Measurable, Achievable, Relevant, Time-bound)

- [ ] Constraints section complete (BMAD enhancement)
  - Evidence: "Cite constraints_assumptions section with technical, business, timeline constraints"
  - Source: Restored from BMAD comprehensive analysis
  - Validate: Constraints inform scope and architecture decisions

- [ ] Template variables properly extracted from discovery
  - Evidence: "Check project-brief.md has populated: project_name, primary_goal, target_outcome, users_affected, business_impact"
  - Validate: No {{placeholder}} variables remain unexpanded

- [ ] Context sufficient for PM phase to proceed
  - Evidence: "Overall assessment: PM can create PRD without returning to discovery"
  - Validate: Business context, user needs, success criteria all documented

## 3. QUALITY & CLARITY

[[LLM: Quality and clarity prevent ambiguity that leads to rework. Analyst must translate discovery insights into clear business requirements without technical implementation details.

Focus on WHAT and WHY, not HOW]]

### 3.1 Content Quality

- ⚠️ [ ] No ambiguous requirements or vague language
  - Evidence: "Scan for vague terms: 'user-friendly', 'fast', 'simple', 'intuitive', 'scalable' without quantification"
  - NOT OK: "Easy to use interface"
  - OK: "New users can complete first transaction within 5 minutes without training"

- [ ] No conflicting statements between sections
  - Evidence: "Check for contradictions (e.g., 'low budget' in constraints vs 'enterprise features' in scope)"
  - Validate: Scope, constraints, and goals are internally consistent

- [ ] Terminology consistent throughout document
  - Evidence: "Verify same concepts use same terms (e.g., 'user' vs 'customer' vs 'client')"
  - Validate: Glossary or defined terms used consistently

- [ ] Audience-appropriate language for PM and stakeholders
  - Evidence: "Check language is business-focused, not overly technical or abstract"
  - Validate: Stakeholders can understand business case without technical background

- [ ] Sufficient detail for PM to proceed without gaps
  - Evidence: "Verify each section has 2+ paragraphs of substantive content, not bullet lists"
  - Validate: PM can create epics/stories without assumptions or guesswork

- [ ] Evidence trail to discovery decisions documented
  - Evidence: "Check rationale sections explain 'why' for key decisions"
  - Examples: "Based on discovery interview finding X", "Competitive analysis revealed Y"

- [ ] Document structure follows template format
  - Evidence: "Verify headings match project-brief-template.yaml section names and order"
  - Validate: Consistent markdown formatting, proper hierarchy

- [ ] References to discovery findings are explicit
  - Evidence: "Check citations to discovery-summary.json findings or discovery outputs"
  - Validate: Key discovery insights incorporated, not siloed

---

## SCORING & VALIDATION SUMMARY

[[LLM: Calculate quality score and generate comprehensive report

**Scoring Calculation:**
1. Total items: 22 (excluding skipped sections)
2. Count critical failures (⚠️ items that failed): {critical_failures}
3. Count standard failures: {standard_failures}
4. Calculate: Score = 100 - (10 × critical_failures) - (5 × standard_failures)
5. Determine status:
   - APPROVED (90-100): Proceed to PM phase immediately
   - CONDITIONAL (70-89): Proceed with noted improvements
   - REJECTED (0-69): Must fix critical gaps before proceeding

**Report Structure:**

# Analyst Quality Gate Validation Report

**Phase**: Analyst
**Checklist**: analyst-quality-gate.md
**Document**: docs/project-brief.md
**Timestamp**: {iso_timestamp}
**Mode**: {interactive|batch|yolo}

## Overall Result

**Status**: {APPROVED|CONDITIONAL|REJECTED}
**Score**: {score}/100
**Total Items**: 22
**Passed**: {passed}
**Failed**: {failed} ({critical_failures} critical, {standard_failures} standard)

## Section Results

### 1. Requirements Depth (7 items)
- Passed: X/7
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### 2. Template Completeness (7 items)
- Passed: X/7
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### 3. Quality & Clarity (8 items)
- Passed: X/8
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

## Failed Items Detail

[For each failed item, provide:]
- Item text
- Evidence requirement
- Why it failed
- Impact on score (-5 or -10)
- Recommendation for fix

## Recommendations

### High Priority (Blocking or Critical)
1. [Specific action to address critical failure]
2. ...

### Medium Priority (Quality Improvements)
1. [Specific action to improve quality]
2. ...

### Low Priority (Nice to Have)
1. [Optional improvements]
2. ...

## Next Steps

**If APPROVED (90-100)**:
✅ Proceed to PM phase immediately
✅ All critical business analysis complete
✅ PM has sufficient context for PRD creation
✅ High confidence in requirements quality

**If CONDITIONAL (70-89)**:
⚠️ May proceed to PM phase
⚠️ Address high-priority recommendations during PRD creation
⚠️ Document known gaps for PM awareness
⚠️ Risk: Minor clarification requests during PM phase

**If REJECTED (0-69)**:
❌ BLOCK progression to PM phase
❌ Must address all critical failures
❌ Re-run analyst elicitation for incomplete sections
❌ Re-run quality gate after fixes
❌ Risk: High downstream rework if proceeding

## Evidence Summary

[Provide summary of evidence collection quality]
- Strong Evidence: X items (specific citations with line numbers)
- Weak Evidence: Y items (general section references)
- No Evidence: Z items (failed validation)

## BMAD Section Validation

**BMAD-Enhanced Sections Status**:
- [ ] User Research section (from discovery user_research_status)
- [ ] Competitive Analysis section (from discovery competitive_landscape)
- [ ] Success Metrics section (from discovery success_criteria)
- [ ] Constraints section (from discovery technical_constraints + business constraints)

**Impact**: These 4 sections are CRITICAL for comprehensive business analysis. Missing sections = REJECT status.

## Discovery-to-Brief Mapping

**Discovery Summary Fields → Project Brief Sections**:
- [ ] project_scope → problem_statement + scope_boundaries
- [ ] target_users → target_users section with personas
- [ ] business_goals → business_goals section with KPIs
- [ ] technical_constraints → constraints_assumptions section
- [ ] competitive_landscape → competitive_landscape section
- [ ] success_criteria → business_goals success metrics
- [ ] market_opportunities → competitive_landscape market positioning
- [ ] integration_requirements → constraints_assumptions dependencies
- [ ] user_research_status → target_users user research section

**Mapping Completeness**: {COMPLETE | PARTIAL | INCOMPLETE}

## Save Results

Save validation results to:
`.codex/state/quality-gate-analyst-{timestamp}.json`

Update workflow.json:
```json
{
  "quality_gate_results": {
    "analyst": {
      "timestamp": "{iso_timestamp}",
      "status": "{APPROVED|CONDITIONAL|REJECTED}",
      "score": {score},
      "checklist": "analyst-quality-gate.md",
      "mode": "{interactive|batch|yolo}",
      "total_items": 22,
      "passed": {passed},
      "failed": {failed},
      "critical_failures": {critical_failures},
      "standard_failures": {standard_failures},
      "bmad_sections_complete": {true|false},
      "discovery_mapping_complete": {true|false},
      "summary": "{one-line summary}"
    }
  },
  "quality_scores": {
    "analyst": {score}
  }
}
```

]]

---

**Checklist Version**: 1.0
**Total Items**: 22
**Critical Items**: 6 (marked with ⚠️)
**Last Updated**: 2025-01-15
**Maintained By**: CODEX Quality Team
**Related**: project-brief-template.yaml, discovery-summary.json, quality-scoring-rubric.md, analyst.md
