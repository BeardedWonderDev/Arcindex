# Workflow Start Protocol

purpose: "Initialize new CODEX workflow via discovery agent"

## Command Handling Protocol

When activated via Task tool from slash command router, you receive minimal context:
- Command: {subcommand name}
- Workflow Type: {type} (only for 'start' command)
- Project Name: {name} (only for 'start' command, if provided)
- Arguments: {additional args} (if applicable)

YOU are responsible for ALL orchestration logic. The router only parses and validates.
Read your own instructions below to determine how to execute each command.

## Start Command Implementation

### Execution Steps

**Step 1: Validate Workflow Type**
- Validate workflow_type against available workflows in .codex/workflows/

**Step 2: Check Existing Workflow**
- If workflow.json exists: Error "Workflow already active. Use /codex continue or start fresh."
- If not exists: Proceed with discovery

**Step 3: SPAWN Discovery Agent Task (step: initialize)**
- Pass: workflow_type, project_name (if provided)
- Discovery agent creates workflow.json and returns questions
- **CRITICAL**: See `.codex/tasks/protocols/output-handling.md` "Task Result Visibility" section
- Task results are INVISIBLE to users - you MUST copy result into YOUR response
- READ Task result → COPY entire text → OUTPUT in your message
- Display questions to user VERBATIM (questions must appear in YOUR message)
- Wait for user to provide answers

**Step 4: SPAWN Discovery Agent Task (step: process_answers)**
- Pass: user_answers
- Discovery agent updates workflow.json and returns summary + elicitation menu
- **CRITICAL**: Task results are INVISIBLE - copy result into YOUR response
- READ Task result → COPY entire text → OUTPUT in your message
- Display summary + menu to user VERBATIM (must appear in YOUR message)
- Wait for user to select elicitation option

**Step 5: IF user selects options 2-9 (elicitation methods)**
- SPAWN Discovery Agent Task (step: process_elicitation)
- Pass: elicitation_option, current_content
- Discovery agent executes method and returns result + menu
- **CRITICAL**: Copy Task result into YOUR response - user cannot see it otherwise
- Display result + menu to user VERBATIM (must appear in YOUR message)
- Repeat until user selects option 1

**Step 6: WHEN user selects option 1 (Proceed)**
- SPAWN Discovery Agent Task (step: finalize)
- Discovery agent marks discovery complete
- Proceed to analyst phase (see continue command)

### Critical Rules

- NEVER create or modify workflow.json yourself - discovery agent does this
- NEVER do discovery yourself - spawn discovery agent
- Display ALL agent outputs VERBATIM - no summarizing
- You are ONLY a coordinator - agents do all work

## Universal Workflow Discovery Protocol

### STEP 1: Parse Command
- Format: /codex start [workflow-type] [project-name]
- Workflow types: greenfield-swift, greenfield-generic, brownfield-enhancement, health-check

### STEP 2: Execute Workflow-Specific Discovery

## CRITICAL UX RULES

1. When user executes `/codex start`, that IS their confirmation to begin. Do NOT ask "Proceed with discovery phase?"
2. Present FULL initialization display (see format below) then IMMEDIATELY spawn Discovery Agent (step: initialize)
3. Display the agent's returned questions VERBATIM in the same response - NEVER use your own question templates
4. HALT after displaying questions - wait for user to provide answers
5. When user selects "1. Proceed to next phase" from discovery elicitation menu, that IS their confirmation to transform to next agent. Do NOT ask additional "PROCEED" or "WAIT" confirmation.

## Initialization Display Format

```
🎯 CODEX Orchestrator Activated

---
Workflow Initialization

- Project: {project_name} [if provided, otherwise "To be determined"]
- Workflow Type: {workflow_type}
- Operation Mode: Interactive (full elicitation)

---
Available CODEX Commands

Workflow Management:
- /codex help - Show guide and system status
- /codex continue - Resume from checkpoint
- /codex status - Show workflow state
- /codex validate - Run validation gates
- /codex rollback - Revert to checkpoint

Operation Modes:
- /codex mode - Show current mode
- /codex interactive - Full elicitation (default)
- /codex batch - Batch elicitation
- /codex yolo - Skip confirmations

---
Current Status

State: Ready to begin discovery phase
Next Step: Spawning Discovery Agent...
```

## GREENFIELD Workflows

### Step a: Display Complete Initialization Info
- Use initialization format above
- If project name provided in command, show it as confirmed in Workflow Initialization section

### Step b: SPAWN Discovery Agent (step: initialize)
- Use Task tool to spawn discovery agent
- Pass workflow_type and project_name (if provided)
- Discovery agent creates workflow.json and returns formatted questions
- **CRITICAL OUTPUT HANDLING** (see `.codex/tasks/protocols/output-handling.md`):
  * Task results are INVISIBLE to users until you display them
  * READ the Task result field
  * COPY the ENTIRE result text
  * OUTPUT that text in YOUR response message
  * Verify questions appear in YOUR message before halting
- Display returned questions VERBATIM to user (questions in YOUR message)
- HALT - wait for user to provide comprehensive answers
- DO NOT present your own questions - always use discovery agent's questions

### Step c: After User Provides Answers
SPAWN Discovery Agent (step: process_answers):
- Use Task tool to spawn discovery agent
- Pass user_answers (complete text of user's response)
- Discovery agent processes answers, updates workflow.json, returns summary + elicitation menu
- **CRITICAL**: Task result is INVISIBLE - copy into YOUR response
- READ Task result → COPY entire text → OUTPUT in your message
- Display summary + menu VERBATIM to user (must appear in YOUR message)
- HALT - wait for user to select elicitation option (1-9)

### Step d: Store Discovery in State
- project_discovery object via state-manager.md (discovery agent handles this)

### Step e: DEFAULT MODE - Automatically Set Operation Mode
**DO NOT prompt user:**
- Default to "interactive" mode
- Read codex-config.yaml for default_mode override if present
- User can change mode anytime with /codex interactive|batch|yolo commands
- DO NOT ask user to select mode during discovery

### Step f: CREATE RUNTIME STATE
Use state-manager.md to initialize workflow.json with:
- workflow_type: "greenfield-swift" (or appropriate)
- project_name: captured from user
- current_phase: "discovery"
- operation_mode: "interactive" (or config default)
- elicitation_required[discovery]: true (for interactive mode)
- elicitation_completed[discovery]: false (initially)
- mode_initialized_at: {timestamp}

### Step g: DISCOVERY ELICITATION
After collecting answers:
- Generate discovery summary as MARKDOWN TEXT (include in your response)
- Format summary with: project name, concept, tech stack, MVP scope
- Present summary INLINE in conversation (DO NOT create files)
- **CRITICAL**: DO NOT create .codex/discovery/ directory or files
- **VIOLATION**: Creating discovery-summary.md violates workflow protocol
- Store discovery data ONLY in workflow.json via state-manager.md
- After presenting inline summary, use advanced-elicitation.md to show 1-9 menu
- Wait for user to select option 1-9 or provide feedback
- If user selects option 1 (Proceed to next phase):
  * Update elicitation_completed[discovery]: true via state-manager.md
  * Proceed directly to step h (NO additional confirmation needed)
- If user selects options 2-9:
  * Execute elicitation method
  * Re-present menu until user selects option 1
  * Then update elicitation_completed[discovery]: true

### Step h: MANDATORY VALIDATION
Run validate-phase.md before transformation

### Step i: MODE PROPAGATION
Read operation_mode from workflow.json and pass to analyst

### Step j: Transform Directly to Analyst
User already confirmed via menu selection:
- Announce: "🎯 Discovery complete! Transforming into Business Analyst [Mode: {mode}]"
- Pass operation_mode in analyst context
- Analyst applies mode-specific elicitation behavior

## BROWNFIELD Workflows

### Step a: Check for Existing CODEX Project Context
- Read .codex/docs/*.md for project documentation
- Read .codex/state/workflow.json for previous history

### Step b: Summarize Understanding and Get Confirmation

### Step c: SPAWN Discovery Agent (step: initialize)
- Use Task tool to spawn discovery agent
- Pass workflow_type="brownfield-enhancement" and project_name (if provided)
- Discovery agent creates workflow.json and returns formatted enhancement questions
- **CRITICAL**: Task result INVISIBLE - copy into YOUR response (see output-handling.md)
- READ Task result → COPY entire text → OUTPUT in your message
- Display returned questions VERBATIM to user (questions in YOUR message)
- HALT - wait for user to provide comprehensive answers
- DO NOT present your own questions - always use discovery agent's questions

### Step d: Store Discovery in State
- enhancement_discovery object via state-manager.md

### Step e: DEFAULT MODE - Automatically Set Operation Mode
**DO NOT prompt user:**
- Check for existing workflow.json and preserve operation_mode if present
- If new workflow, default to "interactive" mode
- Read codex-config.yaml for default_mode override if present
- User can change mode anytime with /codex interactive|batch|yolo commands
- DO NOT ask user to select mode during discovery

### Step f: CREATE/UPDATE RUNTIME STATE
Use state-manager.md to initialize or update with:
- workflow_type: "brownfield-enhancement"
- current_phase: "discovery"
- operation_mode: "interactive" (or config default, or preserved from existing state)
- elicitation_required[discovery]: true (for interactive mode)
- elicitation_completed[discovery]: false (initially)
- mode_initialized_at: {timestamp}

### Step g: DISCOVERY ELICITATION
After collecting answers:
- Generate enhancement summary as MARKDOWN TEXT (include in your response)
- Format summary with: enhancement goal, affected components, constraints
- Present summary INLINE in conversation (DO NOT create files)
- **CRITICAL**: DO NOT create .codex/discovery/ directory or files
- **VIOLATION**: Creating discovery files violates workflow protocol
- Store discovery data ONLY in workflow.json via state-manager.md
- After presenting inline summary, use advanced-elicitation.md to show 1-9 menu
- Wait for user to select option 1-9 or provide feedback
- If user selects option 1 (Proceed to next phase):
  * Update elicitation_completed[discovery]: true via state-manager.md
  * Proceed directly to step h (NO additional confirmation needed)
- If user selects options 2-9:
  * Execute elicitation method
  * Re-present menu until user selects option 1
  * Then update elicitation_completed[discovery]: true

### Step h: MANDATORY VALIDATION
Run validate-phase.md before transformation

### Step i: MODE PROPAGATION
Read operation_mode from workflow.json and pass to analyst

### Step j: Transform Directly to Analyst
User already confirmed via menu selection:
- Announce: "🎯 Discovery complete! Transforming into Business Analyst [Mode: {mode}]"
- Pass operation_mode in analyst context
- Analyst applies mode-specific elicitation behavior

## HEALTH-CHECK Workflows

### Step a: No Discovery Needed
Proceed directly

### Step b: Execute Validation Checks Immediately

### Step c: Report Results Without Agent Transformation

## CRITICAL: MANDATORY PRE-LAUNCH VALIDATION PROTOCOL

- Before ANY agent launch OR transformation, execute validate-phase.md
- validate-phase.md checks .codex/state/workflow.json for elicitation_completed[current_phase]
- If validation fails: **HALT WORKFLOW IMMEDIATELY**
- validate-phase.md presents elicitation menu using .codex/tasks/advanced-elicitation.md
- Block all agent launches and transformations until validation passes
- state-manager.md logs all validation checks with timestamps

## Enforce Elicitation Based on Mode

- Interactive: Full elicitation at all phase transitions (default)
- Batch: Batch elicitation at end of phases
- YOLO: Skip elicitation but still log decisions

## Additional Workflow Management Rules

- Create context checkpoints at strategic breakpoints
- Coordinate agent handoffs with validation
- Ensure "No Prior Knowledge" test passes at each transition
- Handle workflow interruption and resumption gracefully
- Track elicitation_history and elicitation_completed per phase
