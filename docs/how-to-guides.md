# How-To Guides

Practical solutions for common tasks with Tidy CLI.

## :material-code-tags: Linting & Code Quality

### :material-filter: How to run specific linters

Skip tools you don't need:

```bash
# Skip Ruff (linting)
tidy-cli lint run --skip-ruff

# Skip Ruff (formatting)
tidy-cli lint run --skip-format

# Skip MyPy type checking
tidy-cli lint run --skip-mypy

# Skip Pydoclint docstring checking
tidy-cli lint run --skip-pydoclint

# Skip multiple tools
tidy-cli lint run --skip-mypy --skip-pydoclint
```

### :material-file-search: How to lint specific files or directories

Target specific paths:

```bash
# Lint a specific file
tidy-cli lint run src/my_module.py

# Lint a specific directory
tidy-cli lint run src/utils/

# Override default directory at runtime
tidy-cli lint run --default-dir custom_src

# Override pyproject.toml location at runtime
tidy-cli lint run --pyproject-path custom/pyproject.toml
```

### :material-chat-question: How to use interactive mode

Review each tool before running:

```bash
tidy-cli lint run --interactive
```

This prompts you to confirm each linter execution.

### :material-wrench-outline: How to auto-fix issues

Let Tidy CLI fix what it can:

```bash
# Fix all auto-fixable issues
tidy-cli lint run --fix

# Fix issues in specific files
tidy-cli lint run src/my_module.py --fix
```

## :material-test-tube: Testing

### :material-file-document: How to run specific test files

Target individual test files:

```bash
# Run tests in a directory
tidy-cli pytest run tests/unit/

# Run a specific test file
tidy-cli pytest run tests/test_example.py

# Run a specific test function
tidy-cli pytest run tests/test_example.py::test_function

# Override default test directory at runtime
tidy-cli pytest run --default-dir custom_tests

# Override pyproject.toml location at runtime
tidy-cli pytest run --pyproject-path custom/pyproject.toml
```

### :material-text-box: How to see detailed test output

Enable logging for test runs:

```bash
# Show logs (only works with specific paths)
tidy-cli pytest run tests/test_example.py --logs

# Show logs (when running on the entire default folder)
tidy-cli pytest run -e -s
```

### :material-shield: How to run tests with coverage

Coverage report out of the box:

```bash
# Tidy CLI always includes coverage report when running on the entire default folder
tidy-cli pytest run
```

### :material-shield: How to run tests with any Pytest optins

Enable native Pytest options:

```bash
# Tidy CLI allows to add any Pytest native option (example logs and verbosity)
tidy-cli pytest run -e -s -e -v
# Or with long option name
tidy-cli pytest run --extra -s --extra -v
```

## :material-cog: Configuration

### :material-check-circle: How to change default settings

Modify your settings file:

```bash
# Re-initialize to change settings
tidy-cli init

# Or edit directly: local/tidy_cli_settings.json
```

### :material-account-edit: How to override settings at runtime

Override default directories and config paths without changing your saved settings:

```bash
# Override lint default directory
tidy-cli lint run --default-dir custom_src

# Override pytest default directory
tidy-cli pytest run --default-dir custom_tests

# Override pyproject.toml location for linting
tidy-cli lint run --pyproject-path config/custom.toml

# Override pyproject.toml location for testing
tidy-cli pytest run --pyproject-path ../config/custom.toml

# Combine overrides
tidy-cli lint run --default-dir backend/src --pyproject-path backend/pyproject.toml
```

**Note:** Runtime overrides are temporary and don't modify your saved settings in `local/tidy_cli_settings.json`.

### :material-tune: How to configure tools

See [Reference](reference.md#tool-configuration) for complete configuration examples.

## :material-help-circle: Troubleshooting

- **Missing dependencies**: `pip install ruff mypy pydoclint pytest pytest-cov`
- **Path issues**: Check `local/tidy_cli_settings.json` paths

## :material-puzzle: Integration

### :material-pipe: How to use in CI/CD

Add to your workflow:

```yaml
# .github/workflows/ci.yml
- name: Install Tidy CLI
  run: pip install tidy-cli

- name: Run code quality checks
  run: tidy-cli lint run

- name: Run tests
  run: tidy-cli pytest run
```

### :material-git: How to use with pre-commit

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: tidy-cli-lint
        name: Tidy CLI Lint
        entry: tidy-cli lint run --fix
        language: system
        pass_filenames: false
```

### :material-code-braces: How to integrate with IDEs

Configure your IDE to use Tidy CLI tools:

- **Ruff**: Set as default formatter and linter
- **MyPy**: Enable as type checker
- **Pytest**: Set as test runner