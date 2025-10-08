# Phase 2 Level 3 Operational Testing Guide

**Purpose:** Validate Phase 2 feedback mechanisms and quality enhancement features through real-world project execution

**Target:** Next 1-2 projects using CODEX workflow

**Validation Level:** End-to-End Workflow Validation

---

## Overview

Level 3 validation tests the operational effectiveness of Phase 2 features in a complete project workflow from Discovery through Implementation. This guide provides specific scenarios to test and data to capture.

---

## Pre-Project Setup

### 1. Enable Phase 2 Feature Tracking

Create tracking log for the project:

```bash
# Create project-specific tracking directory
mkdir -p .codex/state/phase2-validation/
PROJECT_NAME="your-project-name"
TRACKING_FILE=".codex/state/phase2-validation/${PROJECT_NAME}-level3-tracking.md"

cat > "$TRACKING_FILE" <<EOF
# Phase 2 Level 3 Validation - ${PROJECT_NAME}

**Project:** ${PROJECT_NAME}
**Start Date:** $(date +"%Y-%m-%d")
**Validation Goal:** Test Phase 2 operational effectiveness

---

## Feedback Loop Tracking

### Feedback Requests Log

| ID | From → To | Issue | Created | Resolved | Duration | Iterations |
|----|-----------|-------|---------|----------|----------|------------|

### Feedback Loop Analysis
- Total requests: 0
- Avg resolution time:
- Max iterations:
- Escalations to user:

---

## PRP Validation Tracking

### PRP Quality Scores

| Epic | Story | PRP File | Pre-flight Score | Pass/Fail | Issues Found |
|------|-------|----------|------------------|-----------|--------------|

### Validation Failures
- Total PRPs created:
- Failed validation:
- Common issues:

---

## Failure Escalation Tracking

### Escalation Events

| Story | Validation Level | Failure Count | Escalation Level | Outcome |
|-------|------------------|---------------|------------------|---------|

### Escalation Statistics
- Level 1 (Auto-retry):
- Level 2 (Pattern analysis):
- Level 3 (User intervention):
- Level 4 (Checkpoint):

---

## Epic Learning Tracking

### Epic 1 Execution

| Story | PRP Quality | Actual Hours | Est Hours | Patterns Found | Issues Found |
|-------|-------------|--------------|-----------|----------------|--------------|

### Epic 2 Improvements (if applicable)

**Quality Score Comparison:**
- Epic 1 avg PRP quality:
- Epic 2 avg PRP quality:
- Improvement:

**Time Estimate Accuracy:**
- Epic 1 variance:
- Epic 2 variance:
- Improvement:

---

## Zero-Knowledge & Confidence Tracking

### Architecture Validation

| Epic | Zero-Knowledge Score | Gaps Found | Confidence Score | Weak Areas |
|------|----------------------|------------|------------------|------------|

EOF

echo "✅ Created tracking file: $TRACKING_FILE"
```

### 2. Verify Phase 2 Components Active

```bash
# Check all Phase 2 task files exist
echo "Checking Phase 2 task files..."
for task in request-feedback prp-validation-enforcement failure-escalation \
            capture-execution-learnings epic-learning-integration \
            zero-knowledge-test confidence-scoring; do
    if [ -f ".codex/tasks/${task}.md" ]; then
        echo "✓ ${task}.md"
    else
        echo "✗ MISSING: ${task}.md"
    fi
done

# Check workflow.json has Phase 2 fields
echo ""
echo "Checking workflow.json Phase 2 fields..."
if grep -q "feedback_requests" .codex/state/workflow.json.template; then
    echo "✓ feedback_requests field"
else
    echo "✗ MISSING: feedback_requests field"
fi

if grep -q "execution_reports" .codex/state/workflow.json.template; then
    echo "✓ execution_reports field"
else
    echo "✗ MISSING: execution_reports field"
fi

if grep -q "epic_learnings" .codex/state/workflow.json.template; then
    echo "✓ epic_learnings field"
else
    echo "✗ MISSING: epic_learnings field"
fi
```

---

## Testing Scenarios by Phase

### Phase 1-3: Discovery → Analysis → PM (PRD Creation)

**Goal:** Create foundation for testing feedback loops

**Actions:**
1. Execute normal workflow through PM phase
2. Create PRD with at least 2 epics
3. Ensure PRD has some intentional ambiguities for testing

**Intentional Ambiguities to Plant (for testing feedback):**
- Use vague terms like "real-time" without specifics
- Reference "payment processing" without specifying provider
- Mention "user authentication" without method details
- Use "scalable" without quantifying requirements

**Tracking:**
```markdown
### Phase 1-3 Completion
- [x] Discovery complete
- [x] Analysis complete
- [x] PRD created with 2+ epics
- [x] Planted ambiguities for feedback testing:
  - [ ] Vague latency requirement
  - [ ] Unspecified integration
  - [ ] Generic scalability claim
```

---

### Phase 4: Architecture Design (Epic 1) - FEEDBACK LOOP TEST

**Scenario 1: Architect Requests Feedback from PM**

**Test Steps:**

1. **During architecture creation, architect encounters ambiguity:**
   ```markdown
   Story 1.3 says "real-time updates" but doesn't specify latency requirement
   ```

2. **Architect invokes feedback request:**
   ```bash
   # Architect uses: *request-feedback pm "Story 1.3..."
   # System should execute request-feedback.md task
   ```

3. **Verify Feedback Creation:**
   ```bash
   # Check workflow.json for new feedback request
   jq '.feedback_requests | last' .codex/state/workflow.json

   # Should show:
   # - id: fb-{timestamp}
   # - from_agent: architect
   # - to_agent: pm
   # - status: pending
   # - issue: "Story 1.3 acceptance criteria unclear..."
   ```

4. **Verify Feedback Context Package:**
   ```bash
   # Check for context file
   ls -la .codex/state/feedback/fb-*.md
   ```

5. **PM Resolves Feedback:**
   ```bash
   # PM uses: *update docs/prd.md
   # PM uses: *resolve-feedback {fb-id} "Clarified: real-time = <100ms..."
   ```

6. **Verify Resolution:**
   ```bash
   # Check workflow.json for resolution
   jq '.feedback_requests | last | select(.status == "resolved")' .codex/state/workflow.json

   # Should show:
   # - status: resolved
   # - resolved_at: {timestamp}
   # - resolution: "Clarified: real-time = <100ms..."
   ```

**Track Results:**
```markdown
| fb-001 | Architect → PM | Story 1.3 latency unclear | 2025-10-08 10:30 | 2025-10-08 10:45 | 15 min | 1 |
```

**Test Coverage:**
- [ ] Feedback request created successfully
- [ ] workflow.json updated with feedback object
- [ ] Context package created
- [ ] PM received notification (manual check)
- [ ] PM updated document
- [ ] Feedback marked resolved
- [ ] Resolution time < 30 minutes
- [ ] Only 1 iteration needed

---

**Scenario 2: Run Zero-Knowledge Test on Architecture**

**Test Steps:**

1. **After architecture draft complete, run zero-knowledge test:**
   ```bash
   # Execute zero-knowledge test
   ARCHITECTURE_FILE="docs/architecture-epic-1.md"
   OUTPUT_FILE=".codex/state/zero-knowledge-test-results.md"

   bash .codex/tasks/zero-knowledge-test.md
   ```

2. **Verify Gap Report Generated:**
   ```bash
   cat .codex/state/zero-knowledge-test-results.md
   ```

3. **Check Completeness Score:**
   ```bash
   # Extract completeness percentage
   grep "Overall Completeness:" .codex/state/zero-knowledge-test-results.md

   # Target: ≥95%
   ```

4. **Remediate Gaps if Found:**
   - Review gap report
   - Add missing information to architecture
   - Re-run zero-knowledge test
   - Verify completeness improved

**Track Results:**
```markdown
| Epic 1 | 92% (1st run) → 98% (2nd run) | 5 gaps (missing API specs) | - | - |
```

**Test Coverage:**
- [ ] Zero-knowledge test executed
- [ ] Gap report generated
- [ ] Gaps identified (missing info, vague language, assumptions)
- [ ] Gaps remediated
- [ ] Completeness ≥95% achieved
- [ ] Results logged

---

**Scenario 3: Run Confidence Scoring**

**Test Steps:**

1. **Architect runs confidence scoring:**
   ```bash
   bash .codex/tasks/confidence-scoring.md
   ```

2. **Provide dimension scores (0-10 each):**
   - Technology Selection: 8
   - Scalability Approach: 7
   - Security Design: 9
   - API Design: 8
   - Data Model: 7
   - Deployment Strategy: 6
   - Testing Approach: 8
   - Error Handling: 7
   - Performance Optimization: 7
   - Integration Points: 8

3. **Verify Confidence Report:**
   ```bash
   cat .codex/state/confidence-scoring-results.md
   ```

4. **Check Overall Score:**
   ```bash
   # Extract overall confidence
   grep "Overall Confidence:" .codex/state/confidence-scoring-results.md

   # Target: ≥85/100
   ```

5. **Address Weak Areas (< 7/10):**
   - Review weak area recommendations
   - Enhance architecture for weak dimensions
   - Re-run confidence scoring
   - Verify improvement

**Track Results:**
```markdown
| Epic 1 | - | - | 75/100 (1st) → 88/100 (2nd) | Deployment Strategy (6→8) |
```

**Test Coverage:**
- [ ] Confidence scoring executed
- [ ] All 10 dimensions scored
- [ ] Overall score calculated
- [ ] Weak areas identified
- [ ] Weak areas addressed
- [ ] Final score ≥85/100
- [ ] Results logged

---

### Phase 5: PRP Creation (Epic 1) - VALIDATION ENFORCEMENT TEST

**Scenario 4: PRP Validation Enforcement**

**Test Steps:**

1. **PRP Creator creates PRP for Epic 1 Story 1:**
   ```bash
   # PRP creation workflow
   ```

2. **Before marking PRP complete, run validation enforcement:**
   ```bash
   PRP_FILE="PRPs/epic-1-story-1.md"
   bash .codex/tasks/prp-validation-enforcement.md
   ```

3. **Verify Validation Checks:**
   ```bash
   # Check validation log
   ls -la .codex/state/validation-logs/prp-validation-*.log
   ```

4. **Intentionally Create Low-Quality PRP (for testing):**
   - Omit validation commands
   - Include broken file references
   - Include broken URLs
   - Skip verification log section

5. **Verify Validation FAILS:**
   ```bash
   # Should fail with score < 90
   # Should list specific issues:
   # - Missing validation commands
   # - Broken file refs
   # - Broken URLs
   # - No verification log
   ```

6. **Fix Issues and Re-validate:**
   - Add validation commands
   - Fix file references
   - Fix URLs
   - Add verification log

7. **Verify Validation PASSES:**
   ```bash
   # Should pass with score ≥ 90
   # Should create verification log
   # Should update workflow.json
   ```

**Track Results:**
```markdown
| Epic 1 | Story 1 | epic-1-story-1.md | 65/100 → 94/100 | Fail → Pass | Missing validation commands, broken URLs |
```

**Test Coverage:**
- [ ] PRP validation enforcement executed
- [ ] Low-quality PRP failed validation (score < 90)
- [ ] Specific issues identified
- [ ] Remediation guidance provided
- [ ] Issues fixed
- [ ] Re-validation passed (score ≥ 90)
- [ ] Verification log created
- [ ] workflow.json updated

---

### Phase 6: Implementation (Epic 1) - FAILURE ESCALATION TEST

**Scenario 5: Failure Escalation Protocol**

**Test Steps:**

1. **During Level 2 validation (Unit Tests), simulate failures:**

   **Attempt 1-3 (Level 1: Auto-retry):**
   ```bash
   # Execute tests, simulate failure
   # System should auto-retry
   # Track: failure count = 1, 2, 3
   ```

2. **Verify Level 1 Behavior:**
   ```bash
   # Should see: "Level 1 Escalation: Auto-Retry"
   # Should see: "Attempt: X/3"
   # Should retry automatically
   ```

3. **Attempt 4-6 (Level 2: Pattern Analysis):**
   ```bash
   # Continue failing tests
   # Track: failure count = 4, 5, 6
   ```

4. **Verify Level 2 Behavior:**
   ```bash
   # Should see: "Level 2 Escalation: Pattern Analysis"
   # Should analyze error pattern
   # Should suggest strategy adjustment
   # Check pattern detection:
   grep -i "pattern:" .codex/state/escalations/escalation-*.md
   ```

5. **Attempt 7+ (Level 3: User Intervention):**
   ```bash
   # Continue failing tests
   # Track: failure count = 7
   ```

6. **Verify Level 3 Behavior:**
   ```bash
   # Should see: "Level 3 Escalation: User Intervention Required"
   # Should create escalation report
   ls -la .codex/state/escalations/escalation-*.md

   # Review escalation report
   cat .codex/state/escalations/escalation-*.md

   # Should show:
   # - Failure history
   # - Attempted solutions
   # - User action options
   ```

7. **User Provides Guidance and Resolves:**
   ```bash
   # Manual intervention to fix root cause
   # Re-run validation
   # Should succeed
   ```

8. **(Optional) Test Level 4 Checkpoint:**
   ```bash
   # If user chooses abort:
   # Should create checkpoint
   ls -la .codex/state/checkpoints/checkpoint-*.json

   # Verify checkpoint contains:
   # - Current state
   # - Completed work
   # - Failure context
   # - Recovery guidance
   ```

**Track Results:**
```markdown
| Story 1 | Level 2 | 8 | Level 3 | User fixed mock configuration, passed on retry |
```

**Test Coverage:**
- [ ] Level 1 auto-retry triggered (failures 1-3)
- [ ] Level 2 pattern analysis triggered (failures 4-6)
- [ ] Pattern correctly identified
- [ ] Strategy adjustment suggested
- [ ] Level 3 user intervention triggered (failures 7+)
- [ ] Escalation report created
- [ ] User options presented
- [ ] Issue resolved after intervention
- [ ] (Optional) Level 4 checkpoint created and valid

---

**Scenario 6: Execution Learning Capture**

**Test Steps:**

1. **At PRP execution start:**
   ```bash
   # Execute capture-execution-learnings.md
   PRP_FILE="PRPs/epic-1-story-1.md"
   EPIC_NUM=1
   STORY_NUM=1
   ESTIMATED_HOURS=4
   ACTION="start"

   bash .codex/tasks/capture-execution-learnings.md
   ```

2. **Verify Execution Report Created:**
   ```bash
   cat .codex/state/execution-reports/epic-1-story-1.json

   # Should have:
   # - report_id
   # - prp_file
   # - start_time
   # - estimated_duration_hours: 4
   # - validation_results (all false initially)
   ```

3. **After Each Validation Level:**
   ```bash
   # Level 1 complete
   ACTION="level_complete"
   VALIDATION_LEVEL=1
   VALIDATION_PASSED=true
   ATTEMPTS=1

   bash .codex/tasks/capture-execution-learnings.md

   # Repeat for each level (0, 1, 2, 3, 4)
   ```

4. **Capture PRP Quality Issues (if failures occurred):**
   ```bash
   # If validation failed, system prompts:
   # "Were any issues caused by PRP quality?"
   # Enter: "PRP referenced outdated API endpoint, should have been /v2/users"
   ```

5. **Capture Working Patterns (if validation passed):**
   ```bash
   # If validation passed, system prompts:
   # "Did you use any particularly effective patterns?"
   # Enter: "Repository pattern with dependency injection worked well"
   ```

6. **After All Validations Complete:**
   ```bash
   ACTION="final"
   ACTUAL_HOURS=5.5

   bash .codex/tasks/capture-execution-learnings.md
   ```

7. **Verify Final Report:**
   ```bash
   cat .codex/state/execution-reports/epic-1-story-1.json

   # Should have:
   # - end_time
   # - actual_duration_hours: 5.5
   # - prp_quality_assessment: 0-100 score
   # - All validation_results populated
   # - patterns_that_worked: [...]
   # - prp_quality_issues: [...]
   # - improvements_for_next_prp: [...]
   ```

8. **Verify workflow.json Updated:**
   ```bash
   jq '.execution_reports | last' .codex/state/workflow.json

   # Should show path to execution report
   ```

**Track Results:**
```markdown
| Story 1 | 88/100 | 5.5h | 4h | Repository pattern with DI | PRP had outdated API endpoint |
```

**Test Coverage:**
- [ ] Execution report initialized on start
- [ ] Validation results updated per level
- [ ] PRP quality issues captured (if any)
- [ ] Working patterns captured (if any)
- [ ] Final report generated with quality score
- [ ] Actual vs estimated hours tracked
- [ ] Improvements extracted
- [ ] workflow.json updated with report path

---

### Phase 7: Epic 2 Start - EPIC LEARNING INTEGRATION TEST

**Scenario 7: Epic Learning Integration**

**Prerequisites:**
- Epic 1 complete with execution reports
- Epic 2 ready to begin

**Test Steps:**

1. **Before Creating Epic 2 PRPs, Run Learning Integration:**
   ```bash
   COMPLETED_EPIC=1
   NEXT_EPIC=2

   bash .codex/tasks/epic-learning-integration.md
   ```

2. **Verify Learning Extraction:**
   ```bash
   # System should:
   # - Find all epic-1-story-*.json reports
   # - Extract successful patterns
   # - Identify PRP gaps
   # - Analyze validation issues
   # - Calculate time variance
   ```

3. **Verify Learning Summary Created:**
   ```bash
   cat .codex/state/epic-learnings/epic-1-learning-summary.md

   # Should include:
   # - Successful patterns to reuse
   # - PRP gaps to address
   # - Validation issues encountered
   # - Time estimate recommendations
   # - Epic 2 PRP creation checklist
   ```

4. **Verify Integration Checklist Created:**
   ```bash
   cat .codex/state/epic-learnings/epic-2-integration-checklist.md

   # Should include:
   # - Pre-creation review items
   # - During-creation application points
   # - Post-creation validation checks
   ```

5. **Verify workflow.json Updated:**
   ```bash
   jq '.epic_learnings.learnings | last' .codex/state/workflow.json

   # Should show:
   # - epic_id: 1
   # - learning_summary_file
   # - integration_checklist_file
   # - patterns_count
   # - gaps_count
   ```

6. **Apply Learnings to Epic 2 PRPs:**
   - Review learning summary before creating PRPs
   - Use integration checklist during PRP creation
   - Verify Epic 1 patterns included in Epic 2 PRPs
   - Verify Epic 1 gaps NOT repeated in Epic 2 PRPs

7. **Compare Epic 1 vs Epic 2 Quality:**
   ```bash
   # After Epic 2 execution, compare:
   # - Average PRP quality scores
   # - Average time estimate accuracy
   # - Validation failure rates
   # - Pattern reuse count
   ```

**Track Results:**
```markdown
**Quality Score Comparison:**
- Epic 1 avg PRP quality: 85/100
- Epic 2 avg PRP quality: 92/100
- Improvement: +7 points (8.2%)

**Time Estimate Accuracy:**
- Epic 1 variance: +35% (consistently over)
- Epic 2 variance: +12% (much closer)
- Improvement: 23 percentage points
```

**Test Coverage:**
- [ ] Learning integration executed before Epic 2
- [ ] All Epic 1 execution reports analyzed
- [ ] Patterns extracted (successful and failed)
- [ ] PRP gaps identified
- [ ] Learning summary generated
- [ ] Integration checklist created
- [ ] Learnings applied to Epic 2 PRPs
- [ ] Quality improvement measured (Epic 2 > Epic 1)
- [ ] Time estimate accuracy improved

---

## Success Criteria

### Feedback Loops ✅
- [x] At least 1 feedback request successfully created
- [x] Feedback tracked in workflow.json with status progression
- [x] PM successfully resolved feedback
- [x] Resolution time < 30 minutes
- [x] No more than 3 iterations per feedback request
- [x] Context package created and usable

### PRP Validation ✅
- [x] At least 1 PRP failed pre-flight validation (intentional)
- [x] Specific issues identified in validation failure
- [x] PRP fixed and re-validated successfully
- [x] All PRPs score ≥90 before execution
- [x] Verification logs created
- [x] workflow.json updated with validation results

### Failure Escalation ✅
- [x] Level 1 auto-retry triggered
- [x] Level 2 pattern analysis triggered
- [x] Level 3 user intervention triggered (optional but ideal)
- [x] Escalation reports created
- [x] No infinite retry loops
- [x] Recovery successful after escalation

### Epic Learning ✅
- [x] Execution reports captured for all Epic 1 stories
- [x] Learning summary generated before Epic 2
- [x] Patterns extracted and documented
- [x] PRP gaps identified
- [x] Learnings applied to Epic 2
- [x] Measurable quality improvement (Epic 2 > Epic 1)

### Architecture Validation ✅
- [x] Zero-knowledge test executed
- [x] Completeness ≥95% achieved
- [x] Confidence scoring executed
- [x] Overall confidence ≥85/100
- [x] Weak areas identified and addressed

---

## Data Collection Checklist

At the end of the project, ensure you've captured:

- [ ] Feedback request data (count, resolution time, iterations)
- [ ] PRP validation data (scores, failure rate, issues)
- [ ] Failure escalation data (level distribution, recovery rate)
- [ ] Execution learning data (reports, patterns, gaps)
- [ ] Epic learning data (quality improvement, time accuracy)
- [ ] Architecture validation data (completeness, confidence scores)

**Export Data:**
```bash
# Create final Level 3 validation report
cat > .codex/state/phase2-validation/${PROJECT_NAME}-level3-results.md <<EOF
# Phase 2 Level 3 Validation Results - ${PROJECT_NAME}

**Project:** ${PROJECT_NAME}
**Completion Date:** $(date +"%Y-%m-%d")

## Summary

**Feedback Loops:** [count] requests, [avg time] resolution, [max iterations]
**PRP Validation:** [count] PRPs, [score] avg quality, [failures] failed validation
**Failure Escalation:** [L1 count] L1, [L2 count] L2, [L3 count] L3, [L4 count] L4
**Epic Learning:** [improvement]% quality improvement Epic 1→2
**Architecture Validation:** [completeness]% completeness, [confidence]/100 confidence

## Overall Assessment

✅ PASSED / ⚠️ NEEDS IMPROVEMENT / ❌ FAILED

**Recommendation:** [Next steps]
EOF
```

---

## Next Steps

After completing Level 3 validation:
1. Review results against success criteria
2. Identify any Phase 2 feature refinements needed
3. Proceed to Level 4 metrics validation (requires 2-3 projects)
4. Document lessons learned for CODEX improvement
