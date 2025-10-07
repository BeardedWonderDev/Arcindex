# CODEX Architecture: Persistent Orchestrator Pattern

**Document Version:** 1.0
**Date:** October 3, 2025
**Author:** CODEX Development Team
**Status:** Finalized

---

## 1. Overview

This document describes the architectural transformation of CODEX from a Task-based orchestrator to a **Persistent Orchestrator Pattern**. This change fundamentally restructured how CODEX coordinates workflow phases, manages state, and handles the discovery process.

### Summary of Changes

- **Orchestrator Location**: Moved from ephemeral Task executions to persistent main context
- **Discovery Process**: Extracted into dedicated discovery agent with 4-step protocol
- **State Management**: Centralized exclusively in agent Tasks (never in orchestrator)
- **Coordination Model**: Orchestrator became pure coordinator - spawns agents, displays outputs verbatim
- **Token Impact**: Minimal overhead (~2-3k tokens) while gaining conversation memory

### Context

The architectural changes were implemented to resolve critical issues in the discovery phase workflow while establishing a scalable pattern for all future CODEX workflow phases. The transformation occurred on October 3, 2025, following extensive analysis of workflow execution patterns and token accumulation behaviors.

---

## 2. The Problem We Were Solving

### 2.1 Original Architecture Issues

The original CODEX architecture spawned the orchestrator as a Task execution via the `/codex` slash command. This led to several critical problems:

#### Problem 1: Broken Discovery Flow

**Expected Behavior:**
```
User: /codex start greenfield-generic ProjectName
→ Present discovery questions
→ Collect answers
→ Generate discovery summary
→ Present elicitation menu (options 1-9)
→ User selects elicitation or proceeds
→ Transform to analyst
```

**Actual Behavior:**
```
User: /codex start greenfield-generic ProjectName
→ Present discovery questions ONE AT A TIME conversationally
→ NEVER generated discovery summary
→ NEVER presented elicitation menu
→ Discovery phase appeared to complete but never actually finished
```

#### Problem 2: Mixed State Management Responsibilities

The orchestrator contained logic for BOTH coordination AND state management:

```yaml
# From original orchestrator.md (problematic)
workflow-management:
  - Create runtime state IMMEDIATELY after discovery questions
  - Update workflow.json with discovery data
  - Track elicitation_completed status
  - Manage operation_mode transitions
```

This violated separation of concerns and made the orchestrator heavyweight.

#### Problem 3: No Conversation Memory

Because the orchestrator was spawned as a fresh Task for each command, it had:
- No memory of previous phases
- No context of user interactions
- Difficulty making informed decisions about next agent to spawn
- Required re-reading state files constantly

### 2.2 Root Cause Analysis

The fundamental issue was **architectural confusion about the orchestrator's role**:

**What we thought orchestrator was:**
- A coordinator that spawns agents and manages workflow

**What orchestrator actually became:**
- A worker agent trying to do discovery itself
- A state manager mixing coordination with data operations
- An ephemeral Task with no conversation continuity

**Why discovery failed:**
1. Orchestrator tried to ask questions conversationally (one at a time)
2. No dedicated protocol for multi-step discovery workflow
3. State creation happened in orchestrator (wrong location)
4. Discovery completion never properly signaled to elicitation system
5. Orchestrator had discovery logic mixed with coordination logic

**Architectural Smell:**
```yaml
# Red flag: Orchestrator doing work instead of coordinating
workflow-management.GREENFIELD:
  a. Display initialization info
  b. Ask discovery questions  # ← WRONG: Should spawn discovery agent
  c. Store discovery in state  # ← WRONG: Should be in agent Task
  d. Generate summary          # ← WRONG: Should be agent's job
  e. Present elicitation menu  # ← WRONG: Should receive from agent
```

---

## 3. The Solution: Persistent Orchestrator Pattern

The solution involved three architectural changes working in concert:

### 3.1 Core Architectural Principles

**Principle 1: Orchestrator in Main Context**
- Orchestrator activates in the main conversation context (not as Task)
- Gains conversation memory and workflow awareness
- Remains lightweight coordinator without doing work

**Principle 2: Dedicated Discovery Agent**
- All discovery work happens in specialized discovery agent
- Agent operates through 4-step protocol with defined inputs/outputs
- Agent manages its own state creation and updates

**Principle 3: Agent-Based State Management**
- Agents (not orchestrator) read and write workflow.json
- State operations happen in agent Task contexts
- Orchestrator never touches state files directly

### 3.2 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    MAIN CONVERSATION CONTEXT                 │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         CODEX ORCHESTRATOR (Persistent)            │    │
│  │                                                     │    │
│  │  Role: Pure Coordinator                            │    │
│  │  - Spawns agents via Task tool                     │    │
│  │  - Displays agent outputs verbatim                 │    │
│  │  - Waits for user responses                        │    │
│  │  - Determines next agent to spawn                  │    │
│  │  - NEVER reads/writes state                        │    │
│  │  - NEVER does work                                 │    │
│  │                                                     │    │
│  │  Memory: Full conversation history                 │    │
│  │  Token Cost: ~2-3k total (lightweight)             │    │
│  └─────────────────┬──────────────────────────────────┘    │
│                    │                                         │
│                    │ Spawns agents via Task tool             │
│                    ▼                                         │
└─────────────────────────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┬──────────────┬───────────┐
        ▼                         ▼              ▼           ▼
   ┌─────────┐              ┌─────────┐    ┌─────────┐ ┌─────────┐
   │ TASK 1  │              │ TASK 2  │    │ TASK 3  │ │ TASK N  │
   │Discovery│              │Analyst  │    │   PM    │ │  ...    │
   │ Agent   │              │ Agent   │    │ Agent   │ │         │
   │         │              │         │    │         │ │         │
   │Fresh 40k│              │Fresh 40k│    │Fresh 40k│ │Fresh 40k│
   │context  │              │context  │    │context  │ │context  │
   └────┬────┘              └────┬────┘    └────┬────┘ └────┬────┘
        │                        │              │           │
        │ All agents read/write workflow.json for state    │
        └───────────────┬────────┴──────────────┴──────────┘
                        ▼
               ┌─────────────────┐
               │ workflow.json   │
               │                 │
               │ Persistent State│
               │ - current_phase │
               │ - operation_mode│
               │ - discovery_data│
               │ - elicitation_* │
               │ - etc.          │
               └─────────────────┘
```

### 3.3 Execution Flow Pattern

```
User: /codex start greenfield-generic ProjectName
    ↓
┌───────────────────────────────────────────────────────────────┐
│ Slash Command Router (codex.md)                              │
│ - Parses: command="start", workflow="greenfield-generic"     │
│ - Validates: .codex/ directory exists                        │
│ - Reads: .codex/agents/orchestrator.md                       │
│ - Activates: Orchestrator in MAIN CONTEXT                    │
└───────────────────────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR (Main Context - Persistent)                     │
│ Action: Spawn Discovery Agent (step: initialize)             │
└───────────────────────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────────────────────┐
│ TASK #1: Discovery Agent (initialize)                        │
│ - Creates workflow.json with initial state                   │
│ - Returns: Formatted discovery questions                     │
│ - TERMINATES                                                  │
└───────────────────────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR (Main Context)                                  │
│ - Receives questions from Task #1                            │
│ - Displays questions VERBATIM to user                        │
│ - Waits for user to answer                                   │
└───────────────────────────────────────────────────────────────┘
    ↓
User provides answers
    ↓
┌───────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR (Main Context)                                  │
│ Action: Spawn Discovery Agent (step: process_answers)        │
└───────────────────────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────────────────────┐
│ TASK #2: Discovery Agent (process_answers)                   │
│ - Reads workflow.json for context                            │
│ - Parses user answers into structured data                   │
│ - Updates workflow.json with discovery_data                  │
│ - Generates discovery summary (inline markdown)              │
│ - Loads elicitation menu (1-9 options)                       │
│ - Returns: Summary + menu                                    │
│ - TERMINATES                                                  │
└───────────────────────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR (Main Context)                                  │
│ - Receives summary + menu from Task #2                       │
│ - Displays VERBATIM to user                                  │
│ - Waits for user to select option                            │
└───────────────────────────────────────────────────────────────┘
    ↓
User selects option 3 (Critique and Refine)
    ↓
┌───────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR (Main Context)                                  │
│ Action: Spawn Discovery Agent (step: process_elicitation)    │
└───────────────────────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────────────────────┐
│ TASK #3: Discovery Agent (process_elicitation)               │
│ - Reads workflow.json for discovery context                  │
│ - Loads elicitation method #3                                │
│ - Executes method on summary                                 │
│ - Updates workflow.json if content changed                   │
│ - Returns: Elicitation result + updated summary + menu       │
│ - TERMINATES                                                  │
└───────────────────────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR (Main Context)                                  │
│ - Receives result from Task #3                               │
│ - Displays VERBATIM to user                                  │
│ - Waits for user to select option                            │
└───────────────────────────────────────────────────────────────┘
    ↓
[User can repeat elicitation as many times as desired]
    ↓
User selects option 1 (Proceed to next phase)
    ↓
┌───────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR (Main Context)                                  │
│ Action: Spawn Discovery Agent (step: finalize)               │
└───────────────────────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────────────────────┐
│ TASK #4: Discovery Agent (finalize)                          │
│ - Reads workflow.json                                        │
│ - Updates state: discovery_state = "complete"                │
│ - Updates state: current_phase = "analyst"                   │
│ - Returns: Confirmation message                              │
│ - TERMINATES                                                  │
└───────────────────────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR (Main Context)                                  │
│ - Receives confirmation from Task #4                         │
│ - Knows discovery is complete (has conversation memory!)     │
│ - Action: Spawn Analyst Agent (section 1)                    │
└───────────────────────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────────────────────┐
│ TASK #5: Analyst Agent (create section 1)                    │
│ - Reads workflow.json for discovery data                     │
│ - Creates project-brief.md section 1                         │
│ - Returns: Section content + elicitation menu                │
│ - TERMINATES                                                  │
└───────────────────────────────────────────────────────────────┘
    ↓
[Pattern continues for all workflow phases...]
```

---

## 4. Architectural Changes

### 4.1 Slash Command Router (`codex.md`)

#### Before: Task-Based Spawning

```yaml
orchestrator-activation-pattern:
  activation_method: Spawn as Task execution
  protocol: |
    When handling /codex commands:
    1. Parse command and arguments
    2. Spawn orchestrator as Task with detailed instructions
    3. Pass command context to Task
    4. Display Task output
```

**Issues:**
- Orchestrator spawned fresh for each command
- Lost conversation memory between commands
- Instructions embedded in Task prompt (heavyweight)
- No context continuity

#### After: Main Context Activation

```yaml
orchestrator-activation-pattern:
  activation_method: Direct adoption in main context
  protocol: |
    When handling any /codex command:

    1. Read .codex/agents/orchestrator.md file completely

    2. Adopt the orchestrator persona as defined in that file:
       - Follow activation-instructions from orchestrator.md
       - Load .codex/config/codex-config.yaml
       - Understand available commands
       - Apply orchestrator's coordination rules

    3. Execute the received command according to orchestrator.md

    4. The orchestrator operates in the MAIN CONTEXT (not as Task)
       - You ARE the orchestrator
       - You coordinate by spawning sub-agent Tasks
       - You display sub-agent outputs verbatim
       - You never do work yourself - you only coordinate

    CRITICAL: You become the orchestrator in the main context.
```

**Benefits:**
- Orchestrator persists throughout conversation
- Gains full conversation memory
- Lightweight activation (reads file, adopts persona)
- Context awareness enables better coordination

**Impact:**
- Token cost in main context: ~2-3k total (one-time)
- Orchestrator remembers prior phases naturally
- Can make context-aware decisions about next agent
- Simpler mental model (orchestrator = conversation coordinator)

### 4.2 Discovery Agent (`discovery.md`) - NEW

A completely new agent was created to handle all discovery work in isolated Tasks.

#### Purpose

Handle all project discovery work through a structured 4-step protocol with defined inputs and outputs for each step.

#### Four-Step Protocol

**Step 1: Initialize**
- **Called when:** Orchestrator starts workflow, no workflow.json exists
- **Receives:** workflow_type, project_name (optional)
- **Does:**
  - Creates workflow.json via state-manager.md
  - Determines questions based on workflow type
  - Formats questions as clean markdown
- **Returns:** Formatted discovery questions
- **State:** Creates initial workflow.json

**Step 2: Process Answers**
- **Called when:** User has answered discovery questions
- **Receives:** user_answers (text), workflow_type
- **Does:**
  - Reads workflow.json for context
  - Parses answers into structured data
  - Updates workflow.json with discovery_data
  - Generates inline discovery summary
  - Loads elicitation menu (1-9 options)
- **Returns:** Summary + elicitation menu
- **State:** Updates project_discovery field

**Step 3: Process Elicitation**
- **Called when:** User selected elicitation option (2-9)
- **Receives:** elicitation_option (number), current_content (summary)
- **Does:**
  - Reads workflow.json for discovery context
  - Loads and executes elicitation method
  - Updates workflow.json if content changed
  - Logs elicitation in elicitation_history
  - Re-presents summary + menu
- **Returns:** Elicitation result + updated summary + menu
- **State:** Updates discovery data, logs elicitation

**Step 4: Finalize**
- **Called when:** User selected option 1 "Proceed to next phase"
- **Receives:** none (reads from workflow.json)
- **Does:**
  - Reads workflow.json
  - Updates discovery_state = "complete"
  - Updates current_phase = "analyst"
  - Marks elicitation_completed.discovery = true
- **Returns:** Confirmation message
- **State:** Marks discovery complete, ready for analyst

#### Critical Rules

```yaml
output-protocol:
  - NEVER display output to user directly
  - ALWAYS return formatted markdown to orchestrator
  - Orchestrator presents output verbatim
  - DO NOT create files (summary is inline text)
  - DO NOT wait for user input
  - DO NOT call other agents
```

#### State Management Ownership

The discovery agent **owns** all discovery state operations:

```yaml
state-operations:
  creates:
    - workflow.json (initial structure)
    - project_discovery object

  updates:
    - discovery_data (parsed answers)
    - discovery_state (questions_pending → summary_pending → complete)
    - elicitation_completed.discovery
    - current_phase (discovery → analyst)

  logs:
    - elicitation_history entries
    - transformation_history entries
```

The orchestrator **never** touches workflow.json - it only reads from discovery agent outputs.

### 4.3 Orchestrator (`orchestrator.md`)

#### Before: Mixed Responsibilities

```yaml
# OLD orchestrator (problematic mix)
workflow-management.GREENFIELD:
  a. Display initialization info
  b. Ask discovery questions conversationally  # ← Worker behavior
  c. Store discovery in state via state-manager.md  # ← State management
  d. Generate discovery summary  # ← Worker behavior
  e. Present elicitation menu  # ← Worker behavior
  f. Transform to analyst  # ← Coordination behavior (correct)
```

**Problems:**
- Orchestrator doing discovery work (steps b, d, e)
- Orchestrator managing state directly (step c)
- Mixed worker + coordinator responsibilities
- Heavy logic inside orchestrator

#### After: Pure Coordinator

```yaml
# NEW orchestrator (clean separation)
command_implementations:
  start:
    purpose: Initialize new CODEX workflow via discovery agent
    execution: |
      1. Validate workflow_type against available workflows

      2. Check if workflow.json exists (error if yes)

      3. SPAWN Discovery Agent Task (step: initialize):
         - Pass: workflow_type, project_name
         - Discovery agent creates workflow.json and returns questions
         - Display questions to user VERBATIM
         - Wait for user to provide answers

      4. SPAWN Discovery Agent Task (step: process_answers):
         - Pass: user_answers
         - Discovery agent updates workflow.json and returns summary + menu
         - Display summary + menu to user VERBATIM
         - Wait for user to select elicitation option

      5. IF user selects options 2-9 (elicitation):
         - SPAWN Discovery Agent Task (step: process_elicitation)
         - Display result + menu to user VERBATIM
         - Repeat until user selects option 1

      6. WHEN user selects option 1 (Proceed):
         - SPAWN Discovery Agent Task (step: finalize)
         - Proceed to analyst phase

    critical_rules:
      - NEVER create or modify workflow.json yourself
      - NEVER do discovery yourself - spawn discovery agent
      - Display ALL agent outputs VERBATIM - no summarizing
      - You are ONLY a coordinator - agents do all work
```

**Benefits:**
- Clear separation of concerns
- Orchestrator = lightweight coordinator
- All work happens in agents
- All state operations happen in agent Tasks
- Verbatim output display preserves agent work

#### Agent Coordination Protocol

```yaml
agent-coordination:
  purpose: Orchestrator spawns all agents as Task executions

  core-principle: |
    YOU (orchestrator) are a COORDINATOR ONLY. You:
    - NEVER read or write workflow.json (agents do this)
    - NEVER do discovery, analysis, or any actual work (agents do this)
    - ONLY spawn agents via Task tool
    - ONLY display agent outputs verbatim
    - ONLY wait for user responses
    - ONLY determine which agent to spawn next

  agent-spawning-protocol:
    use-task-tool: true

    pattern: |
      For each agent, use Task tool with:

      Task(
        subagent_type: "general-purpose",
        description: "{agent_name} - {what they're doing}",
        prompt: "Activate {agent_name} at .codex/agents/{agent}.md

        {Agent-specific context parameters}

        Read your agent file for complete instructions.
        Read .codex/state/workflow.json for current state.
        Do your work, update state, and return output."
      )

  output-handling:
    - Receive complete output from agent Task
    - Display output VERBATIM to user (no modification, no summary)
    - Wait for user response
    - Determine next agent to spawn based on user response
    - Repeat pattern
```

---

## 5. The Workflow Pattern

### 5.1 Detailed Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                      USER INTERACTION                            │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    /codex start greenfield-generic ProjectName
                              │
┌─────────────────────────────┴────────────────────────────────────┐
│                                                                   │
│  STEP 1: Slash Command Router (codex.md)                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ • Parse: command="start", workflow="greenfield-generic"    │ │
│  │ • Validate: .codex/ directory exists                       │ │
│  │ • Read: .codex/agents/orchestrator.md                      │ │
│  │ • Activate: Orchestrator in MAIN CONTEXT                   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
└───────────────────────────────┬───────────────────────────────────┘
                                ▼
┌───────────────────────────────────────────────────────────────────┐
│                    MAIN CONVERSATION CONTEXT                      │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  ORCHESTRATOR (Persistent)                                  │ │
│  │  • Adopts orchestrator persona                              │ │
│  │  • Loads codex-config.yaml                                  │ │
│  │  • Determines action: Spawn Discovery Agent (initialize)    │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                  │                                │
│                                  │ Spawn Task                     │
│                                  ▼                                │
│         ┌────────────────────────────────────────────┐           │
│         │  TASK #1: Discovery Agent (initialize)    │           │
│         │  ┌──────────────────────────────────────┐ │           │
│         │  │ • Create workflow.json               │ │           │
│         │  │ • Set workflow_type, project_name    │ │           │
│         │  │ • Set current_phase: "discovery"     │ │           │
│         │  │ • Format questions for workflow type │ │           │
│         │  │ • Return: Formatted questions        │ │           │
│         │  └──────────────────────────────────────┘ │           │
│         │                TERMINATES                  │           │
│         └────────────────────────────────────────────┘           │
│                                  │                                │
│                        Output returned to orchestrator            │
│                                  ▼                                │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  ORCHESTRATOR                                               │ │
│  │  • Receives formatted questions                             │ │
│  │  • Displays questions VERBATIM to user                      │ │
│  │  • Waits for user to answer                                 │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
└───────────────────────────────┬───────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                      USER INTERACTION                            │
│  User provides comprehensive answers to all questions            │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────────┐
│                    MAIN CONVERSATION CONTEXT                      │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  ORCHESTRATOR                                               │ │
│  │  • Receives user answers                                    │ │
│  │  • Determines action: Spawn Discovery Agent (process_answers)│ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                  │                                │
│                                  │ Spawn Task                     │
│                                  ▼                                │
│         ┌────────────────────────────────────────────┐           │
│         │  TASK #2: Discovery Agent (process_answers)│          │
│         │  ┌──────────────────────────────────────┐ │           │
│         │  │ • Read workflow.json for context     │ │           │
│         │  │ • Parse user_answers                 │ │           │
│         │  │ • Update workflow.json:              │ │           │
│         │  │   - project_discovery data           │ │           │
│         │  │   - discovery_state: "summary_pending"│ │          │
│         │  │ • Generate discovery summary (inline) │ │          │
│         │  │ • Load elicitation menu (1-9 options)│ │           │
│         │  │ • Return: Summary + menu             │ │           │
│         │  └──────────────────────────────────────┘ │           │
│         │                TERMINATES                  │           │
│         └────────────────────────────────────────────┘           │
│                                  │                                │
│                        Output returned to orchestrator            │
│                                  ▼                                │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  ORCHESTRATOR                                               │ │
│  │  • Receives summary + menu                                  │ │
│  │  • Displays VERBATIM to user                                │ │
│  │  • Waits for user to select option (1-9)                    │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
└───────────────────────────────┬───────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                      USER INTERACTION                            │
│  User selects option 3 (Critique and Refine)                    │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────────┐
│                    MAIN CONVERSATION CONTEXT                      │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  ORCHESTRATOR                                               │ │
│  │  • Receives option selection                                │ │
│  │  • Determines: Spawn Discovery Agent (process_elicitation)  │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                  │                                │
│                                  │ Spawn Task                     │
│                                  ▼                                │
│         ┌─────────────────────────────────────────────┐          │
│         │  TASK #3: Discovery Agent (process_elicitation)│       │
│         │  ┌──────────────────────────────────────┐ │           │
│         │  │ • Read workflow.json for context     │ │           │
│         │  │ • Load elicitation method #3         │ │           │
│         │  │ • Execute method on summary          │ │           │
│         │  │ • Update workflow.json if changed    │ │           │
│         │  │ • Log in elicitation_history         │ │           │
│         │  │ • Return: Result + summary + menu    │ │           │
│         │  └──────────────────────────────────────┘ │           │
│         │                TERMINATES                  │           │
│         └────────────────────────────────────────────┘           │
│                                  │                                │
│                        Output returned to orchestrator            │
│                                  ▼                                │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  ORCHESTRATOR                                               │ │
│  │  • Receives elicitation result + updated summary + menu     │ │
│  │  • Displays VERBATIM to user                                │ │
│  │  • Waits for next option selection                          │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
└───────────────────────────────┬───────────────────────────────────┘
                                │
                         [User can repeat elicitation]
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                      USER INTERACTION                            │
│  User selects option 1 (Proceed to next phase)                  │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────────┐
│                    MAIN CONVERSATION CONTEXT                      │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  ORCHESTRATOR                                               │ │
│  │  • Receives proceed signal                                  │ │
│  │  • Determines action: Spawn Discovery Agent (finalize)      │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                  │                                │
│                                  │ Spawn Task                     │
│                                  ▼                                │
│         ┌────────────────────────────────────────────┐           │
│         │  TASK #4: Discovery Agent (finalize)      │           │
│         │  ┌──────────────────────────────────────┐ │           │
│         │  │ • Read workflow.json                 │ │           │
│         │  │ • Update state:                      │ │           │
│         │  │   - discovery_state: "complete"      │ │           │
│         │  │   - current_phase: "analyst"         │ │           │
│         │  │   - elicitation_completed.discovery: true │ │      │
│         │  │ • Return: Confirmation message       │ │           │
│         │  └──────────────────────────────────────┘ │           │
│         │                TERMINATES                  │           │
│         └────────────────────────────────────────────┘           │
│                                  │                                │
│                        Output returned to orchestrator            │
│                                  ▼                                │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  ORCHESTRATOR                                               │ │
│  │  • Receives confirmation                                    │ │
│  │  • Displays confirmation to user                            │ │
│  │  • Has conversation memory of entire discovery phase!       │ │
│  │  • Determines next action: Spawn Analyst Agent              │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                  │                                │
│                                  │ Spawn Task                     │
│                                  ▼                                │
│         ┌────────────────────────────────────────────┐           │
│         │  TASK #5: Analyst Agent (section 1)       │           │
│         │  ┌──────────────────────────────────────┐ │           │
│         │  │ • Read workflow.json for discovery   │ │           │
│         │  │ • Create project-brief.md section 1  │ │           │
│         │  │ • Update state                       │ │           │
│         │  │ • Return: Section + elicitation menu │ │           │
│         │  └──────────────────────────────────────┘ │           │
│         │                TERMINATES                  │           │
│         └────────────────────────────────────────────┘           │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘

[Pattern continues for all workflow phases: PM, Architect, PRP Creator, Dev, QA]
```

### 5.2 State Persistence Model

```
┌─────────────────────────────────────────────────────────────────┐
│                     workflow.json (Persistent)                  │
│                                                                 │
│  {                                                              │
│    "workflow_type": "greenfield-generic",                       │
│    "project_name": "ProjectName",                               │
│    "current_phase": "analyst",  ← Updated by agents            │
│    "operation_mode": "interactive",                             │
│    "discovery_state": "complete",  ← Updated by discovery agent │
│    "project_discovery": {  ← Created/updated by discovery agent │
│      "concept": "...",                                          │
│      "tech_context": "...",                                     │
│      "existing_inputs": "..."                                   │
│    },                                                           │
│    "elicitation_history": [  ← Logged by agents                │
│      {                                                          │
│        "phase": "discovery",                                    │
│        "method": "critique_and_refine",                         │
│        "timestamp": "2025-10-03T10:30:00Z"                      │
│      }                                                          │
│    ],                                                           │
│    "elicitation_completed": {  ← Tracked by agents             │
│      "discovery": true,                                         │
│      "analyst": false                                           │
│    },                                                           │
│    "transformation_history": [  ← Logged by agents             │
│      {                                                          │
│        "from": "discovery",                                     │
│        "to": "analyst",                                         │
│        "timestamp": "2025-10-03T10:35:00Z"                      │
│      }                                                          │
│    ]                                                            │
│  }                                                              │
│                                                                 │
│  WHO TOUCHES THIS FILE:                                         │
│  ✅ Discovery Agent (creates, updates discovery data)          │
│  ✅ Analyst Agent (reads discovery, updates analyst state)     │
│  ✅ PM Agent (reads prior data, updates PM state)              │
│  ✅ All workflow agents (read/write their relevant sections)   │
│                                                                 │
│  WHO NEVER TOUCHES THIS FILE:                                  │
│  ❌ Orchestrator (only coordinates, never reads/writes state)  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Token Accumulation Analysis

### 6.1 Before: Task-Based Orchestrator

```
Main Conversation Context:
├─ Slash command invocation: ~500 tokens
├─ Orchestrator Task output displayed: ~15k tokens
├─ User interaction: ~2k tokens
├─ Discovery Task output displayed: ~8k tokens
├─ User answers: ~3k tokens
├─ Analyst Task output displayed: ~20k tokens
└─ ... (pattern repeats)
    Total in main context: ~100-120k tokens (only displayed outputs)

Each Orchestrator Task (ephemeral):
├─ Fresh context: 40k available
├─ Orchestrator instructions: ~15k tokens
├─ Config files: ~2k tokens
├─ State reads: ~3k tokens
├─ Coordination logic: ~5k tokens
└─ Output generation: ~10k tokens
    Total per Task: ~35k tokens
    Memory: NONE (fresh each time)
```

### 6.2 After: Persistent Orchestrator

```
Main Conversation Context:
├─ Orchestrator activation: ~500 tokens
├─ Orchestrator persona (one-time): ~2-3k tokens  ← NEW
├─ Config load (one-time): ~500 tokens  ← NEW
├─ Discovery questions displayed: ~1k tokens
├─ User interaction: ~2k tokens
├─ Discovery summary displayed: ~3k tokens
├─ User answers: ~3k tokens
├─ Elicitation results displayed: ~2k tokens
├─ Analyst output displayed: ~20k tokens
└─ ... (pattern repeats)
    Total in main context: ~102-123k tokens (orchestrator + outputs)
    Orchestrator overhead: ~2-3k tokens total
    Memory: FULL CONVERSATION (orchestrator has context)

Each Agent Task (ephemeral):
├─ Fresh context: 40k available
├─ Agent-specific instructions: ~5-10k tokens
├─ State reads: ~3k tokens
├─ Work execution: ~15-20k tokens
├─ Output generation: ~5k tokens
└─ State updates: ~2k tokens
    Total per Task: ~30-40k tokens
    Memory: NONE (fresh each time, but state persists in workflow.json)
```

### 6.3 Comparison Analysis

| Metric | Before (Task Orchestrator) | After (Persistent Orchestrator) | Delta |
|--------|---------------------------|----------------------------------|-------|
| **Main Context Total** | 100-120k tokens | 102-123k tokens | +2-3k |
| **Orchestrator Overhead** | 0 (ephemeral Task) | ~2-3k (one-time in main) | +2-3k |
| **Orchestrator Memory** | None (fresh each time) | Full conversation | ✅ Major benefit |
| **Agent Task Size** | 30-40k tokens | 30-40k tokens | 0 |
| **State Management Location** | Mixed (orchestrator + agents) | Only in agents | ✅ Cleaner |
| **Context Continuity** | None | Full | ✅ Major benefit |
| **Coordination Quality** | Poor (no memory) | Excellent (full memory) | ✅ Major benefit |

### 6.4 Conclusion

**Token Cost:** Minimal increase (~2-3k tokens, or ~2% overhead)

**Benefits Gained:**
- Orchestrator has full conversation memory
- Can make context-aware decisions about next agent
- Natural reference to prior phases
- Better user experience (feels like continuity)
- Cleaner architecture (state only in agents)

**Trade-off Analysis:**
- Cost: 2-3k tokens in main context (negligible)
- Benefit: Conversation memory + cleaner architecture (massive)
- **Result: Overwhelmingly positive trade-off**

---

## 7. Why This Architecture?

### 7.1 Rationale for Persistent Orchestrator

#### 1. Conversation Memory

**Problem Solved:**
```
Before:
User: "Let's continue from where we left off"
Orchestrator (fresh Task): "I don't have context of what we did before"

After:
User: "Let's continue from where we left off"
Orchestrator (persistent): "Yes, we completed discovery and started analyst.
                            Ready to proceed to PM phase?"
```

**Why It Matters:**
- Natural conversation flow
- Better coordination decisions
- User doesn't have to repeat context
- Orchestrator can reference prior phases intelligently

#### 2. Better Coordination Decisions

**Example Scenario:**
```yaml
Context: Discovery complete, analyst section 2 just finished

Before (No Memory):
- Orchestrator spawned fresh
- Reads state file to understand context
- Makes decision based only on state data
- No awareness of user's working style or preferences

After (With Memory):
- Orchestrator remembers discovery questions
- Knows user selected elicitation method 3 twice
- Recognizes user's thoroughness preference
- Can suggest: "Based on your attention to detail in discovery,
               would you like to review section 2 before proceeding?"
```

#### 3. Minimal Token Cost

**Analysis:**
```
Orchestrator persona: ~2-3k tokens (one-time)
Main context capacity: ~200k tokens
Percentage overhead: 1.5%

This is negligible cost for significant benefit.
```

#### 4. Simpler Mental Model

**Developer Perspective:**
```
Before:
- Orchestrator is ephemeral Task
- Lives in different context than conversation
- Requires explicit state passing
- Confusing: "Am I talking to orchestrator or main Claude?"

After:
- Orchestrator IS the conversation
- Lives in main context persistently
- Natural flow of information
- Clear: "I'm talking to orchestrator throughout workflow"
```

#### 5. BMAD Alignment

The persistent orchestrator pattern was proven in BMAD:

```yaml
# From .bmad-core/agents/bmad-orchestrator.md
activation-instructions:
  - STEP 1: Read THIS ENTIRE FILE
  - STEP 2: Adopt the persona defined below
  - STEP 3: Load configuration
  - STEP 4: Greet user and run *help
  - CRITICAL: ONLY greet user, then HALT to await commands
```

BMAD orchestrator:
- Lives in main context
- Coordinates other agents
- Has conversation memory
- Proven pattern with excellent UX

CODEX adapted this proven pattern for workflow orchestration.

### 7.2 Rationale for Discovery Agent

#### 1. Separation of Concerns

**Before (Mixed Responsibilities):**
```yaml
orchestrator.md:
  - Coordination logic
  - Discovery question logic  ← Wrong place
  - Discovery state management  ← Wrong place
  - Elicitation logic  ← Wrong place
  - Agent spawning  ← Correct place
```

**After (Clean Separation):**
```yaml
orchestrator.md:
  - Coordination logic ✅
  - Agent spawning ✅

discovery.md:
  - Discovery question logic ✅
  - Discovery state management ✅
  - Elicitation logic ✅
```

#### 2. Reusability

The same discovery agent handles multiple workflow types:

```yaml
discovery-agent-reuse:
  greenfield-swift:
    - Initialize: questions for greenfield workflow
    - Process: same protocol
    - Elicitation: same menu system
    - Finalize: same completion pattern

  greenfield-generic:
    - Initialize: questions for greenfield workflow
    - Process: same protocol
    - Elicitation: same menu system
    - Finalize: same completion pattern

  brownfield-enhancement:
    - Initialize: questions for brownfield workflow
    - Process: same protocol
    - Elicitation: same menu system
    - Finalize: same completion pattern

  health-check:
    - Skip discovery entirely
```

One agent, multiple workflow types, consistent protocol.

#### 3. State Management Ownership

**Clear Ownership Model:**
```
Discovery Agent owns:
✅ Creation of workflow.json
✅ Updates to project_discovery
✅ Updates to discovery_state
✅ Logging of elicitation_history
✅ Setting current_phase to "analyst"

Orchestrator owns:
✅ Determining which agent to spawn next
✅ Displaying agent outputs verbatim
✅ Waiting for user responses
✅ Coordinating workflow progression

Clear boundaries = easier to reason about = fewer bugs
```

#### 4. Clean Protocol

**Four-Step Protocol Benefits:**

**Step 1: Initialize**
- Single responsibility: Create state and return questions
- Clear input: workflow_type, project_name
- Clear output: Formatted questions
- Testable: Can verify question format for each workflow type

**Step 2: Process Answers**
- Single responsibility: Parse answers, create summary, load menu
- Clear input: user_answers
- Clear output: Summary + menu
- Testable: Can verify parsing and summary generation

**Step 3: Process Elicitation**
- Single responsibility: Execute elicitation method
- Clear input: elicitation_option, current_content
- Clear output: Elicitation result + updated summary + menu
- Testable: Can verify each elicitation method

**Step 4: Finalize**
- Single responsibility: Mark complete and transition
- Clear input: none (reads state)
- Clear output: Confirmation
- Testable: Can verify state transitions

**Protocol Clarity:**
- Each step has one job
- Each step has defined inputs/outputs
- Steps can be tested independently
- Orchestrator just calls steps in sequence

#### 5. Testable in Isolation

**Testing Strategy:**
```python
# Test discovery agent independently of orchestrator
def test_discovery_initialize():
    agent = DiscoveryAgent()
    output = agent.execute(step="initialize",
                          workflow_type="greenfield-generic",
                          project_name="TestProject")
    assert "discovery questions" in output
    assert workflow_json_created()

def test_discovery_process_answers():
    # Setup: workflow.json exists from initialize
    agent = DiscoveryAgent()
    output = agent.execute(step="process_answers",
                          user_answers="Concept: ... Tech: ...")
    assert "summary" in output
    assert "elicitation menu" in output
    assert project_discovery_populated()

def test_discovery_process_elicitation():
    # Setup: discovery summary exists
    agent = DiscoveryAgent()
    output = agent.execute(step="process_elicitation",
                          elicitation_option=3,
                          current_content="...")
    assert "critique" in output
    assert elicitation_history_logged()

def test_discovery_finalize():
    # Setup: discovery complete
    agent = DiscoveryAgent()
    output = agent.execute(step="finalize")
    assert current_phase() == "analyst"
    assert elicitation_completed("discovery") == True
```

### 7.3 Rationale for Agent-Based State Management

#### 1. Single Responsibility Principle

**Design Principle:**
```
Agent Responsibilities:
- Do specialized work (discovery, analysis, PM work, etc.)
- Manage state related to that work
- Return outputs to orchestrator

Orchestrator Responsibilities:
- Coordinate agents
- Display outputs
- Determine next agent
- NEVER touch state
```

**Why This Matters:**
- Clear boundaries prevent confusion
- Bugs stay isolated (state bugs in agents, not orchestrator)
- Orchestrator stays lightweight
- Agents are self-contained units

#### 2. Context Efficiency

**Token Efficiency Analysis:**

**Before (Orchestrator Manages State):**
```
Main Context (Orchestrator):
├─ Orchestrator logic: 15k tokens
├─ State management logic: 5k tokens
├─ State read operations: 3k tokens
├─ State write operations: 2k tokens
└─ Coordination logic: 5k tokens
    Total: 30k tokens in main context

Agent Tasks:
├─ Agent-specific logic: 10k tokens
├─ State reads: 3k tokens
└─ Work execution: 20k tokens
    Total: 33k tokens per agent Task
```

**After (Agents Manage State):**
```
Main Context (Orchestrator):
├─ Orchestrator logic: 2k tokens
└─ Coordination logic: 1k tokens
    Total: 3k tokens in main context (10x reduction!)

Agent Tasks:
├─ Agent-specific logic: 10k tokens
├─ State reads: 3k tokens
├─ State writes: 2k tokens
└─ Work execution: 20k tokens
    Total: 35k tokens per agent Task (+2k, negligible)
```

**Result:**
- Main context: 27k tokens saved (orchestrator stays lightweight)
- Agent Tasks: 2k tokens added (negligible in 40k context)
- Net benefit: Massive reduction in main context complexity

#### 3. Fault Tolerance

**Scenario: Conversation Interrupted**

**Before (Orchestrator Has State Logic):**
```
Problem: If main conversation lost, orchestrator state logic lost
Recovery: Must reconstruct orchestrator with state management
Risk: State operations might differ in reconstructed orchestrator
```

**After (Agents Have State Logic):**
```
Benefit: workflow.json persists on disk
Recovery: New orchestrator can resume by reading workflow.json
Resilience: State operations always happen in fresh agent Tasks
Consistency: Agent Tasks always use same state-manager.md protocol
```

**Example Recovery:**
```
User's computer crashes during analyst phase

Before:
1. User restarts Claude Code
2. Orchestrator needs to be re-spawned
3. Orchestrator might have different state logic (if updated)
4. Risk of state inconsistency

After:
1. User restarts Claude Code
2. User: "/codex continue"
3. New orchestrator reads workflow.json
4. Sees current_phase: "analyst"
5. Spawns analyst agent to continue
6. Agent uses same state-manager.md as before
7. Seamless recovery
```

---

## 8. Benefits Achieved

### 8.1 Functional Benefits

✅ **Discovery Works Correctly**
- Questions presented all at once (not conversationally)
- Answers processed into structured data
- Summary generated and displayed
- Elicitation menu presented (options 1-9)
- User can iterate on elicitation multiple times
- Proceed to analyst only when user selects option 1

✅ **State Management is Clean**
- Orchestrator never touches workflow.json
- All state operations in agent Tasks
- Clear ownership boundaries
- State persists across interruptions

✅ **Orchestrator is Lightweight**
- Only ~2-3k tokens in main context
- Pure coordination logic
- No worker responsibilities
- No state management code

✅ **Agent Outputs Displayed Verbatim**
- User sees complete agent work
- No summarization by orchestrator
- Elicitation menus presented exactly as agents format them
- Transparency in what agents produce

### 8.2 Architectural Benefits

✅ **Clean Separation of Concerns**
```
Orchestrator:
- Coordinate workflow
- Spawn agents
- Display outputs
- Wait for user

Discovery Agent:
- Ask questions
- Parse answers
- Generate summary
- Execute elicitation
- Manage discovery state

Analyst Agent:
- Create project brief
- Execute elicitation
- Manage analyst state

[Pattern continues for all agents]
```

✅ **Scalable Pattern**
```
Discovery → Analyst → PM → Architect → PRP Creator → Dev → QA

Same pattern for all phases:
1. Orchestrator spawns agent Task
2. Agent reads workflow.json
3. Agent does work
4. Agent updates state
5. Agent returns output
6. Orchestrator displays verbatim
7. User responds
8. Repeat

Consistent, predictable, scalable
```

✅ **Conversation Memory for Coordination**
```
Orchestrator remembers:
- Which questions user answered
- Which elicitation methods user selected
- User's working style (thorough vs quick)
- Previous phases completed
- Context for better coordination decisions
```

✅ **Minimal Token Overhead**
```
Cost: ~2-3k tokens (1.5% of 200k context)
Benefit: Full conversation memory + clean architecture
Trade-off: Overwhelmingly positive
```

### 8.3 User Experience Benefits

✅ **Natural Conversation Flow**
```
Before:
User: "Continue from where we left off"
Orchestrator: [Has no memory, asks for context]

After:
User: "Continue from where we left off"
Orchestrator: "Yes, we completed analyst section 2. Ready for section 3?"
```

✅ **Transparency**
```
User sees exactly what agents produce:
- Complete section content (not summaries)
- Full elicitation menus
- Detailed outputs
- No hidden orchestrator processing
```

✅ **Iterative Refinement**
```
Discovery elicitation loop:
1. Agent presents summary
2. User selects elicitation method
3. Agent executes method
4. Agent presents updated summary + menu
5. Repeat until user satisfied
6. User selects "Proceed"

Same pattern works for all phases
```

### 8.4 Developer Benefits

✅ **Easier to Reason About**
```
Question: "Where does discovery state get created?"
Answer: "In discovery agent, step: initialize"

Question: "Who updates current_phase to analyst?"
Answer: "Discovery agent, step: finalize"

Question: "Does orchestrator ever read workflow.json?"
Answer: "No, never. Only agents read/write state."

Clear, simple, consistent answers
```

✅ **Easier to Test**
```python
# Test each agent independently
test_discovery_agent_initialize()
test_discovery_agent_process_answers()
test_discovery_agent_process_elicitation()
test_discovery_agent_finalize()

# Test orchestrator coordination
test_orchestrator_spawn_discovery_agent()
test_orchestrator_display_output_verbatim()
test_orchestrator_spawn_next_agent_based_on_phase()
```

✅ **Easier to Debug**
```
Bug: "Discovery summary not generating"
Debug path:
1. Check discovery agent, step: process_answers
2. Verify summary generation logic
3. Check if workflow.json has discovery_data
4. Fix in discovery agent only

Orchestrator is not involved - clean isolation
```

✅ **Easier to Extend**
```
New requirement: "Add brownfield-migration workflow"

Steps:
1. Define questions in discovery agent for migration workflow
2. Create migration-specific agents (if needed)
3. Orchestrator pattern stays the same
4. No changes to orchestrator code

Scalable, modular, extensible
```

---

## 9. Comparison to Previous Architecture

| Aspect | Previous (Task-Based Orchestrator) | Current (Persistent Orchestrator) | Winner |
|--------|-----------------------------------|-----------------------------------|---------|
| **Orchestrator Location** | Ephemeral Task | Main Context | ✅ Current |
| **Conversation Memory** | None (fresh each time) | Full conversation history | ✅ Current |
| **State Management** | Mixed (orchestrator + agents) | Only in agents | ✅ Current |
| **Token Overhead** | 0 (fresh Task) | ~2-3k (one-time) | ✅ Previous (negligible diff) |
| **Discovery Protocol** | In orchestrator (broken) | Dedicated agent (4-step) | ✅ Current |
| **Coordination Quality** | Poor (no memory) | Excellent (full context) | ✅ Current |
| **Separation of Concerns** | Mixed responsibilities | Clean separation | ✅ Current |
| **Agent Output Display** | Sometimes summarized | Always verbatim | ✅ Current |
| **State Ownership** | Unclear boundaries | Clear agent ownership | ✅ Current |
| **Context Continuity** | Broken across commands | Seamless throughout workflow | ✅ Current |
| **Testability** | Difficult (mixed concerns) | Easy (isolated components) | ✅ Current |
| **Debuggability** | Hard (orchestrator + agents) | Easy (clear boundaries) | ✅ Current |
| **Extensibility** | Modify orchestrator for new workflows | Add agents, orchestrator unchanged | ✅ Current |
| **Recovery from Interruption** | Requires state reconstruction | Read workflow.json, continue | ✅ Current |
| **Mental Model Complexity** | Confusing (ephemeral coordinator) | Clear (persistent coordinator) | ✅ Current |

### Summary

**Previous architecture had ONE advantage:**
- Zero token cost in main context (orchestrator was ephemeral Task)

**Current architecture has FOURTEEN advantages:**
- Conversation memory
- Better coordination
- Clean separation of concerns
- Verbatim output display
- Clear state ownership
- Context continuity
- Easy testing
- Easy debugging
- Easy extension
- Better recovery
- Simpler mental model
- Dedicated discovery protocol
- Scalable pattern
- Better UX

**Trade-off:** ~2-3k tokens (~1.5% overhead) for 14 major benefits

**Result:** Overwhelmingly better architecture

---

## 10. Future Considerations

### 10.1 Pattern Extension to All Phases

**Current State:**
- Discovery agent fully implemented with 4-step protocol
- Analyst, PM, Architect, PRP Creator, Dev, QA agents planned

**Future Pattern:**
Each agent follows the discovery agent model:
```yaml
agent_pattern:
  activation: Spawned by orchestrator via Task tool

  protocol_steps:
    step_1: Initialize (read state, determine work)
    step_2: Execute (do specialized work)
    step_3: Elicitation (present menu, handle user selection)
    step_4: Finalize (update state, return confirmation)

  state_management:
    - Agent reads workflow.json for context
    - Agent updates workflow.json with results
    - Agent logs in transformation_history
    - Agent marks elicitation_completed

  output_protocol:
    - Return formatted output to orchestrator
    - Orchestrator displays verbatim
    - User responds
    - Repeat cycle
```

**Benefits:**
- Consistent pattern across all phases
- Predictable behavior for users
- Easy to add new agent types
- Orchestrator never changes (stable coordination layer)

### 10.2 Enhanced Orchestrator Intelligence

**Current State:**
- Orchestrator determines next agent based on current_phase in workflow.json
- Simple decision tree: discovery → analyst → PM → architect → etc.

**Future Enhancements:**

**Smart Agent Selection:**
```yaml
orchestrator_enhancement_1:
  capability: Context-aware agent selection

  example:
    scenario: User says "I need to add a new feature to existing project"

    current_behavior:
      - Orchestrator: "Use /codex start brownfield-enhancement"

    enhanced_behavior:
      - Orchestrator remembers: Project exists, discovery done before
      - Orchestrator suggests: "Skip discovery, go straight to analyst for feature?"
      - User confirms
      - Orchestrator spawns analyst with existing project context
```

**Proactive Elicitation Suggestions:**
```yaml
orchestrator_enhancement_2:
  capability: Learn user's elicitation preferences

  example:
    observation: User selected method 3 (Critique) 5 times in discovery

    future_suggestions:
      - When analyst presents section 1:
        "I notice you prefer Critique and Refine. Would you like me to
         automatically apply that method to each section?"
```

**Quality Gate Awareness:**
```yaml
orchestrator_enhancement_3:
  capability: Proactive validation reminders

  example:
    context: PM phase complete, architect about to start

    enhanced_behavior:
      - Orchestrator: "Before proceeding to architect, would you like to
                       run validation gates on the PRD?"
      - If yes: Spawn validation agent
      - If no: Proceed to architect
```

### 10.3 Discovery Agent Specialization

**Current State:**
- One discovery agent handles all workflow types
- Questions determined by workflow_type parameter

**Future Specialization:**

**Workflow-Specific Discovery Agents:**
```yaml
specialized_discovery_agents:
  greenfield-swift-discovery:
    questions:
      - iOS-specific questions
      - SwiftUI preferences
      - Target iOS versions
      - App Store submission requirements

  brownfield-migration-discovery:
    questions:
      - Current tech stack
      - Migration constraints
      - Timeline requirements
      - Risk tolerance

  health-check-discovery:
    questions:
      - What to validate
      - Validation depth
      - Remediation preferences
```

**Benefits:**
- More targeted questions
- Better context for specialized workflows
- Cleaner discovery agent code (less branching)

### 10.4 State Management Protocol Formalization

**Current State:**
- Agents use state-manager.md for state operations
- Protocol is documented but not enforced

**Future Formalization:**

**State Schema Validation:**
```yaml
workflow_json_schema:
  version: "1.0"

  required_fields:
    - workflow_type
    - project_name
    - current_phase
    - operation_mode

  phase_specific_fields:
    discovery:
      required: [discovery_state, project_discovery]
    analyst:
      required: [analyst_state, project_brief_sections]
    pm:
      required: [pm_state, prd_sections]

  validation_on_update:
    - Check required fields exist
    - Validate enum values (phases, modes, states)
    - Ensure transformation_history is append-only
    - Verify elicitation_completed is boolean
```

**State Transition Validation:**
```yaml
valid_phase_transitions:
  discovery:
    - analyst  # Normal progression

  analyst:
    - pm  # Normal progression
    - discovery  # Rollback allowed

  pm:
    - architect  # Normal progression
    - analyst  # Rollback allowed

  # Validation: Reject invalid transitions
  # Example: discovery → architect (INVALID, must go through analyst)
```

**State Audit Trail:**
```yaml
transformation_history_schema:
  required_fields:
    - timestamp: ISO 8601
    - from_phase: string
    - to_phase: string
    - triggered_by: "user" | "agent" | "orchestrator"
    - elicitation_completed: boolean
    - operation_mode: "interactive" | "batch" | "yolo"

  immutability:
    - History is append-only
    - Cannot modify past entries
    - Enables full workflow replay
```

### 10.5 Multi-Project Workflow Support

**Current State:**
- One workflow.json per project
- Single active workflow at a time

**Future Enhancement:**

**Project Workspace Management:**
```yaml
multi_project_support:
  structure:
    .codex/state/
      ├─ project-1/
      │  └─ workflow.json
      ├─ project-2/
      │  └─ workflow.json
      └─ active-project.json  # Tracks current project

  orchestrator_commands:
    - /codex switch-project [name]
    - /codex list-projects
    - /codex project-status [name]

  benefits:
    - Work on multiple projects
    - Switch contexts easily
    - Maintain separate workflow states
```

### 10.6 Collaboration Features

**Future Vision:**

**Multi-User Workflow Coordination:**
```yaml
collaboration_support:
  scenario: "Team using CODEX for project development"

  workflow_json_extension:
    assigned_agents:
      analyst: "Alice"
      pm: "Bob"
      architect: "Charlie"

    approval_required:
      - phase: "analyst"
        approver: "Product Owner"
      - phase: "architect"
        approver: "Tech Lead"

  orchestrator_behavior:
    - Check if current user can execute phase
    - Request approval from designated approver
    - Track approval history in transformation_history
```

### 10.7 Performance Optimizations

**Future Optimizations:**

**State Caching:**
```yaml
state_cache_optimization:
  problem: "Agents read workflow.json repeatedly"

  solution:
    - Orchestrator maintains in-memory cache
    - Updates cache when agents modify state
    - Passes cached state to agents (reduce disk I/O)

  benefit:
    - Faster agent spawning
    - Reduced file system operations
    - Lower latency in workflow execution
```

**Batch Agent Execution:**
```yaml
batch_execution_optimization:
  scenario: "User in YOLO mode wants all sections done"

  current_behavior:
    - Spawn agent for section 1
    - Wait for completion
    - Spawn agent for section 2
    - Wait for completion
    - [Repeat for all sections]

  optimized_behavior:
    - Spawn all section agents in parallel
    - Collect outputs as they complete
    - Display results in order
    - Proceed to next phase when all complete

  benefit:
    - Faster workflow completion
    - Better utilization of compute resources
```

---

## 11. References

### 11.1 Core Architecture Files

**Slash Command Router:**
- **Path:** `/Users/brianpistone/Development/BeardedWonder/CODEX/.claude/commands/codex.md`
- **Purpose:** Routes `/codex` commands and activates orchestrator in main context
- **Key Section:** `orchestrator-activation-pattern`

**Orchestrator:**
- **Path:** `/Users/brianpistone/Development/BeardedWonder/CODEX/.codex/agents/orchestrator.md`
- **Purpose:** Master coordinator for all CODEX workflows
- **Key Sections:**
  - `agent-coordination` (coordination protocol)
  - `workflow-management` (workflow execution)
  - `command-handling-protocol` (command implementations)

**Discovery Agent:**
- **Path:** `/Users/brianpistone/Development/BeardedWonder/CODEX/.codex/agents/discovery.md`
- **Purpose:** Handle discovery through 4-step protocol
- **Key Sections:**
  - `step-definitions` (initialize, process_answers, process_elicitation, finalize)
  - `activation-protocol` (how orchestrator spawns discovery)
  - `output-protocol` (return to orchestrator rules)

**Configuration:**
- **Path:** `/Users/brianpistone/Development/BeardedWonder/CODEX/.codex/config/codex-config.yaml`
- **Purpose:** System-wide configuration
- **Key Sections:**
  - `elicitation` (elicitation system settings)
  - `state` (state persistence settings)
  - `agent_coordination` (coordination settings)

### 11.2 Related Documentation

**CODEX Architecture:**
- **Path:** `/Users/brianpistone/Development/BeardedWonder/CODEX/docs/codex-architecture.md`
- **Purpose:** High-level CODEX system architecture
- **Relation:** This document extends architecture with orchestrator pattern details

**CODEX User Guide:**
- **Path:** `/Users/brianpistone/Development/BeardedWonder/CODEX/docs/CODEX-User-Guide.md`
- **Purpose:** End-user documentation for using CODEX
- **Relation:** User-facing view of orchestrator pattern in action

**Task Tool Agent Pattern Analysis:**
- **Path:** `/Users/brianpistone/Development/BeardedWonder/CODEX/docs/task-tool-agent-pattern-analysis.md`
- **Purpose:** Analysis of Task-based agent execution patterns
- **Relation:** Technical foundation for agent spawning protocol

**BMAD Workflow Execution Analysis:**
- **Path:** `/Users/brianpistone/Development/BeardedWonder/CODEX/docs/bmad-workflow-execution-analysis.md`
- **Purpose:** Analysis of BMAD orchestrator pattern
- **Relation:** Source pattern that CODEX orchestrator adapted from

### 11.3 Inspiration: BMAD Orchestrator Pattern

**BMAD Orchestrator:**
- **Path:** `/Users/brianpistone/Development/BeardedWonder/CODEX/.bmad-core/agents/bmad-orchestrator.md`
- **Purpose:** Proven orchestrator pattern from BMAD system
- **Key Learnings:**
  - Persistent orchestrator in main context
  - Lightweight coordination-only role
  - Agent transformation for specialized work
  - Conversation memory for better UX

**CODEX Adaptations:**
```yaml
bmad_pattern_to_codex_adaptations:
  bmad:
    - Transform orchestrator into specialized agents
    - Agents work in same context as orchestrator
    - State implicit in conversation

  codex:
    - Orchestrator spawns agents as Tasks
    - Agents work in isolated Task contexts
    - State explicit in workflow.json

  why_different:
    - CODEX workflows are multi-phase and long-running
    - Need fresh context for each agent (40k limit)
    - Need persistent state across interruptions
    - Need parallel agent execution capability
```

### 11.4 Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-10-03 | Initial documentation of persistent orchestrator pattern | CODEX Team |

### 11.5 Related Issues & PRs

*This section will be populated if/when CODEX moves to GitHub with issue tracking*

### 11.6 Contact & Contribution

For questions about this architecture or suggestions for improvements:

**Internal Documentation:**
- This document: `docs/architecture-persistent-orchestrator.md`
- Architecture overview: `docs/codex-architecture.md`
- User guide: `docs/CODEX-User-Guide.md`

**Implementation Files:**
- Orchestrator: `.codex/agents/orchestrator.md`
- Discovery: `.codex/agents/discovery.md`
- Slash command: `.claude/commands/codex.md`

---

## Appendix A: Architectural Decision Records (ADR)

### ADR-001: Orchestrator Location (Main Context vs Task)

**Status:** Accepted
**Date:** 2025-10-03
**Decision Makers:** CODEX Development Team

**Context:**
Original architecture spawned orchestrator as ephemeral Task for each `/codex` command. This lost conversation memory and made coordination decisions difficult.

**Decision:**
Move orchestrator to main conversation context as persistent coordinator.

**Rationale:**
- Gain conversation memory for better coordination
- Minimal token cost (~2-3k, or 1.5% overhead)
- Simpler mental model (orchestrator = conversation)
- Proven pattern from BMAD

**Consequences:**
- ✅ Better coordination decisions
- ✅ Natural conversation flow
- ✅ Context-aware agent spawning
- ⚠️ Slight token increase in main context (negligible)

**Alternatives Considered:**
1. Keep orchestrator as Task, pass state explicitly ❌ (loses memory)
2. Hybrid: Orchestrator in main, but re-read state constantly ❌ (inefficient)
3. **Selected:** Persistent orchestrator in main context ✅

---

### ADR-002: Discovery Agent Extraction

**Status:** Accepted
**Date:** 2025-10-03
**Decision Makers:** CODEX Development Team

**Context:**
Discovery logic was embedded in orchestrator, causing broken discovery flow and mixed responsibilities.

**Decision:**
Extract all discovery logic into dedicated discovery agent with 4-step protocol.

**Rationale:**
- Separation of concerns (orchestrator = coordinator, discovery = worker)
- Clear protocol with defined inputs/outputs
- Testable in isolation
- Reusable across workflow types

**Consequences:**
- ✅ Discovery works correctly
- ✅ Clean separation of concerns
- ✅ Easy to test and debug
- ✅ Scalable to other agents

**Alternatives Considered:**
1. Fix discovery logic in orchestrator ❌ (doesn't solve mixed responsibilities)
2. Create discovery template that orchestrator uses ❌ (still mixed logic)
3. **Selected:** Dedicated discovery agent ✅

---

### ADR-003: State Management Ownership

**Status:** Accepted
**Date:** 2025-10-03
**Decision Makers:** CODEX Development Team

**Context:**
Original architecture had orchestrator managing state via state-manager.md, mixing coordination with data operations.

**Decision:**
All state operations (read/write workflow.json) happen exclusively in agent Tasks, never in orchestrator.

**Rationale:**
- Single responsibility: Agents do work AND manage their state
- Context efficiency: State operations in 40k agent context, not main context
- Fault tolerance: State persists even if orchestrator conversation lost
- Clear ownership: Each agent owns its state updates

**Consequences:**
- ✅ Orchestrator stays lightweight (~2-3k tokens)
- ✅ Clear boundaries between coordination and state
- ✅ Better recovery from interruptions
- ✅ Easier to reason about data flow

**Alternatives Considered:**
1. Orchestrator manages all state ❌ (heavyweight, mixed concerns)
2. Shared state manager service ❌ (added complexity)
3. **Selected:** Agent-owned state management ✅

---

### ADR-004: Verbatim Output Display

**Status:** Accepted
**Date:** 2025-10-03
**Decision Makers:** CODEX Development Team

**Context:**
Early implementations had orchestrator summarizing agent outputs, hiding details from users.

**Decision:**
Orchestrator MUST display all agent outputs verbatim, with no modification or summarization.

**Rationale:**
- Transparency: Users see complete agent work
- Quality: Users can evaluate full agent outputs
- Elicitation: Users see complete elicitation menus
- Trust: Users know what agents produced

**Consequences:**
- ✅ Complete transparency
- ✅ Better user trust
- ✅ Accurate elicitation workflow
- ⚠️ More tokens in main context (but necessary for quality)

**Alternatives Considered:**
1. Smart summarization (show highlights) ❌ (loses details)
2. Collapsible sections (show/hide details) ❌ (added complexity)
3. **Selected:** Always verbatim ✅

---

## Appendix B: Key Code Patterns

### Pattern 1: Orchestrator Spawning Discovery Agent

```yaml
# From orchestrator.md - command_implementations.start

When user executes: /codex start greenfield-generic ProjectName

Orchestrator executes:
  1. Validate workflow_type exists

  2. SPAWN Discovery Agent (initialize):

     Task(
       subagent_type: "general-purpose",
       description: "Discovery - Initialize workflow",
       prompt: """
         Activate Discovery Agent at .codex/agents/discovery.md

         Step: initialize
         Workflow Type: greenfield-generic
         Project Name: ProjectName

         Create workflow.json and return discovery questions.
       """
     )

  3. Receive output from Task:
     "📋 Discovery Questions\n\nPlease provide answers..."

  4. Display output VERBATIM to user

  5. Wait for user to answer
```

### Pattern 2: Discovery Agent Processing Answers

```yaml
# From discovery.md - step: process_answers

When orchestrator spawns: Discovery Agent (process_answers)

Discovery Agent executes:
  1. Read workflow.json for context:
     {
       "workflow_type": "greenfield-generic",
       "project_name": "ProjectName",
       "current_phase": "discovery",
       "discovery_state": "questions_pending"
     }

  2. Parse user_answers:
     "1. Concept: Ag dealer inventory management
      2. Inputs: None, starting fresh
      3. Context: React + Node.js, PostgreSQL"

     Into structured data:
     {
       "concept": "Ag dealer inventory management",
       "existing_inputs": "None",
       "tech_context": "React + Node.js, PostgreSQL"
     }

  3. Update workflow.json via state-manager.md:
     {
       "project_discovery": {
         "concept": "Ag dealer inventory management",
         "existing_inputs": "None",
         "tech_context": "React + Node.js, PostgreSQL"
       },
       "discovery_state": "summary_pending"
     }

  4. Generate inline summary:
     "Project: ProjectName
      Concept: Ag dealer inventory management system
      Tech Stack: React, Node.js, PostgreSQL
      Starting fresh with no existing materials"

  5. Load elicitation menu from advanced-elicitation.md:
     "1. Proceed to next phase
      2. Show me examples
      3. Critique and refine
      ..."

  6. Return to orchestrator:
     "✅ Discovery Complete

      📋 Summary:
      [Generated summary]

      🎨 Elicitation Menu:
      [1-9 menu]"

  7. TERMINATE
```

### Pattern 3: State-Only Operations in Agents

```yaml
# Anti-pattern (WRONG - orchestrator touching state):
orchestrator:
  workflow-management:
    - Read workflow.json for current_phase  # ❌ WRONG
    - Update current_phase to "analyst"  # ❌ WRONG
    - Spawn analyst agent

# Correct pattern (orchestrator coordinates, agent manages state):
orchestrator:
  workflow-management:
    - Spawn discovery agent (finalize)  # ✅ CORRECT
    - Receive confirmation
    - Spawn analyst agent based on confirmation  # ✅ CORRECT

discovery_agent (finalize):
  - Read workflow.json  # ✅ Agent reads
  - Update current_phase to "analyst"  # ✅ Agent writes
  - Return confirmation to orchestrator  # ✅ Agent returns
```

### Pattern 4: Agent Task Spawning Template

```yaml
# Universal pattern for orchestrator spawning any agent:

Task(
  subagent_type: "general-purpose",
  description: "{AgentName} - {What they're doing}",
  prompt: """
    Activate {AgentName} at .codex/agents/{agent-file}.md

    [Agent-specific parameters]
    {param1}: {value1}
    {param2}: {value2}

    Read your agent file for complete instructions.
    Read .codex/state/workflow.json for current state.
    Do your work, update state, and return output.
  """
)

# Orchestrator receives output
# Orchestrator displays output VERBATIM
# Orchestrator waits for user response
# Orchestrator determines next agent to spawn
# Repeat
```

---

## Appendix C: Glossary

**Orchestrator:**
The persistent coordinator living in main conversation context. Spawns agents, displays outputs, waits for user, determines next steps. NEVER does work or manages state.

**Discovery Agent:**
Specialized agent handling project discovery through 4-step protocol (initialize, process_answers, process_elicitation, finalize).

**Agent Task:**
Ephemeral Task execution spawned by orchestrator using Task tool. Has fresh 40k context. Reads state, does work, updates state, returns output, terminates.

**workflow.json:**
Persistent state file storing complete workflow state (phase, mode, discovery data, elicitation history, etc.). Owned by agents, never touched by orchestrator.

**Main Context:**
The primary conversation context where orchestrator lives and user interacts. ~200k token capacity. Accumulates orchestrator persona + all displayed agent outputs.

**Verbatim Display:**
Orchestrator protocol rule: ALL agent outputs must be displayed exactly as returned, with no modification, summarization, or reformatting.

**4-Step Protocol:**
Discovery agent's structured workflow: initialize → process_answers → process_elicitation → finalize. Each step has defined inputs, outputs, and state operations.

**State Manager:**
Task file (state-manager.md) that provides protocol for reading/writing workflow.json. Used exclusively by agents, never by orchestrator.

**Elicitation Menu:**
9-option menu presented after agent work completion, allowing user to refine outputs through various elicitation methods before proceeding to next phase.

**Operation Mode:**
Workflow execution mode (interactive/batch/yolo) controlling elicitation behavior. Stored in workflow.json, propagated through all agent transformations.

**Conversation Memory:**
Orchestrator's ability to remember full conversation history, enabling context-aware coordination decisions and natural interaction flow.

**Separation of Concerns:**
Architectural principle: Orchestrator = coordinator only, Agents = workers + state managers. Clear boundaries prevent mixed responsibilities.

---

**End of Document**

*For questions or clarifications about this architecture, refer to the reference files listed in Section 11, or contact the CODEX development team.*
