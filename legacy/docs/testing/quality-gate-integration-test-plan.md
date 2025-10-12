# Quality Gate Integration Test Plan

## Overview

This test plan provides comprehensive integration testing scenarios for the CODEX quality gate wiring system. It covers workflow orchestration, end-to-end execution, edge cases, and regression validation to ensure quality gates function correctly across all phases and operation modes.

**Document Version**: 1.0
**Created**: 2025-10-08
**Status**: Design Complete, Implementation Pending

## Test Objectives

1. **Validate Quality Gate Orchestration**: Ensure quality gates trigger correctly at phase transitions and orchestrator respects gate results
2. **Verify End-to-End Workflows**: Confirm complete workflows execute with quality gates across all operation modes
3. **Test Edge Cases**: Validate system behavior under error conditions, boundary values, and unusual states
4. **Ensure Regression Safety**: Verify existing functionality remains intact after quality gate integration

## Test Categories Summary

| Category | Test Scenarios | Estimated Time | Priority |
|----------|---------------|----------------|----------|
| 1. Workflow-Level Tests | 12 scenarios | 6-8 hours | CRITICAL |
| 2. End-to-End Tests | 9 scenarios | 10-14 hours | CRITICAL |
| 3. Edge Case Tests | 15 scenarios | 8-12 hours | HIGH |
| 4. Regression Tests | 10 scenarios | 4-6 hours | HIGH |
| **TOTAL** | **46 scenarios** | **28-40 hours** | - |

---

## Category 1: Workflow-Level Integration Tests

**Purpose**: Validate quality gate triggering, orchestrator integration, and phase transition logic.

### Test Group 1.1: Quality Gate Triggering (4 scenarios)

#### Test 1.1.1: Quality Gate Triggers at Discovery → Analyst Transition
**Objective**: Verify discovery quality gate executes when transitioning to analyst phase

**Preconditions**:
- Discovery phase completed with elicitation_completed['discovery'] = true
- workflow.json exists with valid state

**Test Steps**:
1. Complete discovery phase with 9 questions answered
2. Mark discovery phase complete
3. Trigger phase transition to analyst
4. Verify quality-gate agent invoked
5. Verify discovery-quality-gate.md checklist loaded
6. Verify gate execution completes

**Expected Results**:
- Quality gate automatically triggered before analyst phase starts
- discovery-quality-gate.md checklist executed
- workflow.json updated with quality_gate_results['discovery']
- Timestamp and mode recorded correctly

**Validation Criteria**:
```bash
# Check workflow.json contains quality gate result
jq '.quality_gate_results.discovery' .codex/state/workflow.json
# Expected: Object with status, score, timestamp, mode

# Verify result file created
test -f .codex/state/quality-gate-discovery-*.json
```

**Time Estimate**: 45 minutes

---

#### Test 1.1.2: Quality Gate Triggers at PM → Architect Transition
**Objective**: Verify PM quality gate executes with 90-item checklist

**Preconditions**:
- PM phase completed with PRD created
- elicitation_completed['pm'] = true

**Test Steps**:
1. Complete PM phase with PRD document
2. Mark PM phase complete
3. Trigger phase transition to architect
4. Verify quality-gate agent invoked
5. Verify pm-quality-gate.md checklist (90 items) loaded
6. Complete gate execution in batch mode

**Expected Results**:
- PM quality gate triggered automatically
- All 90 checklist items evaluated
- Score calculated: 100 - (10 × critical_fails) - (5 × standard_fails)
- Status determined: APPROVED/CONDITIONAL/REJECTED based on score

**Validation Criteria**:
```bash
# Verify 90 items evaluated
gate_result=$(jq '.quality_gate_results.pm' .codex/state/workflow.json)
total_items=$(echo $gate_result | jq '.sections[].items_checked' | awk '{s+=$1} END {print s}')
test $total_items -eq 90
```

**Time Estimate**: 1 hour

---

#### Test 1.1.3: Quality Gate Triggers at Architect → PRP Transition
**Objective**: Verify architect quality gate executes with 169-item checklist

**Preconditions**:
- Architect phase completed with architecture.md created
- All 5 enhanced sections present (frontend, testing, platform, error-handling, confidence)

**Test Steps**:
1. Complete architect phase with architecture document
2. Mark architect phase complete
3. Trigger phase transition to PRP creator
4. Verify quality-gate agent invoked
5. Verify architect-quality-gate.md checklist (169 items) loaded
6. Complete gate execution

**Expected Results**:
- Architect quality gate triggered
- All 169 items evaluated
- Frontend-only sections skipped if backend project
- Confidence scoring evaluated
- Zero-knowledge test criteria checked

**Validation Criteria**:
```bash
# Verify 169 items total (some may be skipped)
gate_result=$(jq '.quality_gate_results.architect' .codex/state/workflow.json)
echo $gate_result | jq '.checklist' | grep "architect-quality-gate.md"
```

**Time Estimate**: 1.5 hours

---

#### Test 1.1.4: Quality Gate Triggers at PRP Creation → Execution Transition
**Objective**: Verify PRP quality gate executes with validation enforcement

**Preconditions**:
- PRP created for feature
- PRP contains file references, URLs, validation commands

**Test Steps**:
1. Complete PRP creation
2. Mark PRP complete
3. Trigger PRP validation enforcement
4. Verify prp-quality-gate.md checklist (30+ items) loaded
5. Verify file references checked
6. Verify URLs validated
7. Verify validation commands require verification log

**Expected Results**:
- PRP quality gate triggered before execution
- All file references exist and are accessible
- All URLs return HTTP 200 or documented
- Validation commands have verification log section
- Score ≥90 required to proceed

**Validation Criteria**:
```bash
# Verify PRP score threshold enforced
score=$(jq '.quality_gate_results.prp.score' .codex/state/workflow.json)
test $score -ge 90
```

**Time Estimate**: 1 hour

---

### Test Group 1.2: Orchestrator Respecting Gate Results (4 scenarios)

#### Test 1.2.1: APPROVED Status Allows Phase Progression
**Objective**: Verify APPROVED gate (score 90-100) allows workflow to continue

**Preconditions**:
- Quality gate executed with high-quality document
- Gate result: APPROVED, score 95

**Test Steps**:
1. Execute quality gate resulting in APPROVED status
2. Verify workflow.json updated with status="APPROVED"
3. Attempt phase transition
4. Verify transition succeeds without blocking

**Expected Results**:
- Phase transition proceeds immediately
- Next phase agent spawned
- No user intervention required
- transformation_history logs successful transition

**Validation Criteria**:
```bash
# Verify next phase started
current_phase=$(jq -r '.current_phase' .codex/state/workflow.json)
test "$current_phase" = "analyst"  # Or next expected phase
```

**Time Estimate**: 30 minutes

---

#### Test 1.2.2: REJECTED Status Blocks Phase Progression
**Objective**: Verify REJECTED gate (score <70) blocks workflow progression

**Preconditions**:
- Quality gate executed with low-quality document
- Gate result: REJECTED, score 55

**Test Steps**:
1. Execute quality gate resulting in REJECTED status
2. Verify workflow.json updated with status="REJECTED"
3. Attempt phase transition
4. Verify transition blocked
5. Verify detailed remediation presented to user

**Expected Results**:
- Phase transition blocked
- Orchestrator presents specific failures from gate
- User offered options: 1) Fix issues, 2) Override (with justification), 3) Abort
- workflow.json remains in current phase until resolution

**Validation Criteria**:
```bash
# Verify phase NOT progressed
current_phase=$(jq -r '.current_phase' .codex/state/workflow.json)
test "$current_phase" = "pm"  # Still in failing phase

# Verify rejection logged
status=$(jq -r '.quality_gate_results.pm.status' .codex/state/workflow.json)
test "$status" = "REJECTED"
```

**Time Estimate**: 45 minutes

---

#### Test 1.2.3: CONDITIONAL Status Requires User Confirmation
**Objective**: Verify CONDITIONAL gate (score 70-89) prompts user decision

**Preconditions**:
- Quality gate executed with moderate-quality document
- Gate result: CONDITIONAL, score 82

**Test Steps**:
1. Execute quality gate resulting in CONDITIONAL status
2. Verify workflow.json updated with status="CONDITIONAL"
3. Attempt phase transition
4. Verify user prompted with warnings
5. User chooses to proceed
6. Verify transition completes

**Expected Results**:
- Phase transition paused for user decision
- Specific warnings/concerns presented
- User options: 1) Proceed anyway, 2) Fix issues first
- If proceed: transition completes, CONDITIONAL status logged
- If fix: return to document editing

**Validation Criteria**:
```bash
# Verify conditional status logged
status=$(jq -r '.quality_gate_results.pm.status' .codex/state/workflow.json)
test "$status" = "CONDITIONAL"

# Verify user decision recorded
decision=$(jq -r '.quality_gate_results.pm.user_decision' .codex/state/workflow.json)
test "$decision" = "proceed" || test "$decision" = "fix"
```

**Time Estimate**: 45 minutes

---

#### Test 1.2.4: Score Exactly at Threshold (90) is APPROVED
**Objective**: Verify boundary condition: score of exactly 90 counts as APPROVED

**Preconditions**:
- Quality gate executed with precise score of 90

**Test Steps**:
1. Execute quality gate with failures totaling exactly 10 points deduction (score 90)
2. Verify status determined as APPROVED (not CONDITIONAL)
3. Verify phase transition allowed

**Expected Results**:
- Score of 90 → APPROVED status
- Threshold is inclusive: score ≥ 90
- Phase transition proceeds

**Validation Criteria**:
```bash
score=$(jq '.quality_gate_results.pm.score' .codex/state/workflow.json)
status=$(jq -r '.quality_gate_results.pm.status' .codex/state/workflow.json)
test $score -eq 90 && test "$status" = "APPROVED"
```

**Time Estimate**: 30 minutes

---

### Test Group 1.3: Workflow YAML Configuration (4 scenarios)

#### Test 1.3.1: Workflow YAML Correctly Defines Quality Gates
**Objective**: Verify greenfield-swift.yaml has quality gate validation entries

**Test Steps**:
1. Parse greenfield-swift.yaml
2. For each phase (discovery, analyst, pm, architect, prp-creator):
   - Verify validation section exists
   - Verify quality gate checklist specified
   - Verify elicitation_checkpoint: true

**Expected Results**:
- Each phase has validation.quality_gate_checklist defined
- Each phase has validation.elicitation_checkpoint: true
- Checklist filenames match actual files in .codex/checklists/

**Validation Criteria**:
```bash
# Verify quality gate references in workflow YAML
grep -q "quality_gate_checklist" .codex/workflows/greenfield-swift.yaml
grep -q "discovery-quality-gate.md" .codex/workflows/greenfield-swift.yaml
grep -q "pm-quality-gate.md" .codex/workflows/greenfield-swift.yaml
```

**Time Estimate**: 30 minutes

---

#### Test 1.3.2: Workflow YAML Operation Mode Behavior Correct
**Objective**: Verify mode_behavior entries define gate execution per mode

**Test Steps**:
1. Parse workflow YAML mode_behavior sections
2. Verify interactive mode: gate executes section-by-section
3. Verify batch mode: gate executes at phase end
4. Verify YOLO mode: gate skipped but violation logged

**Expected Results**:
- mode_behavior clearly defines when gates execute
- interactive: immediate gate after section
- batch: gate after all sections complete
- yolo: gate bypassed with logged violation

**Validation Criteria**:
```yaml
# Expected in workflow YAML:
mode_behavior: |
  Interactive mode: Quality gate executes after this phase
  Batch mode: Quality gate deferred to phase completion
  YOLO mode: Quality gate skipped (logged violation)
```

**Time Estimate**: 30 minutes

---

#### Test 1.3.3: Phase Transitions Reference Quality Gates
**Objective**: Verify orchestrator checks quality_gate_results before transitions

**Test Steps**:
1. Review orchestrator.md phase transition logic
2. Verify quality gate check before spawning next agent
3. Verify transition logic: if status="REJECTED" → block
4. Verify transition logic: if status="CONDITIONAL" → prompt
5. Verify transition logic: if status="APPROVED" → proceed

**Expected Results**:
- Orchestrator reads workflow.json quality_gate_results
- Transition blocked on REJECTED
- User prompted on CONDITIONAL
- Automatic proceed on APPROVED

**Validation Criteria**:
```bash
# Verify orchestrator has quality gate check logic
grep -q "quality_gate_results" .codex/agents/orchestrator.md
grep -q "REJECTED" .codex/agents/orchestrator.md
```

**Time Estimate**: 45 minutes

---

#### Test 1.3.4: Validation Requirements Match Checklists
**Objective**: Verify workflow validation requirements align with checklist items

**Test Steps**:
1. For each phase, compare workflow YAML validation section to checklist
2. Verify validation requirements in YAML are covered by checklist items
3. Verify no orphaned requirements (in YAML but not checklist)
4. Verify no missing requirements (in checklist but not YAML)

**Expected Results**:
- 100% alignment between workflow validation and checklist coverage
- All workflow requirements testable via checklist
- All critical checklist items reflected in workflow validation

**Validation Criteria**:
```bash
# Example: PM phase
pm_validation=$(grep -A 10 "agent: pm" .codex/workflows/greenfield-swift.yaml | grep "validation:")
pm_checklist_items=$(grep -c "^- \[ \]" .codex/checklists/pm-quality-gate.md)
# Verify all validation points have checklist coverage
```

**Time Estimate**: 1 hour

---

## Category 2: End-to-End Workflow Tests

**Purpose**: Validate complete workflows execute correctly with quality gates across all operation modes.

### Test Group 2.1: Greenfield-Swift Complete Workflow (3 scenarios)

#### Test 2.1.1: Complete Workflow in Interactive Mode
**Objective**: Run full greenfield-swift workflow with interactive quality gates

**Preconditions**:
- Clean CODEX state
- operation_mode set to "interactive"

**Test Steps**:
1. Start greenfield-swift workflow
2. Complete discovery phase (9 questions)
3. Execute discovery quality gate interactively (section-by-section)
4. Complete analyst phase (project brief)
5. Execute analyst quality gate interactively
6. Complete PM phase (PRD with epics/stories)
7. Execute PM quality gate interactively (90 items)
8. Complete architect phase (architecture with 5 sections)
9. Execute architect quality gate interactively (169 items)
10. Complete PRP creation
11. Execute PRP quality gate with validation enforcement
12. Verify workflow.json has all quality_gate_results

**Expected Results**:
- Each quality gate executes immediately after phase completion
- User prompted section-by-section for validation
- Evidence collection required for each item
- All gates result in APPROVED or CONDITIONAL (proceed)
- Complete workflow.json with 5 quality gate results
- No phase skipped or blocked

**Validation Criteria**:
```bash
# Verify all 5 phases have quality gate results
phases=("discovery" "analyst" "pm" "architect" "prp")
for phase in "${phases[@]}"; do
  result=$(jq ".quality_gate_results.$phase" .codex/state/workflow.json)
  test "$result" != "null" || echo "Missing $phase gate result"
done

# Verify workflow completed
status=$(jq -r '.workflow_status' .codex/state/workflow.json)
test "$status" = "completed"
```

**Time Estimate**: 4-5 hours

---

#### Test 2.1.2: Complete Workflow in Batch Mode
**Objective**: Run full greenfield-swift workflow with batch quality gates

**Preconditions**:
- Clean CODEX state
- operation_mode set to "batch"

**Test Steps**:
1. Start greenfield-swift workflow in batch mode
2. Complete discovery phase
3. Verify quality gate deferred to phase end
4. Complete all discovery sections, then execute gate in batch
5. Repeat for analyst, PM, architect, PRP phases
6. For each phase: all sections drafted, then single gate execution
7. Verify comprehensive gate reports at each phase end

**Expected Results**:
- Quality gates execute once per phase (not section-by-section)
- Batch mode presents comprehensive report
- All validation items checked at once
- User reviews full report, then proceeds
- Same quality standards as interactive mode
- Faster execution due to batching

**Validation Criteria**:
```bash
# Verify batch mode logged in each gate result
for phase in discovery analyst pm architect prp; do
  mode=$(jq -r ".quality_gate_results.$phase.mode" .codex/state/workflow.json)
  test "$mode" = "batch" || echo "$phase not in batch mode"
done
```

**Time Estimate**: 3-4 hours

---

#### Test 2.1.3: Complete Workflow in YOLO Mode
**Objective**: Run full greenfield-swift workflow with quality gates bypassed

**Preconditions**:
- Clean CODEX state
- operation_mode set to "yolo"

**Test Steps**:
1. Start greenfield-swift workflow in YOLO mode
2. Complete discovery phase
3. Verify quality gate skipped but violation logged
4. Repeat for all phases: analyst, PM, architect, PRP
5. Verify workflow completes without quality gate blocking
6. Verify all violations logged in workflow.json

**Expected Results**:
- Quality gates skipped for all phases
- Each skip logged as violation with timestamp
- Workflow proceeds without quality validation
- violations array in workflow.json has 5 entries
- Each violation: {phase, type: "quality_gate_skipped", mode: "yolo", timestamp}

**Validation Criteria**:
```bash
# Verify violations logged
violation_count=$(jq '.violations | length' .codex/state/workflow.json)
test $violation_count -eq 5

# Verify violation type
jq '.violations[0].type' .codex/state/workflow.json | grep "quality_gate_skipped"
```

**Time Estimate**: 2-3 hours

---

### Test Group 2.2: Quality Gate Execution Across Phases (3 scenarios)

#### Test 2.2.1: Discovery → Analyst with 15-Item Checklist
**Objective**: Verify discovery quality gate (15 items) executes correctly

**Test Steps**:
1. Complete discovery with 9 questions answered
2. Trigger discovery quality gate
3. Verify 15 validation items checked:
   - Project scope clarity (5 items)
   - Context completeness (5 items)
   - Workflow readiness (5 items)
4. Verify discovery-summary.json persistence validated
5. Verify template variables extracted

**Expected Results**:
- All 15 items evaluated
- discovery-summary.json exists and validated
- Score reflects quality of discovery phase
- Analyst can proceed with sufficient context

**Validation Criteria**:
```bash
# Verify discovery summary exists
test -f .codex/state/discovery-summary.json

# Verify 15 items in gate result
items=$(jq '[.sections[].items_checked] | add' .codex/state/quality-gate-discovery-*.json)
test $items -eq 15
```

**Time Estimate**: 1 hour

---

#### Test 2.2.2: PM → Architect with 90-Item Checklist and Story Sizing
**Objective**: Verify PM quality gate validates PRD comprehensively

**Test Steps**:
1. Complete PM phase with PRD containing epics and stories
2. Trigger PM quality gate (90 items + 10 story sizing items = 100 total)
3. Verify validation categories:
   - Problem definition & MVP scope
   - User experience
   - Functional requirements
   - Epic structure
   - Story sizing & complexity (AI-optimized)
4. Verify story sizing guidance checked:
   - Stories sized 4-8 hours ideal
   - Vertical slices validated
   - AI-friendly boundaries

**Expected Results**:
- All 100 items evaluated
- Story sizing appropriate for AI implementation
- Vertical slice pattern followed
- PRD quality sufficient for architecture phase

**Validation Criteria**:
```bash
# Verify 100 items (90 base + 10 story sizing)
items=$(jq '[.sections[].items_checked] | add' .codex/state/quality-gate-pm-*.json)
test $items -ge 90
```

**Time Estimate**: 1.5 hours

---

#### Test 2.2.3: Architect → PRP with 184-Item Checklist and AI Suitability
**Objective**: Verify architect quality gate validates comprehensively

**Test Steps**:
1. Complete architect phase with all 5 enhanced sections
2. Trigger architect quality gate (169 + 15 AI items = 184 total)
3. Verify validation categories:
   - Frontend architecture (skip if backend-only)
   - Backend architecture
   - Data architecture
   - Testing strategy
   - Platform selection
   - Error handling
   - Confidence scoring
   - AI implementation readiness (15 items)
4. Verify zero-knowledge test criteria
5. Verify confidence scoring calculated

**Expected Results**:
- All 184 items evaluated (some skipped if backend-only)
- AI suitability validated (explicit patterns, examples)
- Confidence score 0-100 calculated
- PRP creator has complete technical context

**Validation Criteria**:
```bash
# Verify 184 items total
items=$(jq '[.sections[].items_checked] | add' .codex/state/quality-gate-architect-*.json)
test $items -ge 169

# Verify confidence score present
confidence=$(jq '.confidence_score' .codex/state/quality-gate-architect-*.json)
test $confidence -ge 0 && test $confidence -le 100
```

**Time Estimate**: 2 hours

---

### Test Group 2.3: State Persistence and Recovery (3 scenarios)

#### Test 2.3.1: workflow.json Updated After Each Gate
**Objective**: Verify workflow.json correctly tracks all quality gate results

**Test Steps**:
1. Start workflow, execute first quality gate
2. Read workflow.json, verify quality_gate_results['discovery'] present
3. Execute second quality gate
4. Verify quality_gate_results['analyst'] added without corrupting 'discovery'
5. Continue for all phases
6. Verify final workflow.json has complete history

**Expected Results**:
- workflow.json updated atomically after each gate
- No data loss between updates
- All gate results preserved
- transformation_history logs all gate executions

**Validation Criteria**:
```bash
# Verify incremental updates
jq '.quality_gate_results | keys' .codex/state/workflow.json
# Expected: ["discovery", "analyst", "pm", "architect", "prp"]

# Verify transformation history
jq '.transformation_history[] | select(.action | contains("quality_gate"))' .codex/state/workflow.json
```

**Time Estimate**: 1 hour

---

#### Test 2.3.2: Quality Gate Results Persist Across Sessions
**Objective**: Verify workflow can be resumed with quality gate history intact

**Test Steps**:
1. Start workflow, complete discovery and analyst with gates
2. Save workflow.json
3. Simulate session termination (close CODEX)
4. Restart workflow from workflow.json
5. Verify previous quality gate results still present
6. Continue with PM phase
7. Verify new gate results added alongside old

**Expected Results**:
- Quality gate results survive workflow suspension/resume
- No data loss on restart
- Workflow state fully recoverable
- All timestamps and modes preserved

**Validation Criteria**:
```bash
# After restart, verify old results still present
jq '.quality_gate_results.discovery' .codex/state/workflow.json
jq '.quality_gate_results.analyst' .codex/state/workflow.json
# Both should return valid objects
```

**Time Estimate**: 1 hour

---

#### Test 2.3.3: Separate Gate Result Files Created
**Objective**: Verify individual gate result files saved for audit trail

**Test Steps**:
1. Execute quality gate for each phase
2. Verify separate result file created: .codex/state/quality-gate-{phase}-{timestamp}.json
3. Verify file contains: phase, checklist, timestamp, mode, status, score, sections, evidence
4. Verify files readable and parseable

**Expected Results**:
- 5 separate gate result files after complete workflow
- Each file has complete validation details
- Files serve as audit trail
- Files can regenerate workflow.json summary if needed

**Validation Criteria**:
```bash
# Verify result files exist
ls .codex/state/quality-gate-discovery-*.json
ls .codex/state/quality-gate-pm-*.json
ls .codex/state/quality-gate-architect-*.json

# Verify file structure
jq keys .codex/state/quality-gate-pm-*.json
# Expected: ["phase", "checklist", "timestamp", "mode", "status", "score", "sections", "evidence"]
```

**Time Estimate**: 45 minutes

---

## Category 3: Edge Case Tests

**Purpose**: Validate system behavior under error conditions, boundary values, and unusual states.

### Test Group 3.1: Missing or Invalid Data (5 scenarios)

#### Test 3.1.1: Missing Quality Gate Result at Transition
**Objective**: Verify orchestrator handles missing quality_gate_results entry

**Test Steps**:
1. Complete discovery phase
2. Manually delete quality_gate_results['discovery'] from workflow.json
3. Attempt transition to analyst phase
4. Verify orchestrator detects missing gate result
5. Verify user prompted to execute quality gate

**Expected Results**:
- Transition blocked due to missing gate result
- User notified: "Quality gate required before proceeding"
- User options: 1) Execute gate now, 2) Skip (YOLO mode only), 3) Abort
- After gate execution, transition proceeds

**Validation Criteria**:
```bash
# Simulate missing gate result
jq 'del(.quality_gate_results.discovery)' .codex/state/workflow.json > temp.json
mv temp.json .codex/state/workflow.json

# Attempt transition should fail gracefully
# Expected: Error message, user prompt
```

**Time Estimate**: 45 minutes

---

#### Test 3.1.2: Corrupted workflow.json
**Objective**: Verify system detects and recovers from corrupted state file

**Test Steps**:
1. Start workflow, complete discovery phase
2. Corrupt workflow.json (invalid JSON syntax)
3. Attempt to read workflow state
4. Verify error detected
5. Verify recovery options presented:
   - Restore from backup
   - Recreate from last checkpoint
   - Start fresh (lose progress)

**Expected Results**:
- JSON parse error detected
- User notified with clear error message
- Recovery options presented
- If backup exists, restoration possible
- If no backup, graceful failure with guidance

**Validation Criteria**:
```bash
# Corrupt workflow.json
echo "{ invalid json" > .codex/state/workflow.json

# Attempt to read should fail gracefully
jq '.' .codex/state/workflow.json
# Expected: parse error

# System should detect and handle
```

**Time Estimate**: 1 hour

---

#### Test 3.1.3: Quality Gate Task Execution Failure
**Objective**: Verify handling of execute-quality-gate.md task failure

**Test Steps**:
1. Trigger quality gate execution
2. Simulate task failure (e.g., checklist file missing)
3. Verify error caught and logged
4. Verify user notified with specific error
5. Verify workflow not corrupted by failure

**Expected Results**:
- Task failure caught gracefully
- Specific error reported: "Checklist file not found: pm-quality-gate.md"
- workflow.json remains valid
- User options: 1) Fix issue and retry, 2) Skip gate (logged), 3) Abort

**Validation Criteria**:
```bash
# Simulate missing checklist
mv .codex/checklists/pm-quality-gate.md /tmp/

# Trigger gate execution
# Expected: Error message, not crash

# Restore checklist
mv /tmp/pm-quality-gate.md .codex/checklists/
```

**Time Estimate**: 45 minutes

---

#### Test 3.1.4: Checklist File Invalid Format
**Objective**: Verify handling of malformed checklist markdown

**Test Steps**:
1. Corrupt pm-quality-gate.md (remove required sections)
2. Trigger PM quality gate
3. Verify format validation fails
4. Verify specific format errors reported
5. Verify workflow.json not corrupted

**Expected Results**:
- Checklist validation detects invalid format
- Specific errors: "Missing LLM initialization", "No checklist items found"
- Gate execution aborted safely
- User notified with remediation guidance

**Validation Criteria**:
```bash
# Corrupt checklist format
echo "# Broken Checklist" > .codex/checklists/pm-quality-gate.md

# Attempt gate execution
# Expected: Validation error before execution
```

**Time Estimate**: 45 minutes

---

#### Test 3.1.5: Missing Evidence in Interactive Mode
**Objective**: Verify evidence collection enforcement in interactive mode

**Test Steps**:
1. Execute quality gate in interactive mode
2. For validation item, provide no evidence citation
3. Verify system requires evidence before proceeding
4. Provide insufficient evidence (vague)
5. Verify system requests specific citation
6. Provide proper evidence (document section reference)
7. Verify acceptance

**Expected Results**:
- Evidence required for each validation item
- Empty evidence rejected: "Please cite specific document section"
- Vague evidence rejected: "Be more specific - provide section and line numbers"
- Proper evidence accepted: "Section 3.2, lines 45-50: User authentication flow"

**Validation Criteria**:
```bash
# Evidence stored in gate result
evidence=$(jq '.sections[0].evidence[0].evidence' .codex/state/quality-gate-pm-*.json)
test -n "$evidence"  # Evidence present
test ${#evidence} -gt 20  # Evidence substantial
```

**Time Estimate**: 1 hour

---

### Test Group 3.2: Boundary Conditions (5 scenarios)

#### Test 3.2.1: Score Exactly at APPROVED/CONDITIONAL Boundary (90)
**Objective**: Verify boundary: score 90 is APPROVED, 89 is CONDITIONAL

**Test Steps**:
1. Create gate result with score exactly 90
2. Verify status = APPROVED
3. Verify transition allowed
4. Create gate result with score exactly 89
5. Verify status = CONDITIONAL
6. Verify user prompted

**Expected Results**:
- Score 90: APPROVED (boundary inclusive)
- Score 89: CONDITIONAL
- Clear threshold enforcement

**Validation Criteria**:
```python
# Scoring logic test
def test_boundary():
    assert determine_status(90) == "APPROVED"
    assert determine_status(89) == "CONDITIONAL"
    assert determine_status(70) == "CONDITIONAL"
    assert determine_status(69) == "REJECTED"
```

**Time Estimate**: 30 minutes

---

#### Test 3.2.2: Score Exactly at CONDITIONAL/REJECTED Boundary (70)
**Objective**: Verify boundary: score 70 is CONDITIONAL, 69 is REJECTED

**Test Steps**:
1. Create gate result with score exactly 70
2. Verify status = CONDITIONAL
3. Verify user prompted (can proceed with warning)
4. Create gate result with score exactly 69
5. Verify status = REJECTED
6. Verify transition blocked

**Expected Results**:
- Score 70: CONDITIONAL (lower boundary inclusive)
- Score 69: REJECTED
- Clear blocking threshold

**Time Estimate**: 30 minutes

---

#### Test 3.2.3: Maximum Score (100) with All Items Passed
**Objective**: Verify perfect score handling

**Test Steps**:
1. Execute quality gate with all items passing
2. Verify score calculated as 100
3. Verify status = APPROVED
4. Verify no warnings or concerns
5. Verify transition proceeds immediately

**Expected Results**:
- Score: 100
- Status: APPROVED
- Message: "Quality gate passed with perfect score"
- No user intervention required

**Time Estimate**: 30 minutes

---

#### Test 3.2.4: Minimum Score (0) with All Items Failed
**Objective**: Verify catastrophic failure handling

**Test Steps**:
1. Execute quality gate with all items failing
2. Verify score calculated as 0
3. Verify status = REJECTED
4. Verify comprehensive failure report
5. Verify transition blocked absolutely

**Expected Results**:
- Score: 0
- Status: REJECTED
- Detailed failure list for all items
- Strong warning: "Document requires major rework before proceeding"
- No override option (too many failures)

**Time Estimate**: 30 minutes

---

#### Test 3.2.5: Empty Checklist (0 Items)
**Objective**: Verify handling of checklist with no validation items

**Test Steps**:
1. Create checklist file with no validation items
2. Attempt gate execution
3. Verify error detected
4. Verify user notified: "Invalid checklist: no validation items found"

**Expected Results**:
- Gate execution fails validation
- Cannot calculate score from 0 items
- User notified to fix checklist
- Workflow not corrupted

**Time Estimate**: 30 minutes

---

### Test Group 3.3: Concurrent and State Conflicts (5 scenarios)

#### Test 3.3.1: Concurrent Gate Executions (Same Phase)
**Objective**: Verify system prevents concurrent gate execution on same phase

**Test Steps**:
1. Start quality gate execution for PM phase
2. While gate running, attempt second PM gate execution
3. Verify second execution blocked
4. Verify message: "Quality gate already in progress for this phase"
5. Complete first execution
6. Verify second execution can proceed

**Expected Results**:
- Only one gate execution per phase at a time
- Lock mechanism prevents concurrent execution
- Lock released after completion
- workflow.json remains consistent

**Time Estimate**: 1 hour

---

#### Test 3.3.2: Gate Execution During Phase Transition
**Objective**: Verify gate execution doesn't conflict with phase transition

**Test Steps**:
1. Complete phase, trigger automatic gate execution
2. Verify phase remains locked until gate completes
3. Verify transition blocked during gate execution
4. Verify gate completion releases phase lock
5. Verify transition proceeds after gate

**Expected Results**:
- Phase locked during gate execution
- Transition cannot proceed until gate completes
- Clear status indicator: "Executing quality gate..."
- Automatic transition after APPROVED gate

**Time Estimate**: 45 minutes

---

#### Test 3.3.3: workflow.json Modified During Gate Execution
**Objective**: Verify atomic workflow.json updates prevent corruption

**Test Steps**:
1. Start quality gate execution
2. Simulate external modification to workflow.json
3. Gate execution completes, attempts to save results
4. Verify conflict detected
5. Verify resolution strategy:
   - Read latest workflow.json
   - Merge gate results
   - Save atomically
   - No data loss

**Expected Results**:
- Atomic file operations prevent corruption
- Conflict detection works
- Merge strategy preserves all data
- workflow.json remains valid JSON

**Validation Criteria**:
```bash
# Simulate concurrent write
# Gate should detect and handle gracefully
```

**Time Estimate**: 1.5 hours

---

#### Test 3.3.4: Multiple Workflows in Same Directory
**Objective**: Verify workflow isolation when multiple workflows exist

**Test Steps**:
1. Start workflow A, complete discovery
2. Start workflow B (different project), complete discovery
3. Verify workflow A gates only update workflow-A.json
4. Verify workflow B gates only update workflow-B.json
5. Verify no cross-contamination

**Expected Results**:
- Each workflow has isolated state file
- Quality gates update correct workflow
- No shared state between workflows
- Concurrent workflows supported

**Time Estimate**: 1 hour

---

#### Test 3.3.5: Gate Result File Already Exists (Timestamp Collision)
**Objective**: Verify handling of filename collision for gate result files

**Test Steps**:
1. Execute quality gate, creating result file with timestamp
2. Immediately re-execute gate (same timestamp possible)
3. Verify second file gets unique name (append counter or milliseconds)
4. Verify both files valid
5. Verify workflow.json references latest

**Expected Results**:
- Unique filename guaranteed
- No file overwrite
- Both executions logged
- Latest result used for workflow decisions

**Time Estimate**: 30 minutes

---

## Category 4: Regression Tests

**Purpose**: Ensure existing CODEX functionality remains intact after quality gate integration.

### Test Group 4.1: Existing Workflow Compatibility (4 scenarios)

#### Test 4.1.1: Pre-Quality-Gate workflow.json Still Works
**Objective**: Verify backward compatibility with old workflow state files

**Test Steps**:
1. Create workflow.json without quality_gate_results field (old format)
2. Attempt to load workflow
3. Verify system detects old format
4. Verify automatic migration to new format
5. Verify workflow proceeds normally

**Expected Results**:
- Old format detected
- quality_gate_results field added with empty object {}
- quality_scores field added with empty object {}
- Workflow proceeds without error
- No data loss from old format

**Validation Criteria**:
```bash
# Create old-format workflow.json
jq 'del(.quality_gate_results, .quality_scores)' .codex/state/workflow.json > old-format.json

# Load should succeed with migration
# Verify new fields added
jq '.quality_gate_results' old-format.json
# Expected: {}
```

**Time Estimate**: 1 hour

---

#### Test 4.1.2: Elicitation Enforcement Still Works
**Objective**: Verify elicitation still required independent of quality gates

**Test Steps**:
1. Start workflow in interactive mode
2. Complete phase section without elicitation
3. Verify elicitation enforcement still triggers
4. Verify elicitation required before quality gate
5. Complete elicitation, then execute quality gate

**Expected Results**:
- Elicitation enforcement unchanged
- elicitation_completed check still works
- Quality gate cannot execute without elicitation
- Order: elicitation → quality gate → transition

**Validation Criteria**:
```bash
# Verify elicitation_completed still tracked
jq '.elicitation_completed' .codex/state/workflow.json

# Verify both elicitation and quality gate required
```

**Time Estimate**: 1 hour

---

#### Test 4.1.3: State Management Intact
**Objective**: Verify existing state management functions still work

**Test Steps**:
1. Test state-manager.md functions:
   - Read workflow.json
   - Update current_phase
   - Update elicitation_completed
   - Add transformation_history entry
2. Verify all state operations work with new fields present
3. Verify no function broken by quality_gate_results addition

**Expected Results**:
- All state management functions work
- New fields coexist with old
- No unexpected side effects
- State integrity preserved

**Time Estimate**: 1.5 hours

---

#### Test 4.1.4: Agent Commands Still Work
**Objective**: Verify existing agent commands unaffected by quality gate integration

**Test Steps**:
1. Test each agent's existing commands:
   - discovery: *ask-questions
   - analyst: *create-project-brief
   - pm: *create-prd
   - architect: *design-architecture
   - prp-creator: *create-prp
2. Verify all commands execute normally
3. Verify new quality gate commands added without breaking old

**Expected Results**:
- All existing commands work
- No command conflicts
- New quality gate commands coexist
- Help output shows both old and new commands

**Time Estimate**: 1 hour

---

### Test Group 4.2: Workflow Execution Consistency (3 scenarios)

#### Test 4.2.1: Health-Check Workflow Still Works
**Objective**: Verify health-check.yaml workflow unaffected

**Test Steps**:
1. Execute health-check workflow
2. Verify all validation steps execute
3. Verify workflow completes successfully
4. Verify no quality gate interference (health-check doesn't use gates)

**Expected Results**:
- Health-check workflow completes normally
- No unexpected quality gate triggers
- Validation steps unchanged
- No performance degradation

**Time Estimate**: 30 minutes

---

#### Test 4.2.2: Brownfield-Enhancement Workflow Still Works
**Objective**: Verify brownfield workflow (Phase 1 deferred) unaffected

**Test Steps**:
1. Execute brownfield-enhancement.yaml workflow
2. Verify workflow phases execute
3. Verify no quality gate triggers (not yet implemented for brownfield)
4. Verify workflow completes normally

**Expected Results**:
- Brownfield workflow unchanged
- No quality gate execution
- No errors from missing quality gate infrastructure
- Workflow completes successfully

**Time Estimate**: 1 hour

---

#### Test 4.2.3: Generic Greenfield Workflow Still Works
**Objective**: Verify greenfield-generic.yaml works alongside greenfield-swift

**Test Steps**:
1. Execute greenfield-generic.yaml workflow
2. Verify quality gates trigger (if implemented)
3. Verify workflow completes successfully
4. Verify no interference between generic and swift workflows

**Expected Results**:
- Generic workflow works correctly
- Quality gates execute if configured
- No workflow cross-contamination
- Both generic and swift workflows supported

**Time Estimate**: 1.5 hours

---

### Test Group 4.3: Performance and Resource Usage (3 scenarios)

#### Test 4.3.1: Quality Gate Execution Time Acceptable
**Objective**: Verify quality gates don't significantly slow workflow

**Test Steps**:
1. Measure workflow execution time without quality gates (YOLO mode)
2. Measure workflow execution time with quality gates (batch mode)
3. Calculate overhead percentage
4. Verify overhead acceptable (<30% increase)

**Expected Results**:
- Quality gate overhead <30%
- Batch mode faster than interactive
- YOLO mode unchanged (gates skipped)
- Overhead justified by quality improvement

**Validation Criteria**:
```bash
# Time measurements
time_without_gates = workflow_duration_yolo
time_with_gates = workflow_duration_batch
overhead = (time_with_gates - time_without_gates) / time_without_gates
assert overhead < 0.30  # Less than 30% overhead
```

**Time Estimate**: 2 hours

---

#### Test 4.3.2: Memory Usage Acceptable
**Objective**: Verify quality gate state doesn't cause memory issues

**Test Steps**:
1. Monitor memory usage during workflow with quality gates
2. Verify workflow.json size remains manageable (<10MB)
3. Verify gate result files don't accumulate excessively
4. Test with 10 sequential workflows

**Expected Results**:
- Memory usage stable across workflows
- workflow.json size grows linearly (not exponentially)
- Gate result files archived or cleaned up
- No memory leaks

**Time Estimate**: 1.5 hours

---

#### Test 4.3.3: File System Impact Acceptable
**Objective**: Verify quality gate files don't overwhelm filesystem

**Test Steps**:
1. Execute 20 workflows with quality gates
2. Count gate result files created: 20 workflows × 5 phases = 100 files
3. Measure total disk usage
4. Verify file cleanup mechanism works (old files archived)

**Expected Results**:
- File count manageable
- Disk usage <100MB for 100 gate result files
- Optional: archive or cleanup old result files
- No filesystem performance degradation

**Time Estimate**: 1 hour

---

## Test Execution Plan

### Phase 1: Critical Path Tests (Week 1)
**Duration**: 8-10 hours
**Focus**: Workflow-level and basic E2E tests

- Test 1.1.1-1.1.4: Quality gate triggering (4 hours)
- Test 1.2.1-1.2.4: Orchestrator respecting gate results (3 hours)
- Test 2.1.1: Complete workflow interactive mode (4 hours)

**Deliverable**: Core functionality validated, critical bugs identified

---

### Phase 2: Comprehensive E2E Tests (Week 2)
**Duration**: 10-12 hours
**Focus**: All operation modes and state persistence

- Test 2.1.2-2.1.3: Batch and YOLO modes (5 hours)
- Test 2.2.1-2.2.3: Phase-specific gate execution (4 hours)
- Test 2.3.1-2.3.3: State persistence (3 hours)

**Deliverable**: All operation modes validated, state management verified

---

### Phase 3: Edge Cases and Robustness (Week 3)
**Duration**: 10-14 hours
**Focus**: Error handling and boundary conditions

- Test 3.1.1-3.1.5: Missing/invalid data (4 hours)
- Test 3.2.1-3.2.5: Boundary conditions (2.5 hours)
- Test 3.3.1-3.3.5: Concurrent execution (4.5 hours)

**Deliverable**: Robust error handling validated, edge cases covered

---

### Phase 4: Regression and Performance (Week 4)
**Duration**: 6-8 hours
**Focus**: Backward compatibility and performance

- Test 4.1.1-4.1.4: Existing workflow compatibility (4.5 hours)
- Test 4.2.1-4.2.3: Workflow execution consistency (3 hours)
- Test 4.3.1-4.3.3: Performance and resource usage (4.5 hours)

**Deliverable**: No regressions, acceptable performance, production-ready

---

## Test Environment Setup

### Required Infrastructure

```yaml
Test Environment:
  - Clean CODEX installation
  - All checklists present: discovery, analyst, pm, architect, prp
  - quality-gate agent configured
  - execute-quality-gate.md task functional
  - State directory: .codex/state/ with proper permissions
  - Test fixtures:
      - Sample project briefs
      - Sample PRDs with epics/stories
      - Sample architectures
      - Sample PRPs

Test Data:
  - test-project-brief.md: Valid project brief for analyst phase
  - test-prd.md: Valid PRD with 3 epics, 12 stories for PM phase
  - test-architecture.md: Valid architecture with all 5 sections
  - test-prp.md: Valid PRP with file refs, URLs, validation commands
  - test-workflow-states/:
      - discovery-complete.json
      - analyst-complete.json
      - pm-complete.json
      - architect-complete.json

Automation Tools:
  - Workflow state generator: create test workflow.json files
  - Quality gate result generator: create test gate result files
  - Validation script: verify gate results format
  - Cleanup script: reset test environment between runs
```

---

## Test Automation Framework

### Utilities to Build

#### 1. Test Fixture Generator
```bash
# .codex/tests/generate-test-fixtures.sh
# Generates valid test data for all phases
generate_test_project_brief() { ... }
generate_test_prd() { ... }
generate_test_architecture() { ... }
generate_test_prp() { ... }
```

#### 2. Workflow State Simulator
```bash
# .codex/tests/simulate-workflow-state.sh
# Creates workflow.json at any phase
simulate_state_at_phase() {
  phase=$1  # discovery, analyst, pm, architect, prp
  # Generate workflow.json with appropriate state
}
```

#### 3. Quality Gate Result Validator
```bash
# .codex/tests/validate-gate-result.sh
# Verifies gate result file format
validate_gate_result() {
  result_file=$1
  # Check required fields present
  # Verify score calculation correct
  # Verify status determination correct
}
```

#### 4. Test Cleanup Script
```bash
# .codex/tests/cleanup-test-env.sh
# Resets environment between test runs
cleanup() {
  rm -f .codex/state/workflow.json
  rm -f .codex/state/quality-gate-*.json
  rm -f docs/project-brief.md docs/prd.md docs/architecture.md
  # Restore clean state
}
```

---

## Success Criteria

### Overall Test Coverage
- [ ] All 46 test scenarios executed
- [ ] 100% pass rate for critical path tests (Category 1 & 2)
- [ ] ≥95% pass rate for edge cases (Category 3)
- [ ] 100% pass rate for regression tests (Category 4)

### Functional Validation
- [ ] Quality gates trigger at all phase transitions
- [ ] Orchestrator respects APPROVED/CONDITIONAL/REJECTED statuses
- [ ] All 3 operation modes work (interactive, batch, YOLO)
- [ ] State persistence works correctly
- [ ] No data corruption under any scenario

### Performance Validation
- [ ] Quality gate overhead <30%
- [ ] Memory usage stable across workflows
- [ ] File system impact manageable
- [ ] No performance regression in existing workflows

### Robustness Validation
- [ ] All edge cases handled gracefully
- [ ] Error messages clear and actionable
- [ ] Recovery mechanisms work
- [ ] No workflow corruption under failure

---

## Risk Assessment and Mitigation

### High Risk Areas

**1. Orchestrator State Management During Gate Execution**
- **Risk**: workflow.json corruption during concurrent updates
- **Mitigation**: Atomic file operations, lock mechanism, validation before/after
- **Test Coverage**: Category 3.3 (5 scenarios)

**2. Phase Transition Logic with Gate Results**
- **Risk**: Incorrect blocking/allowing of transitions
- **Mitigation**: Comprehensive status handling, clear decision tree
- **Test Coverage**: Category 1.2 (4 scenarios)

**3. Backward Compatibility**
- **Risk**: Breaking existing workflows
- **Mitigation**: Migration logic, format detection, graceful degradation
- **Test Coverage**: Category 4.1 (4 scenarios)

### Medium Risk Areas

**4. Quality Gate Scoring Calculation**
- **Risk**: Incorrect score leading to wrong status
- **Mitigation**: Extensive boundary condition testing
- **Test Coverage**: Category 3.2 (5 scenarios)

**5. Evidence Collection in Interactive Mode**
- **Risk**: Users bypassing evidence requirements
- **Mitigation**: Strict validation, clear requirements
- **Test Coverage**: Category 3.1.5

### Low Risk Areas

**6. File Reference Validation**
- **Risk**: False positives/negatives in existence checks
- **Mitigation**: Standard file system calls, clear error messages
- **Test Coverage**: Category 2.2.3

---

## Appendix A: Test Data Templates

### Sample workflow.json at Discovery Complete

```json
{
  "workflow_id": "test-001",
  "workflow_name": "Test Swift iOS App",
  "current_phase": "discovery",
  "operation_mode": "interactive",
  "elicitation_completed": {
    "discovery": true
  },
  "quality_gate_results": {},
  "quality_scores": {},
  "transformation_history": [
    {
      "timestamp": "2025-01-15T10:00:00Z",
      "action": "phase_completed",
      "phase": "discovery",
      "details": "9 questions answered"
    }
  ],
  "violations": []
}
```

### Sample Quality Gate Result File

```json
{
  "phase": "pm",
  "checklist": "pm-quality-gate.md",
  "timestamp": "2025-01-15T14:30:00Z",
  "mode": "batch",
  "overall_status": "APPROVED",
  "overall_score": 92,
  "sections": [
    {
      "section_id": "mvp-scope",
      "section_title": "MVP Scope Definition",
      "items_checked": 15,
      "items_passed": 14,
      "items_failed": 1,
      "evidence": [
        {
          "item": "Essential features clearly distinguished from nice-to-haves",
          "passed": true,
          "evidence": "PRD Section 2.1, lines 45-67: MVP features listed with priority levels",
          "notes": "Clear separation between P0 (MVP) and P1/P2 (future)"
        },
        {
          "item": "Each Epic ties back to specific user needs",
          "passed": false,
          "evidence": "Epic 3 doesn't clearly map to user need",
          "notes": "FAIL: Epic 3 lacks user need justification"
        }
      ]
    }
  ],
  "recommendations": [
    {
      "priority": "medium",
      "action": "Add user need mapping for Epic 3",
      "rationale": "Ensures all development work is user-driven"
    }
  ]
}
```

---

## Appendix B: Validation Commands Reference

### Verify Quality Gate Result Structure
```bash
# Check result file has required fields
required_fields=("phase" "checklist" "timestamp" "mode" "overall_status" "overall_score" "sections")
for field in "${required_fields[@]}"; do
  jq -e ".$field" result.json > /dev/null || echo "Missing $field"
done
```

### Verify Score Calculation
```python
def calculate_expected_score(sections):
    critical_fails = sum(1 for s in sections for e in s['evidence']
                        if not e['passed'] and e.get('is_critical'))
    standard_fails = sum(1 for s in sections for e in s['evidence']
                        if not e['passed'] and not e.get('is_critical'))
    return max(0, 100 - (10 * critical_fails) - (5 * standard_fails))

# Verify actual score matches expected
assert result['overall_score'] == calculate_expected_score(result['sections'])
```

### Verify Status Determination
```python
def determine_expected_status(score):
    if score >= 90:
        return "APPROVED"
    elif score >= 70:
        return "CONDITIONAL"
    else:
        return "REJECTED"

# Verify status correct for score
assert result['overall_status'] == determine_expected_status(result['overall_score'])
```

---

## Document Metadata

**Test Plan Version**: 1.0
**Created**: 2025-10-08
**Author**: AI IDE Agent
**Status**: Design Complete
**Next Steps**:
1. Review test plan with project team
2. Create test tasks in Archon
3. Build test automation framework
4. Execute Phase 1 critical path tests
5. Iterate based on findings

**Related Documents**:
- `/Users/brianpistone/Development/BeardedWonder/CODEX/PRPs/phase-1-critical-quality-foundation.md`
- `/Users/brianpistone/Development/BeardedWonder/CODEX/PRPs/phase-2-feedback-and-quality-enhancement.md`
- `/Users/brianpistone/Development/BeardedWonder/CODEX/.codex/workflows/greenfield-swift.yaml`
- `/Users/brianpistone/Development/BeardedWonder/CODEX/.codex/state/workflow.json.template`

**Estimated Total Testing Effort**: 28-40 hours across 4 weeks
**Critical Path**: 8-10 hours (Week 1)
**Production Readiness**: After all 46 scenarios pass
