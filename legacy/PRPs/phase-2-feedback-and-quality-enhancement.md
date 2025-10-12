name: "Phase 2: Feedback Mechanisms & Quality Enhancement Implementation"
description: |

---

## Goal

**Feature Goal**: Implement iterative feedback loops, PRP quality enforcement, failure escalation protocols, and QA infrastructure to transform CODEX from a one-way pipeline to a quality-assured, feedback-driven development workflow.

**Deliverable**: Complete Phase 2 (Weeks 4-5) implementation including:
- Week 4: Feedback request protocol, PRP validation enforcement, failure escalation, epic-based workflow updates (24-38 hours)
- Week 5: QA reviewer enhancements, execution learning capture, architect validation infrastructure (18-23 hours)

**Success Definition**:
- All agents can request and provide feedback bi-directionally (PM↔Architect, PRP↔Execution)
- PRP validation enforced with verification logs before execution
- 4-level failure escalation protocol operational
- Epic-based incremental workflow implemented (architecture & PRPs per-epic)
- Enhanced QA review capabilities operational
- Execution learnings captured and fed back to PRP creation
- Architect validation infrastructure complete (zero-knowledge test, confidence scoring, handoff tasks)

## User Persona (if applicable)

**Target User**: CODEX workflow orchestrator and individual agents (PM, Architect, PRP Creator, QA, Dev)

**Use Case**: Enable agents to request clarification, provide feedback, escalate failures, and iteratively improve documents based on downstream insights

**User Journey**:
1. Agent encounters ambiguity or issue in upstream document
2. Agent invokes feedback request with specific context
3. Workflow updates with feedback status
4. Upstream agent notified and resolves feedback
5. Updated document flows back to requesting agent
6. Implementation proceeds with improved context
7. Execution learnings captured and fed to next epic's PRP creation

**Pain Points Addressed**:
- One-way pipeline with no refinement path (assumption of perfection)
- Missing PRP validation causes downstream failures
- No systematic failure handling leading to workflow abandonment
- All documentation created upfront with no progressive learning
- QA has limited review capabilities
- No mechanism to capture and apply execution learnings

## Why

- **Business Value**: 670-823% ROI through reduced rework (17-21 hours saved per project), 90% reduction in incomplete handoffs, 40-50% PRD quality improvement
- **Integration with Existing Features**: Builds on Phase 1 quality gates and validation infrastructure, enhances existing agent capabilities
- **Problems This Solves**:
  - Eliminates assumption of perfection model
  - Enables iterative refinement cycles (BMAD's key advantage)
  - Prevents PRP execution failures through validation
  - Provides systematic failure handling and recovery
  - Enables progressive learning through epic-based creation
  - Captures and applies implementation insights to future work

## What

Implement comprehensive feedback and quality enhancement infrastructure across CODEX workflow:

### Week 4 Deliverables:

1. **Feedback Request Protocol (8-10h)**
   - Bi-directional feedback between PM↔Architect
   - Execution feedback to PRP Creator
   - Workflow.json feedback tracking
   - Agent commands: `*request-feedback`, `*resolve-feedback`, `*update`

2. **PRP Validation Command Enforcement (6-10h)**
   - Phase 0 pre-flight validation gate
   - Verification log requirement (PRPs must prove commands tested)
   - File reference existence checks
   - URL validation and accessibility checks
   - Validation command execution verification

3. **PRP Failure Escalation Protocol (6-10h)**
   - Level 1 (0-3 failures): Automatic retry with context
   - Level 2 (4-6 failures): Pattern analysis and adjustment
   - Level 3 (7+ or 3x same error): User intervention request
   - Level 4: Abort with checkpoint and recovery options

4. **Epic-Based Workflow Updates (4-8h)**
   - Update workflow definitions for per-epic architecture creation
   - Update workflow definitions for per-epic PRP creation
   - Just-in-time creation pattern (only create what's next)
   - Epic learning feedback loop integration

### Week 5 Deliverables:

5. **QA Reviewer Agent Enhancements (12-15h)**
   - Enhanced review capabilities beyond current implementation
   - Comprehensive test architecture review
   - Risk-based review depth adaptation
   - Active refactoring authority
   - NFR validation (security, performance, reliability, maintainability)

6. **Execution Learning Capture System (included in Week 4)**
   - Execution report generation (`prp-execution-report-{feature}.json`)
   - Track: validation results, attempts, PRP issues, working patterns
   - Post-execution report with improvement recommendations
   - Feed learnings to next epic's PRP creation

7. **Architect Validation Infrastructure (3-4h)**
   - Zero-knowledge test implementation (1h)
   - Confidence scoring system (1h)
   - Enhanced handoff task creation (1-2h)
   - PRP creation guidance in architecture documents

### Success Criteria

- [ ] PM can request feedback from Architect with specific context
- [ ] Architect can request feedback from PM on unclear requirements
- [ ] PRP Creator receives execution feedback and applies to next epic
- [ ] workflow.json tracks all feedback requests with status
- [ ] PRP pre-flight validation rejects PRPs scoring <90
- [ ] All file references verified to exist before PRP execution
- [ ] All URLs validated and accessible
- [ ] Validation commands proven executable with verification log
- [ ] Failure escalation handles 0-3 failures automatically
- [ ] Pattern analysis activates at 4-6 failures
- [ ] User intervention requested at 7+ failures or 3x same error
- [ ] Epic-based architecture creation implemented (Epic 1 only, then Epic 2 after implementation)
- [ ] Epic-based PRP creation implemented (just-in-time, per-epic)
- [ ] QA agent performs comprehensive test architecture review
- [ ] QA agent can perform active refactoring
- [ ] Execution reports capture all validation attempts and issues
- [ ] Zero-knowledge test validates architecture completeness
- [ ] Confidence scoring quantifies architecture quality (0-100)
- [ ] Handoff tasks provide clear PRP creation guidance

## All Needed Context

### Context Completeness Check

_"If someone knew nothing about this codebase, would they have everything needed to implement this successfully?"_

**Yes** - This PRP includes:
- Complete gap analysis from bmad-vs-codex-comprehensive-analysis.md
- Exact file paths and patterns from .bmad-core reference implementation
- Specific CODEX patterns and conventions from codebase analysis
- Implementation details from BMAD's proven feedback mechanisms
- Clear task structures following CODEX task pattern

### Documentation & References

```yaml
# MUST READ - Core Analysis and Requirements
- file: docs/v0.1-Plan/bmad-vs-codex-comprehensive-analysis.md
  why: Complete gap analysis with all Phase 2 requirements, effort estimates, implementation details
  critical: Lines 3451-3466 (Phase 2 specification), Lines 2333-2390 (Feedback request protocol), Lines 2477-2503 (PRP validation and escalation)
  pattern: Extract exact gap numbers (GAP-PM-6, GAP-PRP-2.1, GAP-PRP-4.1, GAP-PRP-6.2) for implementation specs

# BMAD Reference Implementation - Feedback & Review Patterns
- file: .bmad-core/tasks/review-story.md
  why: BMAD's comprehensive QA review workflow pattern
  pattern: Risk-based review depth, comprehensive analysis categories, gate decision criteria
  gotcha: QA only updates "QA Results" section of story files, never modifies other sections

- file: .bmad-core/agents/qa.md
  why: QA agent persona and command structure
  pattern: Agent activation instructions, command definitions, dependency management
  critical: story-file-permissions restrict QA to only updating QA Results section

- file: .bmad-core/agents/po.md
  why: Product Owner validation layer and cross-functional review
  pattern: Guardian of quality principles, validation commands, collaborative approach

- file: .bmad-core/agents/pm.md
  why: PM agent structure for feedback capability enhancement
  pattern: Command structure, task execution, elicitation methods

- file: .bmad-core/agents/architect.md
  why: Architect agent structure for feedback request capability
  pattern: Research commands, documentation creation, checklist execution

# CODEX Current Implementation - Extension Points
- file: .codex/agents/orchestrator.md
  why: Orchestrator controls workflow progression and agent coordination
  pattern: Agent spawning, workflow state management, phase transitions
  gotcha: Orchestrator must maintain workflow.json state integrity during feedback cycles

- file: .codex/agents/pm.md
  why: PM agent to enhance with feedback resolution commands
  pattern: Current command structure at lines 54-66, persona at lines 40-52
  critical: Add `*update` and `*resolve-feedback` commands following existing pattern

- file: .codex/agents/architect.md
  why: Architect agent to enhance with feedback request capability
  pattern: Current command structure, research capabilities
  critical: Add `*request-feedback` command for upstream clarification

- file: .codex/agents/prp-creator.md
  why: PRP creator to enhance with execution feedback integration
  pattern: Current PRP creation workflow, validation patterns
  critical: Add execution learnings review before creating next epic's PRPs

- file: .codex/agents/qa.md
  why: Existing QA agent to enhance with comprehensive review capabilities
  pattern: Current review workflow, validation gates
  critical: Enhance with BMAD's test architecture review depth

- file: .codex/tasks/state-manager.md
  why: State management patterns for feedback request tracking
  pattern: workflow.json update operations, state validation
  critical: Add feedback_requests array to workflow.json structure

- file: .codex/tasks/validation-gate.md
  why: Existing validation gate pattern to extend for PRP pre-flight
  pattern: Evidence-based validation, scoring rubric, gate decision criteria
  critical: Lines 1-100 show validation structure to adapt for PRP validation

- file: .codex/tasks/execute-quality-gate.md
  why: Quality gate execution pattern for checklist-based validation
  pattern: Systematic validation approach, evidence collection, scoring
  critical: Pattern for executing architect validation checklist

- file: .codex/checklists/prp-quality-gate.md
  why: Existing PRP quality validation checklist (50+ items)
  pattern: Context completeness check, file reference verification, validation command testing
  critical: Use as basis for pre-flight validation gate

- file: .codex/checklists/architect-quality-gate.md
  why: Architect validation checklist (169 items) for handoff validation
  pattern: 9 categories including frontend architecture, testing strategy, AI suitability
  critical: Use for zero-knowledge test and confidence scoring

- file: .codex/templates/architecture-template.yaml
  why: Architecture template to enhance with PRP creation guidance
  pattern: Section structure, elicitation requirements
  critical: Add PRP creation guidance section at end (Component 5 from gap analysis)

- file: .codex/state/workflow.json.template
  why: Workflow state structure to extend for feedback tracking
  pattern: Current state fields, elicitation tracking, phase transitions
  critical: Add feedback_requests array, execution_reports array, epic_learning array

# Implementation Patterns from Current Codebase
- file: .codex/tasks/create-doc.md
  why: Standard task structure pattern for new tasks
  pattern: YAML inputs section, elicitation requirements, step-by-step workflow
  critical: Follow this structure for request-feedback.md, prp-validation-enforcement.md, failure-escalation.md

- file: .codex/tasks/persist-discovery-summary.md
  why: Pattern for persisting findings to filesystem and workflow.json
  pattern: File creation, workflow.json updates, template usage
  critical: Use same pattern for execution report persistence

- file: .codex/workflows/greenfield-generic.yaml
  why: Workflow definition structure for epic-based updates
  pattern: Phase definitions, agent assignments, validation gates
  critical: Update phases to support per-epic architecture and PRP creation
```

### Current Codebase Tree

```bash
.codex/
├── agents/              # Agent persona definitions
│   ├── analyst.md
│   ├── architect.md    # ENHANCE: Add *request-feedback command
│   ├── dev.md
│   ├── discovery.md
│   ├── orchestrator.md # ENHANCE: Add feedback routing logic
│   ├── pm.md          # ENHANCE: Add *update and *resolve-feedback commands
│   ├── prp-creator.md # ENHANCE: Add execution learnings integration
│   ├── qa.md          # ENHANCE: Add comprehensive review capabilities
│   └── quality-gate.md
├── checklists/         # Quality validation checklists
│   ├── analyst-quality-gate.md
│   ├── architect-quality-gate.md  # USE: For zero-knowledge test
│   ├── discovery-quality-gate.md
│   ├── pm-quality-gate.md
│   └── prp-quality-gate.md        # USE: For PRP pre-flight validation
├── config/
│   └── codex-config.yaml
├── data/              # Knowledge base and protocols
│   ├── codex-kb.md
│   ├── elicitation-methods.md
│   ├── quality-scoring-rubric.md
│   ├── template-variable-extraction-protocol.md
│   └── vertical-slice-pattern.md
├── state/
│   └── workflow.json.template     # ENHANCE: Add feedback tracking fields
├── tasks/             # Executable workflow tasks
│   ├── advanced-elicitation.md
│   ├── context-handoff.md
│   ├── create-doc.md
│   ├── execute-quality-gate.md
│   ├── persist-discovery-summary.md
│   ├── prp-quality-check.md
│   ├── state-manager.md
│   ├── validate-phase.md
│   └── validation-gate.md
├── templates/         # Document templates
│   ├── architecture-template.yaml  # ENHANCE: Add PRP guidance section
│   ├── prd-template.yaml
│   ├── project-brief-template.yaml
│   └── prp-enhanced-template.md
└── workflows/         # Workflow definitions
    ├── brownfield-enhancement.yaml
    ├── greenfield-generic.yaml     # ENHANCE: Epic-based phases
    ├── greenfield-swift.yaml       # ENHANCE: Epic-based phases
    └── health-check.yaml

PRPs/                  # Product Requirement Prompts
└── templates/
    └── prp_base.md   # Base template structure
```

### Desired Codebase Tree with Files to be Added

```bash
.codex/
├── tasks/
│   ├── request-feedback.md          # NEW: Feedback request protocol
│   ├── prp-validation-enforcement.md # NEW: PRP pre-flight validation
│   ├── failure-escalation.md         # NEW: 4-level escalation protocol
│   ├── capture-execution-learnings.md # NEW: Execution report generation
│   └── epic-learning-integration.md  # NEW: Apply learnings to next epic
├── data/
│   └── feedback-request-template.yaml # NEW: Feedback request structure
└── state/
    ├── execution-reports/            # NEW: Directory for execution reports
    └── epic-learnings/               # NEW: Directory for epic learnings

Files to ENHANCE (not create):
- .codex/agents/pm.md                 # Add *update, *resolve-feedback commands
- .codex/agents/architect.md          # Add *request-feedback command
- .codex/agents/orchestrator.md       # Add feedback routing logic
- .codex/agents/prp-creator.md        # Add execution learnings review
- .codex/agents/qa.md                 # Add comprehensive review capabilities
- .codex/templates/architecture-template.yaml  # Add PRP creation guidance
- .codex/state/workflow.json.template # Add feedback_requests, execution_reports arrays
- .codex/workflows/greenfield-generic.yaml     # Epic-based phase structure
- .codex/workflows/greenfield-swift.yaml       # Epic-based phase structure
```

### Known Gotchas of our codebase & Library Quirks

```yaml
# CRITICAL: State Management
- workflow.json is runtime state - must be maintained in memory and filesystem
- All state updates MUST update both in-memory state and file
- State corruption causes workflow failure - validate before and after updates
- Feedback cycles must not break phase progression logic

# CRITICAL: Agent Command Patterns
- All commands require * prefix (e.g., *request-feedback)
- Commands defined in agent YAML under 'commands' section
- Agent activation follows strict pattern: Read file → Adopt persona → Load config → Greet → Run *help
- Tasks are loaded ONLY when user requests execution, not during activation

# CRITICAL: Elicitation Requirements
- Tasks with elicit=true REQUIRE user interaction - cannot be bypassed
- Menu format is "1-9" (not "0-8+9") - consistency critical
- Operation modes affect elicitation: interactive (section-by-section), batch (draft all then elicit), yolo (skip elicitation)

# CRITICAL: Quality Gate Patterns
- Gates use 0-100 scoring: quality_score = 100 - (20*FAILs) - (10*CONCERNS)
- Gate decisions: PASS (all met), CONCERNS (non-critical issues), FAIL (blocking issues), WAIVED (explicit override)
- Evidence-based validation required - no subjective "looks good"
- Gate files saved to specific locations defined in workflow

# CRITICAL: Epic-Based Workflow
- Architecture created ONLY for current epic (not entire project)
- PRPs created just-in-time (Epic 1 first, then Epic 2 after Epic 1 implementation)
- Epic learnings feed forward (Epic 1 insights improve Epic 2 artifacts)
- Context window pressure reduced by epic-scoping

# CRITICAL: Feedback Cycle Constraints
- Max 3 iterations per phase pair
- If max exceeded → escalate to user intervention
- Feedback must include: from_agent, to_agent, issue description, context reference, status
- Orchestrator routes feedback, doesn't resolve it

# CRITICAL: PRP Validation
- Pre-flight validation MUST score ≥90 to proceed
- All file references must exist and be readable
- All URLs must be accessible (HTTP 200)
- All validation commands must be executable and proven with verification log
- Validation failures HALT execution with specific remediation guidance

# CRITICAL: Failure Escalation Levels
- Level 1 (0-3 failures): Automatic retry with enhanced context
- Level 2 (4-6 failures): Pattern analysis, strategy adjustment
- Level 3 (7+ failures OR 3x same error): User intervention required
- Level 4: Abort with checkpoint, provide recovery options
- Must track: failure count, failure types, patterns, attempted solutions

# CRITICAL: QA Review Permissions
- QA can ONLY update "QA Results" section of story/document files
- QA can perform refactoring but must document all changes
- QA cannot modify: Status, Story, Acceptance Criteria, Tasks, Dev Notes, other sections
- QA creates separate gate file, doesn't embed gate in story file
```

## Implementation Blueprint

### Phase Sequence and Dependencies

```yaml
# Week 4 must complete before Week 5
# Within each week, tasks have dependencies:

Week 4 Sequence:
  1. Create feedback-request-template.yaml (1h) - No dependencies
  2. Create request-feedback.md task (3-4h) - Depends on template
  3. Update PM agent with feedback commands (2-3h) - Depends on task
  4. Update Architect agent with feedback command (2-3h) - Depends on task
  5. Update Orchestrator with routing logic (3-4h) - Depends on agent updates
  6. Create prp-validation-enforcement.md task (3-4h) - No dependencies
  7. Enhance PRP pre-flight with enforcement (3-4h) - Depends on task
  8. Create failure-escalation.md task (3-4h) - No dependencies
  9. Integrate escalation into dev/execution workflow (3-4h) - Depends on task
  10. Update workflow definitions for epic-based (4-8h) - Can run parallel

Week 5 Sequence:
  1. Create capture-execution-learnings.md task (4-6h) - No dependencies
  2. Enhance dev agent with learning capture (3-4h) - Depends on task
  3. Create epic-learning-integration.md task (3-4h) - No dependencies
  4. Enhance PRP creator with learning review (3-4h) - Depends on task
  5. Enhance QA agent with BMAD review depth (4-6h) - Can run parallel
  6. Create zero-knowledge test task (1h) - No dependencies
  7. Create confidence scoring task (1h) - No dependencies
  8. Enhance architecture template with PRP guidance (1-2h) - No dependencies
```

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: CREATE .codex/data/feedback-request-template.yaml
  - IMPLEMENT: Feedback request data structure
  - STRUCTURE:
      id: "fb-{timestamp}"
      from_agent: "agent_id"
      to_agent: "agent_id"
      issue: "Description of ambiguity/issue"
      context:
        document: "file_path"
        section: "section_name"
        line_refs: [line_numbers]
      status: "pending|in_progress|resolved|closed"
      priority: "high|medium|low"
      created_at: "ISO-8601"
      resolved_at: "ISO-8601|null"
      resolution: "Description of how resolved"
  - NAMING: feedback-request-template.yaml
  - PLACEMENT: .codex/data/

Task 2: CREATE .codex/tasks/request-feedback.md
  - IMPLEMENT: Feedback request protocol task
  - FOLLOW pattern: .codex/tasks/create-doc.md (task structure, inputs section, workflow steps)
  - SECTIONS:
      - Inputs: from_agent, to_agent, issue, context
      - Prerequisites: Document exists, specific issue identified
      - Workflow Steps:
        1. Validate feedback request (all required fields present)
        2. Generate feedback ID from template
        3. Update workflow.json feedback_requests array
        4. Create feedback context package for target agent
        5. Log feedback creation in transformation_history
      - Outputs: Updated workflow.json, feedback context file
  - NAMING: request-feedback.md
  - DEPENDENCIES: feedback-request-template.yaml
  - PLACEMENT: .codex/tasks/

Task 3: MODIFY .codex/agents/pm.md
  - IMPLEMENT: Add feedback resolution commands
  - FOLLOW pattern: Existing commands section lines 54-66
  - ADD commands (in commands YAML block):
      - update {document}: Execute task to update document based on feedback
      - resolve-feedback {feedback_id}: Mark feedback as resolved with resolution notes
  - ADD to dependencies.tasks:
      - request-feedback.md
  - PRESERVE: All existing commands, persona definition, activation instructions
  - CRITICAL: Maintain YAML structure integrity

Task 4: MODIFY .codex/agents/architect.md
  - IMPLEMENT: Add feedback request command
  - FOLLOW pattern: Existing commands section
  - ADD commands (in commands YAML block):
      - request-feedback {to_agent} {issue}: Execute request-feedback task with context
  - ADD to dependencies.tasks:
      - request-feedback.md
  - PRESERVE: All existing commands, persona, research capabilities
  - CRITICAL: Maintain YAML structure integrity

Task 5: MODIFY .codex/agents/orchestrator.md
  - IMPLEMENT: Feedback routing logic
  - FIND pattern: Agent spawning logic (existing coordination patterns)
  - ADD: Feedback request detection and routing
  - LOGIC:
      1. Monitor workflow.json feedback_requests array
      2. When new feedback with status=pending detected:
         a. Identify target agent from to_agent field
         b. Prepare feedback context package
         c. Spawn target agent with feedback context
         d. Update feedback status to in_progress
      3. When feedback resolved:
         a. Update feedback status to resolved
         b. Notify originating agent
         c. Resume workflow from interruption point
  - PRESERVE: Existing phase transition logic, state management
  - PLACEMENT: Add new section "Feedback Coordination" after existing agent coordination

Task 6: CREATE .codex/tasks/prp-validation-enforcement.md
  - IMPLEMENT: PRP pre-flight validation gate
  - FOLLOW pattern: .codex/tasks/execute-quality-gate.md (validation execution structure)
  - SECTIONS:
      - Inputs: prp_file_path
      - Validation Steps:
        1. Execute prp-quality-check.md to get score
        2. HALT if score < 90 with detailed failure report
        3. Verify all file references exist (Read tool test each)
        4. Verify all URLs accessible (simple HTTP check or note for user)
        5. Parse validation commands from PRP
        6. Require verification log section proving commands tested
        7. Generate validation report
      - Output: PASS (score ≥90, all verified) or FAIL (detailed remediation)
      - Remediation Guidance:
          - Score < 90: List specific checklist failures
          - File missing: Exact paths that don't exist
          - URL broken: Which URLs failed and status
          - Commands unverified: Missing verification log section
  - NAMING: prp-validation-enforcement.md
  - PLACEMENT: .codex/tasks/

Task 7: MODIFY .codex/agents/prp-creator.md
  - IMPLEMENT: Integrate validation enforcement in workflow
  - FIND: PRP creation completion point
  - ADD: Before marking PRP complete:
      1. Auto-execute prp-validation-enforcement.md on created PRP
      2. If validation FAILS:
         a. Present detailed remediation to user
         b. Offer to fix automatically where possible
         c. Re-validate after fixes
      3. If validation PASSES:
         a. Mark PRP as validated in workflow.json
         b. Proceed to next phase
  - PRESERVE: Existing PRP creation logic, research workflow

Task 8: CREATE .codex/tasks/failure-escalation.md
  - IMPLEMENT: 4-level failure escalation protocol
  - FOLLOW pattern: .codex/tasks/state-manager.md (state update patterns)
  - STRUCTURE:
      - Inputs: failure_context (type, message, attempted_solution, validation_level)
      - Escalation Logic:
        Level 1 (failure_count 0-3):
          - Action: Automatic retry with enhanced context
          - Context enhancement: Add related documentation, example patterns
          - Log: Failure details, enhancement applied
          - Retry: Execute with enhanced context

        Level 2 (failure_count 4-6):
          - Action: Pattern analysis
          - Analysis: Identify failure pattern (syntax, logic, integration, etc.)
          - Strategy: Adjust approach based on pattern
          - Examples:
              - Syntax errors: Add strict validation step
              - Logic errors: Break down into smaller units
              - Integration errors: Review integration points
          - Retry: With adjusted strategy

        Level 3 (failure_count 7+ OR same_error_count ≥ 3):
          - Action: User intervention request
          - Report: Failure history, attempted solutions, pattern analysis
          - Options: 1) Provide guidance, 2) Skip failing component, 3) Abort
          - Decision: User selects intervention approach

        Level 4 (Abort selected):
          - Action: Create checkpoint
          - Checkpoint: Save current state, completed components, failure context
          - Recovery options:
              1. Resume from checkpoint with new approach
              2. Manual fix then resume
              3. Restart from earlier phase with learnings
          - Location: .codex/state/checkpoints/{feature}-{timestamp}.json
  - NAMING: failure-escalation.md
  - PLACEMENT: .codex/tasks/

Task 9: MODIFY .codex/agents/dev.md
  - IMPLEMENT: Integrate failure escalation
  - FIND: Error handling and retry logic
  - ADD: On validation failure:
      1. Invoke failure-escalation.md task with failure context
      2. Track failure count and type in workflow.json
      3. Execute escalation level actions
      4. If user intervention: Present options and await decision
      5. If checkpoint: Save state and present recovery options
  - PRESERVE: Existing implementation workflow, validation execution

Task 10: MODIFY .codex/workflows/greenfield-generic.yaml
  - IMPLEMENT: Epic-based phase structure
  - CURRENT structure: All phases run sequentially
  - NEW structure: Epic-aware phase grouping
  - CHANGES:
      architecture_design phase:
        - Add: epic_scope parameter (which epic to architect)
        - Change: description to "Design architecture for Epic {N} only"
        - Add: epic_foundation flag for Epic 1 (includes core infrastructure)

      prp_creation phase:
        - Add: epic_scope parameter
        - Change: description to "Create PRPs for Epic {N} stories"
        - Add: prerequisite check: Epic N-1 implementation complete (if N > 1)

      Add: epic_learning_review phase (new)
        - agent: prp-creator
        - description: "Review Epic N execution learnings before creating Epic N+1 PRPs"
        - inputs: execution-reports from Epic N
        - outputs: learning-summary.md, updated PRP patterns
  - NAMING: Keep existing filename
  - PATTERN: Repeat for greenfield-swift.yaml

Task 11: MODIFY .codex/workflows/greenfield-swift.yaml
  - IMPLEMENT: Epic-based phase structure (same as Task 10)
  - APPLY: Same changes as greenfield-generic.yaml
  - SWIFT-SPECIFIC: Maintain Swift validation commands and tooling

Task 12: CREATE .codex/tasks/capture-execution-learnings.md
  - IMPLEMENT: Execution learning capture system
  - FOLLOW pattern: .codex/tasks/persist-discovery-summary.md (persistence pattern)
  - WORKFLOW:
      1. During PRP execution, track:
         - validation_results: {level: {passed: bool, attempts: int, issues: []}}
         - prp_quality_issues: [issues encountered from PRP]
         - patterns_that_worked: [successful patterns used]
         - missing_or_incorrect_info: [PRP gaps discovered]
         - actual_vs_estimated_time: {estimated: hours, actual: hours}

      2. After validation level completion:
         - Update execution report with results
         - If level failed: Capture failure details, attempts, resolution

      3. After full PRP completion:
         - Generate comprehensive execution report
         - Save to: .codex/state/execution-reports/epic-{N}-story-{M}.json
         - Update workflow.json execution_reports array

      4. Include in report:
         - prp_file: path
         - execution_duration_hours: actual time
         - estimated_duration_hours: from PRP
         - validation_results: per level
         - prp_quality_assessment: score 0-100
         - improvements_for_next_prp: []
         - patterns_to_reuse: []
         - gotchas_discovered: []
  - NAMING: capture-execution-learnings.md
  - PLACEMENT: .codex/tasks/

Task 13: MODIFY .codex/agents/dev.md
  - IMPLEMENT: Execution learning capture integration
  - FIND: Validation execution points
  - ADD: At each validation level:
      1. Before execution: Invoke capture-execution-learnings.md with "start" action
      2. After execution: Invoke with "complete" action and results
      3. On failure: Invoke with "failure" action and details
  - PRESERVE: Existing validation workflow

Task 14: CREATE .codex/tasks/epic-learning-integration.md
  - IMPLEMENT: Apply learnings to next epic's PRP creation
  - FOLLOW pattern: .codex/tasks/context-handoff.md (context preparation)
  - WORKFLOW:
      1. Before creating Epic N+1 PRPs:
         a. Read all execution reports from Epic N
         b. Extract common patterns:
            - Successful patterns (reuse these)
            - Failed patterns (avoid these)
            - PRP gaps (fix these)
            - Validation issues (prevent these)
         c. Generate learning summary

      2. Create learning integration checklist:
         - [ ] Successful patterns documented for reuse
         - [ ] Failed patterns added to anti-patterns
         - [ ] PRP gaps addressed in Epic N+1 PRPs
         - [ ] Validation commands verified
         - [ ] File references updated
         - [ ] URL references validated
         - [ ] Gotchas added to Known Gotchas section

      3. Enhance Epic N+1 PRP creation with:
         - Proven patterns from Epic N
         - Corrected file references
         - Validated validation commands
         - New gotchas in context
         - Improved time estimates based on actuals
  - NAMING: epic-learning-integration.md
  - PLACEMENT: .codex/tasks/

Task 15: MODIFY .codex/agents/prp-creator.md
  - IMPLEMENT: Epic learning review before PRP creation
  - FIND: PRP creation initiation point
  - ADD: Before creating PRPs for Epic N (where N > 1):
      1. Check if Epic N-1 complete
      2. Execute epic-learning-integration.md task
      3. Review learning summary with user
      4. Apply learnings to PRP creation strategy
  - PRESERVE: Existing PRP creation workflow, research patterns

Task 16: MODIFY .codex/agents/qa.md
  - IMPLEMENT: Comprehensive review capabilities from BMAD
  - CURRENT: Basic QA review workflow
  - ADD from BMAD (.bmad-core/tasks/review-story.md):
      - Risk-based review depth:
          Auto-escalate to deep review when:
          - Auth/payment/security files touched
          - No tests added
          - Diff > 500 lines
          - Previous gate FAIL/CONCERNS
          - Story has > 5 acceptance criteria

      - Comprehensive analysis categories:
          A. Requirements Traceability (AC → Tests mapping with Given-When-Then)
          B. Code Quality Review (architecture, refactoring, duplication, performance, security)
          C. Test Architecture Assessment (coverage, level appropriateness, design quality)
          D. NFR Validation (security, performance, reliability, maintainability)
          E. Testability Evaluation (controllability, observability, debuggability)
          F. Technical Debt Identification

      - Active refactoring authority:
          - Can refactor code when safe and appropriate
          - Must run tests after changes
          - Document all changes in QA Results with WHY and HOW

      - Standards compliance:
          - Verify adherence to docs/coding-standards.md
          - Check docs/unified-project-structure.md
          - Validate docs/testing-strategy.md
  - PRESERVE: Existing gate file creation, permissions (QA Results section only)

Task 17: CREATE .codex/tasks/zero-knowledge-test.md
  - IMPLEMENT: Validate architecture completeness from external perspective
  - FOLLOW pattern: .codex/tasks/prp-quality-check.md (checklist execution)
  - WORKFLOW:
      1. Simulate: "Developer who knows nothing about this project"
      2. Execute architect-quality-gate.md checklist (169 items)
      3. For each checklist item, verify:
         - Is information present in architecture document?
         - Is information specific and actionable?
         - Could someone implement this with no prior knowledge?
      4. Track gaps:
         - Missing information
         - Vague or generic guidance
         - Assumptions not documented
      5. Generate gap report with specific remediation
  - NAMING: zero-knowledge-test.md
  - PLACEMENT: .codex/tasks/

Task 18: CREATE .codex/tasks/confidence-scoring.md
  - IMPLEMENT: Quantify architecture quality 0-100
  - FOLLOW pattern: .codex/data/quality-scoring-rubric.md (scoring methodology)
  - SCORING formula:
      Base: 100 points
      Deductions:
        - Missing critical section: -20 points each
        - Incomplete section: -10 points each
        - Vague guidance: -5 points each
        - No examples provided: -3 points each

      Categories (from architect-quality-gate.md):
        1. Frontend Architecture (0-20 points)
        2. Backend Architecture (0-20 points)
        3. Data Architecture (0-15 points)
        4. Infrastructure & DevOps (0-10 points)
        5. Testing Strategy (0-12 points)
        6. Security Architecture (0-10 points)
        7. AI Agent Suitability (0-8 points)
        8. PRP Creation Guidance (0-5 points)

      Score interpretation:
        90-100: Excellent - High confidence for one-pass implementation
        80-89: Good - Minor clarifications may be needed
        70-79: Adequate - Some gaps, expect questions
        60-69: Concerning - Significant gaps, likely delays
        <60: Inadequate - Major rework needed
  - NAMING: confidence-scoring.md
  - PLACEMENT: .codex/tasks/

Task 19: MODIFY .codex/templates/architecture-template.yaml
  - IMPLEMENT: Add PRP Creation Guidance section
  - FIND: End of template sections
  - ADD new section (after all existing sections):
      Section: PRP Creation Guidance
      Description: "Provide specific guidance for PRP creators on implementing this architecture"
      Elicit: false
      Content structure:
        ## PRP Creation Guidance

        **Critical Sections for PRPs:**
        - [List specific architecture sections with page/line references]
        - Example: "Section 3.2: Database schema details (lines X-Y) for data models"

        **Implementation Priorities (Epic-Based):**
        1. [Epic 1 scope with specific architecture sections to reference]
        2. [Epic 2 scope with specific architecture sections to reference]

        **Architectural Constraints:**
        - [Constraint 1]: [Implication for implementation]
        - Example: "Must use PostgreSQL 14+: Affects data models, migrations, connection pooling"

        **Pattern Examples:**
        - [Pattern type]: [Specific file reference]
        - Example: "Component pattern: src/components/UserProfile/ (props, state, styling)"
        - Example: "API pattern: src/api/users/createUser.ts (validation, error handling)"
        - Example: "Test pattern: tests/unit/services/UserService.test.ts (fixtures, mocks)"

        **Known Gotchas:**
        - [Technology/Library]: [Specific gotcha and workaround]
        - Example: "React 18: useEffect cleanup required for async operations"
  - PRESERVE: All existing sections, elicitation requirements

Task 20: MODIFY .codex/state/workflow.json.template
  - IMPLEMENT: Add feedback and learning tracking fields
  - FIND: Root level JSON structure
  - ADD fields:
      "feedback_requests": []  // Array of feedback request objects
      "execution_reports": []  // Array of execution report file paths
      "epic_learnings": []     // Array of epic learning summary objects
      "current_epic": 1        // Current epic number for incremental workflow
  - ADD to transformation_history events:
      "feedback_requested"
      "feedback_resolved"
      "execution_report_generated"
      "epic_learning_captured"
  - PRESERVE: All existing fields, structure, validation logic

Task 21: CREATE .codex/state/execution-reports/ directory
  - CREATE: Directory for execution report storage
  - LOCATION: .codex/state/execution-reports/
  - PURPOSE: Store execution learning reports per epic/story
  - NAMING convention: epic-{N}-story-{M}.json

Task 22: CREATE .codex/state/epic-learnings/ directory
  - CREATE: Directory for epic learning summaries
  - LOCATION: .codex/state/epic-learnings/
  - PURPOSE: Store consolidated learnings per epic
  - NAMING convention: epic-{N}-learning-summary.md
```

### Implementation Patterns & Key Details

```yaml
# Feedback Request Pattern
# From: .codex/agents/architect.md using request-feedback command
workflow:
  1. Architect encounters unclear requirement in PRD
  2. Invokes: *request-feedback pm "Story 1.3 acceptance criteria unclear - 'real-time' undefined"
  3. System executes request-feedback.md task:
     - Creates feedback object with ID fb-{timestamp}
     - Updates workflow.json feedback_requests array
     - Sets status: "pending"
  4. Orchestrator detects pending feedback
  5. Orchestrator spawns PM agent with feedback context
  6. PM reviews issue and executes: *update docs/prd.md
  7. PM executes: *resolve-feedback fb-{id} "Clarified: real-time = <100ms response"
  8. System updates feedback status: "resolved"
  9. Orchestrator notifies Architect
  10. Architect resumes with updated PRD

# PRP Validation Enforcement Pattern
# From: .codex/agents/prp-creator.md before marking PRP complete
workflow:
  1. PRP Creator completes PRP creation
  2. Before marking complete, auto-executes: prp-validation-enforcement.md
  3. Validation checks:
     a. Execute prp-quality-check.md → get score
     b. If score < 90: HALT with detailed report
     c. Read each file reference → verify exists
     d. Check each URL → verify accessible
     e. Parse validation commands → require verification log section
  4. If any check fails:
     - Present detailed remediation
     - Offer auto-fix where possible
     - Re-validate after fixes
  5. If all pass:
     - Mark PRP validated in workflow.json
     - Proceed to execution phase

# Failure Escalation Pattern
# From: .codex/agents/dev.md during validation execution
workflow:
  1. Dev executes validation level (e.g., Level 2: Unit Tests)
  2. Validation fails (tests fail)
  3. Dev invokes: failure-escalation.md with context:
     - failure_type: "test_failure"
     - message: "5 unit tests failing in UserService"
     - attempted_solution: "Fixed imports, updated mocks"
     - validation_level: 2
  4. Escalation reads workflow.json failure_count
  5. Determines escalation level:
     - 0-3 failures: Level 1 - Auto retry with enhanced context
        Action: Add UserService examples, error handling patterns
     - 4-6 failures: Level 2 - Pattern analysis
        Analysis: "Repeated mock configuration errors"
        Strategy: "Use test fixture factory pattern"
     - 7+ or 3x same: Level 3 - User intervention
        Report: Show failure history, attempted solutions
        Options: 1) Guide, 2) Skip component, 3) Abort
     - Abort: Level 4 - Checkpoint
        Save: Current state, completed work, failure context
        Recovery: Resume, manual fix, or restart with learnings
  6. Execute appropriate level action
  7. Update workflow.json with escalation outcome

# Epic-Based Workflow Pattern
# From: .codex/workflows/greenfield-generic.yaml
workflow:
  Phase 1-3 (Discovery → Analysis → PM):
    - Execute normally (project-wide scope)
    - PM creates complete PRD with ALL epics and stories

  Phase 4 (Architecture) - Epic 1 ONLY:
    - Architect creates architecture for Epic 1 features only
    - Include: Core infrastructure, Epic 1 patterns, foundational decisions
    - Epic 1 architecture becomes foundation reference
    - Save to: docs/architecture-epic-1.md

  Phase 5 (PRP Creation) - Epic 1 ONLY:
    - PRP Creator creates PRPs for Epic 1 stories only
    - Uses: docs/architecture-epic-1.md as reference
    - Save to: PRPs/epic-1/

  Phase 6 (Implementation) - Epic 1:
    - Dev implements Epic 1 stories
    - Captures execution learnings per story

  Phase 7 (Epic Learning Review) - BEFORE Epic 2:
    - PRP Creator reviews Epic 1 execution reports
    - Identifies: Successful patterns, failed patterns, PRP gaps
    - Creates: epic-1-learning-summary.md

  Phase 4 (Architecture) - Epic 2:
    - Architect creates architecture for Epic 2 features
    - Builds on: Epic 1 architecture (reference, don't duplicate)
    - Applies: Learnings from Epic 1 implementation
    - Save to: docs/architecture-epic-2.md

  Phase 5 (PRP Creation) - Epic 2:
    - PRP Creator creates PRPs for Epic 2 stories
    - Uses: Epic 1 learnings to improve PRP quality
    - References: Both architecture-epic-1.md and architecture-epic-2.md

  Repeat for Epic 3, 4, etc.

# QA Comprehensive Review Pattern
# From: .codex/agents/qa.md enhanced with BMAD capabilities
workflow:
  1. Story marked "Review" by Dev
  2. QA invokes: *review {story_id}
  3. Risk Assessment (determines review depth):
     - Check: Auth/payment/security files touched? → Deep review
     - Check: No tests added? → Deep review
     - Check: Diff > 500 lines? → Deep review
     - Check: Previous gate FAIL/CONCERNS? → Deep review
     - Check: Story has > 5 ACs? → Deep review
  4. If Deep Review triggered:
     A. Requirements Traceability:
        - Map each AC to validating tests (Given-When-Then format)
        - Identify coverage gaps
     B. Code Quality Review:
        - Architecture patterns, refactoring opportunities
        - Performance, security vulnerabilities
     C. Test Architecture:
        - Coverage adequacy, level appropriateness (unit/integration/e2e)
        - Test design quality, edge case coverage
     D. NFR Validation:
        - Security: auth, authorization, data protection
        - Performance: response times, resource usage
        - Reliability: error handling, recovery
        - Maintainability: code clarity, documentation
     E. Testability:
        - Controllability, observability, debuggability
     F. Technical Debt:
        - Accumulated shortcuts, missing tests, architecture violations
  5. Active Refactoring:
     - If safe and appropriate, refactor code
     - Run tests to verify changes don't break functionality
     - Document WHY and HOW in QA Results section
  6. Update Story:
     - ONLY update "QA Results" section
     - Include: Assessment, refactoring performed, compliance check, improvements checklist
  7. Create Gate File:
     - Location: qa.qaLocation/gates/{epic}.{story}-{slug}.yml
     - Gate decision: PASS | CONCERNS | FAIL | WAIVED
     - Quality score: 100 - (20*FAILs) - (10*CONCERNS)
     - Evidence: tests reviewed, risks identified, AC coverage
     - NFR validation per category
     - Recommendations: immediate (must fix) and future (can defer)
  8. Recommend Status:
     - ✓ Ready for Done (if PASS)
     - ✗ Changes Required (if CONCERNS/FAIL with unchecked improvements)

# Zero-Knowledge Test Pattern
# From: .codex/tasks/zero-knowledge-test.md
workflow:
  1. Architecture document created
  2. Before handoff to PRP Creator, execute zero-knowledge test
  3. Simulate: "Developer with no project knowledge"
  4. For each item in architect-quality-gate.md (169 items):
     - Question: Is this information in the architecture?
     - Question: Is it specific and actionable?
     - Question: Could someone implement with no prior knowledge?
  5. Track gaps:
     - Missing: Information not present at all
     - Vague: Generic guidance like "use best practices"
     - Assumed: Assumes knowledge not documented
  6. Generate gap report:
     - List each gap with specific section reference
     - Provide remediation: What to add, where to add it
  7. Architect reviews gaps and fills them
  8. Re-run zero-knowledge test until pass threshold (e.g., 95% complete)

# Confidence Scoring Pattern
# From: .codex/tasks/confidence-scoring.md
workflow:
  1. Architecture document complete
  2. Execute confidence-scoring.md task
  3. Evaluate each category (from architect-quality-gate.md):
     - Frontend Architecture: 0-20 points
       Check: Component patterns, state management, routing, UI standards
     - Backend Architecture: 0-20 points
       Check: API design, service layer, data access, error handling
     - Data Architecture: 0-15 points
       Check: Schema design, migrations, relationships, constraints
     - Infrastructure: 0-10 points
       Check: Deployment, scaling, monitoring, CI/CD
     - Testing Strategy: 0-12 points
       Check: Test pyramid, coverage, frameworks, examples
     - Security: 0-10 points
       Check: Auth, authorization, data protection, threat model
     - AI Suitability: 0-8 points
       Check: Clear patterns, examples, constraints, anti-patterns
     - PRP Guidance: 0-5 points
       Check: Implementation priorities, constraints, pattern examples
  4. Calculate total score (0-100)
  5. Apply deductions:
     - Missing critical section: -20
     - Incomplete section: -10
     - Vague guidance: -5
     - No examples: -3
  6. Generate confidence report:
     - Overall score with interpretation
     - Category breakdown
     - Specific improvements needed
     - Expected implementation success rate
  7. Architect can review and improve before handoff
```

### Integration Points

```yaml
STATE:
  - file: .codex/state/workflow.json
    fields_to_add:
      - feedback_requests: []
      - execution_reports: []
      - epic_learnings: []
      - current_epic: 1
      - failure_count: 0
      - failure_history: []

AGENTS:
  - file: .codex/agents/pm.md
    commands_to_add:
      - *update {document}: Update document based on feedback
      - *resolve-feedback {id}: Resolve feedback request

  - file: .codex/agents/architect.md
    commands_to_add:
      - *request-feedback {agent} {issue}: Request clarification from upstream agent

  - file: .codex/agents/orchestrator.md
    logic_to_add:
      - Feedback request detection and routing
      - Epic progression control
      - Learning integration coordination

  - file: .codex/agents/prp-creator.md
    logic_to_add:
      - PRP validation enforcement before completion
      - Epic learning review before Epic N+1 PRP creation

  - file: .codex/agents/dev.md
    logic_to_add:
      - Failure escalation on validation errors
      - Execution learning capture at each validation level

  - file: .codex/agents/qa.md
    capabilities_to_add:
      - Risk-based review depth
      - Comprehensive analysis (6 categories)
      - Active refactoring authority
      - NFR validation
      - Technical debt identification

WORKFLOWS:
  - file: .codex/workflows/greenfield-generic.yaml
    structure_to_add:
      - epic_scope parameter to architecture_design phase
      - epic_scope parameter to prp_creation phase
      - epic_learning_review phase (new)
      - prerequisite checks for Epic N > 1

  - file: .codex/workflows/greenfield-swift.yaml
    structure_to_add:
      - Same as greenfield-generic.yaml

TEMPLATES:
  - file: .codex/templates/architecture-template.yaml
    section_to_add:
      - PRP Creation Guidance (Section at end)
        - Critical sections for PRPs
        - Implementation priorities (epic-based)
        - Architectural constraints
        - Pattern examples
        - Known gotchas

DIRECTORIES:
  - create: .codex/state/execution-reports/
    purpose: Store execution learning reports

  - create: .codex/state/epic-learnings/
    purpose: Store epic learning summaries

  - create: .codex/state/checkpoints/
    purpose: Store failure recovery checkpoints
```

## Validation Loop

### Level 1: File and Structure Validation (Immediate)

```bash
# Verify all new files created
test -f .codex/data/feedback-request-template.yaml && echo "✓ Feedback template" || echo "✗ Missing feedback template"
test -f .codex/tasks/request-feedback.md && echo "✓ Request feedback task" || echo "✗ Missing request feedback task"
test -f .codex/tasks/prp-validation-enforcement.md && echo "✓ PRP validation task" || echo "✗ Missing PRP validation task"
test -f .codex/tasks/failure-escalation.md && echo "✓ Failure escalation task" || echo "✗ Missing failure escalation task"
test -f .codex/tasks/capture-execution-learnings.md && echo "✓ Capture learnings task" || echo "✗ Missing capture learnings task"
test -f .codex/tasks/epic-learning-integration.md && echo "✓ Epic learning task" || echo "✗ Missing epic learning task"
test -f .codex/tasks/zero-knowledge-test.md && echo "✓ Zero-knowledge test" || echo "✗ Missing zero-knowledge test"
test -f .codex/tasks/confidence-scoring.md && echo "✓ Confidence scoring" || echo "✗ Missing confidence scoring"

# Verify directories created
test -d .codex/state/execution-reports && echo "✓ Execution reports dir" || echo "✗ Missing execution reports dir"
test -d .codex/state/epic-learnings && echo "✓ Epic learnings dir" || echo "✗ Missing epic learnings dir"
test -d .codex/state/checkpoints && echo "✓ Checkpoints dir" || echo "✗ Missing checkpoints dir"

# Verify agent modifications contain new commands
grep -q "\*request-feedback" .codex/agents/architect.md && echo "✓ Architect feedback command" || echo "✗ Missing architect feedback command"
grep -q "\*update" .codex/agents/pm.md && echo "✓ PM update command" || echo "✗ Missing PM update command"
grep -q "\*resolve-feedback" .codex/agents/pm.md && echo "✓ PM resolve command" || echo "✗ Missing PM resolve command"

# Verify workflow.json template has new fields
grep -q "feedback_requests" .codex/state/workflow.json.template && echo "✓ Feedback tracking field" || echo "✗ Missing feedback tracking"
grep -q "execution_reports" .codex/state/workflow.json.template && echo "✓ Execution reports field" || echo "✗ Missing execution reports"
grep -q "epic_learnings" .codex/state/workflow.json.template && echo "✓ Epic learnings field" || echo "✗ Missing epic learnings"
grep -q "current_epic" .codex/state/workflow.json.template && echo "✓ Current epic field" || echo "✗ Missing current epic"

# Verify workflow epic-based structure
grep -q "epic_scope" .codex/workflows/greenfield-generic.yaml && echo "✓ Epic scope parameter" || echo "✗ Missing epic scope"
grep -q "epic_learning_review" .codex/workflows/greenfield-generic.yaml && echo "✓ Epic learning phase" || echo "✗ Missing epic learning phase"

# Expected: All ✓. If any ✗, create missing file following task pattern.
```

### Level 2: Content and Integration Validation

```bash
# Test feedback request workflow
echo "Testing feedback request protocol..."
# 1. Create test feedback request using template
# 2. Verify workflow.json updated with feedback object
# 3. Verify feedback has required fields: id, from_agent, to_agent, issue, context, status
# 4. Verify status is "pending"

# Test PRP validation enforcement
echo "Testing PRP validation enforcement..."
# 1. Create test PRP with known issues (missing file refs, broken URLs, no verification log)
# 2. Execute prp-validation-enforcement.md task
# 3. Verify validation FAILS with detailed report
# 4. Verify report lists specific issues found
# 5. Fix issues and re-validate
# 6. Verify validation PASSES

# Test failure escalation levels
echo "Testing failure escalation protocol..."
# 1. Simulate failure with count=2 (Level 1)
# 2. Verify automatic retry with enhanced context
# 3. Simulate failure with count=5 (Level 2)
# 4. Verify pattern analysis executed
# 5. Simulate failure with count=8 (Level 3)
# 6. Verify user intervention requested
# 7. Simulate abort (Level 4)
# 8. Verify checkpoint created in .codex/state/checkpoints/

# Test epic-based workflow
echo "Testing epic-based workflow..."
# 1. Start workflow with Epic 1
# 2. Verify architecture created for Epic 1 only
# 3. Verify PRPs created for Epic 1 only
# 4. Complete Epic 1 implementation
# 5. Verify execution reports generated
# 6. Start Epic 2
# 7. Verify learning review executed before Epic 2 architecture
# 8. Verify Epic 1 learnings applied to Epic 2 PRPs

# Test QA comprehensive review
echo "Testing QA comprehensive review..."
# 1. Create test story with security files touched
# 2. Invoke QA *review command
# 3. Verify risk assessment triggers deep review
# 4. Verify all 6 analysis categories executed
# 5. Verify gate file created with NFR validation
# 6. Verify QA Results section updated (only)
# 7. Verify other sections untouched

# Expected: All tests pass. If failures, debug integration points.
```

### Level 3: End-to-End Workflow Validation

```bash
# Complete workflow test: Discovery → Epic 1 → Epic 2 with feedback
echo "Running end-to-end workflow test..."

# Phase 1: Project setup
# 1. Execute discovery phase
# 2. Create project brief
# 3. Create complete PRD with all epics

# Phase 2: Epic 1 Architecture with feedback loop
# 4. Create Epic 1 architecture
# 5. Simulate architect finding PRD ambiguity
# 6. Execute: *request-feedback pm "Epic 1 Story 2: unclear acceptance criteria"
# 7. Verify feedback request in workflow.json
# 8. PM receives feedback, executes: *update docs/prd.md
# 9. PM executes: *resolve-feedback {id} "Clarified AC with specific metrics"
# 10. Verify architect receives updated PRD
# 11. Architect completes Epic 1 architecture

# Phase 3: Epic 1 PRP Creation with validation
# 12. Create Epic 1 PRPs
# 13. PRP validation auto-executes
# 14. Simulate validation finding broken URL
# 15. Verify validation FAILS with specific remediation
# 16. Fix broken URL
# 17. Re-validate, verify PASS
# 18. PRPs marked validated in workflow.json

# Phase 4: Epic 1 Implementation with escalation
# 19. Execute Epic 1 PRPs
# 20. Simulate validation failure (3 times, same error)
# 21. Verify Level 3 escalation (user intervention)
# 22. Provide user guidance
# 23. Implementation succeeds
# 24. Execution reports generated for each story

# Phase 5: Epic 2 with learning integration
# 25. Learning review executes before Epic 2
# 26. Verify Epic 1 execution reports analyzed
# 27. Verify learning summary created
# 28. Create Epic 2 architecture
# 29. Verify Epic 1 learnings referenced
# 30. Create Epic 2 PRPs
# 31. Verify Epic 1 patterns applied
# 32. Verify Epic 1 gotchas added to context

# Phase 6: QA Comprehensive Review
# 33. Mark story for review
# 34. QA executes comprehensive review
# 35. Verify risk assessment correct
# 36. Verify all analysis categories completed
# 37. Verify gate file created with proper scoring
# 38. Verify story updated (QA Results only)

# Expected: Complete workflow executes without errors, all feedback loops functional
```

### Level 4: Quality Metrics Validation

```bash
# Validate success criteria achievement

# Feedback Loop Metrics
echo "Validating feedback loop metrics..."
# 1. Count feedback requests created during test workflow
# 2. Verify all feedback requests resolved
# 3. Measure feedback resolution time
# 4. Verify no feedback loops stuck in "pending"
# Expected: 100% feedback resolution rate

# PRP Validation Metrics
echo "Validating PRP quality metrics..."
# 1. Count PRPs validated
# 2. Count PRPs that failed pre-flight validation
# 3. Count issues found (missing files, broken URLs, unverified commands)
# 4. Measure remediation time
# Expected: 100% PRPs validated before execution, >90 quality scores

# Failure Escalation Metrics
echo "Validating failure handling metrics..."
# 1. Count failures by escalation level
# 2. Verify Level 1 auto-recovery rate
# 3. Verify Level 2 pattern analysis effectiveness
# 4. Verify Level 3 user interventions resolved failures
# 5. Verify Level 4 checkpoints enable recovery
# Expected: <10% failures reach Level 3, 100% recovery from Level 4

# Epic Learning Metrics
echo "Validating epic learning metrics..."
# 1. Count execution reports generated
# 2. Count learnings captured per epic
# 3. Measure PRP quality improvement Epic 1 → Epic 2
# 4. Count patterns reused from Epic 1 in Epic 2
# 5. Count gotchas from Epic 1 avoided in Epic 2
# Expected: Measurable quality improvement each epic

# QA Review Metrics
echo "Validating QA review metrics..."
# 1. Count stories reviewed
# 2. Count deep reviews triggered by risk assessment
# 3. Count refactorings performed by QA
# 4. Measure NFR validation coverage
# 5. Count technical debt items identified
# Expected: 100% story coverage, risk-appropriate review depth

# Architect Validation Metrics
echo "Validating architect quality metrics..."
# 1. Execute zero-knowledge test on all architectures
# 2. Count gaps found
# 3. Measure gap remediation rate
# 4. Calculate confidence scores
# 5. Correlate confidence scores with implementation success
# Expected: >90% zero-knowledge test pass rate, >85 average confidence score

# Overall Quality Improvement
echo "Validating overall quality improvements..."
# 1. Measure rework time with vs without feedback loops
# 2. Measure PRP execution success rate with vs without validation
# 3. Measure implementation time Epic 1 vs Epic 2 (learning effect)
# 4. Measure incomplete handoffs before vs after
# Expected:
#   - 90% reduction in incomplete handoffs
#   - 40-50% PRD quality improvement
#   - 17-21 hours saved per project (670-823% ROI)
#   - Progressive quality improvement across epics
```

## Final Validation Checklist

### Technical Validation

- [ ] All new task files created following .codex/tasks/ pattern
- [ ] All agent modifications preserve existing structure and commands
- [ ] All workflow modifications maintain phase progression logic
- [ ] workflow.json.template has all new tracking fields
- [ ] All directories created with proper permissions
- [ ] All file references in tasks are absolute paths
- [ ] All YAML syntax validated

### Feature Validation - Week 4 Deliverables

- [ ] Feedback request protocol functional (PM↔Architect, PRP↔Execution)
- [ ] Feedback requests tracked in workflow.json with status
- [ ] Orchestrator routes feedback to correct agents
- [ ] PM can update documents and resolve feedback
- [ ] Architect can request clarification from PM
- [ ] Max 3 iterations enforced, escalates to user if exceeded
- [ ] PRP validation enforces ≥90 quality score before execution
- [ ] File references verified to exist
- [ ] URLs validated for accessibility
- [ ] Validation commands require verification log proof
- [ ] Failure escalation handles 4 levels correctly
- [ ] Level 1: Auto-retry with enhanced context (0-3 failures)
- [ ] Level 2: Pattern analysis and strategy adjustment (4-6 failures)
- [ ] Level 3: User intervention request (7+ or 3x same error)
- [ ] Level 4: Checkpoint creation and recovery options
- [ ] Epic-based architecture creation (Epic N only, not all upfront)
- [ ] Epic-based PRP creation (just-in-time, per-epic)
- [ ] Epic prerequisites enforced (Epic 2 requires Epic 1 complete)

### Feature Validation - Week 5 Deliverables

- [ ] QA performs risk-based review depth determination
- [ ] QA executes comprehensive analysis (6 categories)
- [ ] QA can perform active refactoring with test verification
- [ ] QA documents all changes in QA Results section only
- [ ] QA creates gate files with NFR validation
- [ ] QA gate scoring: quality_score = 100 - (20*FAILs) - (10*CONCERNS)
- [ ] Execution reports capture validation results per level
- [ ] Execution reports track attempts, issues, patterns, gotchas
- [ ] Execution reports saved to .codex/state/execution-reports/
- [ ] Epic learning review executes before Epic N+1
- [ ] Learnings extracted: successful patterns, failed patterns, PRP gaps
- [ ] Learnings applied to Epic N+1 PRPs
- [ ] Zero-knowledge test validates architecture completeness
- [ ] Confidence scoring quantifies architecture quality (0-100)
- [ ] Architecture template includes PRP creation guidance
- [ ] Handoff tasks provide clear implementation priorities

### Code Quality Validation

- [ ] All tasks follow .codex/tasks/create-doc.md pattern
- [ ] All agent modifications maintain persona definitions
- [ ] All workflow modifications maintain validation gates
- [ ] State management preserves integrity during feedback cycles
- [ ] Epic progression logic prevents premature phase transitions
- [ ] Failure tracking prevents infinite retry loops
- [ ] All file paths are absolute, not relative
- [ ] All YAML structures are valid and parseable
- [ ] All task dependencies clearly documented
- [ ] All gotchas from BMAD incorporated

### Documentation & Integration

- [ ] All new commands documented in agent help output
- [ ] All new tasks have clear input/output specifications
- [ ] All workflow changes documented in workflow YAML
- [ ] All state fields documented in template
- [ ] Integration points verified (agent→task→state→workflow)
- [ ] Feedback flow documented (request→route→resolve→notify)
- [ ] Escalation levels documented with examples
- [ ] Epic learning flow documented (capture→analyze→apply)
- [ ] QA review categories documented with examples
- [ ] Validation requirements documented per level

### Success Metrics Achievement

- [ ] Feedback loops reduce rework by measured amount
- [ ] PRP validation prevents downstream failures (measurable)
- [ ] Failure escalation prevents workflow abandonment (measurable)
- [ ] Epic learning improves quality progressively (Epic 1 → Epic 2 scores)
- [ ] QA review finds issues before production (gate statistics)
- [ ] Zero-knowledge test improves architecture completeness (gap reduction)
- [ ] Confidence scoring predicts implementation success (correlation)
- [ ] Overall ROI target: 670-823% (17-21 hours saved per project)

---

## Anti-Patterns to Avoid

### Feedback Loops
- ❌ Don't allow infinite feedback cycles (max 3 iterations enforced)
- ❌ Don't bypass feedback status tracking in workflow.json
- ❌ Don't resolve feedback without actual document updates
- ❌ Don't request feedback for trivial clarifications (use judgment)
- ❌ Don't allow feedback requests without specific context reference

### PRP Validation
- ❌ Don't execute PRPs without pre-flight validation
- ❌ Don't accept PRP scores < 90 without remediation
- ❌ Don't skip file reference verification
- ❌ Don't skip URL accessibility checks
- ❌ Don't accept PRPs without validation command verification logs
- ❌ Don't auto-fix validation issues without user awareness

### Failure Escalation
- ❌ Don't retry indefinitely without escalation
- ❌ Don't skip pattern analysis at Level 2
- ❌ Don't proceed without user intervention at Level 3
- ❌ Don't lose context when creating checkpoints
- ❌ Don't restart from scratch when checkpoint exists

### Epic-Based Workflow
- ❌ Don't create architecture for all epics upfront
- ❌ Don't create PRPs before epic is ready for implementation
- ❌ Don't ignore Epic N-1 learnings when creating Epic N artifacts
- ❌ Don't proceed to Epic 2 before Epic 1 implementation complete
- ❌ Don't duplicate Epic 1 architecture in Epic 2 (reference it instead)

### QA Review
- ❌ Don't skip risk assessment (determines review depth)
- ❌ Don't modify story sections other than QA Results
- ❌ Don't perform refactoring without running tests after
- ❌ Don't create gate decisions without evidence
- ❌ Don't skip NFR validation categories

### Execution Learning
- ❌ Don't discard execution reports after epic completion
- ❌ Don't create Epic N+1 PRPs without reviewing Epic N learnings
- ❌ Don't repeat Epic N mistakes in Epic N+1
- ❌ Don't ignore patterns that worked well in Epic N
- ❌ Don't lose gotchas discovered during implementation

### State Management
- ❌ Don't update in-memory state without persisting to file
- ❌ Don't corrupt workflow.json structure with invalid JSON
- ❌ Don't lose state during feedback cycles
- ❌ Don't proceed with corrupted state (validate first)
- ❌ Don't bypass state validation checks

---

## Implementation Confidence Score: 8.5/10

### Confidence Rationale:

**High Confidence (9-10) Aspects:**
- Complete reference implementation in BMAD-core provides proven patterns ✓
- All gaps clearly identified with specific file locations ✓
- Task patterns well-established in current CODEX codebase ✓
- State management infrastructure already exists ✓
- Agent modification patterns consistent and repeatable ✓

**Medium Confidence (7-8) Aspects:**
- Epic-based workflow requires careful orchestration logic (7.5)
- Feedback cycle termination conditions need rigorous testing (8)
- Failure escalation pattern analysis complexity (7.5)
- Integration between multiple new systems (feedback + escalation + learning) (8)

**Areas Requiring Extra Attention:**
1. **Orchestrator Feedback Routing**: Complex state machine logic - test thoroughly
2. **Epic Progression Control**: Prevent premature Epic N+1 start - validate prerequisites
3. **Failure Pattern Analysis**: Level 2 escalation requires pattern recognition - may need refinement
4. **State Consistency**: Multiple concurrent state updates during feedback cycles - validate atomicity

### Risk Mitigation:
- **Integration Testing**: Validate all feedback loops end-to-end before production
- **State Validation**: Add comprehensive state integrity checks before/after updates
- **Checkpoint Recovery**: Test Level 4 checkpoint recovery thoroughly
- **Epic Learning Quality**: Validate learning extraction produces actionable insights

### Expected One-Pass Implementation Success: 85%

The 15% risk primarily in:
- Complex orchestrator logic for feedback routing (5%)
- Epic progression state management edge cases (5%)
- Failure pattern analysis accuracy (5%)

All risks can be mitigated through thorough validation at Levels 2-4.