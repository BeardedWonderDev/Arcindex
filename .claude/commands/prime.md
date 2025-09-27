> Command for priming Claude Code with core knowledge about your project

# Prime Context for Claude Code

Use the command `tree` to get an understanding of the project structure.

The use 7 parralel sub-agents to complete each of the following simultanulously:

- Start with reading the CLAUDE.md file if it exists to get an understanding of the project.

- Read the README.md file if it exists to get an understanding of the project.

- Read any PRP documents in the PRPs/ directory and their referenced files to get and an understanding of the project goals and current status

- Read any project documents in the docs/ directory and their referenced files to get and an understanding of the project goals and current status

- Read the files in .bmad-core to understand the BMAD side of what our project is trying to replicate/integrate

- Read the files in .codex/ to understand what we have implemented so far and think hard to get a complete understanding of how the codex project works.

- Review the git log to understand recent changes and updates to the project.

Consolidate your findings from all the sub-agents and explain back to me:
- Project structure
- Project purpose and goals
- Key files and their purposes
- Any important dependencies
- Any important configuration files