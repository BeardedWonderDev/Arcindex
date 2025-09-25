# CODEX Enhanced Phase 1 Workflow Implementation Plan

**Date**: September 24, 2025
**Version**: 2.0
**Status**: Ready for Implementation
**Estimated Time**: 6 hours

## Executive Summary

This plan addresses critical UX issues in CODEX workflow initialization by implementing BMAD's proven patterns for project discovery and elicitation. The current system technically enforces elicitation but provides poor user experience with multiple confirmations, no basic discovery, and overwhelming domain-specific menus. This plan maintains the working technical enforcement while dramatically improving the user experience.

## Problem Analysis

### Issues Identified in Testing Session

1. **Poor Onboarding Flow**: Multiple confirmations before starting workflow
2. **No Project Discovery**: System assumes project purpose from name rather than asking
3. **Overwhelming Initial Elicitation**: Complex 9-area agricultural dealership domain menu instead of basic discovery
4. **Incorrect Menu Format**: Using 0-8 + 9 format instead of BMAD's 1-9 format

### Root Cause

The Phase 1 implementation as documented in docs/codex-elicitation-orchestration-analysis.md correctly enforced elicitation technically but missed the user experience patterns that make BMAD successful. CODEX jumps directly to complex domain elicitation without first understanding what the project actually is.

## BMAD Pattern Analysis

### Key BMAD Success Patterns (from `.bmad-core/`)

#### 1. Transformation Pattern (`.bmad-core/agents/bmad-orchestrator.md`)
- **Line 36-48**: Orchestrator persona that transforms into specialized agents
- **Line 57-67**: Commands for transformation (`*agent [name]`)
- **Line 113-117**: Transformation behavior - "Match name/role to agents, Announce transformation, Operate until exit"

#### 2. Project Brief Creation Flow (`.bmad-core/templates/project-brief-tmpl.yaml`)
- **Line 11-26**: Interactive workflow with custom elicitation options
- **Line 28-38**: Introduction section that asks for mode preference and project context
- **Line 40-49**: Executive Summary as first substantial content section
- **Lines throughout**: Section-by-section building with elicitation after each

#### 3. Advanced Elicitation Pattern (`.bmad-core/tasks/advanced-elicitation.md`)
- **Line 22-30**: Section review → Offer elicitation → Simple selection (1-9)
- **Line 83-98**: Elicitation menu format with "1. Proceed to next section"
- **Line 99-104**: Response handling for numeric selections

#### 4. Elicitation Methods (`.bmad-core/data/elicitation-methods.md`)
- **Lines 7-24**: Core reflective methods (Expand/Contract, Critique, etc.)
- **Lines 25-48**: Structural analysis methods
- **Lines 49-70**: Risk and challenge methods
- **Lines 71-96**: Creative exploration methods

## Implementation Plan

### Phase 1.1: Orchestrator Universal Discovery Enhancement

#### File: `.codex/agents/orchestrator.md`

**Current State (Lines to Modify)**:
- **Lines 118-137**: Current `workflow-management` section needs universal discovery
- **Lines 138-151**: Current `agent-coordination` needs transformation pattern
- **Lines 122-129**: Current pre-launch validation needs workflow-specific logic

**Changes Required**:

```yaml
# Replace lines 118-137 with:
workflow-management:
  - Parse YAML workflow definitions from .codex/workflows/
  - Maintain state in .codex/state/workflow.json
  - Track operation_mode (interactive|batch|yolo) in state

  # NEW: Universal Workflow Discovery Protocol
  workflow-initialization:
    - STEP 1: Parse command to get workflow type and optional project name
      # Format: /codex start [workflow-type] [project-name]

    - STEP 2: Workflow-specific discovery based on type:

      GREENFIELD workflows:
        a. Capture project name from command (if provided)
        b. Ask comprehensive discovery questions:
           - "What's your project name/working title?" (if not provided)
           - "Brief project concept: (describe what you're building)"
           - "Any existing inputs? (research, brainstorming, or starting fresh?)"
        c. Transform to analyst for project brief creation

      BROWNFIELD workflows:
        a. Check for existing CODEX project context:
           - Read .codex/docs/*.md for project documentation
           - Read .codex/state/workflow.json for previous workflow history
           - Check for PRPs, architecture docs, etc.
        b. Summarize understanding:
           "Based on existing documentation, I understand this is [summary]. Is this correct?"
        c. Get user confirmation/corrections
        d. Ask enhancement-specific questions:
           - "What enhancement/feature are you adding?"
           - "Which component/area does this affect?"
           - "Any constraints or requirements for this enhancement?"
        e. Transform to analyst for enhancement documentation

      HEALTH-CHECK workflows:
        a. No discovery needed - proceed directly
        b. Execute validation checks immediately
        c. Report results without agent transformation

    - STEP 3: Create/update workflow state with discovery results
    - STEP 4: Transform to appropriate agent with full context (NOT Task tool)
```

**Add New Section (After line 151)**:

```yaml
# NEW: Agent Transformation Protocol (BMAD Pattern)
agent-transformation:
  - Match workflow phase to specialized agent
  - Read agent definition file directly (.codex/agents/{agent}.md)
  - Announce transformation: "📊 Transforming into Business Analyst"
  - Adopt complete agent persona and capabilities
  - Pass discovered project context to agent
  - Maintain workflow state through transformation
  - Execute agent until phase completion or exit
  - Return to orchestrator for next phase transition
```

### Phase 1.2: Analyst Agent Enhancement

#### File: `.codex/agents/analyst.md`

**Current State (Lines to Modify)**:
- **Lines 19-39**: Activation instructions need workflow-aware discovery
- **Lines 133-141**: Business analysis methods need proper elicitation

**Changes Required**:

```yaml
# Modify lines 23-28 to add:
  - STEP 3.5: **WORKFLOW-AWARE ACTIVATION**:
    - Check workflow type from state (greenfield vs brownfield)
    - For greenfield: Prepare project brief creation workflow
    - For brownfield: Load existing project context first
    - Use discovery context passed from orchestrator
    - Begin section-by-section content creation

# Add after line 141:
content-creation-pattern:
  - Create substantial section content (match BMAD depth)
  - Include for each section:
    * Main content
    * Rationale & Trade-offs
    * Key decisions made
    * Assumptions
    * Areas for validation
  - Present elicitation menu using 1-9 format:
    * "1. Proceed to next section"
    * "2-9. Context-appropriate elicitation methods"
  - Wait for user selection before proceeding
  - Execute elicitation method if 2-9 selected
  - Continue to next section if 1 selected
```

### Phase 1.3: Elicitation Task Alignment

#### File: `.codex/tasks/advanced-elicitation.md`

**Current Implementation**: Already exists but needs menu format correction

**Changes Required**:

```markdown
# Line 83-98 - Update menu format to:

**Elicitation Menu Format:**

```text
Please select an option:

1. Proceed to next section
2. Expand or Contract for Audience
3. Critique and Refine
4. Identify Potential Risks and Unforeseen Issues
5. Challenge from Critical Perspective
6. [Context-appropriate method]
7. [Context-appropriate method]
8. [Context-appropriate method]
9. [Context-appropriate method]

Select 1-9 or just type your question/feedback:
```

**Response Handling:**
- **Number 1**: Proceed to next section or continue conversation
- **Numbers 2-9**: Execute the selected method, then re-offer the menu
- **Direct Feedback**: Apply user's suggested changes and continue
```

### Phase 1.4: Workflow State Template

#### File: `.codex/state/workflow.json` (Template for new structure)

**New Structure Required**:

```json
{
  "workflow_id": "unique-workflow-id",
  "workflow_type": "greenfield-swift|brownfield-enhancement|health-check",
  "project_name": "User provided project name",
  "operation_mode": "interactive|batch|yolo",

  "project_discovery": {
    "project_concept": "Brief description from user",
    "existing_inputs": "What user has already",
    "discovery_completed": false,
    "discovery_timestamp": "ISO timestamp"
  },

  "enhancement_discovery": {
    "enhancement_description": "For brownfield only",
    "affected_components": "frontend|backend|both",
    "constraints": "Any specific requirements"
  },

  "current_phase": "discovery|analyst|pm|architect|prp_creator|implementation",
  "phase_status": "initiating|in_progress|completed",

  "elicitation_completed": {
    "discovery": false,
    "analyst": false,
    "pm": false,
    "architect": false,
    "prp_creator": false
  },

  "elicitation_history": [
    {
      "phase": "phase_name",
      "timestamp": "ISO timestamp",
      "method": "elicitation_method_used",
      "result": "summary_of_outcome"
    }
  ],

  "agent_context": {
    "current_agent": "orchestrator|analyst|pm|architect",
    "transformation_history": [],
    "passed_context": {}
  }
}
```

### Phase 1.5: Workflow Configuration Updates

#### Files: `.codex/workflows/*.yaml` (All workflow files)

**Example: `.codex/workflows/greenfield-swift.yaml`**

**Add Discovery Phase**:

```yaml
phases:
  - id: discovery
    agent: orchestrator
    required: true
    tasks:
      - project_discovery
      - context_capture
    outputs:
      - project_context
      - discovery_completed

  - id: analyst
    agent: analyst
    required: true
    requires: discovery.completed
    inputs:
      - project_context
    validation:
      level_0:
        check: discovery_completed = true
        elicit: true
```

## Implementation Steps

### Step-by-Step Execution Plan

1. **Hour 1-2: Orchestrator Enhancement**
   - Backup current orchestrator.md
   - Implement universal discovery protocol (lines 118-137)
   - Add transformation pattern (new section after line 151)
   - Test with sample commands

2. **Hour 3: Analyst Agent Updates**
   - Backup current analyst.md
   - Add workflow-aware activation (lines 23-28)
   - Implement content creation pattern (after line 141)
   - Verify integration with orchestrator

3. **Hour 4: Elicitation Task Fixes**
   - Update advanced-elicitation.md menu format
   - Correct response handling for 1-9 format
   - Ensure method selection strategy aligns with BMAD

4. **Hour 5: State Management**
   - Create new workflow.json template
   - Update state tracking logic
   - Test state persistence through transformations

5. **Hour 6: Testing & Refinement**
   - Test greenfield workflow: `/codex start greenfield-swift TestProject`
   - Test brownfield workflow: `/codex start brownfield-enhancement`
   - Verify discovery → transformation → elicitation flow
   - Fine-tune based on test results

## Expected User Experience

### Greenfield Workflow Example

```
User: /codex start greenfield-swift AgDealership

CODEX: What's your project name/working title?
> Ag Dealership Inventory

CODEX: Brief project concept: (describe what you're building)
> Multi-location inventory management system for agricultural equipment dealerships

CODEX: Any existing inputs? (research, brainstorming, or starting fresh?)
> starting fresh

CODEX: 📊 Transforming into Business Analyst
Perfect! Let's begin creating your Project Brief for the Ag Dealership Inventory system.

Section 1: Executive Summary
[Rich content with rationale, trade-offs, assumptions, validation areas]

Please select an option:
1. Proceed to next section
2. Expand or Contract for Audience
3. Critique and Refine
4. Identify Potential Risks
[etc...]

Select 1-9 or type your feedback:
```

### Brownfield Workflow Example

```
User: /codex start brownfield-enhancement

CODEX: [Checking for existing project context...]
I found documentation for "Ag Dealership Inventory": A multi-location inventory
management system for agricultural equipment dealerships.

Is this the project you want to enhance? (yes/no)
> yes

CODEX: What enhancement or feature are you adding?
> Equipment maintenance scheduling module

CODEX: Which components will this affect? (frontend/backend/both)
> both

CODEX: Any specific constraints or requirements?
> Must integrate with existing service department workflows

CODEX: 📊 Transforming into Business Analyst
Let me document this enhancement for your Ag Dealership Inventory system...
```

## Success Criteria

1. ✅ No multiple confirmations before workflow starts
2. ✅ Basic project discovery before complex elicitation
3. ✅ Correct 1-9 elicitation menu format
4. ✅ Rich content creation matching BMAD depth
5. ✅ Universal support for all workflow types
6. ✅ Transformation pattern instead of Task delegation
7. ✅ Context preservation through agent transitions

## Risk Mitigation

1. **Backup all files before modification**
2. **Test each component individually before integration**
3. **Maintain fallback to current behavior if issues arise**
4. **Document all changes in git commits**
5. **Create test cases for each workflow type**

## Validation Checklist

Before considering implementation complete:

- [ ] Greenfield workflow completes successfully
- [ ] Brownfield workflow recognizes existing context
- [ ] Health-check workflow bypasses discovery
- [ ] Elicitation menu shows 1-9 format correctly
- [ ] Content sections include rationale and trade-offs
- [ ] Agent transformations work smoothly
- [ ] State persists through workflow phases
- [ ] No regression in existing validation enforcement

## Appendix: Key BMAD References

### Critical BMAD Files and Line Numbers

1. **`.bmad-core/agents/bmad-orchestrator.md`**
   - Lines 36-48: Persona definition for transformation
   - Lines 113-117: Transformation behavior
   - Lines 57-67: Command structure

2. **`.bmad-core/templates/project-brief-tmpl.yaml`**
   - Lines 11-26: Workflow mode configuration
   - Lines 28-38: Introduction with mode selection
   - Lines 40-223: Section-by-section template

3. **`.bmad-core/tasks/advanced-elicitation.md`**
   - Lines 22-30: Usage scenario for template creation
   - Lines 83-98: Menu format specification
   - Lines 99-104: Response handling

4. **`.bmad-core/data/elicitation-methods.md`**
   - Lines 7-157: Complete elicitation method definitions

5. **`.bmad-core/utils/workflow-management.md`**
   - Lines 8-72: Workflow execution patterns

## Notes

This implementation maintains all existing Level 0 validation enforcement while dramatically improving the user experience through:

1. Proper discovery before elicitation
2. Universal workflow support
3. Rich content creation
4. Correct menu formatting
5. Agent transformation pattern

The changes are designed to be backward compatible and can be rolled back if needed.