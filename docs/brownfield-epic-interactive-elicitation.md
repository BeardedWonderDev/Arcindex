# CODEX Interactive Elicitation Enhancement - Brownfield Epic

**Date Created:** 2025-09-24
**Epic Type:** Brownfield Enhancement
**Created By:** John (PM Agent)
**Project:** CODEX Orchestration System

---

## Problem Analysis

### Issue Identified
The current CODEX orchestrator command is not providing any interactive elicitation prompts with the user and executes in "YOLO" mode, automatically implementing project plans and creating documents based solely on the project name when running the `codex greenfield swift` command. This bypasses the proven interactive patterns established by BMAD analyst, pm, and architect agents.

### Root Cause Analysis
- **Missing Component:** Interactive elicitation at workflow phase transitions
- **Current Behavior:** Automated progression through workflow phases without user input
- **Expected Behavior:** Mandatory user interaction using BMAD's proven 1-9 option elicitation format
- **Impact:** Reduces quality and user control over workflow outcomes

---

## Project Context Analysis

### Current Project Overview

**Project Purpose:** CODEX (Context Oriented Development and Engineering Experience) is a unified AI-assisted development workflow system that orchestrates specialized agents through systematic phases to achieve context-aware, high-quality code generation with built-in validation.

**Technology Stack:**
- Claude Code native slash commands and agents
- YAML-driven workflow definitions
- Markdown-based agent specifications
- File-based state management
- Git integration for version control
- Task tool for agent coordination

**Architecture Patterns:**
- Agent-based orchestration through Task tool
- Zero prior knowledge document handoffs
- Context breakpoint management
- 4-level progressive validation system
- Template-driven document generation
- BMAD-style elicitation with 1-9 options (currently missing)

**Integration Points:**
- `.codex/agents/orchestrator.md` - Main workflow coordinator
- `.codex/workflows/*.yaml` - Workflow definitions
- `.codex/templates/*.yaml` - Document templates
- `.codex/tasks/create-doc.md` - Document creation with elicitation

### Current System State
- CODEX infrastructure is fully implemented per PRP specification
- All agents and workflow files exist and are functional
- Missing interactive elicitation that should mirror BMAD patterns
- System defaults to automated execution without user confirmation

---

## Epic Definition

### **CODEX Interactive Elicitation Enhancement - Brownfield Enhancement**

#### Epic Goal
Enhance the CODEX orchestration workflow to include mandatory interactive elicitation prompts at each phase transition, ensuring comprehensive user input gathering that mirrors the proven BMAD agent interaction patterns, preventing the "YOLO" mode execution that bypasses critical user feedback.

#### Epic Description

**Existing System Context:**
- Current relevant functionality: CODEX orchestrator launches workflow phases automatically without user interaction
- Technology stack: Claude Code agents, YAML workflows, Task tool coordination
- Integration points: `.codex/agents/orchestrator.md`, workflow YAML files, template systems

**Enhancement Details:**
- What's being added/changed: Add interactive elicitation at each workflow phase transition using BMAD's proven 1-9 option format
- How it integrates: Modify orchestrator agent and workflow templates to enforce elicitation points before phase progression
- Success criteria: Each workflow phase requires user confirmation and refinement before proceeding to the next phase

#### Stories

1. **Story 1:** Add mandatory elicitation points to orchestrator agent workflow coordination logic
   - Modify `.codex/agents/orchestrator.md` to enforce elicitation at phase transitions
   - Integrate with existing `.codex/data/elicitation-methods.md` patterns

2. **Story 2:** Update workflow YAML templates to include elicitation requirements at phase transitions
   - Enhance `.codex/workflows/greenfield-swift.yaml` with elicitation checkpoints
   - Add elicitation validation to workflow execution logic

3. **Story 3:** Modify agent handoff protocol to validate user interaction completion before proceeding
   - Update context handoff validation in `.codex/tasks/context-handoff.md`
   - Ensure state persistence includes elicitation completion status

#### Compatibility Requirements

- [ ] Existing CODEX workflow structure remains unchanged
- [ ] YAML workflow definitions maintain backward compatibility
- [ ] Agent coordination through Task tool continues to function
- [ ] File-based state management preserves existing patterns
- [ ] Zero prior knowledge document handoffs remain intact

#### Risk Mitigation

- **Primary Risk:** Breaking existing automated workflow execution
- **Mitigation:** Add elicitation as optional configuration flag initially, then make mandatory
- **Rollback Plan:** Revert orchestrator agent to bypass elicitation if system becomes unusable

#### Definition of Done

- [ ] Orchestrator agent enforces elicitation at each phase transition
- [ ] Users must interact via 1-9 option format before workflow progression
- [ ] All existing workflow functionality verified through testing
- [ ] Documentation updated to reflect interactive requirements
- [ ] No regression in automated workflow capabilities when elicitation is disabled
- [ ] State management properly tracks elicitation completion
- [ ] Context breakpoints include elicitation status validation

---

## Technical Analysis

### Files Requiring Modification

**Primary Files:**
- `.codex/agents/orchestrator.md` - Add elicitation enforcement logic
- `.codex/workflows/greenfield-swift.yaml` - Add elicitation checkpoints
- `.codex/tasks/context-handoff.md` - Validate elicitation completion

**Supporting Files:**
- `.codex/config/codex-config.yaml` - Add elicitation configuration options
- `.codex/state/workflow.json` - Track elicitation completion status
- `.codex/data/elicitation-methods.md` - Already exists, ensure integration

### Integration Patterns

**Elicitation Pattern (from BMAD):**
```yaml
elicitation:
  required: true
  format: "1-9 numbered options"
  option_1: "Proceed to next section"
  methods: "From .codex/data/elicitation-methods.md"
  validation: "User must select option before progression"
```

**Workflow Enhancement Pattern:**
```yaml
sequence:
  - agent: analyst
    creates: docs/project-brief.md
    template: project-brief-template.yaml
    elicitation:
      required: true
      checkpoint: "after_brief_creation"
    validation:
      - context_completeness: true
      - elicitation_completed: true
```

### Existing Patterns to Leverage

**From BMAD System:**
- `.bmad-core/data/elicitation-methods.md` - Proven elicitation techniques
- `.bmad-core/tasks/create-doc.md` - Template with mandatory elicitation
- `.bmad-core/agents/pm.md` - Reference implementation with elicitation

**From CODEX System:**
- `.codex/agents/orchestrator.md` - Central coordination point
- `.codex/workflows/greenfield-swift.yaml` - Workflow sequence definition
- `.codex/state/workflow.json` - State persistence structure

---

## Story Manager Handoff

**Context for Detailed Story Development:**

"Please develop detailed user stories for this brownfield epic. Key considerations:

- This is an enhancement to an existing CODEX orchestration system using Claude Code agents and YAML workflows
- Integration points: `.codex/agents/orchestrator.md` (main coordinator), workflow YAML files, template elicitation systems
- Existing patterns to follow: BMAD's mandatory 1-9 elicitation format from `.bmad-core/data/elicitation-methods.md`
- Critical compatibility requirements: Must not break existing automated workflow capabilities
- Each story must include verification that current CODEX functionality remains intact while adding interactive requirements

The epic should maintain system integrity while delivering mandatory user interaction at workflow phase transitions."

---

## Success Metrics

### Validation Criteria

**User Experience:**
- Users receive interactive prompts at each workflow phase
- Elicitation follows proven 1-9 option format
- Workflow cannot progress without user interaction
- Clear feedback when elicitation is required

**Technical Integration:**
- No regression in existing CODEX functionality
- State management properly tracks elicitation status
- Context handoffs include elicitation validation
- Configuration allows elicitation to be enabled/disabled

**Quality Assurance:**
- All existing test workflows continue to pass
- New elicitation workflows complete successfully
- Error handling gracefully manages elicitation failures
- Documentation accurately reflects new interactive requirements

---

## Next Steps

1. **Story Development:** Create detailed user stories with acceptance criteria
2. **Technical Design:** Design elicitation integration architecture
3. **Implementation Planning:** Sequence development tasks by dependency
4. **Testing Strategy:** Plan validation of both new and existing functionality
5. **Migration Path:** Plan rollout strategy for existing CODEX users

---

*This document captures the complete analysis and epic definition for enhancing CODEX with interactive elicitation capabilities, addressing the "YOLO" mode issue identified in the current implementation.*