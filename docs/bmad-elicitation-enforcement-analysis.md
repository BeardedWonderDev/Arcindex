# BMAD Elicitation Enforcement Analysis

**Analysis Date:** 2025-09-24
**Purpose:** Deep dive into how BMAD enforces elicitation at the workflow level to guide CODEX implementation of anti-YOLO mechanisms
**Status:** Complete Analysis

---

## Executive Summary

BMAD implements a sophisticated multi-layered elicitation enforcement system that prevents "YOLO mode" (bypassing user interaction) through explicit HARD STOPs, workflow validation, and template-driven constraints. The system uses both technical enforcement mechanisms and clear workflow patterns to ensure user interaction is mandatory at critical decision points.

**Key Finding:** BMAD prevents YOLO mode through **explicit workflow violations** that trigger when agents attempt to bypass required user interaction points.

---

## 1. HARD STOP Implementation Mechanisms

### 1.1 Workflow Violation Indicators

**File:** `.codex/tasks/create-doc.md` (Lines 10-16, 24-40)

BMAD implements explicit "VIOLATION INDICATOR" patterns:

```markdown
## ⚠️ CRITICAL EXECUTION NOTICE ⚠️
**THIS IS AN EXECUTABLE WORKFLOW - NOT REFERENCE MATERIAL**

1. **DISABLE ALL EFFICIENCY OPTIMIZATIONS** - This workflow requires full user interaction
2. **MANDATORY STEP-BY-STEP EXECUTION** - Each section must be processed sequentially with user feedback
3. **ELICITATION IS REQUIRED** - When `elicit: true`, you MUST use the 1-9 format and wait for user response
4. **NO SHORTCUTS ALLOWED** - Complete documents cannot be created without following this workflow

**VIOLATION INDICATOR:** If you create a complete document without user interaction, you have violated this workflow.
```

### 1.2 Hard Stop Enforcement Language

**Critical Enforcement Phrases:**
- **"HARD STOP requiring user interaction"** (Line 24)
- **"WAIT FOR USER RESPONSE - Do not proceed until user selects option"** (Line 34)
- **"WORKFLOW VIOLATION: Creating content for elicit=true sections without user interaction violates this task"** (Line 36)

### 1.3 Technical Prevention Mechanisms

```markdown
**CRITICAL: Mandatory Elicitation Format**

**When `elicit: true`, this is a HARD STOP requiring user interaction:**

**YOU MUST:**
1. Present section content
2. Provide detailed rationale (explain trade-offs, assumptions, decisions made)
3. **STOP and present numbered options 1-9:**
   - **Option 1:** Always "Proceed to next section"
   - **Options 2-9:** Select 8 methods from .codex/data/elicitation-methods.md
   - End with: "Select 1-9 or just type your question/feedback:"
4. **WAIT FOR USER RESPONSE** - Do not proceed until user selects option or provides feedback
```

---

## 2. Template-Level Elicitation Enforcement

### 2.1 Template Flag System

**File:** `.bmad-core/templates/prd-tmpl.yaml`

BMAD uses explicit `elicit: true` flags in YAML templates to enforce interaction:

```yaml
workflow:
  mode: interactive
  elicitation: advanced-elicitation

sections:
  - id: requirements
    title: Requirements
    instruction: Draft the list of functional and non functional requirements
    elicit: true    # <-- ENFORCEMENT FLAG

  - id: ui-goals
    title: User Interface Design Goals
    elicit: true    # <-- MANDATORY INTERACTION

  - id: technical-assumptions
    title: Technical Assumptions
    elicit: true    # <-- PREVENTS BYPASSING
```

### 2.2 Template Validation Requirements

**Story Template Example** (`.bmad-core/templates/story-tmpl.yaml`):

```yaml
sections:
  - id: story
    title: Story
    elicit: true        # <-- REQUIRES USER INPUT
    owner: scrum-master
    editors: [scrum-master]

  - id: acceptance-criteria
    title: Acceptance Criteria
    elicit: true        # <-- MANDATORY INTERACTION

  - id: tasks-subtasks
    title: Tasks / Subtasks
    elicit: true        # <-- PREVENTS AUTOMATION
```

---

## 3. 1-9 Option Format Enforcement

### 3.1 Mandatory Format Structure

**Advanced Elicitation Task** (`.claude/commands/BMad/tasks/advanced-elicitation.md`):

```markdown
**Action List Presentation Format:**

```text
**Advanced Elicitation Options**
Choose a number (0-8) or 9 to proceed:

0. [Method Name]
1. [Method Name]
2. [Method Name]
3. [Method Name]
4. [Method Name]
5. [Method Name]
6. [Method Name]
7. [Method Name]
8. [Method Name]
9. Proceed / No Further Actions
```

**Response Handling:**
- **Numbers 0-8**: Execute the selected method, then re-offer the choice
- **Number 9**: Proceed to next section or continue conversation
```

### 3.2 Method Selection Intelligence

The system intelligently selects 9 methods based on context analysis:

```markdown
**Context Analysis**: Before presenting options, analyze:
- **Content Type**: Technical specs, user stories, architecture, requirements, etc.
- **Complexity Level**: Simple, moderate, or complex content
- **Stakeholder Needs**: Who will use this information
- **Risk Level**: High-impact decisions vs routine items
- **Creative Potential**: Opportunities for innovation or alternatives
```

---

## 4. Workflow-Level Validation Gates

### 4.1 Quality Assurance Integration

**File:** `.claude/commands/BMad/tasks/qa-gate.md`

BMAD implements comprehensive validation at workflow level:

```yaml
## Gate Decision Criteria

### PASS
- All acceptance criteria met
- No high-severity issues
- Test coverage meets project standards

### CONCERNS
- Non-blocking issues present
- Should be tracked and scheduled
- Can proceed with awareness

### FAIL
- Acceptance criteria not met
- High-severity issues present
- Recommend return to InProgress

### WAIVED
- Issues explicitly accepted
- Requires approval and reason
- Proceed despite known issues
```

### 4.2 Progressive Validation System

**Enhanced IDE Development Workflow** (`.bmad-core/enhanced-ide-development-workflow.md`):

```markdown
| **Stage**                | **Command** | **Purpose**                             | **Priority**                |
| ------------------------ | ----------- | --------------------------------------- | --------------------------- |
| **After Story Approval** | `*risk`     | Identify integration & regression risks | High for complex/brownfield |
|                          | `*design`   | Create test strategy for dev            | High for new features       |
| **During Development**   | `*trace`    | Verify test coverage                    | Medium                      |
|                          | `*nfr`      | Validate quality attributes             | High for critical features  |
| **After Development**    | `*review`   | Comprehensive assessment                | **Required**                |
```

---

## 5. Workflow Orchestration Controls

### 5.1 Brownfield Workflow Enforcement

**File:** `.bmad-core/workflows/brownfield-fullstack.yaml`

BMAD workflows include explicit decision points:

```yaml
sequence:
  - step: enhancement_classification
    agent: analyst
    action: classify enhancement scope
    notes: |
      Ask user: "Can you describe the enhancement scope? Is this a small fix, a feature addition, or a major enhancement requiring architectural changes?"

  - step: routing_decision
    condition: based_on_classification
    routes:
      single_story:
        agent: pm
        uses: brownfield-create-story
        notes: "Create single story for immediate implementation. Exit workflow after story creation."
```

### 5.2 Agent Handoff Validation

Each workflow step requires explicit validation before proceeding:

```yaml
handoff_prompts:
  classification_complete: |
    Enhancement classified as: {{enhancement_type}}
    {{if single_story}}: Proceeding with brownfield-create-story task for immediate implementation.
    {{if small_feature}}: Creating focused epic with brownfield-create-epic task.
    {{if major_enhancement}}: Continuing with comprehensive planning workflow.
```

---

## 6. Prevention of Efficiency Optimizations

### 6.1 Explicit Efficiency Disabling

**File:** `.codex/tasks/create-doc.md` (Line 11)

```markdown
1. **DISABLE ALL EFFICIENCY OPTIMIZATIONS** - This workflow requires full user interaction
```

### 6.2 YOLO Mode as Explicit Override

BMAD acknowledges YOLO mode but makes it an **explicit user choice**:

```markdown
## YOLO Mode
User can type `#yolo` to toggle to YOLO mode (process all sections at once).
```

**Key Point:** YOLO mode requires explicit user activation - it's not the default behavior.

---

## 7. State Tracking and Validation

### 7.1 Elicitation Completion Tracking

BMAD tracks whether elicitation has been completed before allowing workflow progression:

```yaml
context_management:
  validation_required: "zero_knowledge_test"
  checkpoint_frequency: 600  # seconds

validation:
  - context_completeness_for_pm: true
  - business_case_clarity: true
  - elicitation_completed: true    # <-- VALIDATION FLAG
```

### 7.2 Agent Permission System

Templates include ownership and editing permissions to control who can modify sections:

```yaml
sections:
  - id: status
    title: Status
    owner: scrum-master
    editors: [scrum-master, dev-agent]
  - id: story
    title: Story
    elicit: true
    owner: scrum-master
    editors: [scrum-master]  # <-- PREVENTS UNAUTHORIZED CHANGES
```

---

## 8. Specific Anti-YOLO Patterns for CODEX Implementation

Based on this analysis, CODEX needs to implement these specific mechanisms:

### 8.1 Template Validation Engine

```javascript
// Pseudo-code for CODEX implementation
function validateTemplateExecution(template, sectionId) {
  const section = template.sections.find(s => s.id === sectionId);

  if (section.elicit === true) {
    if (!userInteractionCompleted(sectionId)) {
      throw new WorkflowViolationError(
        "HARD STOP: Section requires user interaction via 1-9 elicitation format"
      );
    }
  }

  return validateSectionContent(section);
}
```

### 8.2 Workflow State Validation

```javascript
function validateWorkflowProgression(currentPhase, nextPhase) {
  const currentValidation = workflow.phases[currentPhase].validation;

  for (const requirement of currentValidation) {
    if (requirement.includes('elicitation_completed') &&
        !state.elicitationCompleted[currentPhase]) {
      throw new WorkflowViolationError(
        "Cannot proceed: Elicitation not completed for current phase"
      );
    }
  }
}
```

### 8.3 Agent Coordination Enforcement

```javascript
function enforceAgentHandoff(fromAgent, toAgent, context) {
  // Validate "zero knowledge test"
  if (!passesZeroKnowledgeTest(context)) {
    throw new ContextViolationError(
      "Context handoff fails zero knowledge validation"
    );
  }

  // Check elicitation completion
  if (context.elicitationRequired && !context.elicitationCompleted) {
    throw new ElicitationViolationError(
      "Agent handoff blocked: Required elicitation not completed"
    );
  }
}
```

---

## 9. Implementation Recommendations for CODEX

### 9.1 Hard Stop Implementation

**Implement explicit workflow violation detection:**

1. **Template Parser:** Scan for `elicit: true` flags
2. **Violation Detector:** Monitor for content creation without interaction
3. **Hard Stop Enforcer:** Block workflow progression until interaction complete
4. **State Validator:** Verify elicitation completion before agent handoffs

### 9.2 User Interaction Enforcement

**Required mechanisms:**

1. **1-9 Format Validator:** Ensure exact format compliance
2. **Method Selection Engine:** Intelligently choose elicitation methods
3. **Response Handler:** Process user selections and feedback
4. **Loop Controller:** Continue elicitation until user chooses "proceed"

### 9.3 Anti-Efficiency Safeguards

**Prevent automated bypassing:**

1. **Efficiency Optimizer Disabler:** Explicitly disable shortcuts
2. **Step-by-Step Enforcer:** Require sequential section processing
3. **Interaction Tracker:** Log all user interactions for validation
4. **Override Controller:** Make YOLO mode explicit user choice only

### 9.4 Quality Gate Integration

**Progressive validation enforcement:**

1. **Phase Gate Validator:** Check completion before progression
2. **Agent Handoff Validator:** Ensure context completeness
3. **Zero Knowledge Tester:** Validate handoff documents
4. **State Persistence:** Track validation completion status

---

## 10. Specific Code Patterns for CODEX

### 10.1 Template Elicitation Flag Processing

```yaml
# CODEX Template Enhancement
sections:
  - id: requirements
    title: Requirements
    instruction: "Draft functional and non-functional requirements"
    elicit: true                    # <-- HARD STOP FLAG
    validation_required: true       # <-- PREVENTS BYPASS
    hard_stop: true                # <-- EXPLICIT ENFORCEMENT
    interaction_format: "1-9"      # <-- FORMAT SPECIFICATION
    methods_source: ".codex/data/elicitation-methods.md"
```

### 10.2 Workflow Orchestrator Enhancement

```yaml
# CODEX Workflow Enhancement
sequence:
  - agent: analyst
    creates: "docs/project-brief.md"
    template: "project-brief-template.yaml"
    elicitation:
      required: true                # <-- MANDATORY FLAG
      checkpoint: "after_brief"     # <-- STATE TRACKING
      validation: "user_interaction_complete"
      hard_stop_on_bypass: true     # <-- EXPLICIT PREVENTION
    validation:
      - elicitation_completed: true  # <-- PROGRESSION BLOCKER
      - context_completeness: true
```

### 10.3 Agent Communication Protocol

```markdown
# CODEX Agent Handoff Protocol

## Elicitation Validation Required

Before any agent handoff, validate:

1. **Template Sections:** All `elicit: true` sections completed
2. **User Interaction:** 1-9 format responses recorded
3. **Method Execution:** Selected elicitation methods applied
4. **Context Validation:** Zero knowledge test passed
5. **State Persistence:** Elicitation status saved

**HANDOFF BLOCKER:** If any validation fails, return to source agent with specific feedback.
```

---

## 11. Key Implementation Insights

### 11.1 BMAD's Success Factors

1. **Explicit Language:** Uses "HARD STOP," "VIOLATION," and "MANDATORY"
2. **Technical Enforcement:** Template flags prevent bypassing
3. **State Tracking:** Records interaction completion
4. **Progressive Gates:** Multiple validation layers
5. **User Choice:** YOLO mode available but explicit

### 11.2 Critical Enforcement Points

1. **Template Processing:** `elicit: true` creates mandatory stops
2. **Workflow Progression:** State validation before phase changes
3. **Agent Handoffs:** Context completeness verification
4. **Quality Gates:** Progressive validation requirements
5. **User Override:** Explicit YOLO activation only

### 11.3 Anti-Pattern Prevention

1. **Efficiency Optimization Disabling:** Explicit instructions
2. **Shortcut Prevention:** Step-by-step enforcement
3. **Automated Bypassing:** Workflow violation detection
4. **Context Loss:** Zero knowledge validation
5. **Quality Degradation:** Multi-level validation gates

---

## Conclusion

BMAD prevents YOLO mode through a sophisticated combination of:

1. **Template-level enforcement** (`elicit: true` flags)
2. **Workflow validation gates** (progression blockers)
3. **Explicit violation detection** (hard stop language)
4. **State tracking mechanisms** (interaction completion)
5. **Agent handoff validation** (zero knowledge tests)

**For CODEX:** Implement all five enforcement layers with explicit violation detection and hard stop mechanisms to ensure elicitation cannot be bypassed without explicit user choice.

The key insight is that BMAD treats elicitation as a **workflow requirement**, not a user convenience, and implements technical mechanisms to enforce this at multiple levels of the system architecture.

---

**Analysis completed:** All BMAD elicitation enforcement mechanisms documented and analyzed for CODEX implementation guidance.