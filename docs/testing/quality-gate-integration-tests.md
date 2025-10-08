# Quality Gate Integration Test Plan

## Overview

This document defines the test plan for validating the quality gate integration into CODEX workflow orchestration system (v0.1.0 Option 2).

## Test Scope

### In Scope
- Quality gate configuration in workflow YAML files
- Quality gate invocation at phase transitions
- Enforcement policy application (strict/conditional/advisory)
- State persistence of quality gate results
- YAML syntax validation
- File reference validation

### Out of Scope
- Quality gate checklist content validation (tested separately)
- Quality gate agent internal logic (tested separately)
- End-to-end workflow execution (tested in Phase 2)

## Critical Path Tests (6-8 hours)

### Test 1: Quality Gate Triggers at Phase Transition

**Objective**: Verify quality gate is invoked at discovery → analyst transition

**Preconditions:**
- greenfield-swift.yaml has quality gate configured for discovery phase
- codex-config.yaml has quality_gates.enabled = true
- codex-config.yaml has quality_gates.phases.discovery = true

**Test Steps:**
1. Initialize workflow with discovery phase complete
2. Set elicitation_completed.discovery = true in workflow.json
3. Trigger phase transition to analyst
4. Observe quality gate invocation

**Expected Results:**
- Quality gate agent spawned with validate-discovery command
- Quality gate validation executes on docs/discovery-notes.md
- Results saved to workflow.json quality_gate_results.discovery

**Pass Criteria:**
✅ Quality gate executes automatically
✅ Correct checklist used (.codex/checklists/discovery-quality-gate.md)
✅ Results persisted to state

---

### Test 2: APPROVED Status Allows Progression (Score 90+)

**Objective**: Verify score ≥90 results in APPROVED status and allows progression

**Preconditions:**
- Quality gates enabled
- Enforcement mode: strict
- Test document with high quality (expected score ≥90)

**Test Steps:**
1. Complete analyst phase with high-quality project-brief.md
2. Trigger quality gate validation
3. Observe quality gate score calculation

**Expected Results:**
- Score ≥90
- Status: APPROVED
- allow_progression: true
- No blocking or warnings

**Pass Criteria:**
✅ Status is APPROVED
✅ Score is 90-100
✅ Phase transition proceeds without intervention

---

### Test 3: REJECTED Status Blocks Progression (Score <70)

**Objective**: Verify score <70 results in REJECTED status and blocks progression (strict mode)

**Preconditions:**
- Quality gates enabled
- Enforcement mode: strict
- Test document with low quality (expected score <70)

**Test Steps:**
1. Complete PM phase with incomplete prd.md (missing sections)
2. Trigger quality gate validation
3. Observe enforcement behavior

**Expected Results:**
- Score <70
- Status: REJECTED
- allow_progression: false
- Workflow halts with error message
- Recommendations displayed

**Pass Criteria:**
✅ Status is REJECTED
✅ Score is 0-69
✅ Workflow does not proceed to next phase
✅ Clear error message and recommendations provided

---

### Test 4: CONDITIONAL Status Prompts User (Score 70-89)

**Objective**: Verify score 70-89 results in CONDITIONAL status with appropriate handling

**Preconditions:**
- Quality gates enabled
- Enforcement mode: conditional
- Test document with moderate quality (expected score 70-89)

**Test Steps:**
1. Complete architect phase with acceptable architecture.md (some gaps)
2. Trigger quality gate validation
3. Observe enforcement behavior

**Expected Results:**
- Score 70-89
- Status: CONDITIONAL
- User prompted for review (conditional mode)
- Recommendations displayed
- User can choose to proceed or improve

**Pass Criteria:**
✅ Status is CONDITIONAL
✅ Score is 70-89
✅ User prompt appears (conditional mode)
✅ Both proceed and improve options work

---

### Test 5: YAML Syntax Validation for All Workflows

**Objective**: Verify all 3 workflow YAML files have valid syntax

**Test Steps:**
1. Run Python YAML parser on greenfield-swift.yaml
2. Run Python YAML parser on greenfield-generic.yaml
3. Run Python YAML parser on brownfield-enhancement.yaml

**Expected Results:**
- All 3 files parse without errors
- No YAML syntax errors reported

**Pass Criteria:**
✅ greenfield-swift.yaml parses successfully
✅ greenfield-generic.yaml parses successfully
✅ brownfield-enhancement.yaml parses successfully

**Test Script:**
```bash
#!/bin/bash
echo "Testing YAML Syntax..."

for workflow in .codex/workflows/greenfield-*.yaml .codex/workflows/brownfield-*.yaml; do
    echo "Testing $workflow..."
    python3 -c "import yaml; yaml.safe_load(open('$workflow'))" && echo "✅ PASS" || echo "❌ FAIL"
done
```

---

### Test 6: State Persistence of Quality Gate Results

**Objective**: Verify quality gate results are saved to workflow.json

**Preconditions:**
- Quality gates enabled
- Workflow in progress

**Test Steps:**
1. Execute quality gate for any phase
2. Read workflow.json after completion
3. Verify quality_gate_results field exists and is populated

**Expected Results:**
- workflow.json contains quality_gate_results object
- Object has entry for executed phase
- Entry contains: score, status, timestamp, recommendations

**Pass Criteria:**
✅ quality_gate_results field exists in workflow.json
✅ Phase entry present with all required fields
✅ Timestamp is valid ISO format
✅ Score is 0-100 integer
✅ Status is APPROVED|CONDITIONAL|REJECTED

**Validation Script:**
```bash
# Check workflow.json structure
jq '.quality_gate_results.discovery | {score, status, timestamp, recommendations}' .codex/state/workflow.json
```

---

## Test Execution Steps

### Setup
1. Clone CODEX repository
2. Ensure all workflow YAML files have quality gate configuration
3. Create test documents with known quality levels (high/medium/low)
4. Enable quality gates in codex-config.yaml

### Execute Tests
1. Run Test 1-4 in sequence (4-5 hours)
2. Run Test 5-6 in parallel (1 hour)
3. Document results in test report

### Validate Results
1. Check all expected behaviors occurred
2. Verify no unexpected errors
3. Confirm state persistence works correctly

### Cleanup
1. Reset workflow.json to initial state
2. Restore codex-config.yaml to default (quality_gates.enabled = false)
3. Archive test documents

## Acceptance Criteria

### Must-Have (All Must Pass)
- ✅ Test 1: Quality gate triggers automatically
- ✅ Test 2: APPROVED status allows progression
- ✅ Test 3: REJECTED status blocks progression
- ✅ Test 4: CONDITIONAL status prompts user
- ✅ Test 5: All YAML files parse without errors
- ✅ Test 6: State persists correctly

### Quality Metrics
- **Scoring Formula**: 100 - (10 × critical_failures) - (5 × standard_failures)
- **Critical Failures**: Tests 1, 3, 5
- **Standard Failures**: Tests 2, 4, 6
- **Pass Threshold**: ≥80/100

### Status Thresholds
- **APPROVED** (≥90): All critical tests pass, max 1 standard failure
- **CONDITIONAL** (70-89): All critical tests pass, 2-3 standard failures
- **REJECTED** (<70): Any critical test failure

## Test Report Template

```markdown
# Quality Gate Integration Test Report

**Date**: [date]
**Tester**: [name]
**CODEX Version**: v0.1.0 (Option 2)

## Test Results Summary

| Test | Status | Score | Notes |
|------|--------|-------|-------|
| Test 1: Phase Transition Trigger | PASS/FAIL | - | [notes] |
| Test 2: APPROVED Status | PASS/FAIL | - | [notes] |
| Test 3: REJECTED Status | PASS/FAIL | - | [notes] |
| Test 4: CONDITIONAL Status | PASS/FAIL | - | [notes] |
| Test 5: YAML Syntax | PASS/FAIL | - | [notes] |
| Test 6: State Persistence | PASS/FAIL | - | [notes] |

**Overall Score**: [score]/100
**Overall Status**: APPROVED | CONDITIONAL | REJECTED

## Issues Identified

1. [Issue description]
   - Severity: Critical | Standard | Minor
   - Recommendation: [fix recommendation]

## Recommendations

1. [Recommendation 1]
2. [Recommendation 2]

## Next Steps

- [ ] Address critical issues
- [ ] Review conditional findings
- [ ] Proceed to Phase 4 testing (if APPROVED/CONDITIONAL)
```

## Extended Test Scenarios (Future Phases)

For comprehensive testing beyond critical path (Phase 2+):

### Configuration Tests
- Test 7: Quality gates disabled globally
- Test 8: Quality gates disabled per-phase
- Test 9: Invalid configuration handling

### Enforcement Mode Tests
- Test 10: Strict mode enforcement
- Test 11: Conditional mode with user bypass
- Test 12: Advisory mode (no blocking)

### Edge Case Tests
- Test 13: Missing checklist file handling
- Test 14: Corrupted quality gate results handling
- Test 15: Timeout handling for long-running validations

### Integration Tests
- Test 16: Orchestrator integration end-to-end
- Test 17: Multi-phase workflow with quality gates
- Test 18: Brownfield workflow with skip_items

### Performance Tests
- Test 19: Quality gate execution time (<2 minutes)
- Test 20: Parallel quality gate execution (if applicable)

## Notes

- This test plan focuses on critical path for Option 2 implementation (40-50 hours)
- Extended scenarios available for Phase 2+ comprehensive validation
- Tests should be executed in order to ensure dependencies are met
- All tests assume quality gates infrastructure exists (checklists, agent, execution task)

## References

- Quality gate checklists: `.codex/checklists/*-quality-gate.md`
- Quality gate agent: `.codex/agents/quality-gate.md`
- Execution task: `.codex/tasks/execute-quality-gate.md`
- Workflow files: `.codex/workflows/*.yaml`
- Configuration: `.codex/config/codex-config.yaml`
