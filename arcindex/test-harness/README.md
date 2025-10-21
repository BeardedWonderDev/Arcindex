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
│   └── discovery-task.txt  # Canonical discovery prompt
├── results/               # Generated workspaces (gitignored)
└── archive/               # Reserved for future automation (gitignored)
```

## Quick Start

1. **Create a workspace**

   ```bash
   arcindex/test-harness/scripts/run-test.sh
   ```

   Pass `--task <file>` to reuse an alternative prompt file.

2. **Follow the instructions** the script prints to initialise a virtual environment and run the CLI:

   ```bash
   cd arcindex/test-harness/results/arcindex-local-main-20250101-123000
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e '.[dev]'
   cp ../../.env .    # optional: reuse your API key in the sandbox
   arcindex start --task "$(< discovery-task.txt)"
   ```

3. **Inspect outputs** inside the workspace. Every run writes to the quickstart run tree:
   - `runs/<run_id>/workflow.json` – current workflow snapshot.
   - `runs/<run_id>/discovery-summary.json` – structured discovery output.
   - `runs/<run_id>/logs/events.ndjson` – event stream suitable for SSE clients.
   Delete the folder when you are finished.

4. **Repeatable runs**. The copied `discovery-task.txt` contains the canonical discovery answers lifted from the legacy workflow. Edit or swap it with `--task <file>` when invoking `run-test.sh` if you need different scenarios.

## Notes

- Workspaces live under `arcindex/test-harness/results/` and are ignored by git.
- The `archive/` directory exists for future automation (analysis scripts can move completed runs there).
- The harness intentionally keeps dependencies minimal; expand as subsequent phases introduce additional workflows or when wiring the FastAPI bridge into workspace tests.
