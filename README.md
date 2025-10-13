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
  <h3 align="center">Arcindex</h3>
  <p align="center">
    Adaptive Review &amp; Coordination with Integrated Development Experience
    <br />
    <em>AI-Orchestrated Workflows for One-Pass Implementation Success</em>
    <br />
    <br />
    <a href="#about-the-project"><strong>Get the overview »</strong></a>
    <br />
    <br />
    <a href="#usage">Planned Usage</a>
    ·
    <a href="#roadmap">Roadmap</a>
    ·
    <a href="#contributing">Contribute</a>
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
      <a href="#project-status">Project Status</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#initial-setup">Initial Setup</a></li>
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

> **⚠️ Development Status**: Arcindex is in active migration (Phase 0 of the OpenAI Codex SDK rebuild). The legacy implementation now lives entirely under `legacy/` for reference while the new CLI/runtime is constructed at the repository root.

Arcindex is the evolution of our internal CODEX initiative—an AI-powered orchestration system that runs multi-phase software development workflows from discovery through implementation and validation. The project is being rebuilt to run on the OpenAI Codex SDK with a Python-based CLI, keeping the original ambition of “one-pass implementation success” while modernizing the runtime and tooling.

Arcindex inherits two foundational influences:
- **BMAD Method** – agentic planning workflows, elicitation standards, and comprehensive checklist discipline.
- **Product Requirement Prompt (PRP) system** – implementation-ready prompts that fuse context, strategy, and validation commands.

This migration preserves those philosophies while delivering a unified CLI experience.

**Key Objectives:**

- **Adaptive Context Preservation** – maintain complete state across discovery, product management, architecture, implementation, and QA so any phase can restart with zero prior knowledge.
- **Guided Elicitation** – enforce structured human feedback through standardized 1–9 elicitation menus and recorded responses at every critical checkpoint.
- **Evidence-Driven Validation** – capture quality gate scores, evidence, and escalation paths in persistent state and expose them through CLI tooling.
- **Multi-Agent Coordination** – orchestrate specialized assistants (discovery, analyst, PM, architect, PRP, dev, QA) to hand off artifacts, enforce validation, and surface learnings.

The migration is captured in detail inside [`MIGRATION-PLAN.md`](MIGRATION-PLAN.md).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- Python (CLI + orchestration runtime)
- OpenAI Codex SDK
- YAML / JSON configuration
- GitHub Actions (automation & CI)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Project Status

| Track | Status | Notes |
|-------|--------|-------|
| Repository restructure | ✅ | Legacy CODEX archived under `legacy/`; root prepared for SDK build |
| Migration plan | ✅ | Phased strategy documented in `MIGRATION-PLAN.md` |
| SDK scaffolding | ✅ | Phase 0: scaffolding `arcindex/`, CLI entry point, tooling baseline |
| Discovery orchestration | 🚧 | Phase 1: CLI-based discovery workflow available; analyst handoff queued |
| Analyst/PM/Architect phases | ⚪ | Planned follow-on phases after discovery parity |
| PRP & QA automation | ⚪ | Targeted for later migration phases (5–6) |
| Documentation refresh | 🚧 | README updated; deeper docs follow as phases land |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Getting Started

Arcindex is currently in early migration. Until the new CLI is shipped, setup focuses on cloning the repo, reviewing the migration plan, and preparing the Python environment for contributions.

### Prerequisites

- Python 3.11+
- make (optional, for future helper scripts)
- Node.js (optional, only needed when exploring the archived legacy implementation inside `legacy/`)

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone git@github.com:BeardedWonder/CODEX.git
   cd CODEX
   ```
2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. **Install development requirements**
   ```bash
   pip install -r arcindex/requirements-dev.txt
   # or, if you prefer editable installs:
   pip install -e '.[dev]'
   ```
4. **Review the migration plan**
   ```bash
   less MIGRATION-PLAN.md
   ```
5. **Pick a migration phase**
   - Align contributions with the roadmap in the next section.
   - Open design notes or draft specs before large changes.

> The CLI is not yet wired end-to-end. Watch the roadmap for Phase 1 completion to begin running discovery workflows.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Usage

### Run the Discovery Workflow

1. **Install the project locally** (editable mode recommended):
   ```bash
   pip install -e '.[dev]'
   ```

2. **Create an answers file** with responses to the nine discovery questions (numbered `1.` through `9.`).

3. **Start the CLI**:
   ```bash
   arcindex start --project-name "Arcindex" --answers-file path/to/answers.txt --elicitation-choice 1
   ```

   If you prefer not to install the package, set `PYTHONPATH=.` and run `python3 -m arcindex.cli ...` instead.

4. **Optional flags**:
   - `--config` – point to a custom runtime configuration file.
   - `--mode` – override the operation mode (`interactive`, `batch`, or `yolo`).
   - `--answers-file` – provide a numbered answers file to skip interactive prompts.
   - `--elicitation-choice` – non-interactive selection for the elicitation menu (default is `1`).

The CLI writes `workflow.json` and `discovery-summary.json` to the configured state directory, ready for the analyst phase in the upcoming milestone.

### Spin Up an Isolated Test Workspace

Use the built-in harness to create disposable sandboxes so you can experiment without touching the main project tree:

```bash
arcindex/test-harness/scripts/run-test.sh --local
# or test a different branch
arcindex/test-harness/scripts/run-test.sh --branch main
```

Each run produces a new folder under `arcindex/test-harness/results/arcindex-<mode>-<timestamp>/` containing a clean copy of the code and a pre-filled `discovery-inputs.txt`. Follow the printed instructions to install dependencies and run `arcindex start ...` inside the sandbox. Delete the folder when you're done.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Features

Planned features for the Arcindex SDK implementation:

- **CLI-first orchestration** with workflow configs, mode awareness, and state persistence.
- **Persona-driven assistants** for discovery, analyst, PM, architect, PRP, developer, and QA roles.
- **Progressive validation gates** with scoring, evidence capture, and escalation paths.
- **Epic-aware planning** and PRP generation for incremental delivery.
- **Quality automation** including PRP verification logs, failure escalation, and QA handoffs.
- **Regression harness** to compare outputs and validation metrics across runs.

As phases complete, this section will expand with concrete capabilities and links to documentation.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Roadmap

- [x] Repository restructure and migration plan
- [ ] Phase 0: Scaffold `arcindex/`, Python environment, lint/test tooling
- [ ] Phase 1: Discovery orchestrator MVP (CLI entry point, state persistence, elicitation)
- [ ] Phase 2: Analyst phase integration with gating and artifact generation
- [ ] Phase 3: Product management phase (PRD generation, checklist enforcement)
- [ ] Phase 4: Architecture phase with epic-aware planning and confidence scoring
- [ ] Phase 5: PRP creation, failure escalation, and validation level tooling
- [ ] Phase 6: QA persona, quality automation, reporting
- [ ] Phase 7: Regression harness parity, documentation suite, initial SDK release

See the [open issues](https://github.com/BeardedWonder/CODEX/issues) for up-to-date priorities, or propose new tasks aligned with the phases above.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Contributing

Arcindex welcomes contributions that align with the migration roadmap.

1. Fork the repository.
2. Create a feature branch for your phase/task.
3. Discuss major design changes via issues or draft PRs before implementation.
4. Run formatting and tests (commands will be documented once Phase 0 tooling lands).
5. Submit a PR referencing the relevant migration phase.

> During the migration, avoid modifying files inside `legacy/` unless a migration task explicitly requires reference updates.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Contact

Project Maintainer – Brian Pistone  
Project Link – [https://github.com/BeardedWonder/CODEX](https://github.com/BeardedWonder/CODEX)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Acknowledgments

- The BMAD Method project and contributors for the baseline agent workflows, elicitation patterns, and checklist rigor that inspired CODEX and now Arcindex.
- The Product Requirement Prompt (PRP) community for the structured implementation playbooks we continue to refine.
- All contributors to the original CODEX orchestration prototype.
- OpenAI Codex SDK for the upcoming runtime foundation.
- Community tools and libraries that will support the migration.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
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
