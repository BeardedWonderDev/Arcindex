<!-- Powered by CODEX™ Core -->

# PRP Quality Check Task

## Purpose
Systematic validation of enhanced PRP documents to ensure they meet CODEX quality standards and enable one-pass implementation success.

## When to Execute
- After PRP creation by prp-creator agent
- Before handoff to dev agent for implementation
- When validating existing PRPs for quality
- During workflow checkpoint validation

## Task Execution Steps

### Step 1: Zero-Knowledge Validation Test

**The Ultimate Test**: Could a fresh Claude instance with no prior conversation context successfully implement this feature using only:
- The PRP document content
- Access to the codebase (but no guidance on where to look)
- Its general training knowledge

#### Validation Checklist

```yaml
context-completeness:
  - [ ] All referenced workflow documents are summarized in PRP
  - [ ] No implicit knowledge assumptions
  - [ ] All technical decisions explained
  - [ ] Complete implementation path provided

reference-accessibility:
  - [ ] All URLs include section anchors
  - [ ] All file paths are absolute and exist
  - [ ] All patterns point to specific examples
  - [ ] All commands are executable

implementation-clarity:
  - [ ] Tasks have clear dependency order
  - [ ] File names and locations are explicit
  - [ ] Integration points are documented
  - [ ] Validation commands are provided
```

### Step 2: Workflow Context Integration Check

Verify the PRP properly synthesizes all workflow phases:

```yaml
project-brief-integration:
  required_elements:
    - [ ] Business context included
    - [ ] Target users identified
    - [ ] Success metrics defined
    - [ ] Constraints documented
  score: _/4

prd-integration:
  required_elements:
    - [ ] All FRs addressed
    - [ ] All NFRs considered
    - [ ] User stories mapped
    - [ ] Acceptance criteria included
  score: _/4

architecture-integration:
  required_elements:
    - [ ] Technology stack followed
    - [ ] Component structure respected
    - [ ] Patterns identified
    - [ ] Security measures included
  score: _/4

total-integration-score: _/12 (must be ≥11 to pass)
```

### Step 3: Information Density Validation

Check that all information is specific and actionable:

#### Anti-Patterns to Flag
- ❌ "Refer to the documentation" without specific URL
- ❌ "Follow existing patterns" without file reference
- ❌ "Use standard approach" without defining standard
- ❌ "Implement as needed" without specific requirements
- ❌ Generic task descriptions without concrete specs

#### Required Specificity
- ✅ URLs with section anchors: `https://docs.example.com/api#authentication`
- ✅ File patterns with line numbers: `src/services/UserService.swift:45-120`
- ✅ Explicit naming: `Create UserAuthenticationService class`
- ✅ Concrete validation: `Run 'swift test --filter UserAuthTests'`

#### Gold Standard Examples (from /prp-create)

**URLs with section anchors**:
- ❌ `https://docs.fastapi.com`
- ✅ `https://docs.fastapi.com/tutorial/dependencies/#dependencies-with-yield`

**File references with patterns**:
- ❌ "Follow similar pattern in services folder"
- ✅ "FOLLOW pattern: src/services/database_service.py (service structure, error handling on lines 45-89)"

**Task specifications**:
- ❌ "Create the models"
- ✅ "CREATE src/models/auth_models.py - IMPLEMENT: LoginRequest, LoginResponse Pydantic models - NAMING: CamelCase for classes, snake_case for fields"

**Validation commands**:
- ❌ "Run tests"
- ✅ `uv run pytest src/services/tests/test_auth_service.py -v`

### Step 4: Implementation Task Quality

Evaluate each implementation task for:

```yaml
task-quality-criteria:
  dependency-ordering:
    - Tasks in correct sequence
    - Dependencies explicit
    - No circular dependencies

  task-specificity:
    - File path provided
    - Class/function names specified
    - Parameters defined
    - Return types documented

  validation-inclusion:
    - Test approach defined
    - Success criteria clear
    - Error cases covered

  integration-clarity:
    - Connection points identified
    - Data flow documented
    - Error propagation defined
```

### Step 5: Validation Gate Verification

Confirm all four validation levels are properly defined:

```bash
# Level 1: Syntax validation commands exist and work
validation_level_1:
  - Command provided: [YES/NO]
  - Command tested: [YES/NO]
  - Expected output defined: [YES/NO]

# Level 2: Unit test commands and coverage targets
validation_level_2:
  - Test command provided: [YES/NO]
  - Coverage target specified: [YES/NO]
  - Test patterns identified: [YES/NO]

# Level 3: Integration test approach
validation_level_3:
  - Integration tests defined: [YES/NO]
  - Test data provided: [YES/NO]
  - Expected results documented: [YES/NO]

# Level 4: Acceptance criteria validation
validation_level_4:
  - User story validation included: [YES/NO]
  - Performance benchmarks set: [YES/NO]
  - Security checks defined: [YES/NO]
```

### Step 6: Anti-Pattern Detection

Scan for common PRP quality issues:

```yaml
anti-patterns:
  - [ ] Vague requirements ("should be fast")
  - [ ] Missing error handling specs
  - [ ] No rollback/recovery plan
  - [ ] Unclear data models
  - [ ] Missing security considerations
  - [ ] No performance targets
  - [ ] Incomplete test coverage
  - [ ] Missing documentation requirements
```

### Step 7: Scoring and Recommendations

Calculate overall PRP quality score:

```yaml
scoring:
  zero_knowledge_validation: _/25
  workflow_integration: _/12
  information_density: _/20
  task_quality: _/20
  validation_gates: _/12
  anti_pattern_absence: _/11

  total_score: _/100

  grade:
    95-100: "A+ - Ready for one-pass implementation"
    90-94: "A - Minor improvements recommended"
    85-89: "B+ - Some clarification needed"
    80-84: "B - Significant gaps to address"
    Below 80: "FAIL - Requires major revision"
```

### Step 8: Generate Quality Report

Create a quality report with:

1. **Executive Summary**
   - Overall score and grade
   - Implementation readiness assessment
   - Critical issues (if any)

2. **Detailed Findings**
   - Section-by-section analysis
   - Specific improvements needed
   - Missing context identification

3. **Recommendations**
   - Priority fixes required
   - Enhancement suggestions
   - Additional research needed

4. **Validation Results**
   - Commands tested and results
   - File references verified
   - URL accessibility checked

## Output Format

```markdown
# PRP Quality Check Report

**PRP**: [PRP filename]
**Date**: [Current date]
**Overall Score**: [Score]/100 ([Grade])
**Implementation Readiness**: [Ready/Needs Work/Not Ready]

## Critical Issues
[List any blocking issues]

## Validation Results
[Detailed test results]

## Recommendations
[Prioritized improvement list]

## Certification
[ ] This PRP is certified ready for implementation
[ ] This PRP requires revision before implementation
```

## Success Criteria

The PRP passes quality check when:
- Score ≥ 90/100
- Zero-knowledge test passes
- All validation gates defined
- No critical anti-patterns detected
- All references verified accessible

## Common Issues and Fixes

| Issue | Fix |
|-------|-----|
| Vague requirements | Add specific acceptance criteria |
| Missing context | Include workflow document summaries |
| Generic references | Add file paths and line numbers |
| No validation | Define all 4 validation levels |
| Implicit knowledge | Document all assumptions explicitly |

## Task Dependencies

- Requires: Completed PRP document
- Provides: Quality report and certification
- Blocks: Implementation if score < 90

## Execution Time

Estimated: 10-15 minutes for comprehensive check

## Tools Required

- File system access for reference verification
- Command execution for validation testing
- URL checker for documentation links