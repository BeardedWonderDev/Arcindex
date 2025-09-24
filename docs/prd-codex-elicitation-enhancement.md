# CODEX Interactive Elicitation Enhancement Brownfield PRD

## Intro Project Analysis and Context

### Existing Project Overview

#### Analysis Source
- IDE-based fresh analysis combined with extensive documentation review

#### Current Project State
CODEX (Context Oriented Development and Engineering Experience) is a fully implemented AI-assisted development workflow orchestration system. It coordinates specialized agents through systematic workflow phases to achieve context-aware, high-quality code generation with built-in validation. The system currently operates in "YOLO mode" by default, automatically progressing through workflow phases without user interaction.

### Available Documentation Analysis

#### Available Documentation
✓ Tech Stack Documentation (via project files analysis)
✓ Source Tree/Architecture (.codex directory structure)
✓ Coding Standards (implicit in workflow definitions)
✓ API Documentation (agent interfaces documented)
✓ External API Documentation (Task tool integration)
✗ UX/UI Guidelines (N/A - command-line tool)
✓ Technical Debt Documentation (identified in analysis)
✓ Other: Complete PRP documentation, workflow YAML files, agent specifications

### Enhancement Scope Definition

#### Enhancement Type
✓ Major Feature Modification
✓ Integration with New Systems (BMAD elicitation patterns)

#### Enhancement Description
Integrate BMAD's proven interactive elicitation system into CODEX workflows to replace the current "YOLO mode" execution with mandatory user interaction points at workflow phase transitions, using the established 1-9 option format for gathering user feedback and refinement.

#### Impact Assessment
✓ Significant Impact (substantial existing code changes)
- Requires modifications to core orchestrator agent
- Updates needed across all workflow YAML files
- State management enhancements for tracking elicitation

### Goals and Background Context

#### Goals
- Eliminate unintended "YOLO mode" execution by enforcing user interaction at critical points
- Port BMAD's proven elicitation patterns directly into CODEX without modification
- Ensure comprehensive user input gathering that matches BMAD quality standards
- Implement five-layer enforcement system to prevent elicitation bypassing
- Maintain backward compatibility while adding interaction requirements

#### Background Context
The current CODEX system automatically executes workflow phases without user interaction, leading to assumptions and potentially misaligned outputs. BMAD has proven that mandatory elicitation using a structured 1-9 option format significantly improves document quality and user satisfaction. This enhancement brings CODEX to feature parity with BMAD by implementing the same interaction patterns that have been successful in production use.

### Change Log
| Change | Date | Version | Description | Author |
|--------|------|---------|-------------|--------|
| Initial Draft | 2025-09-24 | 1.0 | Created brownfield PRD for elicitation enhancement | John (PM) |

## Requirements

### Functional Requirements

**FR1:** The CODEX orchestrator SHALL enforce mandatory user interaction at each workflow phase transition when operating in interactive mode (default).

**FR2:** The system SHALL implement the exact 1-9 option elicitation format from BMAD, presenting 8 contextually relevant elicitation methods plus a "proceed" option.

**FR3:** Each workflow phase SHALL validate elicitation completion before allowing progression to the next phase, creating a "hard stop" that cannot be bypassed programmatically.

**FR4:** The system SHALL track all user interactions and elicitation choices in the workflow state file for audit and recovery purposes.

**FR5:** The orchestrator SHALL detect and report workflow violations when agents attempt to bypass required elicitation points.

**FR6:** The system SHALL support three operational modes: Interactive (default with mandatory elicitation), Batch (automated with comprehensive reporting), and YOLO (full automation requiring explicit "#yolo" user confirmation).

**FR7:** All YAML templates SHALL support `elicit: true` flags that trigger mandatory interaction requirements at the section level.

**FR8:** The system SHALL intelligently select appropriate elicitation methods from `.codex/data/elicitation-methods.md` based on the current context and content type.

**FR9:** Agent handoffs SHALL validate that all required elicitation has been completed before accepting context documents.

**FR10:** The system SHALL preserve all existing CODEX functionality while adding the elicitation layer, ensuring no regression in core capabilities.

### Non-Functional Requirements

**NFR1:** The elicitation interface SHALL respond to user input within 100ms to maintain a responsive interactive experience.

**NFR2:** The system SHALL maintain the existing file-based state management approach, adding elicitation tracking without changing the fundamental persistence mechanism.

**NFR3:** All elicitation prompts SHALL use clear, consistent language that matches BMAD's proven patterns for user comprehension.

**NFR4:** The system SHALL gracefully handle interruptions during elicitation, allowing users to resume from the last completed interaction point.

**NFR5:** Error messages for workflow violations SHALL be explicit and actionable, clearly indicating what elicitation was skipped and how to comply.

**NFR6:** The elicitation system SHALL add no more than 5% overhead to the total workflow execution time when in batch mode.

**NFR7:** Documentation SHALL be updated to reflect all new interaction requirements with clear examples of each elicitation scenario.

**NFR8:** The implementation SHALL follow existing CODEX patterns for agent communication, using the Task tool for coordination without introducing new dependencies.

### Compatibility Requirements

**CR1:** Existing CODEX workflow YAML files SHALL remain functional with minimal modifications limited to adding elicitation flags.

**CR2:** The current state management JSON structure SHALL be extended rather than replaced, preserving backward compatibility with existing state files.

**CR3:** All agent interfaces through the Task tool SHALL continue to function without modification to the core coordination mechanism.

**CR4:** Integration with Claude Code's native slash commands and agent system SHALL remain unchanged, with elicitation added as an internal workflow enhancement.

## Technical Constraints and Integration Requirements

### Existing Technology Stack

**Languages**: Pure Claude Code agent instructions (natural language)
**Frameworks**: Claude Code Agent Framework, YAML configuration system
**Database**: File-based JSON state management
**Infrastructure**: Local file system, Git version control
**External Dependencies**: Task tool (agent coordination), Slash command system, Claude Code native capabilities

### Integration Approach

**Database Integration Strategy**: Extend existing JSON state files with elicitation tracking fields. Maintain current file-based approach with added properties for interaction history, elicitation completion status per phase, and user selection tracking.

**API Integration Strategy**: Leverage existing Task tool interfaces without modification. Add elicitation validation as pre-handoff checks within agent instructions. Use natural language enforcement through agent instruction modifications.

**Frontend Integration Strategy**: Command-line interaction remains unchanged. Elicitation prompts use standard text output with numbered options. No new UI components required - pure text-based interaction through Claude Code interface.

**Testing Integration Strategy**: Extend existing workflow testing to include elicitation scenarios. Add violation detection tests. Create test harnesses for all three modes (interactive, batch, YOLO).

### Code Organization and Standards

**File Structure Approach**: Maintain existing `.codex/` directory structure. Add elicitation methods to `.codex/data/elicitation-methods.md`. Update existing files in-place rather than creating new parallel structures.

**Naming Conventions**: Follow CODEX conventions - kebab-case for files, camelCase for properties in JSON, YAML for configuration, Markdown for agent instructions and documentation.

**Coding Standards**: Natural language instructions in agent files. YAML schema consistency across templates. Maintain zero-code implementation approach using declarative configuration and agent instructions.

**Documentation Standards**: Update existing agent instruction blocks with enforcement notices. Add violation indicators clearly marked with ⚠️ symbols. Document elicitation requirements in workflow YAML comments.

### Deployment and Operations

**Build Process Integration**: No build process required - pure configuration and agent instruction changes. Version control tracks YAML and Markdown changes. No compilation or bundling needed.

**Deployment Strategy**: Rolling update via Git. Users pull latest changes to get elicitation features. Feature flag in config enables gradual rollout (elicitation_enabled: true/false initially).

**Monitoring and Logging**: Elicitation interactions logged to workflow state JSON. Violation detection logged to `.codex/debug-log.md` per CODEX patterns. User selections tracked for audit trail in `.codex/state/` directory.

**Configuration Management**: New config section in `.codex/config/codex-config.yaml` for elicitation settings. Mode selection (interactive/batch/yolo) configurable per workflow. Elicitation method preferences customizable.

### Risk Assessment and Mitigation

**Technical Risks**:
- Agent instruction parsing may not enforce hard stops consistently in Claude Code
- Natural language enforcement could be circumvented by sophisticated prompts
- State file corruption could lose elicitation history

**Integration Risks**:
- Existing workflows might break if elicitation is too rigid
- Agent handoff validation could create deadlocks
- Task tool timeouts during user interaction pauses

**Deployment Risks**:
- Users with existing workflows in progress may experience interruptions
- Backward compatibility issues with older state files
- Learning curve for users accustomed to automatic execution

**Mitigation Strategies**:
- Implement elicitation as opt-in initially, then make default after validation
- Add comprehensive violation detection with clear error messages
- Create state file migration utility for backward compatibility
- Provide detailed documentation with examples
- Add recovery mechanism for interrupted elicitation sessions
- Test extensively with real CODEX workflows before release

## Epic and Story Structure

### Epic Approach

**Epic Structure Decision**: Single comprehensive epic focused on implementing the complete elicitation system across CODEX. This is the optimal approach because:

1. All changes are interdependent - partial implementation would leave the system in an inconsistent state
2. The enhancement represents a cohesive feature addition rather than multiple unrelated changes
3. Testing and validation require the complete system to verify enforcement works end-to-end
4. User experience demands consistency - having elicitation in some phases but not others would be confusing

The epic will be broken into sequential stories that can be implemented incrementally while maintaining system stability at each step.

## Epic 1: CODEX Interactive Elicitation Enhancement

**Epic Goal**: Transform CODEX from automatic "YOLO mode" execution to an interactive, user-guided workflow system by implementing BMAD's proven elicitation patterns at all critical decision points.

**Integration Requirements**: All modifications must preserve existing CODEX functionality while adding mandatory interaction layers. Changes are limited to agent instructions, workflow YAML configurations, and state management enhancements.

### Story 1.1: Foundation - Port Elicitation Infrastructure

As a CODEX developer,
I want to establish the elicitation foundation by porting BMAD's elicitation methods and patterns,
so that the system has the necessary infrastructure for interactive workflows.

**Acceptance Criteria:**
1. `.codex/data/elicitation-methods.md` created with all 20+ BMAD elicitation methods
2. `.codex/config/codex-config.yaml` updated with elicitation configuration section
3. Elicitation mode flags (interactive/batch/yolo) defined in config
4. State schema documented for elicitation tracking fields
5. No impact on existing workflow execution

**Integration Verification:**
- IV1: Existing CODEX workflows continue to execute without modification
- IV2: Config file changes are backward compatible
- IV3: No performance impact on current automated workflows

### Story 1.2: Orchestrator Agent Enhancement

As a CODEX user,
I want the orchestrator agent to enforce elicitation at phase transitions,
so that I have control over workflow progression and can provide input at critical points.

**Acceptance Criteria:**
1. `.codex/agents/orchestrator.md` updated with elicitation enforcement protocol
2. Violation detection language added with clear indicators
3. HARD STOP implementation at phase boundaries
4. Mode selection prompt at workflow initiation
5. State tracking for elicitation completion per phase

**Integration Verification:**
- IV1: Orchestrator continues to coordinate agents via Task tool
- IV2: Existing automated workflows work when YOLO mode selected
- IV3: State files maintain compatibility with current structure

### Story 1.3: Workflow YAML Template Updates

As a CODEX user,
I want workflow templates to specify elicitation requirements,
so that critical sections require my review and input before proceeding.

**Acceptance Criteria:**
1. `.codex/workflows/greenfield-swift.yaml` updated with elicitation checkpoints
2. `.codex/workflows/brownfield-enhancement.yaml` created with elicitation points
3. `elicit: true` flags added to critical workflow sections
4. Handoff validation rules include elicitation completion checks
5. Template documentation updated with elicitation syntax

**Integration Verification:**
- IV1: Workflows without elicit flags continue unchanged
- IV2: YAML schema remains valid and parseable
- IV3: Agent handoffs function with added validation

### Story 1.4: Create-Doc Task Enhancement

As a CODEX user,
I want the document creation process to include interactive elicitation,
so that generated documents reflect my input and refinements.

**Acceptance Criteria:**
1. `.codex/tasks/create-doc.md` updated with BMAD elicitation workflow
2. 1-9 option format implemented exactly as BMAD specifies
3. Violation indicators added for skipped elicitation
4. Section-by-section processing with user interaction
5. YOLO mode override requires explicit "#yolo" command

**Integration Verification:**
- IV1: Existing document generation works in YOLO mode
- IV2: Template processing maintains current functionality
- IV3: Output documents maintain expected format

### Story 1.5: Agent Instruction Updates for Elicitation

As a CODEX user,
I want all workflow agents to respect elicitation requirements,
so that analyst, PM, and architect phases include proper user interaction.

**Acceptance Criteria:**
1. `.codex/agents/analyst.md` updated with BMAD persona and elicitation
2. `.codex/agents/pm.md` updated with elicitation enforcement
3. `.codex/agents/architect.md` updated with technology selection gates
4. Each agent includes violation detection language
5. Zero knowledge handoff validation includes elicitation checks

**Integration Verification:**
- IV1: Agents maintain current capabilities when elicitation disabled
- IV2: Task tool coordination continues to function
- IV3: Agent outputs remain compatible with downstream phases

### Story 1.6: State Management and Recovery

As a CODEX user,
I want the system to track my elicitation choices and allow session recovery,
so that interrupted workflows can resume from the last interaction point.

**Acceptance Criteria:**
1. `.codex/state/workflow.json` schema extended with elicitation tracking
2. User interaction history persisted after each selection
3. Recovery mechanism detects incomplete elicitation
4. Violation events logged to `.codex/debug-log.md`
5. State migration utility created for existing workflows

**Integration Verification:**
- IV1: Existing state files remain readable
- IV2: State persistence maintains current performance
- IV3: Recovery doesn't interfere with completed workflows

### Story 1.7: Testing and Documentation

As a CODEX user,
I want comprehensive documentation and examples of the elicitation system,
so that I understand how to effectively use the interactive features.

**Acceptance Criteria:**
1. README updated with elicitation modes and usage
2. Example workflows demonstrating all three modes
3. Violation scenarios documented with resolutions
4. Migration guide for existing CODEX users
5. Test cases covering elicitation enforcement

**Integration Verification:**
- IV1: Documentation maintains accuracy for existing features
- IV2: Examples work with current CODEX installation
- IV3: Tests validate both new and existing functionality

---

## Summary

This brownfield PRD provides a comprehensive plan for enhancing CODEX with BMAD's interactive elicitation system. The enhancement will transform CODEX from an automatic "YOLO mode" executor to an interactive, user-guided workflow system that ensures quality through mandatory user engagement at critical decision points.

The implementation follows a low-risk, incremental approach that maintains full backward compatibility while adding powerful new interaction capabilities. Through seven carefully sequenced stories, CODEX will gain the same level of user control and document quality that BMAD has proven effective in production use.

**Story Sequencing Rationale:**
- Stories are ordered to build infrastructure first, then core enforcement, followed by specific implementations, and finally state/recovery with documentation
- Each story is sized for completion in a single Claude Code session (2-4 hours)
- Dependencies flow logically - no story depends on later work
- System remains functional after each story completion
- Risk is minimized by implementing opt-in features before making them mandatory