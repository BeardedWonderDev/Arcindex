# CODEX-BMAD Integration Plan: Complete Implementation Guide

## Executive Summary

This document provides a comprehensive plan for integrating BMAD's proven interactive elicitation and validation patterns into CODEX to solve the "YOLO mode" problem and create structured, guided workflows. The integration should be an almost direct clone/port of BMAD methods for the analyst, PM, and architect phases.

## Core Integration Principle

**BMAD methods should be directly ported, not adapted.** The analyst, PM, and architect workflows in CODEX should function identically to their BMAD counterparts, with only minimal modifications for CODEX-specific context.

## Part 1: Direct Port Requirements

### 1.1 Analyst Agent and Project Brief Workflow

#### Files to Port/Clone:
```
BMAD Source → CODEX Destination
.bmad-core/agents/analyst.md → .codex/agents/analyst.md (UPDATE)
.bmad-core/templates/project-brief-tmpl.yaml → .codex/templates/project-brief-tmpl.yaml (NEW)
.bmad-core/tasks/create-doc.md → .codex/tasks/create-doc.md (UPDATE)
```

#### Implementation Requirements:

**A. Agent Persona Update**
```yaml
# Update .codex/agents/analyst.md with BMAD persona
persona:
  role: Insightful Analyst & Strategic Ideation Partner
  style: Inquisitive, creative, strategic, thorough
  identity: Business Analyst specialized in eliciting and refining project concepts
  focus: Creating comprehensive project briefs through structured elicitation
```

**B. Template Structure (Direct Clone)**
```yaml
# .codex/templates/project-brief-tmpl.yaml
workflow:
  mode: interactive
  elicitation: advanced-elicitation
  custom_elicitation:
    title: "Project Brief Elicitation Actions"
    options:
      - "Expand section with more specific details"
      - "Validate against similar successful products"
      - "Stress test assumptions with edge cases"
      - "Explore alternative solution approaches"
      - "Analyze resource/constraint trade-offs"
      - "Generate risk mitigation strategies"
      - "Challenge scope from MVP minimalist view"
      - "Brainstorm creative feature possibilities"
      - "If only we had [resource/capability/time]..."
      - "Proceed to next section"

sections:
  - id: executive-summary
    elicit: true  # MANDATORY USER INTERACTION
    instruction: |
      Create 1-2 sentence concept description, primary problem, target market, value proposition
  # ... (complete section list from BMAD)
```

**C. Mandatory Elicitation Enforcement**
```markdown
# Add to .codex/agents/analyst.md
## ⚠️ CRITICAL EXECUTION NOTICE ⚠️

**THIS IS AN EXECUTABLE WORKFLOW - NOT REFERENCE MATERIAL**

1. **DISABLE ALL EFFICIENCY OPTIMIZATIONS** - This workflow requires full user interaction
2. **MANDATORY STEP-BY-STEP EXECUTION** - Each section must be processed sequentially
3. **ELICITATION IS REQUIRED** - When `elicit: true`, you MUST use the 1-9 format
4. **NO SHORTCUTS ALLOWED** - Complete documents cannot be created without following this workflow

**When `elicit: true`, this is a HARD STOP requiring user interaction:**

**YOU MUST:**
1. Present section content
2. Provide detailed rationale (explain trade-offs, assumptions, decisions made)
3. **STOP and present numbered options 1-9:**
4. **WAIT FOR USER RESPONSE** - Do not proceed until user selects option or provides feedback

**VIOLATION INDICATOR:** If you create a complete document without user interaction, you have violated this workflow.
```

### 1.2 PM Agent and PRD Workflows

#### Files to Port/Clone:
```
BMAD Source → CODEX Destination
.bmad-core/agents/pm.md → .codex/agents/pm.md (UPDATE)
.bmad-core/templates/prd-tmpl.yaml → .codex/templates/prd-tmpl.yaml (NEW)
.bmad-core/templates/brownfield-prd-tmpl.yaml → .codex/templates/brownfield-prd-tmpl.yaml (NEW)
.bmad-core/checklists/pm-checklist.md → .codex/checklists/pm-checklist.md (NEW)
```

#### Implementation Requirements:

**A. Dual PRD Workflow Support**
```yaml
# .codex/workflows/greenfield-swift.yaml (UPDATE)
phases:
  - id: pm
    agent: pm
    template: prd-tmpl.yaml  # For greenfield

# .codex/workflows/brownfield-enhancement.yaml (NEW)
phases:
  - id: pm
    agent: pm
    template: brownfield-prd-tmpl.yaml  # For brownfield
```

**B. Brownfield Detection Instructions**
```markdown
# Add to PM agent activation instructions
## Project Type Detection Protocol

**IMPORTANT - SCOPE ASSESSMENT REQUIRED:**

1. **Assess Enhancement Complexity:**
   - If this is a simple feature addition (1-2 stories), STOP
   - Recommend using brownfield-create-epic workflow instead

2. **Project Context Detection:**
   - Check if working in IDE with project loaded
   - Look for existing source files, package.json, requirements.txt, etc.
   - If existing codebase detected: Use brownfield-prd-tmpl.yaml
   - If new/empty project: Use standard prd-tmpl.yaml

3. **Deep Assessment Requirement:**
   - MUST thoroughly analyze existing project structure
   - Review architecture patterns, dependencies, conventions
   - Document all constraints from existing system

4. **User Confirmation:**
   - Present: "I've detected this is a [greenfield/brownfield] project because [evidence]"
   - Ask: "Should I proceed with [greenfield/brownfield] PRD template?"
```

**C. Epic Structure Enforcement**
```yaml
# Critical pattern from BMAD
epics:
  validation:
    - sequential: true  # Epics must be logically ordered
    - deliverable: true  # Each epic must be deployable
    - foundation_first: true  # Epic 1 establishes infrastructure
    - value_delivery: true  # Each epic delivers value

  story_requirements:
    - vertical_slice: true  # Complete functionality
    - no_forward_dependencies: true  # No dependencies on later work
    - ai_agent_sized: true  # 2-4 hours of focused work
    - single_session_completable: true  # One agent, one session
```

### 1.3 Architect Agent and Architecture Workflow

#### Files to Port/Clone:
```
BMAD Source → CODEX Destination
.bmad-core/agents/architect.md → .codex/agents/architect.md (UPDATE)
.bmad-core/templates/architecture-tmpl.yaml → .codex/templates/architecture-tmpl.yaml (NEW)
.bmad-core/checklists/architect-checklist.md → .codex/checklists/architect-checklist.md (NEW)
```

#### Implementation Requirements:

**A. Holistic Architecture Approach**
```yaml
# Port complete persona with principles
persona:
  role: Holistic System Architect & Full-Stack Technical Leader
  core_principles:
    - Holistic System Thinking
    - User Experience Drives Architecture
    - Pragmatic Technology Selection
    - Progressive Complexity
    - Cross-Stack Performance Focus
    - Developer Experience as First-Class Concern
    - Security at Every Layer
    - Data-Centric Design
    - Cost-Conscious Engineering
    - Living Architecture
```

**B. Technology Selection Gates**
```yaml
# Architecture template section with mandatory elicitation
sections:
  - id: technology-stack
    title: Technology Stack
    elicit: true  # HARD STOP for user confirmation
    instruction: |
      This is the DEFINITIVE technology selection section. Work with the user to make specific choices:
      1. Review PRD technical assumptions and preferences
      2. For each category, present 2-3 viable options with pros/cons
      3. Make a clear recommendation based on project needs
      4. Get explicit user approval for each selection
      5. Document exact versions (avoid "latest" - pin specific versions)
      6. This table is the single source of truth

      **MANDATORY USER INTERACTION:**
      - Present options in numbered format
      - WAIT for user selection
      - Document user's choice with rationale
```

## Part 2: Five-Layer Elicitation Enforcement System

### Layer 1: Template-Level Flags
```yaml
# In all templates
sections:
  - id: section_name
    elicit: true  # Creates hard stop
    hard_stop_on_bypass: true
    interaction_format: "1-9"
```

### Layer 2: Workflow Violation Detection
```markdown
# Natural language violation detection in orchestrator.md
## ⚠️ WORKFLOW VIOLATION DETECTION ⚠️

**VIOLATION INDICATOR:** If any of these occur, the workflow has been violated:
1. Creating complete documents without user interaction when elicit=true
2. Proceeding past HARD STOP without user selection (1-9)
3. Skipping elicitation for efficiency when mode is "interactive"
4. Generating full phase outputs without checkpoint validation

**ENFORCEMENT:** When violation detected:
- STOP execution immediately
- Report: "WORKFLOW VIOLATION: Created content without required user interaction"
- Require explicit user acknowledgment to continue
```

### Layer 3: Hard Stop Language
```markdown
# Agent instruction update
When encountering `elicit: true`:
1. Present content
2. Show "**HARD STOP - User Interaction Required**"
3. Display 1-9 options
4. WAIT for response (no automatic progression)
```

### Layer 4: State Validation Gates
```yaml
# Workflow YAML state tracking (greenfield-swift.yaml)
handoff_validation:
  elicitation_check: |
    **VALIDATION CHECKPOINT**
    Before proceeding to {{next_phase}}:
    - Was elicitation completed for all required sections? [YES/NO]
    - Did user provide explicit selections (1-9) for each elicit=true section? [YES/NO]
    - Are all mandatory interactions tracked in workflow state? [YES/NO]

    **If ANY answer is NO:** WORKFLOW VIOLATION - Cannot proceed

state_tracking:
  analyst_phase:
    sections_requiring_elicitation: [executive-summary, problem-statement, proposed-solution]
    elicitation_completed: []
    user_interactions: []
```

### Layer 5: Agent Handoff Validation
```yaml
# Workflow YAML update
handoff_validation:
  - zero_knowledge_test: true
  - elicitation_completion: mandatory
  - context_completeness: required
  - user_approval: explicit
```

## Part 3: Implementation Sequence

### Phase 1: Foundation (Day 1-2)
1. **Port elicitation methods data**
   - Copy `.bmad-core/data/elicitation-methods.md` → `.codex/data/elicitation-methods.md`
   - Keep all 20+ methods intact

2. **Update orchestrator agent**
   ```markdown
   # Add to .codex/agents/orchestrator.md
   ## Elicitation Enforcement Protocol

   CRITICAL: At each workflow phase transition:
   1. Check for `elicit: true` flags
   2. HARD STOP - Present 1-9 options
   3. WAIT for user selection
   4. Track completion in state
   5. VALIDATE before handoff

   ## Mode Selection
   At workflow start:
   1. Interactive Mode (default) - Step-by-step with elicitation
   2. Batch Mode - Execute with comprehensive reporting
   3. YOLO Mode - Full automation (require "#yolo" confirmation)
   ```

### Phase 2: Agent Integration (Day 3-4)
1. **Port analyst workflow**
   - Clone project-brief-tmpl.yaml
   - Update analyst.md with BMAD persona
   - Add elicitation enforcement

2. **Port PM workflows**
   - Clone both PRD templates
   - Implement brownfield detection
   - Add epic validation rules

3. **Port architect workflow**
   - Clone architecture-tmpl.yaml
   - Add technology selection gates
   - Implement validation checklist

### Phase 3: State Management (Day 5)
1. **Enhance workflow state tracking**
   ```json
   // .codex/state/workflow.json enhancement (maintain existing JSON format)
   {
     "workflow": {
       "id": "wf_123",
       "mode": "interactive",  // interactive|batch|yolo
       "phases": {
         "analyst": {
           "status": "in_progress",
           "elicitation_required": true,
           "elicitation_completed": false,
           "sections_completed": [],
           "sections_requiring_elicitation": [
             "executive-summary",
             "problem-statement",
             "proposed-solution"
           ],
           "user_interactions": []
         }
       }
     }
   }
   ```

2. **Create validation instructions**
   ```markdown
   # .codex/agents/orchestrator.md addition

   ## Elicitation Validation Protocol

   **VALIDATION RULES:**
   1. Cannot proceed without elicitation completion
   2. Must track user selections (1-9 format)
   3. Validate all elicit=true sections have user interaction
   4. Check for violation patterns:
      - Complete documents created without interaction
      - Sections skipped for efficiency
      - User selections not recorded

   **VIOLATION RESPONSE:**
   - STOP workflow execution
   - Report: "WORKFLOW VIOLATION DETECTED"
   - Require user acknowledgment
   - Document violation in workflow state
   ```

### Phase 4: Testing and Validation (Day 6-7)
1. **Create test workflows**
   - Interactive mode test
   - Batch mode with reporting
   - YOLO mode with override

2. **Validation checklist**
   - [ ] Elicitation gates block progression
   - [ ] User interactions tracked in state
   - [ ] Violations detected and reported
   - [ ] Handoffs validate elicitation completion
   - [ ] Mode selection works correctly

## Part 4: Critical Success Factors

### Must-Have Features
1. **1-9 Option Format**: Exact format from BMAD, no variations
2. **Hard Stop Enforcement**: Cannot bypass without explicit override
3. **State Persistence**: Track all interactions across sessions
4. **Violation Detection**: Flag and report workflow violations
5. **Mode Selection**: User chooses interaction level upfront

### Quality Gates
1. **Elicitation Completion**: 100% for interactive mode
2. **User Control**: Full control at every decision point
3. **Context Preservation**: Zero knowledge handoffs work
4. **Documentation Quality**: Matches BMAD output quality
5. **Workflow Compliance**: No unauthorized bypasses

### Anti-Patterns to Avoid
1. **Automatic Progression**: Never proceed without user input when elicit=true
2. **Efficiency Shortcuts**: Resist optimizing away interaction points
3. **Incomplete Ports**: Must port complete workflows, not partial
4. **Modified Formats**: Keep 1-9 format exactly as BMAD implements
5. **Weak Enforcement**: Hard stops must be truly blocking

## Part 5: Validation Metrics

### Success Criteria
- **Elicitation Rate**: 100% of elicit=true sections trigger interaction
- **Violation Detection**: 100% of bypasses detected and reported
- **User Satisfaction**: Increased control and visibility
- **Quality Improvement**: PRDs and architecture docs match BMAD quality
- **Workflow Completion**: 95%+ successful workflow completions

### Testing Protocol
1. Run workflow without user → Should fail with violation
2. Run with minimal interaction → Should demand full interaction
3. Run with #yolo flag → Should bypass with warning
4. Run interactive mode → Should stop at every elicit=true
5. Check state persistence → Should track all interactions

## Conclusion

The integration of BMAD methods into CODEX requires a direct port of the analyst, PM, and architect workflows with their complete elicitation and validation systems. The key is to resist the temptation to "optimize" or "streamline" - BMAD's deliberate friction points create quality through mandatory user engagement.

By implementing the five-layer enforcement system and maintaining strict adherence to the 1-9 option format, CODEX will transform from an autonomous "YOLO mode" system into a guided, interactive development methodology that ensures quality through structured user participation at critical decision points.

The implementation should take approximately one week, with immediate benefits visible after Phase 1 (foundation) is complete. The most critical aspect is updating the orchestrator to enforce elicitation gates - without this, all other improvements will be ineffective.