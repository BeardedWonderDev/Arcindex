# Claude Code Slash Commands Implementation Guide

## Overview

Claude Code slash commands are custom commands that extend Claude Code's functionality. They are defined as markdown files in the `.claude/commands/` directory and use YAML frontmatter for configuration.

## Command Structure

```markdown
---
name: command-name
description: Brief description of what the command does
arguments: "Description of expected arguments format"
---

# Command Implementation

The command implementation goes here as markdown content.
You can use $ARGUMENTS to access user-provided arguments.

## Usage Example

This command would be invoked as: `/command-name arguments`
```

## Key Requirements

### YAML Frontmatter
- **name**: Must match the filename (without .md extension)
- **description**: Short description shown in help
- **arguments**: Describes expected argument format

### Variable Access
- **$ARGUMENTS**: Contains all arguments passed by user
- Can be parsed and processed within the command

### File Placement
- Commands must be in `.claude/commands/` directory
- Filename determines command name (e.g., `codex.md` → `/codex`)

## Implementation Pattern for CODEX

```markdown
---
name: codex
description: CODEX orchestration system for AI-assisted development workflows
arguments: "[subcommand] [options] - e.g., 'start greenfield-swift' or 'status'"
---

# CODEX Orchestration System

Parse $ARGUMENTS for subcommand routing:
- start: Initialize workflow
- continue: Resume from checkpoint
- status: Show current state
- validate: Run validation gates

## Subcommand Processing

Extract first word from $ARGUMENTS as subcommand, remaining as options.
Route to appropriate orchestrator agent with proper context.
```

## Agent Activation Pattern

Commands often activate specialized agents. The pattern is:

1. Parse command arguments
2. Load configuration files
3. Check current state
4. Launch appropriate agent via Task tool
5. Handle response and update state

## Error Handling

Commands should handle:
- Missing arguments gracefully
- Invalid subcommands with suggestions
- Configuration file errors
- State file corruption
- Agent activation failures

## Best Practices

- Keep command logic simple - delegate to agents
- Provide clear error messages
- Include help/usage information
- Validate arguments before processing
- Maintain consistent command patterns
- Use descriptive argument formats in frontmatter