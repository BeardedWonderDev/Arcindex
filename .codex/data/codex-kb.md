<!-- Powered by CODEX™ Core -->

# CODEX Knowledge Base

## System Overview

CODEX (Context-Optimized Development & Execution System) is an orchestration framework that manages AI-assisted software development workflows from concept to validated implementation.

### Core Principles

1. **Context Window Liberation**: Strategic breakpoints prevent token overflow
2. **Zero-Knowledge Architecture**: Each phase produces self-contained documents
3. **Progressive Validation**: 4-level quality gates ensure correctness
4. **Language Agent Coordination**: Specialized agents enhance quality
5. **Workflow Orchestration**: Systematic progression through development phases

## Workflow Patterns

### Greenfield Development Pattern

```yaml
pattern: greenfield-development
phases:
  1_discovery:
    agent: analyst
    creates: project-brief.md
    validates: Business context completeness

  2_requirements:
    agent: pm
    requires: project-brief.md
    creates: prd.md
    validates: Requirements traceability

  3_design:
    agent: architect
    requires: [project-brief.md, prd.md]
    creates: architecture.md
    validates: Technical feasibility

  4_planning:
    agent: prp-creator
    requires: [project-brief.md, prd.md, architecture.md]
    creates: enhanced-prp.md
    validates: Zero-knowledge completeness

  5_implementation:
    agent: dev
    requires: enhanced-prp.md
    creates: Implementation code
    validates: 4-level progressive validation

  6_validation:
    agent: qa
    requires: Implementation artifacts
    creates: Quality certification
    validates: Production readiness
```

### Context Breakpoint Pattern

```yaml
pattern: context-breakpoint
trigger_conditions:
  - token_count > 40000
  - phase_completion
  - error_recovery_needed

breakpoint_actions:
  1. Create checkpoint document
  2. Validate zero-knowledge handoff
  3. Save workflow state
  4. Create resumption instructions
  5. Clear context window

checkpoint_contents:
  - Essential context only
  - Next phase requirements
  - State recovery information
  - Validation results
```

### Validation Gate Pattern

```yaml
pattern: 4-level-validation
levels:
  1_syntax:
    what: Code syntax and style
    when: After each file creation
    tools: [linters, formatters]
    pass_criteria: Zero errors

  2_unit:
    what: Component functionality
    when: After component completion
    tools: [unit test frameworks]
    pass_criteria: ">80% coverage, all tests pass"

  3_integration:
    what: System interactions
    when: After feature completion
    tools: [integration test suites]
    pass_criteria: "All critical paths pass"

  4_domain:
    what: Language-specific quality
    when: Before phase completion
    tools: [language agents]
    pass_criteria: "All agents approve"
```

## Agent Coordination Patterns

### Sequential Coordination

```yaml
pattern: sequential-handoff
use_when: Output of one agent required by next
example: analyst → pm → architect → prp-creator
handoff_mechanism:
  - Document creation
  - State persistence
  - Validation checkpoint
```

### Parallel Coordination

```yaml
pattern: parallel-execution
use_when: Multiple independent validations needed
example: Language agents during validation
execution:
  - Launch via single Task message
  - Agents work independently
  - Results aggregated on completion
```

### Hierarchical Coordination

```yaml
pattern: orchestrator-delegation
use_when: Complex workflow management
example: CODEX orchestrator managing phase agents
structure:
  orchestrator:
    - Parses workflow YAML
    - Manages state
    - Delegates to phase agents
  phase_agents:
    - Execute specific tasks
    - Report completion
    - Create handoff documents
```

## Document Templates

### Zero-Knowledge Document Structure

```markdown
# [Document Type]

## Context Summary
[Everything needed without prior knowledge]

## Inputs Required
[Explicit list of dependencies]

## Outputs Produced
[What this phase creates]

## Validation Criteria
[How to verify completeness]

## Next Steps
[Clear instructions for next phase]
```

### Handoff Document Pattern

```yaml
handoff_document:
  metadata:
    from_phase: [phase name]
    to_phase: [next phase]
    timestamp: [ISO timestamp]

  context:
    completed_work: [Summary of what was done]
    decisions_made: [Key decisions and rationale]

  requirements:
    next_phase_needs: [What next phase requires]
    validation_needed: [What to verify]

  state:
    workflow_state: [Current state JSON]
    recovery_point: [How to resume if interrupted]
```

## Technology-Specific Patterns

### Swift/iOS Development

```yaml
swift_patterns:
  project_structure:
    - Features folder for modularity
    - MVVM or MVC architecture
    - Protocol-oriented design

  validation_commands:
    syntax: "swiftlint --strict"
    format: "swift-format lint --recursive"
    unit_tests: "swift test"
    ui_tests: "xcodebuild test -scheme AppScheme"

  language_agents:
    - swift-feature-developer
    - swift-syntax-reviewer
    - swift-testing-reviewer
    - swift-performance-reviewer
    - ios-security-auditor
```

### Web Development

```yaml
web_patterns:
  project_structure:
    - Component-based architecture
    - Service layer separation
    - State management patterns

  validation_commands:
    syntax: "npm run lint"
    format: "prettier --check"
    unit_tests: "npm test"
    e2e_tests: "npm run test:e2e"

  common_tools:
    - React/Vue/Angular
    - TypeScript
    - Jest/Vitest
    - Cypress/Playwright
```

## Quality Assurance Patterns

### PRP Quality Metrics

```yaml
prp_quality:
  essential_elements:
    - Zero-knowledge validation score > 95%
    - All references verified accessible
    - Implementation tasks dependency-ordered
    - Validation commands tested

  information_density:
    - No generic references
    - All patterns specific
    - URLs with anchors
    - File paths with line numbers
```

### Test Coverage Requirements

```yaml
coverage_standards:
  unit_tests:
    minimum: 80%
    critical_paths: 100%

  integration_tests:
    api_endpoints: 100%
    user_flows: 100%

  edge_cases:
    error_handling: 100%
    boundary_conditions: 100%
```

## Error Recovery Patterns

### Workflow Interruption Recovery

```yaml
recovery_pattern:
  detect_interruption:
    - Check for incomplete state file
    - Verify last checkpoint

  assess_damage:
    - Identify last successful phase
    - Check partial work

  recovery_strategy:
    - Load last checkpoint
    - Validate existing work
    - Resume from safe point
    - Re-run failed validations
```

### Validation Failure Recovery

```yaml
failure_recovery:
  level_1_syntax:
    - Run auto-fix if available
    - Re-validate
    - Report unfixable issues

  level_2_unit:
    - Identify failing tests
    - Fix implementation
    - Re-run test suite

  level_3_integration:
    - Check integration points
    - Verify data flow
    - Fix and re-test

  level_4_domain:
    - Address agent feedback
    - Apply recommendations
    - Request re-validation
```

## Best Practices

### Document Creation

1. **Always include context summary** - Never assume prior knowledge
2. **Use structured formats** - YAML for configuration, Markdown for documentation
3. **Provide examples** - Show don't just tell
4. **Include validation** - How to verify correctness
5. **Document decisions** - Why not just what

### Agent Development

1. **Single responsibility** - Each agent has one clear purpose
2. **Explicit dependencies** - Document all required inputs
3. **Validation first** - Define success criteria upfront
4. **Stateless operation** - Agents shouldn't maintain state between invocations
5. **Clear handoffs** - Document what next agent needs

### Workflow Design

1. **Progressive enhancement** - Each phase builds on previous
2. **Fail fast** - Validate early and often
3. **Checkpoint frequently** - Enable recovery from any point
4. **Parallelize when possible** - Use Task tool for concurrent operations
5. **Document everything** - Decisions, rationale, constraints

## Common Issues and Solutions

### Issue: Token Limit Exceeded

```yaml
problem: Context window overflow during complex workflows
solution:
  - Implement context breakpoints
  - Create checkpoint documents
  - Use strategic summarization
  - Clear unnecessary context
```

### Issue: Incomplete Handoffs

```yaml
problem: Next phase lacks required context
solution:
  - Use zero-knowledge document template
  - Validate handoff completeness
  - Include explicit dependencies
  - Test with fresh context
```

### Issue: Validation Failures

```yaml
problem: Code fails validation gates
solution:
  - Run validations progressively
  - Fix issues at lowest level first
  - Use language agents for guidance
  - Document fixes for future reference
```

## Metrics and Monitoring

### Workflow Metrics

```yaml
success_metrics:
  - One-pass implementation rate > 85%
  - Validation gate pass rate > 90%
  - Context overflow rate < 5%
  - Average completion time per phase

quality_metrics:
  - PRP zero-knowledge score > 95%
  - Test coverage > 80%
  - Documentation completeness 100%
  - Security validation pass rate 100%
```

### Performance Optimization

```yaml
optimization_strategies:
  parallel_execution:
    - Use Task tool for concurrent agents
    - Batch related operations

  context_management:
    - Summarize verbose content
    - Remove redundant information
    - Use references vs. inline content

  caching:
    - Reuse validation results
    - Cache external API responses
    - Store computed patterns
```

## Evolution and Maintenance

### Adding New Workflows

1. Define workflow YAML in `.codex/workflows/`
2. Create required agent specifications
3. Add necessary templates
4. Define validation strategies
5. Test with sample project

### Extending Language Support

1. Create language-specific patterns in KB
2. Define validation commands
3. Identify language agents
4. Add to workflow configurations
5. Test integration

### Version Migration

```yaml
migration_strategy:
  backwards_compatibility:
    - Maintain old workflow support
    - Provide migration tools
    - Document breaking changes

  upgrade_path:
    - Incremental migrations
    - Validation at each step
    - Rollback capability
```

---

## Quick Reference

### Essential Commands

```bash
# Initialize CODEX workflow
/codex start [workflow-type] [project-name]

# Resume interrupted workflow
/codex continue

# Check workflow status
/codex status

# Run validation gates
/codex validate

# Get help
/codex help
```

### Key Files

```yaml
configuration:
  main: .codex/config/codex-config.yaml

workflows:
  directory: .codex/workflows/

agents:
  directory: .codex/agents/

state:
  file: .codex/state/workflow.json

templates:
  directory: .codex/templates/
```

### Success Checklist

- [ ] Workflow initialized successfully
- [ ] All phases completed
- [ ] Validation gates passed
- [ ] Documentation complete
- [ ] Quality certified

---

_This knowledge base is continuously updated based on CODEX usage patterns and lessons learned._