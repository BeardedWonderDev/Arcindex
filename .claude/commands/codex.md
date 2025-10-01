---
name: codex
description: CODEX orchestration system for AI-assisted development workflows
arguments: "[subcommand] [options] - e.g., 'start greenfield-swift' or 'status'"
---

# /codex Command

When this command is used, process according to the following configuration:

<!-- Powered by CODEX™ Core -->

# CODEX Command Router

ACTIVATION-NOTICE: This file contains the command routing configuration for CODEX orchestration system.

CRITICAL: Read the full YAML BLOCK that FOLLOWS to understand command routing behavior:

## COMPLETE COMMAND DEFINITION FOLLOWS

```yaml
IDE-FILE-RESOLUTION:
  - Dependencies map to .codex/{type}/{name}
  - type=folder (agents|workflows|tasks|templates|config|data), name=file-name
  - Example: orchestrator.md → .codex/agents/orchestrator.md
  - IMPORTANT: Only load these files when processing specific subcommands

REQUEST-RESOLUTION: Match subcommands from $ARGUMENTS flexibly (e.g., "begin"→start, "resume"→continue), ask for clarification if no clear match.

command-processing-instructions:
  - STEP 1: Parse $ARGUMENTS to extract subcommand and options
  - STEP 2: Match subcommand to command-routing rules below
  - STEP 3: For each subcommand, follow the specific routing instructions
  - STEP 4: Delegate complex logic to orchestrator agent via Task tool
  - STEP 5: When Task tool returns, display the EXACT agent response to user without modification
  - DO NOT: Execute implementation logic directly in this command
  - DO NOT: Summarize, reformat, or paraphrase the orchestrator's output
  - DO NOT: Add your own commentary or wrap the output in additional text
  - ONLY: Route to appropriate agent or display information
  - CRITICAL: All workflow management happens in orchestrator agent
  - CRITICAL: Show orchestrator output verbatim to preserve formatting and UX

command:
  name: CODEX Router
  id: codex
  title: CODEX Orchestration System Command Router
  icon: 🎯
  purpose: Route CODEX commands to orchestrator agent for workflow management

routing:
  role: Command Router & Dispatcher
  responsibility: Parse user commands and delegate to CODEX orchestrator
  core_principles:
    - Parse $ARGUMENTS for subcommand identification
    - Route all workflow logic to orchestrator agent
    - Maintain stateless command processing
    - Provide clear error messages for invalid commands
    - Never implement business logic in this router

subcommands:
  start:
    description: Initialize new CODEX workflow
    arguments: "[workflow-type] [project-name]"
    routing: |
      1. Extract workflow-type and project-name from $ARGUMENTS
      2. Verify .codex/ directory exists
      3. If directory missing: Report "CODEX system not installed. Please ensure .codex/ directory exists."
      4. If no workflow-type: List available workflows from .codex/workflows/
         - greenfield-swift: New Swift/iOS projects
         - greenfield-generic: Any language (Python, JS, Go, Rust, etc.)
         - brownfield-enhancement: Add features to existing projects
         - health-check: Validate CODEX system
      5. Launch orchestrator via Task tool with instructions (see below)
      6. CRITICAL: When Task tool returns, display the orchestrator's EXACT response to user
         - DO NOT add "The CODEX orchestrator has been initialized..." or similar commentary
         - DO NOT reformat or summarize the orchestrator's questions
         - DO NOT add your own introduction or explanation
         - The orchestrator's output is complete and should be shown verbatim
         - Simply pass through the agent response without modification

      Task tool instructions:
         "Activate CODEX orchestrator at .codex/agents/orchestrator.md
          Initialize workflow: {workflow-type}
          Project name: {project-name}

          CRITICAL UX: Present complete initialization status (project info, available commands, current status)
          THEN immediately transition into discovery questions WITHOUT asking 'Proceed with discovery phase?'

          The /codex start command IS the user's confirmation to begin.

          Initialization display should include:
          - Workflow Initialization section (project name, workflow type, operation mode)
          - Available CODEX Commands section (workflow management, operation modes, system management)
          - Current Status section (state, next step)

          Then immediately continue with:
          'Let's begin with discovery questions:'

          CRITICAL: Smart question handling based on provided arguments
          - If {project-name} provided: Skip name question, show as confirmed in init display
          - If {project-name} NOT provided: Ask for name as first question

          Discovery questions to ask:
          - [CONDITIONAL] 'What's your project name/working title?' (ONLY if not provided in command)
          - 'Brief Project Concept: What are you building? (1-3 sentences covering problem, users, core functionality)'
          - 'Existing Inputs: Do you have any existing materials (research, designs, technical requirements), or starting fresh?'
          - 'Development Context: Any technical considerations like target platform, technology preferences, or integration requirements?'

          CRITICAL: DO NOT prompt user to select operation mode during discovery
          - Default to 'interactive' mode automatically
          - Read codex-config.yaml for default_mode if present
          - User can change mode anytime with /codex interactive|batch|yolo commands

          After discovery questions:
          - Create runtime state with default operation_mode using state-manager.md
          - Execute discovery elicitation with 1-9 menu
          - Propagate operation_mode to all agent transformations throughout workflow"

  continue:
    description: Resume workflow from last checkpoint
    arguments: none
    routing: |
      1. Check if .codex/state/workflow.json exists
      2. If missing: Report "No active workflow found. Use 'start' to begin."
      3. Launch orchestrator via Task tool with instructions:
         "Activate CODEX orchestrator at .codex/agents/orchestrator.md
          CRITICAL: Execute validate-phase.md for Level 0 elicitation validation before any agent launch
          Check elicitation_completed status for current phase using state-manager.md
          If elicitation required but incomplete: HALT and present elicitation menu
          Resume existing workflow from checkpoint ONLY after validation passes"

  status:
    description: Show current workflow state and system status
    arguments: none
    routing: |
      1. Launch orchestrator via Task tool with instructions:
         "Activate CODEX orchestrator at .codex/agents/orchestrator.md
          Provide comprehensive status report:
          - System health check
          - Current workflow state
          - Available workflows
          - Recent activity"

  validate:
    description: Run validation gates for current phase
    arguments: none
    routing: |
      1. Check if .codex/state/workflow.json exists
      2. If missing: Report "No active workflow to validate."
      3. Launch orchestrator via Task tool with instructions:
         "Activate CODEX orchestrator at .codex/agents/orchestrator.md
          Execute 5-level validation gate system for current phase
          PRIORITY: Use validate-phase.md for Level 0 mode-aware elicitation validation before other levels
          Use .codex/tasks/validation-gate.md for complete validation protocol
          Report any elicitation violations and block progression until resolved"

  # Operation Mode Commands
  mode:
    description: Show current operation mode (interactive|batch|yolo)
    arguments: none
    routing: |
      1. Check if .codex/state/workflow.json exists
      2. If missing: Report "No active workflow. System default: interactive mode."
      3. Launch orchestrator via Task tool with instructions:
         "Activate CODEX orchestrator at .codex/agents/orchestrator.md
          Execute mode_display_command implementation
          Use state-manager.md get_operation_mode query to retrieve current mode
          Display mode with detailed behavior descriptions and switching instructions"

  interactive:
    description: Switch to interactive mode (section-by-section elicitation)
    arguments: none
    routing: |
      1. Check if .codex/state/workflow.json exists
      2. If missing: Report "No active workflow to set mode."
      3. Launch orchestrator via Task tool with instructions:
         "Activate CODEX orchestrator at .codex/agents/orchestrator.md
          Execute mode_switch_command for 'interactive' mode
          Use state-manager.md set_operation_mode action
          Update workflow state and log mode change to transformation_history
          Enable section-by-section elicitation enforcement in all agents
          Display confirmation with new mode behavior"

  batch:
    description: Switch to batch mode (phase-end elicitation)
    arguments: none
    routing: |
      1. Check if .codex/state/workflow.json exists
      2. If missing: Report "No active workflow to set mode."
      3. Launch orchestrator via Task tool with instructions:
         "Activate CODEX orchestrator at .codex/agents/orchestrator.md
          Execute mode_switch_command for 'batch' mode
          Use state-manager.md set_operation_mode action
          Update workflow state and log mode change to transformation_history
          Enable batch elicitation at phase boundaries
          Display confirmation with new mode behavior"

  yolo:
    description: Switch to YOLO mode (skip all elicitation)
    arguments: none
    routing: |
      1. Check if .codex/state/workflow.json exists
      2. If missing: Report "No active workflow to set mode."
      3. Launch orchestrator via Task tool with instructions:
         "Activate CODEX orchestrator at .codex/agents/orchestrator.md
          Execute mode_switch_command for 'yolo' mode with destructive warning
          Use state-manager.md set_operation_mode action
          Require user confirmation before switching to YOLO
          Update workflow state and log mode change to transformation_history
          Skip all elicitation but maintain decision logging
          WARNING: Display reduced quality assurance notice"

  chat-mode:
    description: Start conversational mode with relaxed elicitation timing
    arguments: none
    routing: |
      1. Launch orchestrator via Task tool with instructions:
         "Activate CODEX orchestrator at .codex/agents/orchestrator.md
          Enter chat-mode for conversational assistance with flexible elicitation"

  # System Management Commands
  rollback:
    description: Revert to previous checkpoint (if git integration available)
    arguments: none
    routing: |
      1. Check if .codex/state/workflow.json exists
      2. If missing: Report "No active workflow to rollback."
      3. Launch orchestrator via Task tool with instructions:
         "Activate CODEX orchestrator at .codex/agents/orchestrator.md
          Execute rollback to previous checkpoint using state-manager.md for state recovery"

  agents:
    description: List and coordinate with specialized agents
    arguments: "[agent-name]"
    routing: |
      1. Launch orchestrator via Task tool with instructions:
         "Activate CODEX orchestrator at .codex/agents/orchestrator.md
          List available agents and coordination options"

  workflows:
    description: List available workflow definitions
    arguments: none
    routing: |
      1. Launch orchestrator via Task tool with instructions:
         "Activate CODEX orchestrator at .codex/agents/orchestrator.md
          List all available workflows from .codex/workflows/"

  config:
    description: Show and modify CODEX configuration
    arguments: "[setting] [value]"
    routing: |
      1. Launch orchestrator via Task tool with instructions:
         "Activate CODEX orchestrator at .codex/agents/orchestrator.md
          Display or modify CODEX configuration settings"

  state:
    description: Display detailed workflow state information
    arguments: none
    routing: |
      1. Check if .codex/state/workflow.json exists
      2. If missing: Report "No workflow state to display."
      3. Launch orchestrator via Task tool with instructions:
         "Activate CODEX orchestrator at .codex/agents/orchestrator.md
          Display detailed workflow state including operation mode and elicitation tracking using state-manager.md"

  help:
    description: Display available commands and workflows
    arguments: none
    routing: |
      1. Display command list with descriptions
      2. List workflows from .codex/workflows/ if directory exists
      3. Show usage examples
      4. No orchestrator activation needed

error-handling:
  unknown-subcommand: |
    Report: "Unknown subcommand: {subcommand}"
    Display available commands (same as help)
    Suggest: "Use '/codex help' for available commands"

  missing-directory: |
    Report: "CODEX system not found"
    Suggest: "Ensure .codex/ directory is properly installed"

  invalid-arguments: |
    Report specific argument error
    Show correct usage for the subcommand
    Provide example of correct usage

orchestrator-delegation:
  agent-location: .codex/agents/orchestrator.md
  activation-method: Task tool
  delegation-pattern: |
    Always use Task tool to launch orchestrator with specific instructions
    Never implement workflow logic in this command file
    Pass all context through activation instructions

dependencies:
  agents:
    - orchestrator.md
  workflows:
    - greenfield-swift.yaml
    - greenfield-generic.yaml
    - brownfield-enhancement.yaml
    - health-check.yaml
  config:
    - codex-config.yaml
  state:
    - workflow.json
  tasks:
    - advanced-elicitation.md
    - state-manager.md
    - validate-phase.md

help-display-template: |
  === CODEX Orchestration System ===

  Workflow Management:
  /codex start [workflow] [name] .. Initialize new workflow
  /codex continue ................. Resume from checkpoint
  /codex status ................... Show workflow state
  /codex validate ................. Run 5-level validation gates
  /codex rollback ................. Revert to previous checkpoint

  Operation Modes (Interactive Elicitation):
  /codex mode ..................... Show current operation mode
  /codex interactive .............. Full elicitation mode (default)
  /codex batch .................... Batch elicitation mode
  /codex yolo ..................... Skip elicitation confirmations
  /codex chat-mode ................ Conversational mode

  System Management:
  /codex workflows ................ List available workflow definitions
  /codex agents ................... List and coordinate with agents
  /codex config ................... Show CODEX configuration
  /codex state .................... Display detailed workflow state
  /codex help ..................... Display this help

  Available Workflows:
  [Dynamically list from .codex/workflows/]

  Examples:
  /codex start greenfield-swift "My iOS App"
  /codex start greenfield-generic "Python API"
  /codex start brownfield-enhancement
  /codex mode
  /codex interactive
  /codex continue

  💡 CODEX orchestrates complete development workflows with
  interactive elicitation, context preservation, and 5-level validation gates.
```