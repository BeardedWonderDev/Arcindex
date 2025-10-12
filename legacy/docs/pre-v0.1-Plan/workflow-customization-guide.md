# CODEX Workflow Customization Guide

## Generic Workflow Setup

The `greenfield-generic.yaml` workflow provides a foundation for any programming language. Follow these steps to customize it for your project:

### 1. Language Configuration

Replace placeholders in the workflow file:

```yaml
# Set your primary language
primary: "python"  # javascript, go, rust, etc.

# Set your framework (optional)
framework: "django"  # react, gin, actix, etc.
```

### 2. Command Customization

Update validation commands for your tech stack:

```yaml
tooling:
  - "python -m py_compile ."  # Build/compile command
  - "python -m pytest"        # Test command
  - "flake8 ."               # Lint command
  - "black --check ."        # Format command
```

### 3. Validation Gate Setup

Customize each validation level:

- **Level 1**: Basic syntax checking
- **Level 2**: Unit tests
- **Level 3**: Integration tests
- **Level 4**: Full validation suite

### 4. Language Examples

The workflow includes examples for:
- JavaScript/React
- Python/Django
- Go/Gin
- Rust/Actix

Copy the relevant example and modify for your specific needs.

### 5. Creating Language-Specific Workflows

For frequently used languages, create dedicated workflow files:

1. Copy `greenfield-generic.yaml`
2. Name it `greenfield-{language}.yaml`
3. Remove placeholders and add language-specific configurations
4. Add to workflow selection system

## Supported Languages

Currently tested with:
- Swift (existing)
- JavaScript/TypeScript
- Python
- Go
- Rust

Additional languages can be added by following the customization pattern.

## Language-Specific Configuration Examples

### JavaScript/React Example

```yaml
language_support:
  primary: "javascript"
  framework: "react"
  validation_method: "command_based"
  tooling:
    - "npm run build"
    - "npm test"
    - "eslint src/"
    - "prettier --check src/"

validation_gates:
  level_1:
    commands:
      - "node --check src/**/*.js"
      - "npm run lint:check"
  level_2:
    commands:
      - "npm run test:unit"
  level_3:
    commands:
      - "npm run test:integration"
  level_4:
    commands:
      - "npm run build:prod"
      - "npm run test:all"
      - "eslint --max-warnings 0 src/"
      - "prettier --check src/"
```

### Python/Django Example

```yaml
language_support:
  primary: "python"
  framework: "django"
  validation_method: "command_based"
  tooling:
    - "python -m py_compile ."
    - "python -m pytest"
    - "flake8 ."
    - "black --check ."

validation_gates:
  level_1:
    commands:
      - "python -m py_compile ."
      - "flake8 --max-line-length=88 ."
  level_2:
    commands:
      - "python -m pytest tests/unit/"
  level_3:
    commands:
      - "python -m pytest tests/integration/"
  level_4:
    commands:
      - "python -m pytest --cov=. --cov-report=html"
      - "flake8 --max-complexity=10 ."
      - "black --check ."
      - "mypy ."
```

### Go/Gin Example

```yaml
language_support:
  primary: "go"
  framework: "gin"
  validation_method: "command_based"
  tooling:
    - "go build ./..."
    - "go test ./..."
    - "golangci-lint run"
    - "gofmt -d ."

validation_gates:
  level_1:
    commands:
      - "go build ./..."
      - "gofmt -d ."
  level_2:
    commands:
      - "go test ./..."
  level_3:
    commands:
      - "go test -race ./..."
  level_4:
    commands:
      - "go build -race ./..."
      - "go test -cover ./..."
      - "golangci-lint run"
      - "go vet ./..."
```

### Rust/Actix Example

```yaml
language_support:
  primary: "rust"
  framework: "actix"
  validation_method: "command_based"
  tooling:
    - "cargo build --release"
    - "cargo test"
    - "cargo clippy -- -D warnings"
    - "cargo fmt -- --check"

validation_gates:
  level_1:
    commands:
      - "cargo check"
      - "cargo fmt -- --check"
  level_2:
    commands:
      - "cargo test --lib"
  level_3:
    commands:
      - "cargo test --all"
  level_4:
    commands:
      - "cargo build --release"
      - "cargo test --release"
      - "cargo clippy -- -D warnings"
      - "cargo audit"
```

## Customization Workflow

### Step 1: Copy Template
```bash
cp .codex/workflows/greenfield-generic.yaml .codex/workflows/greenfield-myproject.yaml
```

### Step 2: Replace Placeholders
Edit the copied file and replace all `{{PLACEHOLDER}}` values with your project-specific commands.

### Step 3: Test Configuration
```bash
# Test that your workflow loads correctly
/codex list-workflows | grep myproject

# Test workflow initialization
/codex start greenfield-myproject test-feature
```

### Step 4: Customize Validation
Adjust timeout values and validation criteria based on your project needs:

```yaml
validation_gates:
  level_4:
    timeout: 1200  # Increase for slower build processes
    commands:
      - "your-custom-build-command"
```

## Best Practices

### Command Selection
- **Level 1**: Fast syntax and style checks (< 1 minute)
- **Level 2**: Unit tests only (< 5 minutes)
- **Level 3**: Integration tests (< 10 minutes)
- **Level 4**: Full validation suite (< 15 minutes)

### Error Handling
Each validation command should:
1. Return proper exit codes (0 = success, non-zero = failure)
2. Provide meaningful error output
3. Support automation-friendly output formats

### Performance Tips
- Use parallel test execution when possible
- Cache dependencies between validation levels
- Optimize build commands for CI/CD environments

## Troubleshooting

### Common Issues

**Workflow not found:**
```bash
# Check workflow is in correct directory
ls .codex/workflows/
```

**Command timeouts:**
```yaml
# Increase timeout in workflow definition
timeout: 1800  # 30 minutes
```

**Missing tools:**
```bash
# Ensure all required tools are installed
which python npm go cargo swift
```

### Debugging Commands

```bash
# Test individual validation commands
python -m py_compile .
npm test
go build ./...
cargo test

# Check command exit codes
echo $?
```

## Advanced Customization

### Conditional Validation
```yaml
level_4:
  commands:
    - "npm run test:all"
    - "if [ -f package-lock.json ]; then npm audit; fi"
```

### Environment-Specific Commands
```yaml
validation_gates:
  level_2:
    commands:
      - "NODE_ENV=test npm test"
      - "RUST_BACKTRACE=1 cargo test"
```

### Custom Validation Scripts
```yaml
level_4:
  commands:
    - "./scripts/custom-validation.sh"
    - "python scripts/security-check.py"
```

## Contributing New Language Support

To add support for a new language:

1. Create example configuration following the pattern above
2. Test with a sample project
3. Document any language-specific considerations
4. Submit as enhancement to CODEX project

The goal is to make CODEX workflows accessible to any development stack while maintaining consistent quality assurance patterns.