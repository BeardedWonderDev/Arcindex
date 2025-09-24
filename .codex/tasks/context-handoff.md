<!-- Powered by CODEX™ Core -->

# Context Breakpoint Management Task

## ⚠️ CRITICAL CONTEXT MANAGEMENT NOTICE ⚠️

**THIS IS A CONTEXT LIBERATION SYSTEM - ENABLING ZERO PRIOR KNOWLEDGE ARCHITECTURE**

When this task is invoked:

1. **TOKEN LIMIT MONITORING** - Continuously monitor approaching context window limits (40k threshold)
2. **STRATEGIC BREAKPOINT CREATION** - Create checkpoints at workflow phase boundaries, not arbitrary points
3. **ZERO KNOWLEDGE VALIDATION** - Every checkpoint must pass "No Prior Knowledge" test for handoff capability
4. **COMPLETE CONTEXT PRESERVATION** - Essential context must be preserved without loss of implementation capability

**CRITICAL SUCCESS FACTOR:** Fresh Claude instances must be able to continue work seamlessly from any checkpoint.

## Context Breakpoint Detection

### Automatic Trigger Conditions

Monitor for these breakpoint trigger conditions:

```yaml
token_threshold_triggers:
  warning_threshold: 35000  # tokens - begin preparing for breakpoint
  critical_threshold: 40000  # tokens - must create breakpoint before proceeding
  emergency_threshold: 44000  # tokens - immediate breakpoint creation required

workflow_phase_triggers:
  after_project_brief: "pm_can_create_prd_without_analyst_context"
  after_prd: "architect_can_design_without_pm_context"
  after_architecture: "prp_creator_has_complete_technical_context"
  after_enhanced_prp: "dev_agent_can_implement_without_workflow_context"
  after_implementation: "qa_can_validate_without_implementation_context"

context_complexity_triggers:
  codebase_analysis_complete: "patterns_and_gotchas_documented"
  research_synthesis_complete: "external_documentation_integrated"
  validation_strategy_complete: "project_specific_commands_verified"
```

### Manual Trigger Commands

```bash
# Force checkpoint creation
/codex checkpoint create --reason="manual_breakpoint" --validation=required

# Validate checkpoint readiness
/codex checkpoint validate --test="zero_knowledge" --score-threshold=95

# Test handoff capability
/codex checkpoint test --simulate="fresh_claude_instance"
```

## Checkpoint Creation Process

### 1. Context Analysis and Preparation

```yaml
context_analysis:
  current_phase: "identify_current_workflow_phase"
  completed_artifacts: "list_all_generated_documents"
  essential_context: "extract_implementation_critical_information"
  dependency_mapping: "identify_required_context_for_next_phase"

context_compression:
  business_decisions: "summarize_key_business_choices_and_rationale"
  technical_decisions: "document_architecture_choices_and_constraints"
  implementation_guidance: "extract_specific_patterns_and_examples"
  validation_requirements: "compile_project_specific_validation_commands"
```

### 2. Checkpoint Document Creation

Create comprehensive checkpoint summary document:

```markdown
# CODEX Workflow Checkpoint - {timestamp}

## Checkpoint Metadata
- **Workflow ID**: {workflow_uuid}
- **Phase**: {current_phase}
- **Trigger**: {breakpoint_trigger_reason}
- **Token Count**: {approximate_token_count}
- **Validation Score**: {zero_knowledge_test_score}

## Business Context Summary
{essential_business_context_from_project_brief}

## Product Requirements Summary
{key_features_and_acceptance_criteria_from_prd}

## Architecture Decisions Summary
{technical_architecture_choices_and_constraints}

## Implementation Context
{patterns_gotchas_and_specific_guidance_extracted}

## Next Phase Requirements
{complete_context_needed_for_continuation}

## Validation Commands
{project_specific_commands_for_quality_gates}

## Zero Knowledge Handoff Verification
- [ ] Fresh Claude instance can understand business context
- [ ] All technical decisions are documented with rationale
- [ ] Implementation guidance is specific and actionable
- [ ] Validation strategy is executable without prior context
- [ ] File references are complete with patterns and examples
```

### 3. State Persistence

Save checkpoint state to multiple locations:

```json
// .codex/state/context-checkpoints.json
{
  "checkpoint_id": "uuid",
  "workflow_id": "workflow_uuid",
  "timestamp": "ISO_timestamp",
  "phase": "current_workflow_phase",
  "trigger_reason": "token_threshold|phase_boundary|manual",
  "token_count_estimate": 40000,
  "documents": [
    {
      "path": "docs/project-brief.md",
      "role": "business_context",
      "essential_sections": ["problem_statement", "success_criteria"]
    },
    {
      "path": "docs/prd.md",
      "role": "feature_requirements",
      "essential_sections": ["features", "acceptance_criteria"]
    },
    {
      "path": "docs/architecture.md",
      "role": "technical_design",
      "essential_sections": ["patterns", "constraints", "file_structure"]
    }
  ],
  "checkpoint_document": "docs/checkpoints/checkpoint-{timestamp}.md",
  "zero_knowledge_score": 95,
  "validation_status": "passed|failed",
  "continuation_requirements": {
    "next_phase": "prp_creation|implementation|validation",
    "required_context": ["business_goals", "technical_constraints"],
    "agent_handoff": "prp-creator|dev|qa"
  }
}
```

## Zero Knowledge Validation Test

### Comprehensive Validation Criteria

Execute this validation test on every checkpoint:

```yaml
zero_knowledge_test:
  context_completeness:
    - business_problem_clearly_defined: "Can fresh Claude understand the problem?"
    - success_criteria_measurable: "Are success metrics specific and testable?"
    - technical_constraints_documented: "Are all limitations and requirements clear?"
    - implementation_guidance_specific: "Can implementation proceed without guessing?"

  reference_accessibility:
    - all_urls_accessible: "Verify all documentation URLs work and include anchors"
    - file_patterns_valid: "Check all referenced files exist with correct patterns"
    - code_examples_complete: "Ensure examples are runnable and follow project patterns"
    - validation_commands_executable: "Test all validation commands work in project context"

  workflow_continuity:
    - phase_transition_clear: "Is the next phase requirements unambiguous?"
    - agent_handoff_complete: "Does receiving agent have all needed context?"
    - decision_rationale_preserved: "Are all key decisions documented with reasoning?"
    - context_gaps_identified: "Are any missing pieces clearly noted?"

validation_scoring:
  excellent: 95-100  # Ready for handoff
  good: 85-94       # Minor improvements needed
  acceptable: 75-84 # Significant improvements required
  insufficient: <75 # Major rework required - do not proceed
```

### Automated Validation Execution

```bash
# Run zero knowledge validation
python .codex/utils/zero-knowledge-validator.py \
  --checkpoint-file="docs/checkpoints/checkpoint-{timestamp}.md" \
  --workflow-phase="{current_phase}" \
  --score-threshold=95

# Test URL accessibility
python .codex/utils/url-validator.py \
  --document="docs/checkpoints/checkpoint-{timestamp}.md" \
  --check-anchors=true

# Validate file references
python .codex/utils/file-reference-validator.py \
  --checkpoint-file="docs/checkpoints/checkpoint-{timestamp}.md" \
  --project-root="."
```

## Context Recovery and Resumption

### Checkpoint Loading Process

When resuming from checkpoint:

```yaml
recovery_process:
  1_load_checkpoint_state:
    - read: ".codex/state/context-checkpoints.json"
    - identify: "most_recent_checkpoint_for_workflow"
    - validate: "checkpoint_integrity_and_completeness"

  2_context_reconstruction:
    - load_checkpoint_document: "docs/checkpoints/checkpoint-{timestamp}.md"
    - extract_essential_context: "business_technical_implementation_guidance"
    - validate_context_completeness: "zero_knowledge_test_score_check"

  3_workflow_continuation:
    - identify_next_phase: "from_checkpoint_metadata"
    - prepare_agent_handoff: "compile_context_for_receiving_agent"
    - execute_phase_transition: "launch_appropriate_agent_with_context"

resumption_validation:
  - checkpoint_document_readable: true
  - essential_context_extractable: true
  - next_phase_requirements_clear: true
  - agent_handoff_context_complete: true
```

### Fresh Claude Instance Simulation

Test checkpoint quality with simulated fresh instance:

```python
# Simulate fresh Claude instance workflow resumption
def simulate_fresh_claude_resumption(checkpoint_file):
    """
    Test if a fresh Claude instance could successfully continue
    the workflow from this checkpoint without any prior context.
    """

    # Load only the checkpoint document (no conversation history)
    checkpoint_content = read_file(checkpoint_file)

    # Test comprehension without prior context
    comprehension_test = {
        "business_problem_clear": can_understand_problem(checkpoint_content),
        "technical_requirements_actionable": can_implement_features(checkpoint_content),
        "validation_strategy_executable": can_run_validation(checkpoint_content),
        "next_steps_unambiguous": can_determine_next_actions(checkpoint_content)
    }

    # Calculate zero knowledge score
    score = calculate_comprehension_score(comprehension_test)

    return {
        "zero_knowledge_score": score,
        "ready_for_handoff": score >= 95,
        "improvement_areas": identify_gaps(comprehension_test),
        "context_completeness": assess_completeness(checkpoint_content)
    }
```

## Error Recovery and Fallback

### Context Overflow Emergency Procedures

```yaml
emergency_procedures:
  context_overflow_detected:
    - immediate_action: "create_emergency_checkpoint"
    - preservation_strategy: "save_essential_context_only"
    - continuation_method: "manual_context_curation"
    - recovery_guidance: "resume_from_last_successful_checkpoint"

  checkpoint_validation_failure:
    - retry_strategy: "enhance_context_completeness_and_revalidate"
    - escalation_path: "manual_review_and_improvement"
    - fallback_option: "return_to_previous_successful_checkpoint"

  handoff_failure:
    - diagnosis: "identify_missing_context_elements"
    - remediation: "enhance_checkpoint_document_with_missing_context"
    - validation: "re_run_zero_knowledge_test_until_passing"
```

## Integration with CODEX Workflow

### Orchestrator Integration

The context handoff system integrates seamlessly with CODEX orchestrator:

```yaml
orchestrator_integration:
  automatic_monitoring:
    - token_counting: "continuous_monitoring_during_workflow_phases"
    - threshold_alerts: "warning_notifications_at_35k_tokens"
    - breakpoint_triggers: "automatic_checkpoint_creation_at_40k"

  workflow_phase_coordination:
    - phase_boundary_detection: "identify_natural_breakpoint_opportunities"
    - agent_handoff_preparation: "compile_context_for_receiving_agent"
    - validation_execution: "run_zero_knowledge_test_automatically"

  state_management:
    - checkpoint_registry: "maintain_checkpoint_history_and_metadata"
    - recovery_capability: "enable_resumption_from_any_checkpoint"
    - validation_tracking: "monitor_checkpoint_quality_scores"
```

## Success Metrics

```yaml
context_management_success_metrics:
  breakpoint_effectiveness:
    - zero_knowledge_score: "≥95% for all checkpoints"
    - handoff_success_rate: "≥95% for phase transitions"
    - context_preservation: "no_essential_information_loss"

  workflow_continuity:
    - resumption_success_rate: "≥95% from any checkpoint"
    - fresh_instance_capability: "≥90% successful cold starts"
    - implementation_success_maintenance: "no_degradation_in_one_pass_success"

  efficiency_metrics:
    - breakpoint_frequency: "≤3 per workflow for typical features"
    - context_compression_ratio: "≥80% size_reduction_with_preserved_capability"
    - recovery_time: "≤5_minutes_to_resume_from_checkpoint"
```

---

**CRITICAL REMINDER**: The success of CODEX depends entirely on effective context management. Every checkpoint must enable fresh Claude instances to continue work without any loss of implementation capability or quality.