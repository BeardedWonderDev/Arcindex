# Discovery Quality Gate Checklist

This checklist validates the Discovery phase output before transitioning to the Analyst phase. It ensures complete project scope understanding and sufficient context for requirements analysis.

[[LLM: INITIALIZATION INSTRUCTIONS - DISCOVERY QUALITY GATE

Before proceeding with this checklist, ensure you have access to:

1. **.codex/state/workflow.json** - Workflow state with discovery completion
2. **.codex/state/discovery-summary.json** - Discovery phase outputs
3. **discovery.md** agent output or conversation history
4. **Initial project concept** from user

IMPORTANT: Discovery is the foundation of the entire workflow. Incomplete discovery cascades failures to all downstream phases.

VALIDATION APPROACH:

1. **Completeness** - All 9 discovery questions answered with substance
2. **Clarity** - Answers are specific, not vague or ambiguous
3. **Actionability** - Analyst can proceed with sufficient context
4. **Evidence-Based** - Cite discovery-summary.json or discovery outputs

EXECUTION MODE:
Ask the user which mode to use:

- **Interactive** - Review section by section, collect evidence, confirm before next section
- **Batch** - Complete full analysis, present comprehensive report at end
- **YOLO** - Skip validation (logs violation to workflow.json)

For interactive/batch modes:
- Verify all 9 questions were answered
- Check discovery-summary.json exists and is complete
- Ensure template variables are extractable
- Calculate score: 100 - (10 × critical_fails) - (5 × standard_fails)
- Determine status: APPROVED (90-100), CONDITIONAL (70-89), REJECTED (0-69)

See: `.codex/data/quality-scoring-rubric.md` for detailed scoring methodology]]

## 1. PROJECT SCOPE CLARITY

[[LLM: Project scope must be specific enough for analyst to create detailed requirements. As you validate:

1. Problem statement should be concrete, not abstract
2. Target users should be specific personas, not "everyone"
3. Success criteria should be measurable, not "improve user experience"
4. Project boundaries should be explicit
5. MVP scope should be realistic for timeline

Evidence: Cite discovery-summary.json fields or discovery conversation]]

### 1.1 Problem & Solution Clarity

- ⚠️ [ ] Problem statement is specific and measurable
  - Evidence: "Cite discovery-summary.json 'project_scope' or problem description"
  - NOT OK: "Improve user productivity"
  - OK: "Reduce time to generate financial reports from 4 hours to 30 minutes"

- ⚠️ [ ] Target users are clearly identified with personas
  - Evidence: "Cite discovery-summary.json 'target_users' with specific roles/demographics"
  - NOT OK: "Business users"
  - OK: "Financial analysts at mid-size companies (50-500 employees) generating monthly P&L reports"

- ⚠️ [ ] Success criteria defined with concrete metrics
  - Evidence: "Cite discovery-summary.json 'success_criteria' with measurable outcomes"
  - NOT OK: "Users are satisfied"
  - OK: "80% user adoption within 3 months, NPS score >40, reduce report generation time by 87%"

- [ ] Project boundaries established (what's in/out of scope)
  - Evidence: "Cite what features are explicitly out of MVP scope"
  - OK: "MVP excludes multi-currency support, real-time collaboration, mobile apps"

- [ ] MVP scope realistic for timeline
  - Evidence: "Cite timeline expectations from discovery (e.g., 8-12 weeks for MVP)"
  - Validate: Features align with timeline constraints

### 1.2 Business Value & Goals

- ⚠️ [ ] Business goals documented with quantifiable targets
  - Evidence: "Cite discovery-summary.json 'business_goals' with metrics"
  - NOT OK: "Increase revenue"
  - OK: "Reduce customer churn from 15% to 10%, increase ARPU by $50/month"

- [ ] Value proposition is clear and compelling
  - Evidence: "Cite why this solution is valuable to target users"
  - Validate: Solution addresses real pain point with meaningful impact

- [ ] Market/competitive landscape assessed
  - Evidence: "Cite discovery-summary.json 'competitive_landscape' or competitor analysis"
  - Validate: Differentiation from existing solutions is clear

- [ ] User research conducted or planned
  - Evidence: "Cite discovery-summary.json 'user_research_status'"
  - OK: "5 user interviews completed", "20-person survey planned for validation"

- [ ] Stakeholder expectations aligned
  - Evidence: "Cite key stakeholders and their requirements/constraints"
  - Validate: No conflicting expectations from different stakeholders

## 2. CONTEXT COMPLETENESS

[[LLM: Context from discovery feeds directly into project-brief creation. Missing context = incomplete requirements. Validate that analyst has everything needed]]

### 2.1 Technical Context

- ⚠️ [ ] Technical constraints identified
  - Evidence: "Cite discovery-summary.json 'technical_constraints'"
  - Examples: Must use Python 3.11+, AWS-only infrastructure, integrate with Salesforce API

- [ ] Must-have technology requirements specified
  - Evidence: "Cite required platforms, languages, frameworks"
  - Examples: iOS/Android apps required, React frontend mandated, PostgreSQL database

- [ ] Integration requirements identified
  - Evidence: "Cite discovery-summary.json 'integration_requirements'"
  - Examples: Stripe payments, Auth0 SSO, Snowflake data warehouse

- [ ] Infrastructure constraints documented
  - Evidence: "Cite hosting restrictions, compliance requirements, security mandates"
  - Examples: Must deploy to GCP, HIPAA compliance required, SOC2 certification needed

- [ ] Existing systems/APIs to integrate with mapped
  - Evidence: "Cite external systems from integration_requirements"
  - Validate: Clear understanding of what systems must be integrated

### 2.2 User & Market Context

- [ ] User needs and pain points documented
  - Evidence: "Cite specific user pain points from discovery"
  - Validate: Pain points are specific, not generic

- [ ] Competitive analysis conducted
  - Evidence: "Cite discovery-summary.json 'competitive_landscape'"
  - Validate: 2+ competitors analyzed, gaps identified

- [ ] Market opportunities identified
  - Evidence: "Cite discovery-summary.json 'market_opportunities'"
  - Examples: "Growing remote work trend", "New regulation creating demand"

- [ ] User research findings captured
  - Evidence: "Cite user research data, interview insights, survey results"
  - Validate: Findings inform feature priorities

- [ ] Accessibility/compliance requirements identified
  - Evidence: "Cite WCAG, GDPR, HIPAA, or other standards required"
  - Validate: Requirements will impact design and architecture

## 3. WORKFLOW READINESS

[[LLM: Discovery must provide sufficient context for analyst to proceed. This section validates that the handoff is complete]]

### 3.1 Discovery Completeness

- ⚠️ [ ] All 9 discovery questions answered
  - Evidence: "Verify discovery.md or conversation covered all 9 questions"
  - Questions (from discovery enhancement):
    1. Project scope, goals, constraints (existing 3)
    2. Who are competitors and their strengths/weaknesses?
    3. What market trends is this addressing?
    4. Who are target users and their pain points?
    5. What user research conducted or planned?
    6. What are must-have technical constraints?
    7. What existing systems to integrate with?
    8. Additional questions based on project type

- ⚠️ [ ] Discovery summary persisted to state
  - Evidence: "Verify .codex/state/discovery-summary.json exists and is populated"
  - Validate: File contains all required fields (see data model in PRP Task 12)

- [ ] Each question answered with sufficient depth
  - Evidence: "Check answers are 2-3 paragraphs, not one-sentence responses"
  - Validate: Answers provide actionable context, not platitudes

- [ ] No blocking unknowns remain
  - Evidence: "Identify any 'TBD', 'Unknown', or 'Need to research' responses"
  - Action: If blocking unknowns exist, REJECT and request clarification

### 3.2 Template Variable Extraction

- [ ] Template variables extractable from discovery
  - Evidence: "Verify key variables present: project_name, target_platform, primary_language"
  - Validate: Variables can populate project-brief-template without manual editing

- [ ] Project name clearly defined
  - Evidence: "Cite discovery-summary.json 'project_scope' or project_name"
  - Validate: Name is specific, not generic placeholder

- [ ] Target platform(s) specified
  - Evidence: "Cite platforms: Web, iOS, Android, Desktop, CLI, etc."
  - Validate: Platform choice informs architecture decisions

- [ ] Primary technology stack direction identified
  - Evidence: "Cite language/framework preferences from technical_constraints"
  - Examples: "Python/FastAPI backend", "React/TypeScript frontend"

- [ ] Key terminology and domain concepts defined
  - Evidence: "Cite domain-specific terms that will appear throughout project"
  - Validate: Terminology is consistent and understood

### 3.3 Analyst Transition Readiness

- ⚠️ [ ] Analyst can proceed with sufficient context
  - Evidence: "Overall assessment: Is there enough to create project-brief.md?"
  - Validate: No major gaps requiring another discovery round

- [ ] Project type is clear (greenfield vs brownfield)
  - Evidence: "Verify workflow_type in workflow.json"
  - For CODEX v0.1: Should be greenfield (brownfield deferred)

- [ ] Workflow.json discovery_completed = true
  - Evidence: "Check workflow.json project_discovery.discovery_completed"
  - Action: Must be true to proceed

- [ ] Context handoff documentation exists
  - Evidence: "Verify discovery outputs are accessible to analyst"
  - Validate: discovery-summary.json, workflow.json updated, any notes captured

- [ ] No contradictory information in discovery
  - Evidence: "Check for conflicts (e.g., 'low budget' vs 'enterprise features')"
  - Action: If contradictions exist, REJECT and request clarification

---

## SCORING & VALIDATION SUMMARY

[[LLM: Calculate quality score and generate comprehensive report

**Scoring Calculation:**
1. Total items: 20 (excluding skipped sections)
2. Count critical failures (⚠️ items that failed): {critical_failures}
3. Count standard failures: {standard_failures}
4. Calculate: Score = 100 - (10 × critical_failures) - (5 × standard_failures)
5. Determine status:
   - APPROVED (90-100): Proceed to analyst phase immediately
   - CONDITIONAL (70-89): Proceed with noted improvements
   - REJECTED (0-69): Must fix critical gaps before proceeding

**Report Structure:**

# Discovery Quality Gate Validation Report

**Phase**: Discovery
**Checklist**: discovery-quality-gate.md
**Timestamp**: {iso_timestamp}
**Mode**: {interactive|batch|yolo}

## Overall Result

**Status**: {APPROVED|CONDITIONAL|REJECTED}
**Score**: {score}/100
**Total Items**: 20
**Passed**: {passed}
**Failed**: {failed} ({critical_failures} critical, {standard_failures} standard)

## Section Results

### 1. Project Scope Clarity (10 items)
- Passed: X/10
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### 2. Context Completeness (10 items)
- Passed: X/10
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### 3. Workflow Readiness (10 items)
- Passed: X/10
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

## Failed Items Detail

[For each failed item:]
- Item text
- Why it failed
- Impact on score
- Specific recommendation

## Recommendations

### High Priority (Blocking)
1. [Specific actions to address critical failures]

### Medium Priority
1. [Actions to improve quality]

### Low Priority
1. [Optional improvements]

## Next Steps

**If APPROVED (90-100)**:
✅ Proceed to analyst phase
✅ Discovery summary complete and accessible
✅ Template variables extractable
✅ High confidence in requirements gathering

**If CONDITIONAL (70-89)**:
⚠️ May proceed with caution
⚠️ Document known gaps for analyst
⚠️ Consider additional discovery if time permits

**If REJECTED (0-69)**:
❌ BLOCK progression to analyst
❌ Address critical gaps in discovery
❌ Re-run discovery questions for missing areas
❌ Re-run quality gate after fixes

## Discovery Summary Validation

**discovery-summary.json Status**: {EXISTS | MISSING}

**Required Fields**:
- [ ] project_scope
- [ ] target_users
- [ ] business_goals
- [ ] technical_constraints
- [ ] competitive_landscape
- [ ] success_criteria
- [ ] market_opportunities
- [ ] integration_requirements
- [ ] user_research_status

**Template Variables Extractable**:
- [ ] project_name
- [ ] target_platform
- [ ] primary_language
- [ ] required_integrations

## Save Results

Save validation results to:
`.codex/state/quality-gate-discovery-{timestamp}.json`

Update workflow.json:
```json
{
  "quality_gate_results": {
    "discovery": {
      "timestamp": "{iso_timestamp}",
      "status": "{APPROVED|CONDITIONAL|REJECTED}",
      "score": {score},
      "checklist": "discovery-quality-gate.md",
      "mode": "{mode}",
      "summary": "{one-line summary}"
    }
  },
  "quality_scores": {
    "discovery": {score}
  }
}
```

]]

---

**Checklist Version**: 1.0
**Total Items**: 20
**Critical Items**: 7 (marked with ⚠️)
**Last Updated**: 2024-01-15
**Maintained By**: CODEX Quality Team
**Related**: discovery.md agent, discovery-summary.json, quality-scoring-rubric.md
