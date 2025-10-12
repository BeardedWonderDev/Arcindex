# Contributing to CODEX

Thank you for your interest in contributing to CODEX! This guide will help you get started and understand our development workflow.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Workflow](#development-workflow)
3. [AI Workflow Artifact Policy](#ai-workflow-artifact-policy)
4. [Code Standards](#code-standards)
5. [Commit Guidelines](#commit-guidelines)
6. [Pull Request Process](#pull-request-process)
7. [Questions and Support](#questions-and-support)

## Getting Started

### Prerequisites

- Git installed and configured
- Access to the repository
- Familiarity with the project's tech stack

### Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/BeardedWonder/CODEX.git
   cd CODEX
   ```

2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Make your changes and commit them following our [commit guidelines](#commit-guidelines)

## Development Workflow

1. **Check existing issues** - See if your idea or bug has been discussed
2. **Create a branch** - Use descriptive names: `feature/`, `fix/`, `docs/`
3. **Make changes** - Follow our code standards
4. **Test your changes** - Ensure everything works as expected
5. **Commit your work** - Use conventional commits
6. **Open a pull request** - Provide clear description of changes

## AI Workflow Artifact Policy

### What Are AI Artifacts?

**AI artifacts** are files generated or used by AI-assisted development tools (like Claude Code, Cursor, BMAD, PRP, Aider, etc.) that help you work on your code. These files are valuable for maintaining context during development but shouldn't be part of the main codebase.

Think of them like:
- Your personal development notes
- AI conversation logs
- Tool-specific configuration files
- Planning documents generated for AI assistants

### What Contributors Can Do

**You're free to commit AI artifacts to your feature branches!**

Why? Because they help AI assistants understand your work context and maintain continuity. This makes AI-assisted development more effective and productive.

Example workflow:
```bash
# On your feature branch, commit whatever helps you work:
git add feature.prp.md flattened-codebase.xml docs/ai-notes.md
git commit -m "feat: implement authentication with AI context"
git push origin feature/auth-system
```

Don't worry about cleaning these up manually - our automated system handles it for you.

### What Happens at PR Time

When you open a pull request, our **AI Artifact Auto-Cleanup** workflow automatically:

1. **Analyzes all changed files** - Claude reads the content (not just filenames) to understand what each file is
2. **Identifies artifacts** - Uses semantic understanding to distinguish AI artifacts from legitimate project files
3. **Removes artifacts automatically** - High-confidence artifacts are removed and committed to your branch
4. **Explains its reasoning** - Posts a detailed comment showing what was removed and why
5. **Requests input on uncertain files** - If Claude isn't sure about a file, it asks for your guidance

You'll get a comment like this on your PR:

```markdown
## 🤖 AI Artifact Analysis Complete

### ✅ Removed (High Confidence)
| File | Reason | Evidence |
|------|--------|----------|
| feature.prp.md | PRP artifact | Contains PRP template markers |
| flattened-codebase.xml | BMAD artifact | XML structure matches BMAD output |

### 🟢 Kept (Legitimate Files)
| File | Reason |
|------|--------|
| .codex/agents/analyst.md | Product code in .codex/ directory |
| ROADMAP.md | Root project documentation |

### ❓ Uncertain - Maintainer Review Needed
| File | Question | Why Uncertain |
|------|----------|---------------|
| notes.md | Is this project notes or AI notes? | Not in standard location, needs content analysis |
```

### How to Respond to Uncertain Files

If the cleanup workflow asks about uncertain files, you can respond naturally:

**To keep a file:**
```
@claude keep notes.md - this is our project roadmap, not AI planning
```

**To remove a file:**
```
@claude remove ai-notes.md - those are my personal AI conversation logs
```

**To ask questions:**
```
@claude is .codex/context-manager.ts an artifact?
```

The system learns from your responses and won't flag those files in future PRs!

### Quick Reference: When to Use @claude vs @claude-artifacts

| Scenario | Command | What Happens |
|----------|---------|--------------|
| PR opened/updated | (automatic) | Full artifact analysis runs automatically |
| Force full re-scan | `@claude-artifacts re-check` | Complete re-analysis with detailed report |
| Keep uncertain file | `@claude keep X - because...` | Updates exception list, won't flag again |
| Remove uncertain file | `@claude remove X - it's an artifact` | Removes file and learns the pattern |
| Question about artifact | `@claude is X an artifact?` | Claude analyzes and explains |
| General coding help | `@claude help with feature Y` | Normal Claude Code interaction |

**Simple rule:** Use `@claude` for most interactions. Only use `@claude-artifacts` when you want to force a complete re-analysis.

### Common Artifact Types (FYI)

You don't need to memorize these - the AI knows them all! This is just for reference:

**Entire Directories (Always Artifacts):**
- `docs/` - All AI planning, research, and testing artifacts
- `PRPs/` - All PRP workflow artifacts
- `.bmad-core/` - BMAD reference files (not needed in main)

**Individual Files (Always Artifacts):**
- `*.prp.md` - PRP prompt files (anywhere in repo)
- `flattened-codebase.xml` - BMAD codebase flattener output
- `.cursorignore`, `.cursor/` - Cursor tool artifacts
- `.aiderignore`, `.aider/` - Aider tool artifacts
- `.claude/conversation-*.json`, `.claude/history/` - Conversation logs

**Product Code (Never Artifacts):**
- `.codex/**` - Entire CODEX framework (agents, workflows, tasks, etc.)
- This is the ONLY product code directory

**Root Documentation (Never Artifacts):**
- `README.md`, `ROADMAP.md`, `CHANGELOG.md`, `LICENSE`
- `CONTRIBUTING.md`, `CLAUDE.md`
- `CODEX-User-Guide.md`, `CODEX-Workflow-Guide.md`

**Claude Configuration (Mostly Keep):**
- `.claude/commands/` - Project slash commands (KEEP)
- `.claude/settings.json` - Project config (KEEP)
- `.claude/artifact-exceptions.txt` - Exception system (KEEP)
- `.claude/artifact-policy-reference.md` - Detailed policy (KEEP)
- `.claude/history/`, `.claude/conversation-*.json` - Personal logs (REMOVE)

### Why This Approach?

**For Contributors:**
- Work naturally with AI tools
- No manual cleanup burden
- Artifacts help maintain context in your workflow

**For Maintainers:**
- Clean main branch automatically
- No artifacts leak into production
- Intelligent analysis, not brittle rules

**For the Project:**
- Consistent codebase
- AI-friendly development
- Self-improving system

### Need More Details?

**For Contributors (Humans):**
- **[CLAUDE.md](/CLAUDE.md)** - Core principles and project guidelines
- **This file** - Contributor workflow and standards

**For AI Development:**
- **[.claude/development-reference.md](/.claude/development-reference.md)** - Detailed CODEX development guidance
- **[.claude/artifact-policy-reference.md](/.claude/artifact-policy-reference.md)** - Artifact classification rules

## Development Philosophy

CODEX follows a **fix-forward, beta development approach** during Pre-v0.1.0:

- **No backwards compatibility** - Remove deprecated code immediately
- **KISS** - Keep workflows simple and readable
- **YAGNI** - Don't build features we don't need yet
- **Validate early** - Use quality gates at phase boundaries
- **Document decisions** - Track important choices in ROADMAP.md

For complete Core Principles, see [CLAUDE.md](/CLAUDE.md#core-principles)

## Code Standards

**Working with `.codex/` (product code):**
- All product code lives in `.codex/` directory only
- Follow existing patterns in agents, workflows, and tasks
- Write clear, self-documenting YAML and Markdown
- Use quality checklists from `.codex/checklists/`
- Test your changes against existing workflows

**General standards:**
- Keep workflows simple (KISS principle)
- Don't repeat yourself when appropriate (DRY)
- Clear over clever - optimize for readability
- Add comments for complex workflow logic
- Update ROADMAP.md for architectural decisions

## Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/) for clear and consistent commit history:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Test additions or changes
- `chore:` - Maintenance tasks

**Examples:**
```bash
git commit -m "feat(auth): add OAuth2 authentication"
git commit -m "fix(api): resolve timeout issue in user endpoint"
git commit -m "docs: update installation instructions"
```

## Pull Request Process

1. **Update your branch** with the latest from main:
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Push your changes** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Open a pull request** with:
   - Clear title describing the change
   - Detailed description of what and why
   - Reference any related issues
   - Screenshots/examples if applicable

4. **Wait for artifact cleanup** - The AI will automatically clean artifacts from your PR

5. **Respond to uncertain files** if the AI asks for clarification (see [AI Workflow Artifact Policy](#ai-workflow-artifact-policy))

6. **Address review feedback** from maintainers

7. **Celebrate** when your PR is merged! 🎉

### PR Review Checklist

Before requesting review, ensure:

- [ ] Code follows project standards
- [ ] Tests pass (if applicable)
- [ ] Documentation updated
- [ ] Commit messages follow conventions
- [ ] AI artifacts handled (automatic)
- [ ] No merge conflicts with main

## Questions and Support

- **General questions**: Open a GitHub issue with the `question` label
- **Bug reports**: Open a GitHub issue with the `bug` label
- **Feature requests**: Open a GitHub issue with the `enhancement` label
- **Security issues**: Please email maintainers directly (check README for contact)

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help create a welcoming environment for all contributors

## License

By contributing to CODEX, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to CODEX! Your efforts help make this project better for everyone.
