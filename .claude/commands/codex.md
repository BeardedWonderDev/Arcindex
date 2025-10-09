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

CRITICAL: This is a MINIMAL ROUTER. All orchestration logic lives in .codex/agents/orchestrator.md

## ROUTER DEFINITION

```yaml
IDE-FILE-RESOLUTION:
  - Dependencies map to .codex/{type}/{name}
  - type=folder (agents|workflows|tasks|templates|config|data), name=file-name
  - Example: orchestrator.md → .codex/agents/orchestrator.md

REQUEST-RESOLUTION: Match subcommands from $ARGUMENTS flexibly (e.g., "begin"→start, "resume"→continue), ask for clarification if no clear match.

router-purpose:
  role: Lightweight command parser and dispatcher
  responsibility: Parse user commands and delegate to CODEX orchestrator
  core_principles:
    - Parse $ARGUMENTS for subcommand identification
    - Route ALL workflow logic to orchestrator agent
    - Pass MINIMAL context (command, args only)
    - Maintain stateless command processing
    - Provide clear error messages for invalid commands
    - NEVER implement orchestration logic in this router
    - NEVER embed detailed instructions in Task tool calls

processing-protocol:
  - STEP 1: Parse $ARGUMENTS to extract subcommand and options
  - STEP 2: Validate command exists
  - STEP 3: Check for .codex/ directory if command needs it
  - STEP 4: Activate orchestrator via Task tool with MINIMAL context
  - STEP 5: Display orchestrator output VERBATIM (no modification, no summary)
  - CRITICAL: Orchestrator reads its own instructions from orchestrator.md
  - CRITICAL: Do NOT provide workflow logic in Task tool call

command-routing:
  start:
    description: Initialize new CODEX workflow
    arguments: "[workflow-type] [project-name]"
    handler: |
      1. Parse: workflow_type and project_name from arguments
      2. Validate: .codex/ directory exists
      3. If missing directory: "CODEX system not found. Ensure .codex/ directory exists."
      4. If no workflow_type: List available workflows from .codex/workflows/
      5. Activate orchestrator with minimal context:
         - Command: "start"
         - Workflow type: {workflow_type}
         - Project name: {project_name} (if provided)
      6. Display orchestrator response verbatim

  continue:
    description: Resume workflow from last checkpoint
    handler: |
      1. Validate: .codex/state/workflow.json exists
      2. If missing: "No active workflow found. Use '/codex start' to begin."
      3. Activate orchestrator with minimal context:
         - Command: "continue"
      4. Display orchestrator response verbatim

  status:
    description: Show current workflow state
    handler: |
      1. Activate orchestrator with minimal context:
         - Command: "status"
      2. Display orchestrator response verbatim

  validate:
    description: Run validation gates
    handler: |
      1. Validate: .codex/state/workflow.json exists
      2. If missing: "No active workflow to validate."
      3. Activate orchestrator with minimal context:
         - Command: "validate"
      4. Display orchestrator response verbatim

  mode:
    description: Show current operation mode
    handler: |
      1. Activate orchestrator with minimal context:
         - Command: "mode"
      2. Display orchestrator response verbatim

  interactive:
    description: Switch to interactive mode
    handler: |
      1. Validate: .codex/state/workflow.json exists
      2. If missing: "No active workflow. Start with '/codex start'."
      3. Activate orchestrator with minimal context:
         - Command: "interactive"
      4. Display orchestrator response verbatim

  batch:
    description: Switch to batch mode
    handler: |
      1. Validate: .codex/state/workflow.json exists
      2. If missing: "No active workflow. Start with '/codex start'."
      3. Activate orchestrator with minimal context:
         - Command: "batch"
      4. Display orchestrator response verbatim

  yolo:
    description: Switch to YOLO mode
    handler: |
      1. Validate: .codex/state/workflow.json exists
      2. If missing: "No active workflow. Start with '/codex start'."
      3. Activate orchestrator with minimal context:
         - Command: "yolo"
      4. Display orchestrator response verbatim

  rollback:
    description: Revert to previous checkpoint
    handler: |
      1. Validate: .codex/state/workflow.json exists
      2. If missing: "No active workflow to rollback."
      3. Activate orchestrator with minimal context:
         - Command: "rollback"
      4. Display orchestrator response verbatim

  agents:
    description: List specialized agents
    handler: |
      1. Activate orchestrator with minimal context:
         - Command: "agents"
      2. Display orchestrator response verbatim

  workflows:
    description: List available workflows
    handler: |
      1. Activate orchestrator with minimal context:
         - Command: "workflows"
      2. Display orchestrator response verbatim

  config:
    description: Show CODEX configuration
    arguments: "[setting] [value]"
    handler: |
      1. Activate orchestrator with minimal context:
         - Command: "config"
         - Args: {setting} {value}
      2. Display orchestrator response verbatim

  state:
    description: Display workflow state
    handler: |
      1. Validate: .codex/state/workflow.json exists
      2. If missing: "No workflow state to display."
      3. Activate orchestrator with minimal context:
         - Command: "state"
      4. Display orchestrator response verbatim

  chat-mode:
    description: Conversational mode
    handler: |
      1. Activate orchestrator with minimal context:
         - Command: "chat-mode"
      2. Display orchestrator response verbatim

  test:
    description: Test harness operations
    arguments: "[run|analyze|compare|clean] [options]"
    handler: |
      1. Parse test subcommand from arguments (run/analyze/compare/clean)
      2. Validate: .codex/test-harness/ directory exists
      3. If missing: "Test harness not found. Ensure .codex/test-harness/ directory exists."
      4. Map subcommand to script:
         - run → run-test.sh [branch]
         - analyze → analyze-test.sh [test-dir]
         - compare → compare-tests.sh
         - clean → clean-tests.sh
      5. Construct script path: .codex/test-harness/scripts/{script-name}
      6. Execute script via Bash tool with remaining arguments
      7. Display script output verbatim

      Special handling:
      - run: Pass branch argument if provided, otherwise script prompts interactively
      - analyze: Pass test-dir if provided, otherwise script auto-detects latest
      - compare/clean: No arguments needed, scripts handle interactively

  help:
    description: Display command reference
    handler: |
      Display inline help (no orchestrator activation):

      === CODEX Orchestration System ===

      Workflow Management:
      /codex start [workflow] [name] .. Initialize new workflow
      /codex continue ................. Resume from checkpoint
      /codex status ................... Show workflow state
      /codex validate ................. Run validation gates
      /codex rollback ................. Revert to checkpoint

      Operation Modes:
      /codex mode ..................... Show current mode
      /codex interactive .............. Full elicitation (default)
      /codex batch .................... Batch elicitation
      /codex yolo ..................... Skip elicitation
      /codex chat-mode ................ Conversational mode

      System:
      /codex workflows ................ List available workflows
      /codex agents ................... List specialized agents
      /codex config ................... Show configuration
      /codex state .................... Display workflow state
      /codex help ..................... This help

      Testing & Quality:
      /codex test run [branch] ........ Run test from git branch
      /codex test analyze [dir] ....... Analyze test results
      /codex test compare ............. Compare multiple test runs
      /codex test clean ............... Cleanup test directories

      Available Workflows:
      - greenfield-swift: New Swift/iOS projects
      - greenfield-generic: Any language
      - brownfield-enhancement: Enhance existing projects
      - health-check: Validate CODEX system

      Examples:
      /codex start greenfield-swift "My iOS App"
      /codex start greenfield-generic "Python API"
      /codex continue
      /codex interactive

      💡 CODEX orchestrates complete workflows with validation gates.

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

    3. Execute the received command (start, continue, status, etc.) according to orchestrator.md instructions

    4. The orchestrator operates in the MAIN CONTEXT (not as a separate Task)
       - You ARE the orchestrator
       - You coordinate by spawning sub-agent Tasks
       - You display sub-agent outputs verbatim
       - You never do work yourself - you only coordinate

    5. Command context to process:
       - Command: {command}
       - Workflow Type: {workflow_type} (if applicable for 'start')
       - Project Name: {project_name} (if applicable for 'start')
       - Arguments: {additional_args} (if applicable)

    CRITICAL: You become the orchestrator in the main context, not spawn it as a Task.

error-handling:
  unknown_command:
    message: "Unknown command: {command}"
    action: "Display available commands (same as help)"

  missing_directory:
    message: "CODEX system not found. Ensure .codex/ directory exists."
    action: "halt"

  invalid_arguments:
    message: "Invalid arguments for {command}"
    action: "Show correct usage for the command"

dependencies:
  agents:
    - orchestrator.md
```
