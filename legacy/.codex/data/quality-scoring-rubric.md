# Quality Scoring Rubric

## Overview

This document defines the standardized scoring methodology for all CODEX quality gate validations. Every phase transition (discovery → analyst → PM → architect → PRP → implementation) uses this consistent 0-100 scoring system to ensure high-quality document outputs and implementation success.

## Scoring Methodology

### Base Calculation

```
Quality Score = 100 - (Critical Failures × 10) - (Standard Failures × 5)
```

- **Starting Score**: 100 points
- **Critical Item Failure**: -10 points per item (marked with ⚠️)
- **Standard Item Failure**: -5 points per item
- **Minimum Score**: 0 (score cannot go below zero)
- **Maximum Score**: 100

### Example Calculations

**Example 1**: Perfect Quality
- Total Items: 90
- Critical Failures: 0
- Standard Failures: 0
- **Score**: 100 - (0 × 10) - (0 × 5) = **100 (APPROVED)**

**Example 2**: Minor Issues
- Total Items: 90
- Critical Failures: 0
- Standard Failures: 3
- **Score**: 100 - (0 × 10) - (3 × 5) = **85 (CONDITIONAL)**

**Example 3**: Critical Gap
- Total Items: 90
- Critical Failures: 2
- Standard Failures: 5
- **Score**: 100 - (2 × 10) - (5 × 5) = **55 (REJECTED)**

## Status Thresholds

### APPROVED (90-100)
**Proceed with confidence**

- Quality is excellent, ready for next phase
- All critical requirements met
- Minor or zero defects
- Strong evidence trail
- **Action**: Proceed to next phase immediately

### CONDITIONAL (70-89)
**Proceed with noted improvements**

- Quality is acceptable but has room for improvement
- All critical requirements met, some standard gaps
- Document improvements recommended but not blocking
- **Action**:
  - Proceed to next phase
  - Note improvements for future consideration
  - Track conditional items for follow-up
  - Consider addressing gaps if time permits

### REJECTED (0-69)
**Must fix before proceeding**

- Quality is insufficient for next phase
- Critical requirements missing or incomplete
- High risk of downstream rework and failures
- **Action**:
  - **BLOCK** progression to next phase
  - Provide detailed failure report
  - Specify exactly what must be fixed
  - Re-run quality gate after fixes
  - Do not proceed until score ≥ 70

## Critical vs Standard Items

### Critical Items (⚠️)

Items marked with ⚠️ are **CRITICAL** because:
- Missing them causes cascading failures in downstream phases
- They directly impact implementation success
- They represent core requirements or architectural decisions
- They ensure legal, security, or compliance requirements

**Examples of Critical Items**:
- ⚠️ Problem statement is specific and measurable
- ⚠️ Each Epic ties back to specific user needs
- ⚠️ Exact technology versions specified (not ranges)
- ⚠️ Security requirements have corresponding technical controls
- ⚠️ All referenced files exist and are accessible (PRPs)

### Standard Items

Standard items are important but not immediately blocking:
- Enhance quality and clarity
- Reduce future technical debt
- Improve maintainability
- Support best practices

**Examples of Standard Items**:
- [ ] Documentation is inline and up-to-date
- [ ] Consistent code formatting
- [ ] Comprehensive comments
- [ ] Nice-to-have optimizations

## Evidence Requirements

### Evidence-Based Validation

Every validation item requires **specific evidence** from the document being validated. Vague assessments like "looks good" are not acceptable.

**Good Evidence Examples**:
```
✅ "PRD section 2.3 states: 'Users must be able to register with email verification' - requirement is specific and testable"

✅ "architecture.md line 45 specifies: React 18.2.0 (exact version, not range)"

✅ "Epic 3 in prd.md directly addresses user pain point documented in section 1.2"
```

**Bad Evidence Examples**:
```
❌ "Requirements look complete"
❌ "Architecture seems good"
❌ "I think this is fine"
```

### Evidence Collection Format

For each validation item, collect:

```json
{
  "item": "Specific checklist item text",
  "passed": true/false,
  "evidence": "Cite specific document section, line number, or quote proving requirement",
  "notes": "Additional context or concerns (optional)"
}
```

## Execution Modes

### Interactive Mode
- Present validation section by section
- Collect evidence for each item in real-time
- Get user confirmation before proceeding to next section
- Ideal for: First-time validations, learning the system, complex documents

### Batch Mode
- Process all sections silently
- Collect all evidence
- Present comprehensive report at end
- User reviews full results and confirms
- Ideal for: Experienced users, simple validations, time-constrained scenarios

### YOLO Mode
- **Skip validation entirely**
- Log violation to workflow.json
- Mark as APPROVED to allow progression
- **WARNING**: Violations are tracked for audit
- Ideal for: Experimental work, rapid prototyping, trusted workflows
- **Risk**: No quality assurance, higher downstream failure risk

### Mode Selection

Mode is determined by `workflow.json`:
```json
{
  "operation_mode": "interactive",  // or "batch" or "yolo"
  ...
}
```

## Skip Logic for Conditional Sections

Some checklist sections are conditional based on project type:

### Project Type Conditionals

**[[FRONTEND ONLY]]** - Skip for backend-only projects
```
Example: "Does UI component architecture follow atomic design principles?"
```

**[[BACKEND ONLY]]** - Skip for frontend-only projects
```
Example: "Is database connection pooling properly configured?"
```

**[[GREENFIELD ONLY]]** - Skip for brownfield/enhancement projects
```
Example: "Is project scaffolding complete?"
```

**[[BROWNFIELD ONLY]]** - Skip for greenfield projects
```
Example: "Is existing codebase analysis documented?"
```

### Skip Logic Implementation

When encountering conditional sections:
1. Detect project type from `workflow.json` or document metadata
2. If condition doesn't apply, mark section as SKIPPED
3. Do NOT count skipped items in score calculation
4. Log skipped sections in validation report

**Example**:
```
Project Type: Backend-only API
Checklist: architect-quality-gate.md
Section: "Frontend Architecture (45 items)" [[FRONTEND ONLY]]
Action: SKIP entire section (45 items excluded from scoring)
```

## Quality Score Impact Analysis

### Business Impact

Quality scores directly correlate with implementation success:

| Score Range | One-Pass Success Rate | Downstream Rework Hours |
|------------|----------------------|-------------------------|
| 90-100     | 85%                  | 2-4 hours               |
| 70-89      | 65%                  | 6-10 hours              |
| 50-69      | 35%                  | 12-20 hours             |
| 0-49       | 10%                  | 25+ hours               |

### ROI of Quality Gates

**Without Quality Gates**:
- Average clarification requests: 5-8 per project (5-8 hours)
- Average implementation rework: 8-12 hours per project
- One-pass success rate: ~50%

**With Quality Gates (90+ scores)**:
- Average clarification requests: 1-2 per project (1-2 hours)
- Average implementation rework: 2-4 hours per project
- One-pass success rate: ~85%

**Net Improvement**: 60% reduction in downstream rework (8-12 hours → 2-4 hours)

## Violation Logging (YOLO Mode)

When quality gates are skipped in YOLO mode, violations must be logged:

```json
{
  "violation_log": [
    {
      "timestamp": "2024-01-15T14:30:00Z",
      "phase": "pm",
      "violation_type": "quality_gate_skipped",
      "mode": "yolo",
      "reason": "User chose YOLO mode",
      "risk": "No validation of PRD quality, increased downstream failure risk"
    }
  ]
}
```

Violations are tracked for:
- Audit trail
- Quality metrics
- Risk assessment
- Process improvement analysis

## Reporting Format

### Validation Report Structure

```markdown
# Quality Gate Validation Report

**Phase**: PM
**Checklist**: pm-quality-gate.md
**Mode**: Interactive
**Timestamp**: 2024-01-15T14:30:00Z

## Overall Result

**Status**: CONDITIONAL
**Score**: 85/100
**Total Items**: 90
**Passed**: 85
**Failed**: 5 (0 critical, 5 standard)

## Section Results

### 1. Problem Definition & Context (15 items)
- Passed: 15/15
- Failed: 0
- Status: ✅ COMPLETE

### 2. MVP Scope Definition (20 items)
- Passed: 17/20
- Failed: 3 (0 critical, 3 standard)
- Status: ⚠️ NEEDS IMPROVEMENT

**Failed Items**:
1. [ ] Scope boundaries: Future enhancements section missing
   - Evidence: PRD section 3 does not include "Future Enhancements" subsection
   - Impact: -5 points
   - Recommendation: Add section 3.4 documenting out-of-scope items

...

## Recommendations

### High Priority
1. Add Future Enhancements section to PRD (section 3.4)
2. Clarify acceptance criteria for Epic 2, Story 3

### Medium Priority
1. Improve story sizing documentation
2. Add rationale for exclusion decisions

## Next Steps

**Action**: CONDITIONAL - Proceed to next phase with noted improvements
**Suggested**: Address high-priority recommendations before architect phase
**Required**: None (score above 70 threshold)
```

## Best Practices

### For Validators (Quality-Gate Agent)

1. **Be Thorough**: Check every item systematically
2. **Be Evidence-Based**: Always cite specific document sections
3. **Be Critical**: Don't just check boxes, analyze deeply
4. **Be Fair**: Apply same standards consistently
5. **Be Clear**: Provide actionable feedback for failures

### For Document Authors

1. **Anticipate Validation**: Write with quality gate in mind
2. **Be Specific**: Vague statements will fail validation
3. **Be Complete**: Missing sections will fail validation
4. **Be Structured**: Follow templates to ensure coverage
5. **Be Evidence-Oriented**: Include concrete examples and details

### For Workflow Orchestrators

1. **Enforce Gates**: Don't bypass without good reason
2. **Track Scores**: Monitor quality trends over time
3. **Learn from Failures**: Use rejections to improve process
4. **Celebrate Success**: Recognize high-quality work
5. **Iterate**: Refine checklists based on experience

## Continuous Improvement

### Checklist Evolution

Quality gate checklists should evolve based on:
- Common failure patterns
- New best practices
- Technology changes
- Team feedback
- Success/failure metrics

### Scoring Calibration

Periodically review if:
- Too many APPROVED scores (gates too lenient)
- Too many REJECTED scores (gates too strict)
- Scores don't correlate with implementation success
- Critical vs standard item balance is off

### Metrics to Track

1. **Average quality scores by phase**
2. **Correlation between scores and implementation success**
3. **Time spent on quality validation**
4. **Rework hours before/after quality gates**
5. **Most common failure points**

---

## Appendix: Scoring Edge Cases

### All Items Passed
- Score: 100
- Status: APPROVED
- Action: Proceed immediately

### Mix of Critical and Standard Failures
- Calculate separately: Critical failures hurt more
- Example: 1 critical + 2 standard = 100 - 10 - 10 = 80 (CONDITIONAL)

### High Item Count with Few Failures
- Large checklists (169 items) can absorb more failures
- Example: 169 items, 3 standard failures = 100 - 15 = 85 (CONDITIONAL)
- Philosophy: Absolute failure count matters more than percentage

### Borderline Scores (69, 70, 89, 90)
- Scores exactly at thresholds use inclusive upper bound
- 70 = CONDITIONAL (not REJECTED)
- 90 = APPROVED (not CONDITIONAL)

### Zero Items Applicable (All Skipped)
- If all items are skipped due to project type: Score = N/A
- Cannot calculate quality for non-applicable checklists
- Example: Backend project with frontend checklist
- Action: SKIP checklist entirely, do not force score

---

**Document Version**: 1.0
**Last Updated**: 2024-01-15
**Maintained By**: CODEX Quality Team
**Related Documents**:
- quality-gate.md (agent definition)
- execute-quality-gate.md (task implementation)
- All *-quality-gate.md checklists
