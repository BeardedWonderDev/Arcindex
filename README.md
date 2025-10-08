<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">CODEX</h3>
  <p align="center">
    Context-Oriented Development & Execution System
    <br />
    <em>AI-Powered Orchestration for One-Pass Implementation Success</em>
    <br />
    <br />
    <a href="docs/CODEX-User-Guide.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#usage">View Examples</a>
    ·
    <a href="https://github.com/BeardedWonder/CODEX/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/BeardedWonder/CODEX/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

> **⚠️ Development Status**: CODEX is currently in active development (pre-v0.1.0). Core infrastructure is complete, but the system has not yet undergone comprehensive real-world testing. Early adopters and contributors are welcome!

**CODEX (Context-Oriented Development & Execution System)** is an AI-powered orchestration system that manages complete software development workflows from concept to validated implementation. It eliminates fragmented AI-assisted development by unifying documentation creation with implementation guidance through systematic agent coordination.

**The Problem:**
- Context loss when switching between documentation and coding phases
- Manual coordination overhead between disconnected AI methodologies
- Context window limits breaking complex implementations
- Lack of systematic quality assurance in AI-generated code

**The Solution:**
CODEX orchestrates specialized AI agents through a systematic workflow with built-in validation, targeting 85% one-pass implementation success through:
- **Zero Prior Knowledge Architecture** - Fresh Claude instances can resume from any checkpoint
- **Progressive Validation** - 5-level quality gates from elicitation to domain-specific checks
- **Multi-Language Support** - Swift, Python, JavaScript, Go, Rust, and more
- **Interactive Elicitation** - Mandatory user validation at critical decision points

> **Note**: Performance targets (85% success rate, 40% cycle time reduction) are design goals currently under validation. Comprehensive testing will verify these metrics before v0.1.0 release.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

[![Claude][Claude.ai]][Claude-url]
[![Markdown][Markdown.badge]][Markdown-url]
[![YAML][YAML.badge]][YAML-url]
[![Git][Git.badge]][Git-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* **Claude Code CLI** - Install from [claude.com/claude-code](https://claude.com/claude-code)
* **Git** (recommended for version control)
* **Language-specific tools** (for validation):
  * Swift: Xcode, swiftlint, swift-format
  * Python: pytest, flake8, black
  * JavaScript: npm, eslint, prettier
  * Go: go test, golangci-lint, gofmt
  * Rust: cargo, clippy, rustfmt

### Installation

1. Clone the CODEX repository into your project
   ```sh
   git clone https://github.com/BeardedWonder/CODEX.git
   cd CODEX
   ```

2. Verify CODEX is available
   ```sh
   /codex help
   ```

3. (Optional) Run health check to validate system
   ```sh
   /codex start health-check
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

### Quick Start - Swift/iOS Project

Start a new Swift iOS application in 3 steps:

```sh
# 1. Initialize workflow
/codex start greenfield-swift "TaskMaster Pro"

# 2. Answer discovery questions
# - What are you building? (Brief description)
# - Existing inputs or starting fresh?
# - Any technical considerations?

# 3. Follow elicitation prompts
# Select from 1-9 menu after each section
```

### Quick Start - Python/JavaScript/Other Languages

```sh
# Start generic workflow
/codex start greenfield-generic "FastAPI User Service"

# Configure language tooling when prompted
# - Language: Python
# - Framework: FastAPI
# - Build command: python -m pytest
# - Lint command: flake8
```

### Add Feature to Existing Project

```sh
/codex start brownfield-enhancement
```

### Command Reference

| Command | Description |
|---------|-------------|
| `/codex start [workflow] [name]` | Initialize new workflow |
| `/codex continue` | Resume interrupted workflow |
| `/codex status` | Show current workflow state |
| `/codex validate` | Run 5-level validation gates |
| `/codex mode` | Show/change operation mode |
| `/codex interactive` | Enable full elicitation (default) |
| `/codex batch` | Enable batch elicitation |
| `/codex yolo` | Skip elicitation (not recommended) |
| `/codex help` | Display command reference |

### Available Workflows

1. **greenfield-swift** - New Swift/iOS/macOS projects
2. **greenfield-generic** - Any programming language
3. **brownfield-enhancement** - Add features to existing codebases
4. **health-check** - System validation

_For comprehensive documentation, please refer to the [User Guide](docs/CODEX-User-Guide.md)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- FEATURES -->
## Features

### 🎯 Zero Prior Knowledge Architecture
- Each workflow phase produces self-contained documents
- Fresh Claude instances can resume from any checkpoint
- Strategic breakpoints prevent context window overflow
- Supports features up to 2000+ lines without context limits

### 🌍 Multi-Language Support
- **Swift/iOS**: Complete workflow with specialized validation
- **Generic Template**: Python, JavaScript, Go, Rust, and more
- **Brownfield**: Intelligent existing codebase enhancement
- Customizable validation commands per language

### ✅ 5-Level Progressive Validation
- **Level 0**: Elicitation validation (mandatory user interaction)
- **Level 1**: Syntax & style checks
- **Level 2**: Unit tests (>80% coverage target)
- **Level 3**: Integration tests
- **Level 4**: Language-specific domain validation

### 🤝 Interactive Elicitation System
- **Interactive Mode**: Section-by-section validation with 1-9 menu
- **Batch Mode**: Phase-end elicitation for efficiency
- **YOLO Mode**: Skip elicitation for rapid prototyping
- 20+ elicitation methods (Critique & Refine, Tree of Thoughts, Red Team vs Blue Team, etc.)

### 🔄 Complete Workflow Orchestration
```
Discovery → Business Analysis → Requirements → Architecture → Enhanced PRP → Implementation → QA
```

### 📊 Performance Targets (Design Goals)

> **⚠️ Under Validation**: These targets guide v0.1.0 development but are not yet verified through comprehensive real-world testing. Actual performance metrics will be measured and reported after end-to-end workflow validation.

- 85% one-pass implementation success rate (target)
- 40% development cycle time reduction (target)
- 95% zero-knowledge validation pass rate (target)
- ≤3 context breakpoints per feature up to 2000 lines (target)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

For comprehensive project roadmap including v0.1.0, v0.2.0, and v0.3.0 plans, see **[ROADMAP.md](ROADMAP.md)**.

**Quick Overview:**
- **v0.1.0** - Quality Foundation (In Progress): Archon integration, comprehensive quality gates, feedback loops, Git integration
- **v0.2.0** - Brownfield Support: Existing codebase enhancement workflows, advanced templates
- **v0.3.0** - Advanced Capabilities: Custom workflows, parallel execution, community marketplace

See the [open issues](https://github.com/BeardedWonder/CODEX/issues) for a full list of proposed features and known issues.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

CODEX is in active development and welcomes contributions! Since we're in the pre-v0.1.0 phase, this is an excellent time to shape the project's future.

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make CODEX better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

Don't forget to give the project a star! Thanks again!

### Contribution Workflow

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow [Conventional Commits](https://www.conventionalcommits.org/) specification
- Update documentation for new features
- Add examples to user guide when applicable
- Test workflows end-to-end before submitting PRs
- Maintain the zero-knowledge architecture principle

### Areas Needing Contribution

- **Testing**: Real-world workflow validation
- **Documentation**: Additional examples and use cases
- **Language Templates**: Pre-configured validation for more languages
- **Error Handling**: Edge case coverage
- **Performance**: Optimization of agent coordination

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

**Attribution**: CODEX is a derivative work of the [BMAD (BMad Method)](https://github.com/original-bmad-repo) framework. The core agent coordination patterns, elicitation methodology, and workflow orchestration concepts are adapted from BMAD with significant enhancements for context management and PRP integration.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Project Link: [https://github.com/BeardedWonder/CODEX](https://github.com/BeardedWonder/CODEX)

Documentation: [CODEX User Guide](docs/CODEX-User-Guide.md)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [BMAD (BMad Method)](https://github.com/original-bmad-repo) - Agent-based agile development methodology
* [Claude Code](https://claude.com/claude-code) - AI-powered CLI development environment
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template) - Professional README structure
* [Shields.io](https://shields.io) - Repository badges
* [Conventional Commits](https://www.conventionalcommits.org/) - Commit message specification
* [Semantic Versioning](https://semver.org/) - Version numbering system
* [Keep a Changelog](https://keepachangelog.com/) - Changelog formatting

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/BeardedWonder/CODEX.svg?style=for-the-badge
[contributors-url]: https://github.com/BeardedWonder/CODEX/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/BeardedWonder/CODEX.svg?style=for-the-badge
[forks-url]: https://github.com/BeardedWonder/CODEX/network/members
[stars-shield]: https://img.shields.io/github/stars/BeardedWonder/CODEX.svg?style=for-the-badge
[stars-url]: https://github.com/BeardedWonder/CODEX/stargazers
[issues-shield]: https://img.shields.io/github/issues/BeardedWonder/CODEX.svg?style=for-the-badge
[issues-url]: https://github.com/BeardedWonder/CODEX/issues
[license-shield]: https://img.shields.io/github/license/BeardedWonder/CODEX.svg?style=for-the-badge
[license-url]: https://github.com/BeardedWonder/CODEX/blob/main/LICENSE

[Claude.ai]: https://img.shields.io/badge/Claude-AI-8A2BE2?style=for-the-badge
[Claude-url]: https://claude.com
[Markdown.badge]: https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white
[Markdown-url]: https://www.markdownguide.org/
[YAML.badge]: https://img.shields.io/badge/YAML-CB171E?style=for-the-badge&logo=yaml&logoColor=white
[YAML-url]: https://yaml.org/
[Git.badge]: https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white
[Git-url]: https://git-scm.com/
