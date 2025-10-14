#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Arcindex test harness

Usage: run-test.sh [--answers <file>]

Options:
  --answers <file>   Use a custom discovery answers file for the workspace template.
  -h, --help         Show this help message.

Examples:
  ./run-test.sh
  ./run-test.sh --answers ~/custom-inputs.txt
EOF
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
HARNESS_DIR="$ROOT_DIR/arcindex/test-harness"
RESULTS_DIR="$HARNESS_DIR/results"
ARCHIVE_DIR="$HARNESS_DIR/archive"
TEMPLATES_DIR="$HARNESS_DIR/templates"

ANSWERS_TEMPLATE="$TEMPLATES_DIR/discovery-inputs.txt"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --answers)
      ANSWERS_TEMPLATE="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ ! -f "$ANSWERS_TEMPLATE" ]]; then
  echo "❌ Answers template not found: $ANSWERS_TEMPLATE" >&2
  exit 1
fi

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
RUN_ID="arcindex-local-${TIMESTAMP}"
TARGET_DIR="$RESULTS_DIR/$RUN_ID"

mkdir -p "$TARGET_DIR" "$ARCHIVE_DIR"

# Copy runtime
rsync -a \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  "$ROOT_DIR/arcindex/" "$TARGET_DIR/arcindex/"

# Copy top-level metadata files when present
for file in pyproject.toml README.md MIGRATION-PLAN.md AGENTS.md LICENSE; do
  if [[ -f "$ROOT_DIR/$file" ]]; then
    cp "$ROOT_DIR/$file" "$TARGET_DIR/" 2>/dev/null || true
  fi
done

cp "$ANSWERS_TEMPLATE" "$TARGET_DIR/discovery-inputs.txt"

cat <<EOF
✅ Created Arcindex test workspace

Location: $TARGET_DIR
Template answers: $ANSWERS_TEMPLATE

Next steps:
  cd "$TARGET_DIR"
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -e '.[dev]'
  arcindex start --project-name "Arcindex Test" \\
    --answers-file discovery-inputs.txt \\
    --elicitation-choice 1

When you're finished, remove the workspace by deleting the directory.
Artifacts and event logs will be written under runs/<run_id>/ within the workspace.
EOF
