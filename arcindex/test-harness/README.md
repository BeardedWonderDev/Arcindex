# Arcindex Test Harness

Lightweight utilities for spinning up disposable workspaces when testing the Arcindex CLI.

The harness mirrors the layout of the legacy CODEX tools but is focused on the discovery
workflow MVP. It lets you validate changes without touching the main project directory.

## Directory Layout

```
arcindex/test-harness/
├── scripts/
│   └── run-test.sh        # Create a new isolated workspace
├── templates/
│   └── discovery-inputs.txt
├── results/               # Generated workspaces (gitignored)
└── archive/               # Reserved for future automation (gitignored)
```

## Quick Start

1. **Create a workspace**

   ```bash
   arcindex/test-harness/scripts/run-test.sh --local
   ```

   - `--local` copies the current working tree (including uncommitted changes).
   - `--branch <name>` exports a clean copy of `<name>` using `git archive`.
   - `--answers <file>` overrides the default discovery inputs template.

2. **Follow the instructions** the script prints to initialise a virtual environment and run the CLI:

   ```bash
   cd arcindex/test-harness/results/arcindex-local-main-20250101-123000
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e '.[dev]'
   arcindex start --project-name "Sandbox" --answers-file discovery-inputs.txt --elicitation-choice 1
   ```

3. **Inspect outputs** inside the workspace. Every run writes to both the legacy state path and the run-scoped tree:
   - `runs/<run_id>/workflow.json` – current workflow snapshot.
   - `runs/<run_id>/discovery-summary.json` – structured discovery output.
   - `runs/<run_id>/logs/events.ndjson` – event stream suitable for SSE clients.
   The legacy copies in `arcindex/state/` remain for compatibility. Delete the folder when you are finished.

## Notes

- Workspaces live under `arcindex/test-harness/results/` and are ignored by git.
- The `archive/` directory exists for future automation (analysis scripts can move completed runs there).
- The harness intentionally keeps dependencies minimal; expand as subsequent phases introduce additional workflows or when wiring the FastAPI bridge into workspace tests.
