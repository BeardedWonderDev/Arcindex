# Task Tool Agent Pattern Analysis: Multi-Phase Workflow Architecture

## Executive Summary

This document analyzes how BMAD and CODEX leverage Claude Code's Task tool for agent spawning in multi-phase workflows where each phase requires isolated context but state must persist across the workflow. The analysis reveals a sophisticated pattern that combines **direct agent transformation** for sequential workflow phases with **parallel Task tool spawning** for quality enhancement, creating an architecture that balances context isolation with state continuity.

## Core Architecture Pattern

### Two Distinct Agent Coordination Patterns

BMAD/CODEX employ two complementary agent coordination patterns:

#### 1. **Agent Transformation Protocol** (Sequential Phase Transitions)
- **Purpose**: Direct persona transformation for main workflow phase transitions
- **Mechanism**: Orchestrator reads agent definition file and adopts complete persona
- **Context**: Isolated - each agent gets clean context window
- **State**: Persistent via `.codex/state/workflow.json`
- **Use Case**: Discovery → Analyst → PM → Architect → PRP Creator → Dev

#### 2. **Task Tool Coordination** (Parallel Quality Enhancement)
- **Purpose**: Launch specialized agents for parallel execution and quality enhancement
- **Mechanism**: Task tool spawns independent agent instances
- **Context**: Isolated - each spawned agent operates independently
- **State**: Results aggregated back to coordinating agent
- **Use Case**: Parallel code review, language-specific validation, research tasks

## Key Insight: Why Two Patterns?

The dual pattern exists because:

1. **Sequential workflow phases** (Analyst → PM → Architect) need:
   - Fresh context windows (prevent token overflow)
   - Complete persona adoption (deep role immersion)
   - Direct access to workflow state
   - Ability to update persistent state
   - Mode-aware elicitation behavior

2. **Parallel enhancement tasks** (Swift reviewers, QA agents) need:
   - Simultaneous execution (efficiency)
   - Specialized expertise (narrow focus)
   - Independence from main workflow state
   - Results aggregation without state pollution

## State Persistence Architecture

### The Critical File: `.codex/state/workflow.json`

This file is the **persistent state anchor** that enables context isolation while maintaining workflow continuity:

```json
{
  "workflow_id": "uuid",
  "workflow_type": "greenfield-swift",
  "current_phase": "architect",
  "operation_mode": "interactive",
  "completed_phases": ["discovery", "analyst", "pm"],
  "elicitation_required": {
    "discovery": true,
    "analyst": true,
    "pm": true,
    "architect": true
  },
  "elicitation_completed": {
    "discovery": true,
    "analyst": true,
    "pm": true,
    "architect": false
  },
  "project_discovery": {
    "project_name": "MyApp",
    "concept": "iOS task manager",
    "inputs": "Existing design mockups"
  },
  "documents": {
    "project-brief": "docs/project-brief.md",
    "prd": "docs/prd.md"
  },
  "transformation_history": [
    {
      "timestamp": "2025-10-03T10:00:00Z",
      "from_agent": "orchestrator",
      "to_agent": "analyst",
      "operation_mode": "interactive",
      "elicitation_completed": true
    }
  ],
  "last_updated": "2025-10-03T10:15:00Z"
}
```

### State Manager Task: The Middleware

Located at `.codex/tasks/state-manager.md`, this task provides:

1. **State Initialization**: Create runtime state from template
2. **State Updates**: Track phase transitions, elicitation completion, mode changes
3. **State Validation**: Ensure integrity and consistency
4. **State Queries**: Provide state information to agents and validation gates

**Critical Pattern**: Every agent reads `workflow.json` on activation to understand:
- What phase they're in
- What operation mode to use (interactive/batch/yolo)
- What context was discovered
- What elicitation is required

## Agent Transformation Protocol (Sequential Phases)

### How It Works

```yaml
# From orchestrator.md - agent-transformation-protocol
agent-transformation-protocol:
  - Purpose: Direct agent transformation for workflow phase transitions

  Transformation Process:
    1. MANDATORY: Execute validate-phase.md BEFORE transformation
    2. MODE PROPAGATION: Read operation_mode from workflow.json
    3. If validation fails: HALT and complete elicitation first
    4. Only after validation passes:
       - Match workflow phase to specialized agent persona
       - Update state to new phase via state-manager.md
       - Read agent definition file (.codex/agents/{agent}.md)
       - Announce transformation: "📊 Transforming into Business Analyst [Mode: {mode}]"
       - Adopt complete agent persona from file
       - Pass discovered project context and workflow state WITH MODE
       - Execute agent tasks until phase completion
       - Return to orchestrator for next phase transition

  Context Passing:
    - project_discovery or enhancement_discovery from state
    - workflow type and current phase information
    - elicitation history relevant to agent
    - operation_mode (critical for behavior)
    - mode-specific elicitation behavior rules
```

### Example Transformation Flow

```
1. Orchestrator (current phase)
   ↓
2. Read workflow.json → operation_mode: "interactive"
   ↓
3. Execute validate-phase.md → Check elicitation_completed["discovery"]
   ↓
4. Validation passes → Read .codex/agents/analyst.md
   ↓
5. Announce: "🎯 Transforming into Business Analyst [Mode: interactive]"
   ↓
6. Orchestrator BECOMES analyst (adopts complete persona)
   ↓
7. Analyst reads workflow.json for project_discovery context
   ↓
8. Analyst executes with interactive mode elicitation
   ↓
9. Analyst completes → Updates workflow.json with completion
   ↓
10. Returns control to orchestrator (transformation ends)
```

**Key Point**: This is NOT Task tool spawning - it's **direct persona adoption** within the same conversation thread. The orchestrator literally reads the analyst agent file and becomes that agent.

## Task Tool Coordination (Parallel Execution)

### When Task Tool IS Used

From the codebase analysis:

```yaml
# From orchestrator.md - agent-coordination
agent-coordination:
  - MANDATORY VALIDATION BEFORE LAUNCH: Always run validate-phase.md before Task tool usage
  - PRE-LAUNCH CHECKLIST:
    - Execute validate-phase.md for current_phase validation
    - Only launch agents after validation passes
  - Launch specialized agents via Task tool for parallel execution
  - Pass validation results and elicitation context to launched agents
  - Manage agent handoffs with complete context preservation
  - Coordinate with global language agents in ~/.claude/agents/
  - Aggregate agent feedback and validation results
```

### Example: PRP Creator Using Task Tool

From `.codex/agents/prp-creator.md`:

```yaml
codebase-analysis:
  create-todos: "Plan systematic codebase analysis using TodoWrite"
  spawn-subagents: "Use Task tool to spawn parallel subagents for codebase search"
  search-targets:
    - Similar features and patterns in codebase
    - Existing naming conventions to follow
    - Test patterns for validation approach
    - File organization and structure patterns
  tools: ["Grep", "Glob", "Read", "Task (for subagent spawning)"]

external-research:
  create-todos: "Plan deep external research with specific search targets"
  spawn-subagents: "Use Task tool for parallel research on documentation and examples"
  research-targets:
    - Library documentation with specific URLs
    - Implementation examples from GitHub
    - Best practices and common pitfalls
    - Security considerations
```

### Example: Dev Agent Using Task Tool for Language Agent Coordination

From `.codex/agents/dev.md`:

```yaml
Language Agent Coordination:
  - Swift agent orchestration for iOS/macOS
  - Parallel agent execution via Task tool
  - Quality enhancement through specialization
  - Coordinated refactoring and optimization
```

### Workflow Definition: Multi-Agent Coordination

From `docs/codex-architecture.md` - greenfield-swift.yaml:

```yaml
phase: implementation_coordination
primary_agent: dev
language_agents:
  - swift-feature-developer
  - swift-syntax-reviewer
  - swift-architecture-reviewer
  - swift-performance-reviewer
  - ios-security-auditor

coordination:
  - agent: dev
    action: prp_execution_prep
    validates: ["prp_context_completeness", "referenced_files_exist"]

  - agents: [dev, swift-feature-developer]
    action: parallel_implementation
    tasks: ["core_feature_implementation", "test_generation"]

  - agents: [swift-syntax-reviewer, swift-architecture-reviewer]
    action: quality_enhancement
    input: "implementation_files"
    output: "enhanced_implementation"

  - agent: swift-performance-reviewer
    action: performance_optimization
    condition: "performance_requirements_in_prd"

  - agent: ios-security-auditor
    action: security_validation
    mandatory: true

  - agent: dev
    action: validation_orchestration
    executes: ["level_1_validation", "level_2_validation"]
    requires: "all_language_agents_complete"
```

## Context Isolation vs State Persistence: The Pattern

### Problem Being Solved

Multi-phase workflows face a fundamental tension:

1. **Need Context Isolation**: Each phase needs fresh context to prevent token overflow
2. **Need State Continuity**: Each phase builds on previous phase outputs
3. **Need Quality Enhancement**: Parallel specialized agents improve results
4. **Need Validation Gates**: Prevent progression without requirements met

### Solution Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PERSISTENT STATE LAYER                    │
│                  .codex/state/workflow.json                  │
│                                                              │
│  - workflow_type, current_phase, operation_mode             │
│  - project_discovery context                                │
│  - elicitation_required/completed tracking                  │
│  - transformation_history                                   │
│  - document locations                                       │
└─────────────────────────────────────────────────────────────┘
                            ↑↓ Read/Write via state-manager.md
┌─────────────────────────────────────────────────────────────┐
│              SEQUENTIAL PHASE EXECUTION LAYER                │
│                (Agent Transformation Protocol)               │
│                                                              │
│  Orchestrator → Analyst → PM → Architect → PRP → Dev        │
│                                                              │
│  Each transformation:                                        │
│  1. Read workflow.json for context/mode                     │
│  2. Validate elicitation via validate-phase.md              │
│  3. Transform to new agent persona                          │
│  4. Execute with fresh context window                       │
│  5. Update workflow.json with results                       │
│  6. Return to orchestrator                                  │
└─────────────────────────────────────────────────────────────┘
                            ↑↓ Spawns parallel agents via Task tool
┌─────────────────────────────────────────────────────────────┐
│           PARALLEL QUALITY ENHANCEMENT LAYER                 │
│               (Task Tool Coordination)                       │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Swift       │  │  Syntax      │  │  Performance │      │
│  │  Developer   │  │  Reviewer    │  │  Reviewer    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         ↓                 ↓                  ↓               │
│  ┌────────────────────────────────────────────────┐         │
│  │    Results Aggregated by Coordinating Agent   │         │
│  └────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### Key Mechanisms

#### 1. State Persistence via File System

**Pattern**: Use persistent JSON file as single source of truth

```yaml
State Persistence Mechanism:
  file: .codex/state/workflow.json
  manager: .codex/tasks/state-manager.md

  Operations:
    - initialize_state: Create from template on workflow start
    - update_phase: Record phase transitions
    - record_elicitation: Track user interactions
    - track_documents: Register created artifacts
    - update_mode: Change operation mode

  Access Pattern:
    - Every agent reads on activation
    - Updates via state-manager.md task
    - Validation gates check before progression
    - Survives conversation interruptions
```

#### 2. Context Isolation via Agent Transformation

**Pattern**: Fresh agent = fresh context, but reads shared state

```yaml
Context Isolation Mechanism:
  method: Agent persona transformation

  Isolation:
    - New agent has no memory of previous agent's thinking
    - Fresh context window prevents token overflow
    - Clean slate for specialized reasoning

  Continuity:
    - Reads workflow.json for discovered context
    - Accesses documents created by previous phases
    - Understands operation mode and requirements
    - Knows what elicitation is required

  Result: Isolated context + continuous state
```

#### 3. Parallel Execution via Task Tool

**Pattern**: Spawn independent agents, aggregate results

```yaml
Parallel Execution Mechanism:
  tool: Claude Code Task tool

  Spawning:
    - Primary agent invokes Task tool
    - Multiple agents specified in single call
    - Each agent operates independently
    - No shared state between spawned agents

  Aggregation:
    - Task tool returns when all complete
    - Primary agent receives all results
    - Primary agent synthesizes findings
    - Primary agent updates workflow state

  Result: Parallel work + centralized coordination
```

#### 4. Validation Gates for Quality Control

**Pattern**: Block progression without requirements met

```yaml
Validation Gate Mechanism:
  task: .codex/tasks/validate-phase.md

  Execution:
    - Called before EVERY phase transition
    - Reads workflow.json for elicitation status
    - Checks operation_mode for requirements
    - Blocks if elicitation incomplete

  Enforcement:
    - Interactive mode: Section-level validation
    - Batch mode: Phase-level validation
    - YOLO mode: Bypass with logging

  Result: Quality gates + flexible modes
```

## Practical Example: Complete Workflow Execution

### Scenario: Building iOS Task Manager App

#### Phase 1: Orchestrator Discovery

```
User: /codex start greenfield-swift MyTaskApp

Orchestrator:
1. Initialize workflow.json via state-manager.md
   {
     "workflow_type": "greenfield-swift",
     "project_name": "MyTaskApp",
     "current_phase": "discovery",
     "operation_mode": "interactive"  // Default
   }

2. Ask discovery questions:
   - "What are you building with MyTaskApp?"
   - "Do you have existing materials?"
   - "Technical considerations?"

3. Update workflow.json with project_discovery:
   {
     "project_discovery": {
       "concept": "iOS task manager with sync",
       "inputs": "Figma designs available",
       "tech_prefs": "SwiftUI, Core Data"
     }
   }

4. Present elicitation menu (interactive mode)
5. User selects "1. Proceed to next phase"
6. Update elicitation_completed["discovery"]: true
7. Run validate-phase.md → PASS
8. Transform to analyst
```

#### Phase 2: Analyst (Agent Transformation)

```
Analyst activation:
1. Read workflow.json:
   - operation_mode: "interactive"
   - project_discovery: { concept, inputs, tech_prefs }
   - current_phase: "analyst"

2. Read validation-gate.md for Level 0 enforcement

3. Execute create-doc.md task:
   - Load project-brief-template.yaml
   - Process section-by-section (interactive mode)
   - Present elicitation menu after each section
   - User provides feedback
   - Update section based on feedback

4. Complete project-brief.md document

5. Update workflow.json:
   {
     "documents": { "project-brief": "docs/project-brief.md" },
     "completed_phases": ["discovery", "analyst"],
     "current_phase": "pm",
     "elicitation_completed": { "analyst": true }
   }

6. Return to orchestrator
```

#### Phase 3: PM (Agent Transformation)

```
PM activation:
1. Read workflow.json:
   - operation_mode: "interactive"
   - documents.project-brief: "docs/project-brief.md"
   - current_phase: "pm"

2. Read docs/project-brief.md for business context

3. Execute create-doc.md task:
   - Load prd-template.yaml
   - Process section-by-section (interactive mode)
   - User provides requirements details
   - Update sections based on feedback

4. Complete prd.md document

5. Update workflow.json with PRD completion

6. Return to orchestrator
```

#### Phase 4: PRP Creator (Uses BOTH Patterns!)

```
PRP Creator activation:
1. Read workflow.json for context and mode

2. Read prd.md and architecture.md

3. CREATE TODOS for research plan:
   - Codebase analysis targets
   - External research targets
   - Documentation to fetch

4. SPAWN PARALLEL AGENTS via Task tool:

   Task tool call:
   "Spawn 3 research agents in parallel:

   Agent 1: Search codebase for:
     - Existing Core Data patterns
     - SwiftUI view patterns
     - Test file organization

   Agent 2: Fetch Swift documentation:
     - Core Data concurrency guide
     - SwiftUI lifecycle docs
     - URLSession sync patterns

   Agent 3: Research examples:
     - GitHub Swift task manager repos
     - Core Data + SwiftUI patterns
     - Sync conflict resolution"

5. WAIT for Task tool to return all results

6. SYNTHESIZE research into PRP sections:
   - Integrate codebase patterns found
   - Reference documentation URLs
   - Include example code snippets
   - Specify technology gotchas

7. Create enhanced PRP with complete context

8. Run validate-phase.md → Check PRP quality

9. Update workflow.json with PRP completion

10. Return to orchestrator
```

#### Phase 5: Dev (Uses Task Tool for Language Agents)

```
Dev activation:
1. Read workflow.json for context

2. Read enhanced PRP (complete implementation context)

3. Execute PRP implementation tasks

4. SPAWN LANGUAGE AGENTS via Task tool:

   Task tool call:
   "Launch Swift quality agents in parallel:

   swift-syntax-reviewer:
     - Review code style
     - Check SwiftUI best practices
     - Verify naming conventions

   swift-architecture-reviewer:
     - Validate MVVM compliance
     - Check dependency injection
     - Review protocol usage

   swift-performance-reviewer:
     - Analyze Core Data queries
     - Check memory management
     - Review async operations

   ios-security-auditor:
     - Validate keychain usage
     - Check data encryption
     - Review authentication"

5. RECEIVE aggregated feedback from all agents

6. APPLY quality enhancements:
   - Refactor based on syntax review
   - Improve architecture per architect feedback
   - Optimize per performance suggestions
   - Fix security issues

7. Run 4-level validation gates:
   - Level 1: SwiftLint, swift build
   - Level 2: Unit tests, XCTest
   - Level 3: Integration tests
   - Level 4: Language agent validation

8. Update workflow.json with completion

9. Return to orchestrator
```

## Critical Patterns Identified

### Pattern 1: "Read State, Execute, Update State"

**Every agent follows this cycle:**

```yaml
Agent Lifecycle:
  1. Activation:
     - Read .codex/state/workflow.json
     - Extract: operation_mode, phase, project_discovery
     - Load validation requirements

  2. Execution:
     - Perform phase-specific work
     - Apply mode-appropriate elicitation
     - Create deliverable documents

  3. Completion:
     - Update workflow.json via state-manager.md
     - Record elicitation completion
     - Add transformation history entry
     - Return to orchestrator
```

### Pattern 2: "Validate Before Transform"

**No phase transition without validation:**

```yaml
Validation Protocol:
  Before every transformation:
    1. Execute validate-phase.md
    2. Check elicitation_completed for current phase
    3. If incomplete: HALT, present elicitation menu
    4. If complete: Allow transformation
    5. Log all transitions in transformation_history
```

### Pattern 3: "Mode Propagation"

**Operation mode flows through entire workflow:**

```yaml
Mode Propagation:
  Discovery:
    - Orchestrator sets initial mode (default: interactive)
    - Stores in workflow.json

  Every Transformation:
    - Read mode from workflow.json
    - Pass mode to next agent
    - Agent applies mode-specific behavior:
      * Interactive: Section-level elicitation
      * Batch: Phase-level elicitation
      * YOLO: Skip elicitation, log decisions

  Mode Changes:
    - User can change mode anytime: /codex interactive|batch|yolo
    - Update workflow.json via state-manager.md
    - Next agent picks up new mode
```

### Pattern 4: "Zero Prior Knowledge Handoffs"

**Each phase outputs complete, standalone documents:**

```yaml
Zero Knowledge Principle:
  Document Requirements:
    - Analyst creates project-brief.md
      * PM can create PRD without asking analyst

    - PM creates prd.md
      * Architect can design without PM context

    - Architect creates architecture.md
      * PRP creator has full technical context

    - PRP creator creates enhanced-prp.md
      * Dev can implement without workflow history

  Validation:
    - "No Prior Knowledge" test at each handoff
    - Document must contain ALL needed context
    - Next agent should never need to ask previous phase
```

### Pattern 5: "Task Tool for Parallelism, Not Progression"

**Task tool spawns helpers, not workflow agents:**

```yaml
Task Tool Usage:
  NOT for:
    - Sequential workflow phase transitions
    - Main orchestration flow
    - State management

  FOR:
    - Parallel research tasks
    - Multiple codebase searches
    - Simultaneous quality reviews
    - Language-specific validators
    - External documentation fetching

  Pattern:
    Primary Agent → Spawn Task agents → Aggregate results → Continue
    (State updated by primary agent only)
```

## State Persistence Deep Dive

### Ephemeral vs Persistent Context

**The Challenge:**

```
Ephemeral Context (Conversation Memory):
  - Lost when agent transformation occurs
  - Lost when conversation ends
  - Lost between Task tool spawns
  - Cannot survive interruptions

Persistent State (workflow.json):
  - Survives agent transformations
  - Survives conversation interruptions
  - Survives system restarts
  - Accessible to all agents
```

**The Solution:**

```yaml
Hybrid Architecture:
  Ephemeral Layer:
    - Agent reasoning and thinking
    - User conversation context
    - Current section being drafted
    - In-progress elicitation

  Persistent Layer:
    - Workflow state and phase
    - Operation mode
    - Project discovery answers
    - Elicitation completion status
    - Document locations
    - Transformation history

  Bridge:
    - Every agent reads persistent state on activation
    - Every agent updates persistent state on completion
    - State-manager.md mediates all state operations
```

### State Manager as Middleware

**Location:** `.codex/tasks/state-manager.md`

**Responsibilities:**

```yaml
State Initialization:
  - Create workflow.json from template
  - Set workflow_type, project_name
  - Initialize operation_mode (default: interactive)
  - Create empty tracking arrays

State Updates:
  - update_phase: Record phase transitions
  - record_elicitation: Track user interactions
  - update_mode: Change operation mode
  - track_documents: Register created files

State Validation:
  - validate_integrity: Check JSON structure
  - validate_elicitation: Verify requirements met
  - validate_phase_transition: Ensure prerequisites

State Queries:
  - get_phase_status: Current phase info
  - get_elicitation_status: Completion tracking
  - get_workflow_status: Overall state
  - get_operation_mode: Current mode
```

### State Schema

**Full workflow.json Structure:**

```json
{
  "workflow_id": "uuid-v4",
  "workflow_type": "greenfield-swift",
  "project_name": "MyTaskApp",
  "current_phase": "architect",
  "operation_mode": "interactive",

  "completed_phases": [
    "discovery",
    "analyst",
    "pm"
  ],

  "elicitation_required": {
    "discovery": true,
    "analyst": true,
    "pm": true,
    "architect": true,
    "prp": true,
    "dev": false
  },

  "elicitation_completed": {
    "discovery": true,
    "analyst": true,
    "pm": true,
    "architect": false
  },

  "project_discovery": {
    "project_name": "MyTaskApp",
    "concept": "iOS task manager with cloud sync",
    "inputs": "Figma designs, competitor analysis",
    "tech_prefs": "SwiftUI, Core Data, CloudKit"
  },

  "documents": {
    "project-brief": "docs/project-brief.md",
    "prd": "docs/prd.md",
    "architecture": "docs/architecture.md"
  },

  "transformation_history": [
    {
      "timestamp": "2025-10-03T10:00:00Z",
      "from_agent": "orchestrator",
      "to_agent": "analyst",
      "operation_mode": "interactive",
      "phase": "analyst",
      "elicitation_completed": true
    },
    {
      "timestamp": "2025-10-03T10:30:00Z",
      "from_agent": "analyst",
      "to_agent": "orchestrator",
      "operation_mode": "interactive",
      "phase": "analyst",
      "documents_created": ["docs/project-brief.md"]
    }
  ],

  "elicitation_history": [
    {
      "phase": "analyst",
      "section": "Problem Statement",
      "timestamp": "2025-10-03T10:15:00Z",
      "method_selected": 2,
      "user_response": "Need to emphasize sync conflicts",
      "applied_changes": "Added sync conflict resolution requirement"
    }
  ],

  "mode_changes": [
    {
      "timestamp": "2025-10-03T11:00:00Z",
      "from_mode": "interactive",
      "to_mode": "batch",
      "phase": "pm",
      "reason": "Speed up PRD creation",
      "initiated_by": "user"
    }
  ],

  "violation_log": [],

  "started_at": "2025-10-03T09:45:00Z",
  "last_updated": "2025-10-03T11:05:00Z",
  "status": "active"
}
```

## Answering the Core Questions

### 1. How are tasks invoked?

**Answer:** Tasks are markdown files loaded and executed by agents, NOT spawned via Task tool.

```yaml
Task Invocation Pattern:
  Location: .codex/tasks/{task-name}.md

  Invocation:
    - Agent references task in their workflow
    - Example: "Execute create-doc.md task"
    - Agent reads task file as instructions
    - Agent follows task instructions step-by-step

  NOT:
    - Task tool spawning
    - Subprocess execution
    - API calls

  IS:
    - Reading markdown instructions
    - Following procedural steps
    - Applying specified patterns
```

### 2. What is the relationship between tasks and agents?

**Answer:** Tasks are **execution procedures** that agents follow. Agents have **personas and capabilities**, tasks have **step-by-step workflows**.

```yaml
Agent vs Task:
  Agent (.codex/agents/{agent}.md):
    - WHO: Identity and persona
    - WHAT: Capabilities and expertise
    - WHEN: Workflow phase and purpose
    - HOW: General approach and principles

  Task (.codex/tasks/{task}.md):
    - PROCEDURE: Step-by-step instructions
    - PATTERN: Reusable workflow template
    - RULES: Mandatory behaviors
    - TOOLS: Specific tool usage patterns

  Relationship:
    - Agents EXECUTE tasks
    - Tasks GUIDE agent behavior
    - Multiple agents can use same task
    - Tasks provide consistency across agents
```

**Example:**

```yaml
Analyst Agent:
  persona: "Investigative, business-focused, thorough"
  capability: "Transform user ideas into structured business requirements"
  executes_task: "create-doc.md"

create-doc Task:
  procedure:
    1. Load template specified by agent
    2. Process template sections in order
    3. For sections with elicit: true, present elicitation menu
    4. Wait for user feedback
    5. Update section based on feedback
    6. Continue to next section

  pattern: "Template-driven document creation with mandatory elicitation"

  reusability: "PM agent also executes create-doc.md with different template"
```

### 3. How is context passed between task executions?

**Answer:** Via **workflow.json state file** and **document artifacts**, NOT through conversation memory.

```yaml
Context Passing Mechanisms:

1. Persistent State File:
   Source: .codex/state/workflow.json
   Contains:
     - project_discovery answers
     - operation_mode
     - elicitation completion status
     - document locations
   Access: Every agent reads on activation
   Updates: Via state-manager.md

2. Document Artifacts:
   Source: Documents created by previous phases
   Examples:
     - docs/project-brief.md (analyst output)
     - docs/prd.md (PM output)
     - docs/architecture.md (architect output)
   Access: Agents read documents they depend on
   Pattern: Zero Prior Knowledge principle

3. Template Context:
   Source: Template YAML files
   Contains:
     - Section structure
     - Required inputs (from: field)
     - Elicitation points
   Usage: create-doc task processes templates

NOT via:
   - Conversation memory (ephemeral)
   - Global variables (don't exist)
   - Agent-to-agent direct communication
```

**Example Context Flow:**

```
Discovery Phase:
  User answers → Stored in workflow.json.project_discovery

Analyst Phase:
  Reads: workflow.json.project_discovery
  Creates: docs/project-brief.md
  Updates: workflow.json.documents["project-brief"]

PM Phase:
  Reads:
    - workflow.json.documents["project-brief"] (location)
    - docs/project-brief.md (content)
  Creates: docs/prd.md
  Updates: workflow.json.documents["prd"]

Architect Phase:
  Reads:
    - workflow.json.documents["prd"]
    - docs/prd.md (content)
  Creates: docs/architecture.md
  Updates: workflow.json.documents["architecture"]
```

### 4. How does state persistence work with ephemeral task contexts?

**Answer:** Each agent has ephemeral conversation context but reads/writes persistent file-based state.

```yaml
Ephemeral Context (Lost on Transformation):
  - Current agent's reasoning
  - User conversation flow
  - Section being drafted
  - Temporary research findings

Persistent State (Survives Everything):
  - workflow.json (state file)
  - Document artifacts (.md files)
  - Code files (if created)

Pattern:
  Agent Activation:
    1. Read workflow.json (restore state)
    2. Read referenced documents
    3. Have complete context despite fresh conversation

  Agent Execution:
    - Work happens in ephemeral context
    - Critical decisions recorded to workflow.json
    - Deliverables saved as files

  Agent Completion:
    - Update workflow.json with results
    - Save all documents
    - Ephemeral context discarded (transformation)

  Next Agent:
    - Fresh context (no memory of previous agent)
    - Reads workflow.json (has all state)
    - Reads documents (has all artifacts)
    - Can proceed without prior conversation context
```

**This is the genius of the architecture:**

- **Ephemeral contexts** prevent token overflow and enable clean reasoning
- **Persistent state** maintains workflow continuity and enables resumption
- **Document artifacts** serve as complete handoffs (Zero Prior Knowledge)
- **State validation** prevents gaps or missing context

### 5. Proper pattern for multi-phase workflow with isolated context but persistent state?

**Answer:** The **Agent Transformation + State Persistence** pattern:

```yaml
Multi-Phase Workflow Pattern:

ARCHITECTURE:
  1. Central State File:
     - .codex/state/workflow.json
     - Single source of truth
     - Survives all transformations

  2. Agent Transformation Protocol:
     - Sequential phase transitions
     - Each agent = fresh context
     - Reads state, executes, updates state

  3. Document Artifacts:
     - Zero Prior Knowledge principle
     - Each phase outputs complete document
     - Next phase reads document for context

  4. Validation Gates:
     - Block progression without requirements
     - Ensure state consistency
     - Maintain quality standards

IMPLEMENTATION STEPS:

Step 1: Define State Schema
  - Create workflow.json.template
  - Define all fields needed
  - Include extensibility for custom data

Step 2: Create State Manager
  - Task file: state-manager.md
  - Operations: init, update, validate, query
  - Enforce consistency

Step 3: Define Agent Transformation Protocol
  - Each agent reads state on activation
  - Validation before transformation
  - Update state on completion
  - Clear transformation announcements

Step 4: Implement Validation Gates
  - validate-phase.md task
  - Checks state before progression
  - Blocks if requirements not met
  - Provides clear error messages

Step 5: Use Document Artifacts
  - Each phase creates complete document
  - Documents follow Zero Prior Knowledge
  - Next phase reads documents, not conversation

Step 6: Add Mode Support (Optional)
  - operation_mode field in state
  - Mode-aware agent behavior
  - Flexible elicitation levels

EXECUTION PATTERN:

Orchestrator Phase:
  1. Initialize workflow.json via state-manager
  2. Collect discovery information
  3. Update state with discoveries
  4. Validate elicitation completion
  5. Transform to next agent

Each Agent Phase:
  1. Activation:
     - Read workflow.json for state
     - Read required documents
     - Load validation requirements

  2. Execution:
     - Perform phase-specific work
     - Follow mode-appropriate patterns
     - Create deliverable documents

  3. Validation:
     - Self-validate deliverables
     - Run quality checks
     - Ensure completeness

  4. Completion:
     - Update workflow.json via state-manager
     - Record completion status
     - Log transformation
     - Return to orchestrator

Orchestrator Transition:
  1. Receive completion from agent
  2. Validate completion via validate-phase
  3. Check elicitation requirements
  4. If passed: Transform to next agent
  5. If failed: Present elicitation menu

PARALLEL ENHANCEMENT (Task Tool):

When Needed:
  - Multiple independent searches
  - Parallel quality reviews
  - Simultaneous research tasks
  - Language-specific validation

Pattern:
  Primary Agent:
    1. Define parallel work
    2. Spawn agents via Task tool
    3. Wait for all results
    4. Aggregate findings
    5. Update state with synthesis
    6. Continue workflow

DO NOT use Task tool for:
  - Sequential workflow phases
  - State management
  - Main orchestration
```

## Key Insights for Implementation

### 1. Agent Transformation ≠ Task Tool

**Critical Distinction:**

```
Agent Transformation:
  - Read agent file (.codex/agents/{agent}.md)
  - Adopt complete persona within same conversation
  - Used for: Sequential workflow phases
  - Example: Orchestrator → Analyst → PM

Task Tool:
  - Spawn independent agent processes
  - Parallel execution in separate contexts
  - Used for: Quality enhancement, research, validation
  - Example: Dev spawns Swift reviewers
```

### 2. State File is the Anchor

**Everything revolves around workflow.json:**

```
Without workflow.json:
  ❌ No context persistence
  ❌ No mode tracking
  ❌ No elicitation enforcement
  ❌ No resumption after interruption

With workflow.json:
  ✅ Complete state persistence
  ✅ Mode-aware behavior
  ✅ Validation enforcement
  ✅ Graceful resumption
```

### 3. Validation Gates are Mandatory

**Never skip validation:**

```yaml
Before ANY transformation:
  1. Execute validate-phase.md
  2. Check elicitation_completed
  3. If failed: HALT, elicit, retry
  4. If passed: Allow transformation
  5. Log all checks

This prevents:
  - Incomplete requirements
  - Bypassed elicitation
  - Poor quality handoffs
  - State inconsistency
```

### 4. Mode Propagation is Critical

**Operation mode affects everything:**

```yaml
Mode Implications:

Interactive Mode:
  - Section-level elicitation
  - Maximum user involvement
  - Highest quality output
  - Slower execution

Batch Mode:
  - Phase-level elicitation
  - Minimal interruption
  - Good quality output
  - Faster execution

YOLO Mode:
  - No elicitation
  - Automatic decisions
  - Acceptable quality
  - Fastest execution

Implementation:
  - Store mode in workflow.json
  - Read mode on every agent activation
  - Apply mode-specific behavior
  - Allow mode changes mid-workflow
```

### 5. Document Artifacts Enable Clean Handoffs

**Zero Prior Knowledge principle:**

```yaml
Every Phase Output:
  Requirements:
    - Complete standalone document
    - All context needed for next phase
    - No references to conversation
    - No assumptions about prior knowledge

  Test:
    - Next agent should succeed with only:
      1. workflow.json state
      2. Document artifacts
      3. Agent definition file
    - No conversation history needed

This enables:
  - Fresh Claude instances
  - Interruption recovery
  - Parallel development
  - Context window liberation
```

## Conclusion

BMAD/CODEX's multi-phase workflow architecture demonstrates a sophisticated pattern for managing AI agent coordination:

1. **Agent Transformation Protocol** handles sequential workflow phases with isolated contexts
2. **Persistent State File** (workflow.json) maintains continuity across transformations
3. **Task Tool Coordination** enables parallel quality enhancement without polluting workflow state
4. **Document Artifacts** provide Zero Prior Knowledge handoffs between phases
5. **Validation Gates** ensure quality and completeness at every transition
6. **Mode Propagation** allows flexible elicitation levels throughout workflow

The key insight: **Isolation and persistence are complementary, not contradictory**. Ephemeral conversation contexts prevent token overflow and enable specialized reasoning, while persistent file-based state maintains workflow continuity and enables graceful resumption.

This pattern can be applied to any multi-phase AI workflow requiring:
- Complex, multi-step processes
- Context window management
- Quality assurance gates
- Flexible user interaction levels
- Interruption recovery
- State audit trails

The architecture proves that sophisticated workflow orchestration is possible within Claude Code's constraint of ephemeral conversation contexts, through careful state management and clear separation of concerns between transformation protocols and parallel execution patterns.
