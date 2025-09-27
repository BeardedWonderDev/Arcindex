<!-- Powered by CODEX™ Core -->

# 4-Level Progressive Validation Gate Task

## ⚠️ CRITICAL QUALITY ASSURANCE NOTICE ⚠️

**THIS IS A SYSTEMATIC QUALITY GATE SYSTEM - ENSURING IMPLEMENTATION SUCCESS**

When this task is invoked:

1. **PROGRESSIVE VALIDATION** - Each level must pass before proceeding to the next
2. **PROJECT-SPECIFIC COMMANDS** - Validation commands are tailored to the specific project and technology stack
3. **ACTIONABLE FEEDBACK** - Failed validations provide specific guidance for resolution
4. **LANGUAGE AGENT COORDINATION** - Level 4 integrates with specialized language agents for domain expertise

**SUCCESS REQUIREMENT:** All 5 levels (0-4) must pass for implementation to be considered complete and ready.

## Validation Level Overview

```yaml
validation_levels:
  level_0:
    name: "Elicitation Validation"
    purpose: "Ensure required elicitation completed before phase progression"
    timing: "At every phase transition"
    blocking: true
    enforcement: "HARD STOP - halt_workflow_immediately if incomplete"

  level_1:
    name: "Syntax & Style Validation"
    purpose: "Immediate feedback on code syntax, formatting, and style compliance"
    timing: "After each file creation/modification"
    blocking: true

  level_2:
    name: "Unit Test Validation"
    purpose: "Component-level functionality and logic verification"
    timing: "After component implementation"
    blocking: true

  level_3:
    name: "Integration Test Validation"
    purpose: "System-level integration and end-to-end functionality"
    timing: "After feature completion"
    blocking: true

  level_4:
    name: "Creative & Domain-Specific Validation"
    purpose: "Language-specific agents and domain expertise validation"
    timing: "Final implementation review"
    blocking: true
```

## Level 0: Elicitation Validation (Highest Priority)

### Purpose: Enforce Required User Interaction

This level validates that all required elicitation has been completed for the current phase before allowing progression to the next phase.

### Validation Checks

1. **Check Operation Mode**:
   - Read `.codex/state/workflow.json` for `operation_mode`
   - If mode is `yolo`, skip elicitation validation (but log)
   - If mode is `batch` or `interactive`, continue validation

2. **Check Phase Requirements**:
   - Read `.codex/config/codex-config.yaml` for `elicitation.phase_requirements`
   - Determine if current phase requires elicitation
   - If not required, pass validation

3. **Check Completion Status**:
   - Read `.codex/state/workflow.json` for `elicitation_completed[current_phase]`
   - If `false` and elicitation required: **HALT WORKFLOW**
   - Display: "⚠️ VIOLATION INDICATOR: Elicitation required for [phase] phase before proceeding"

4. **Check Elicitation History**:
   - Verify `elicitation_history` contains entry for current phase
   - Validate method selected and user response recorded
   - If missing: **HALT WORKFLOW**

### Failure Protocol

When Level 0 fails:
1. **HARD STOP** - Do not proceed to Level 1
2. Log violation to `.codex/debug-log.md`
3. Present elicitation options using `.codex/tasks/advanced-elicitation.md`
4. Update state when elicitation completed
5. Re-run Level 0 validation

### Success Criteria

- Operation mode checked and appropriate action taken
- Elicitation requirements for phase verified
- Completion status confirmed as `true` if required
- History contains valid entry for phase
- Proceed to Level 1

## Level 1: Syntax & Style Validation

### Purpose: Immediate Feedback Loop

Catch syntax errors, formatting issues, and style violations immediately to prevent compound errors.

### Execution Strategy

```yaml
level_1_execution:
  trigger: "after_each_file_creation_or_modification"
  timeout: 300  # seconds (5 minutes)
  required: true

  validation_sequence:
    1_syntax_check:
      - purpose: "Verify code compiles and has no syntax errors"
      - blocking: true

    2_style_check:
      - purpose: "Ensure code follows project style guidelines"
      - blocking: false  # warnings only

    3_format_check:
      - purpose: "Verify consistent code formatting"
      - auto_fix: true  # attempt automatic fixing
```

### Project-Specific Commands

#### Swift Projects
```bash
# Syntax validation
swift build --target {target_name} 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Level 1 FAILED: Swift compilation errors detected"
    echo "Fix syntax errors before proceeding"
    exit 1
fi

# Style validation with SwiftLint
swiftlint --config .swiftlint.yml --reporter json > .codex/state/swiftlint-results.json
if [ $(cat .codex/state/swiftlint-results.json | jq '.[] | select(.severity == "error") | length') -gt 0 ]; then
    echo "❌ Level 1 FAILED: SwiftLint errors detected"
    cat .codex/state/swiftlint-results.json | jq -r '.[] | select(.severity == "error") | "Error: \(.rule) at \(.file):\(.line) - \(.reason)"'
    exit 1
fi

# Format validation
swift-format --lint --recursive Sources/ Tests/ 2>&1
if [ $? -ne 0 ]; then
    echo "⚠️  Level 1 WARNING: Formatting issues detected"
    echo "Running swift-format to fix..."
    swift-format --in-place --recursive Sources/ Tests/
fi

echo "✅ Level 1 PASSED: Syntax and style validation complete"
```

#### Python Projects
```bash
# Syntax validation with Python AST
python -m py_compile $(find src/ -name "*.py") 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Level 1 FAILED: Python syntax errors detected"
    exit 1
fi

# Style validation with ruff
ruff check src/ --format=json > .codex/state/ruff-results.json 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Level 1 FAILED: Ruff style violations detected"
    cat .codex/state/ruff-results.json | jq -r '.[] | "Error: \(.code) in \(.filename):\(.location.row) - \(.message)"'
    exit 1
fi

# Type checking with mypy
mypy src/ --json-report .codex/state/mypy-report 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Level 1 FAILED: Type checking errors detected"
    cat .codex/state/mypy-report/index.txt
    exit 1
fi

echo "✅ Level 1 PASSED: Python syntax and style validation complete"
```

### Results Processing

```yaml
level_1_results:
  success_criteria:
    - compilation_successful: true
    - zero_syntax_errors: true
    - style_compliance: ">= 95%"
    - formatting_consistent: true

  failure_handling:
    syntax_errors:
      - action: "halt_workflow_immediately"
      - guidance: "Fix syntax errors before proceeding to next level"
      - tools: ["ide_error_highlighting", "compiler_output"]

    style_violations:
      - action: "provide_specific_fixes"
      - auto_fix_attempt: true
      - guidance: "Review and apply suggested style improvements"

  reporting:
    - save_results_to: ".codex/state/level-1-validation.json"
    - include_metrics: ["error_count", "warning_count", "files_checked"]
    - provide_actionable_feedback: true
```

## Level 2: Unit Test Validation

### Purpose: Component-Level Verification

Verify individual components work correctly in isolation with comprehensive test coverage.

### Execution Strategy

```yaml
level_2_execution:
  trigger: "after_component_implementation_complete"
  timeout: 600  # seconds (10 minutes)
  required: true

  validation_sequence:
    1_test_discovery:
      - purpose: "Find and validate all test files"
      - verify_test_naming_conventions: true

    2_test_execution:
      - purpose: "Run all unit tests with coverage"
      - parallel_execution: true
      - coverage_threshold: 80

    3_test_results_analysis:
      - purpose: "Analyze test results and coverage gaps"
      - identify_untested_code: true
```

### Project-Specific Commands

#### Swift Projects
```bash
# Test discovery and validation
swift test --list-tests 2>&1 | grep -E "^.+Test" > .codex/state/discovered-tests.txt
if [ ! -s .codex/state/discovered-tests.txt ]; then
    echo "❌ Level 2 FAILED: No tests discovered"
    echo "Create unit tests for all implemented components"
    exit 1
fi

# Execute unit tests with coverage
swift test --enable-code-coverage --parallel 2>&1 | tee .codex/state/test-output.txt
if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "❌ Level 2 FAILED: Unit tests failed"
    grep -A 5 -B 5 "FAILED" .codex/state/test-output.txt
    exit 1
fi

# Coverage analysis
xcrun llvm-cov report \
    .build/debug/*/PackageTests \
    --instr-profile=.build/debug/codecov/default.profdata \
    --format=json > .codex/state/coverage-report.json 2>/dev/null

coverage_percentage=$(cat .codex/state/coverage-report.json | jq -r '.data[0].totals.lines.percent // 0')
if (( $(echo "$coverage_percentage < 80" | bc -l) )); then
    echo "❌ Level 2 FAILED: Test coverage below 80% (actual: ${coverage_percentage}%)"
    echo "Add tests for uncovered code paths"
    exit 1
fi

echo "✅ Level 2 PASSED: Unit tests passed with ${coverage_percentage}% coverage"
```

#### Python Projects
```bash
# Test discovery
python -m pytest --collect-only --quiet 2>&1 | grep "::.*test" > .codex/state/discovered-tests.txt
if [ ! -s .codex/state/discovered-tests.txt ]; then
    echo "❌ Level 2 FAILED: No tests discovered"
    echo "Create unit tests for all implemented components"
    exit 1
fi

# Execute tests with coverage
python -m pytest src/ tests/ \
    --cov=src \
    --cov-report=json:.codex/state/coverage.json \
    --cov-report=term-missing \
    --junit-xml=.codex/state/test-results.xml \
    --tb=short 2>&1 | tee .codex/state/test-output.txt

if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "❌ Level 2 FAILED: Unit tests failed"
    python -c "
import xml.etree.ElementTree as ET
tree = ET.parse('.codex/state/test-results.xml')
for failure in tree.findall('.//failure'):
    print(f'FAILED: {failure.get(\"message\", \"Unknown error\")}')
"
    exit 1
fi

# Coverage validation
coverage_percentage=$(cat .codex/state/coverage.json | jq -r '.totals.percent_covered')
if (( $(echo "$coverage_percentage < 80" | bc -l) )); then
    echo "❌ Level 2 FAILED: Test coverage below 80% (actual: ${coverage_percentage}%)"
    exit 1
fi

echo "✅ Level 2 PASSED: Unit tests passed with ${coverage_percentage}% coverage"
```

### Coverage Gap Analysis

```python
# Generate coverage gap report
def analyze_coverage_gaps(coverage_file, source_directory):
    """
    Analyze test coverage gaps and provide specific guidance
    for improving test coverage.
    """

    with open(coverage_file, 'r') as f:
        coverage_data = json.load(f)

    gaps = []
    for file_path, file_data in coverage_data.get('files', {}).items():
        if file_data['summary']['percent_covered'] < 80:
            uncovered_lines = file_data['missing_lines']
            gaps.append({
                'file': file_path,
                'coverage': file_data['summary']['percent_covered'],
                'missing_lines': uncovered_lines,
                'suggestions': generate_test_suggestions(file_path, uncovered_lines)
            })

    return gaps

def generate_test_suggestions(file_path, missing_lines):
    """Generate specific test suggestions for uncovered code"""
    # Implementation would analyze the code and suggest specific test cases
    pass
```

## Level 3: Integration Test Validation

### Purpose: System-Level Integration

Verify components work together correctly and system behavior meets requirements.

### Execution Strategy

```yaml
level_3_execution:
  trigger: "after_feature_implementation_complete"
  timeout: 1200  # seconds (20 minutes)
  required: true

  validation_sequence:
    1_integration_setup:
      - purpose: "Set up test environment and dependencies"
      - database_setup: true
      - service_mocking: true

    2_end_to_end_testing:
      - purpose: "Test complete user workflows"
      - ui_testing: true
      - api_testing: true

    3_performance_validation:
      - purpose: "Verify performance meets requirements"
      - load_testing: conditional
      - memory_testing: true
```

### Project-Specific Commands

#### Swift iOS Projects
```bash
# iOS Simulator integration tests
xcodebuild test \
    -scheme {scheme_name} \
    -destination 'platform=iOS Simulator,name=iPhone 15' \
    -resultBundlePath .codex/state/ios-test-results \
    2>&1 | tee .codex/state/ios-integration-output.txt

if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "❌ Level 3 FAILED: iOS integration tests failed"
    xcrun xcresulttool get --format json --path .codex/state/ios-test-results.xcresult | \
        jq -r '.issues.testFailureSummaries[]? | "FAILED: \(.testCaseName) - \(.message)"'
    exit 1
fi

# macOS integration tests (if applicable)
if [ -f "Package.swift" ] || [ -n "$MACOS_SCHEME" ]; then
    xcodebuild test \
        -scheme {scheme_name} \
        -destination 'platform=macOS' \
        -resultBundlePath .codex/state/macos-test-results \
        2>&1 | tee .codex/state/macos-integration-output.txt

    if [ ${PIPESTATUS[0]} -ne 0 ]; then
        echo "❌ Level 3 FAILED: macOS integration tests failed"
        exit 1
    fi
fi

# Performance validation
instruments -t "Time Profiler" \
    -D .codex/state/performance-trace.trace \
    .build/debug/{target_name} &
INSTRUMENTS_PID=$!
sleep 10  # Run for 10 seconds
kill $INSTRUMENTS_PID

echo "✅ Level 3 PASSED: Integration tests completed successfully"
```

#### Web Application Projects
```bash
# Start test services
docker-compose -f docker-compose.test.yml up -d
sleep 30  # Wait for services to be ready

# API integration tests
python -m pytest tests/integration/ \
    --api-base-url="http://localhost:8000" \
    --database-url="postgresql://test:test@localhost:5432/test_db" \
    --junit-xml=.codex/state/integration-results.xml \
    2>&1 | tee .codex/state/integration-output.txt

if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "❌ Level 3 FAILED: API integration tests failed"
    docker-compose -f docker-compose.test.yml logs
    docker-compose -f docker-compose.test.yml down
    exit 1
fi

# End-to-end UI tests with Playwright
npx playwright test --reporter=json --output-file=.codex/state/e2e-results.json 2>&1 | \
    tee .codex/state/e2e-output.txt

if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "❌ Level 3 FAILED: End-to-end tests failed"
    cat .codex/state/e2e-results.json | jq -r '.suites[].specs[] | select(.ok == false) | "FAILED: \(.title) - \(.tests[0].results[0].error.message // "Unknown error")"'
    docker-compose -f docker-compose.test.yml down
    exit 1
fi

# Cleanup
docker-compose -f docker-compose.test.yml down

echo "✅ Level 3 PASSED: Integration and E2E tests completed successfully"
```

## Level 4: Creative & Domain-Specific Validation

### Purpose: Language Agent & Expert Review

Leverage specialized language agents and domain expertise for advanced quality assurance.

### Execution Strategy

```yaml
level_4_execution:
  trigger: "after_all_previous_levels_pass"
  timeout: 900  # seconds (15 minutes)
  required: true

  validation_sequence:
    1_language_agent_coordination:
      - purpose: "Coordinate with specialized language agents"
      - parallel_execution: true
      - aggregated_feedback: true

    2_domain_specific_validation:
      - purpose: "Apply domain-specific quality checks"
      - security_validation: true
      - performance_analysis: true
      - architecture_compliance: true

    3_creative_validation:
      - purpose: "Apply creative problem-solving validation"
      - edge_case_analysis: true
      - user_experience_review: true
```

## Level 4: Command-Based Domain Validation

### Purpose: Swift Tooling Validation

Leverage Swift development tools for domain-specific validation without agent coordination complexity.

### Execution Strategy

```yaml
level_4_execution:
  trigger: "after_all_previous_levels_pass"
  timeout: 600  # seconds (10 minutes)
  required: true
  coordination_method: "command_based"  # No agent coordination

  validation_sequence:
    1_release_build_validation:
      - purpose: "Verify release configuration builds successfully"
      - blocking: true

    2_comprehensive_testing:
      - purpose: "Run all tests with coverage in release mode"
      - coverage_threshold: 80
      - blocking: true

    3_style_enforcement:
      - purpose: "Strict style and formatting compliance"
      - auto_fix: false
      - blocking: true

    4_swift_package_validation:
      - purpose: "Validate package structure and dependencies"
      - blocking: true
```

### Command-Based Validation

```bash
# Swift Release Build Validation
swift build --configuration Release -v 2>&1 | tee .codex/state/release-build.log
if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "❌ Level 4 FAILED: Release build failed"
    grep -A 5 -B 5 "error:" .codex/state/release-build.log
    exit 1
fi

# Comprehensive Test Suite with Coverage
swift test --configuration Release --enable-code-coverage --parallel 2>&1 | tee .codex/state/release-tests.log
if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "❌ Level 4 FAILED: Release tests failed"
    exit 1
fi

# Strict Style Enforcement
swiftlint --strict --reporter json --config .swiftlint.yml > .codex/state/strict-lint.json
if [ $(cat .codex/state/strict-lint.json | jq 'length') -gt 0 ]; then
    echo "❌ Level 4 FAILED: Strict linting violations"
    cat .codex/state/strict-lint.json | jq -r '.[] | "VIOLATION: \(.rule) at \(.file):\(.line) - \(.reason)"'
    exit 1
fi

# Swift Package Validation
swift package resolve 2>&1 | tee .codex/state/package-resolve.log
if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "❌ Level 4 FAILED: Package resolution failed"
    exit 1
fi

echo "✅ Level 4 PASSED: Command-based domain validation complete"
```

### Domain-Specific Validation Commands

#### Swift iOS Security Validation
```bash
# OWASP Mobile Top 10 compliance check
echo "Running iOS security validation..."

# 1. Data Storage vulnerabilities
grep -r "UserDefaults\|Keychain\|Core Data" Sources/ > .codex/state/data-storage-check.txt
if grep -q "UserDefaults.*password\|UserDefaults.*token\|UserDefaults.*key" .codex/state/data-storage-check.txt; then
    echo "❌ Level 4 FAILED: Sensitive data stored in UserDefaults"
    exit 1
fi

# 2. Cryptography validation
grep -r "CommonCrypto\|CryptoKit\|Security\.framework" Sources/ > .codex/state/crypto-check.txt
if grep -q "MD5\|SHA1\|DES\|RC4" .codex/state/crypto-check.txt; then
    echo "❌ Level 4 FAILED: Weak cryptographic algorithms detected"
    exit 1
fi

# 3. Network security
grep -r "URLSession\|Alamofire\|HTTP" Sources/ > .codex/state/network-check.txt
if grep -q "http://\|allowsArbitraryLoads.*true" .codex/state/network-check.txt; then
    echo "❌ Level 4 WARNING: Insecure network communication detected"
fi

echo "✅ iOS Security validation passed"
```

#### Performance Validation
```bash
# Memory leak detection with Instruments
echo "Running performance validation..."

# Build for profiling
xcodebuild build \
    -scheme {scheme_name} \
    -configuration Release \
    -destination 'platform=iOS Simulator,name=iPhone 15'

# Memory leak analysis
instruments -t "Leaks" \
    -D .codex/state/leaks-analysis.trace \
    .build/release/{target_name} &
INSTRUMENTS_PID=$!
sleep 30
kill $INSTRUMENTS_PID

# Check for leaks
leaks_count=$(instruments -s .codex/state/leaks-analysis.trace | grep -c "Leak:")
if [ $leaks_count -gt 0 ]; then
    echo "❌ Level 4 FAILED: Memory leaks detected ($leaks_count leaks)"
    instruments -s .codex/state/leaks-analysis.trace | grep "Leak:"
    exit 1
fi

echo "✅ Performance validation passed"
```

### Validation Results Aggregation

```yaml
level_4_results_processing:
  agent_feedback_aggregation:
    - collect_all_agent_reports: true
    - identify_critical_issues: true
    - prioritize_recommendations: true
    - generate_unified_action_plan: true

  validation_scoring:
    critical_issues: "automatic_failure"
    major_issues: "requires_fixes_before_completion"
    minor_issues: "recommendations_for_improvement"

  final_assessment:
    - architecture_compliance: "passed|failed"
    - security_validation: "passed|failed"
    - performance_assessment: "optimized|acceptable|needs_improvement"
    - test_quality: "comprehensive|adequate|insufficient"
    - overall_recommendation: "ready_for_deployment|needs_improvements|major_rework_required"
```

## Validation Results Reporting

### Comprehensive Report Generation

```json
{
  "validation_run_id": "uuid",
  "timestamp": "ISO_timestamp",
  "workflow_id": "workflow_uuid",
  "feature_name": "feature_name",
  "overall_status": "passed|failed",

  "level_results": {
    "level_1": {
      "status": "passed|failed",
      "duration_seconds": 45,
      "checks_performed": ["syntax", "style", "formatting"],
      "errors": [],
      "warnings": ["minor formatting issues"],
      "auto_fixes_applied": 3
    },
    "level_2": {
      "status": "passed|failed",
      "duration_seconds": 120,
      "tests_run": 45,
      "tests_passed": 45,
      "tests_failed": 0,
      "coverage_percentage": 87.5,
      "coverage_gaps": []
    },
    "level_3": {
      "status": "passed|failed",
      "duration_seconds": 300,
      "integration_tests_run": 12,
      "e2e_tests_run": 8,
      "performance_benchmarks": {
        "app_launch_time": "1.2s",
        "memory_usage": "45MB",
        "network_requests": "optimized"
      }
    },
    "level_4": {
      "status": "passed|failed",
      "duration_seconds": 400,
      "language_agents": {
        "swift-performance-reviewer": {
          "status": "passed",
          "recommendations": ["consider caching for network requests"]
        },
        "ios-security-auditor": {
          "status": "passed",
          "compliance": "OWASP_compliant"
        }
      }
    }
  },

  "summary": {
    "total_duration_seconds": 865,
    "critical_issues": 0,
    "major_issues": 0,
    "minor_issues": 2,
    "recommendations": [
      "Consider implementing request caching for improved performance",
      "Add accessibility labels for better VoiceOver support"
    ],
    "next_actions": [
      "Address minor performance optimization suggestions",
      "Implementation ready for production deployment"
    ]
  }
}
```

### Actionable Feedback Generation

```python
def generate_actionable_feedback(validation_results):
    """
    Generate specific, actionable feedback for developers
    based on validation results across all 4 levels.
    """

    feedback = {
        "immediate_actions": [],
        "recommended_improvements": [],
        "future_considerations": []
    }

    # Analyze results and generate specific guidance
    for level, results in validation_results["level_results"].items():
        if results["status"] == "failed":
            feedback["immediate_actions"].extend(
                generate_failure_remediation(level, results)
            )
        elif results.get("warnings"):
            feedback["recommended_improvements"].extend(
                generate_improvement_suggestions(level, results)
            )

    return feedback

def generate_failure_remediation(level, results):
    """Generate specific steps to remediate validation failures"""
    remediation_steps = []

    if level == "level_1" and "syntax" in results["errors"]:
        remediation_steps.append({
            "action": "Fix syntax errors",
            "command": "swift build --target {target}",
            "priority": "critical"
        })

    # Additional remediation logic for other levels...

    return remediation_steps
```

## Integration with CODEX Workflow

### Orchestrator Integration

```yaml
workflow_integration:
  automatic_execution:
    - trigger_after_implementation_phase: true
    - progressive_execution: "level_1_before_level_2"
    - blocking_failures: "halt_workflow_on_critical_failures"

  state_management:
    - save_validation_results: ".codex/state/validation-results.json"
    - track_validation_history: true
    - enable_validation_resumption: true

  agent_coordination:
    - integrate_with_language_agents: true
    - parallel_agent_execution: "level_4_only"
    - aggregate_agent_feedback: true
```

### Success Metrics

```yaml
validation_system_metrics:
  reliability:
    - false_positive_rate: "<5%"
    - false_negative_rate: "<2%"
    - validation_consistency: ">95%"

  efficiency:
    - total_validation_time: "<30_minutes_for_typical_feature"
    - level_1_execution_time: "<5_minutes"
    - parallel_execution_efficiency: ">80%"

  quality_impact:
    - post_validation_defect_rate: "<10%"
    - implementation_success_improvement: ">40%"
    - developer_confidence_increase: ">30%"
```

---

**CRITICAL SUCCESS FACTOR**: The 4-level validation system is the final quality gate ensuring CODEX implementations meet production standards. All levels must pass for workflow completion.