# Reference

Complete command and configuration reference for Tidy CLI.

## :material-console: Commands

### Main Commands

| Command | Description |
|---------|-------------|
| `tidy-cli` | Display help and available commands |
| `tidy-cli version` | Show current version |
| `tidy-cli init` | Initialize project settings (interactive) |
| `tidy-cli --install-completion` | Install shell completion |
| `tidy-cli --help` | Show help about commands (available for each subcommand `pytest` and `lint`) |

### :material-code-tags: Lint Commands

#### `tidy-cli lint run`
Run all linting tools (ruff, mypy, pydoclint).

```bash
tidy-cli lint run [PATH] [OPTIONS]
```

**Arguments:**
- `PATH` (optional): Specific file or directory to lint. Defaults to configured lint path.

**Options:**
- `--fix`: Auto-fix issues where possible
- `--interactive`: Prompt before running each tool
- `--skip-ruff`: Skip Ruff linting
- `--skip-format`: Skip Ruff formatting
- `--skip-mypy`: Skip MyPy type checking
- `--skip-pydoclint`: Skip Pydoclint docstring checking
- `--default-dir`: Override the default lint directory at runtime
- `--pyproject-path`: Override the pyproject.toml path at runtime (relative to current working directory)



#### `tidy-cli lint init`
Initialize lint-specific settings.

```bash
tidy-cli lint init
```

### :material-test-tube: Pytest Commands

#### `tidy-cli pytest run`
Run tests with coverage reporting.

```bash
tidy-cli pytest run [PATH] [OPTIONS]
```

**Arguments:**
- `PATH` (optional): Specific test file or directory. Defaults to configured pytest path.

**Options:**
- `--logs`, `-l`: Show detailed test output (only available when PATH is specified)
- `--extra`, `-e`: Pass additional pytest options (can be used multiple times)
- `--default-dir`: Override the default test directory at runtime
- `--pyproject-path`: Override the pyproject.toml path at runtime (relative to default directory)



#### `tidy-cli pytest init`
Initialize pytest-specific settings.

```bash
tidy-cli pytest init
```

## :material-cog: Configuration

### Settings File

Tidy CLI stores configuration in `local/tidy_cli_settings.json`:

```json
{
  "lint_default_path": "src",
  "lint_config_path": "pyproject.toml",
  "pytest_default_path": "tests", 
  "pytest_config_path": "pyproject.toml"
}
```

**Configuration Options:**

| Setting | Description | Default |
|---------|-------------|---------|
| `lint_default_path` | Default directory to lint | `"src"` |
| `lint_config_path` | Path to pyproject.toml for linting tools | `"pyproject.toml"` |
| `pytest_default_path` | Default directory for tests | `"tests"` |
| `pytest_config_path` | Path to pyproject.toml for pytest | `"pyproject.toml"` |

### Tool Configuration Example

Configure underlying tools in `pyproject.toml` (the below are just examples, so **amend** them based on **your project**):

#### :material-lightning-bolt: Ruff Configuration

```toml
[tool.ruff]
target-version = "py310"
line-length = 175

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
    "UP", # pyupgrade
]
ignore = [
    "B008",  # do not perform function calls in argument defaults
]
```

#### :material-wrench-outline: MyPy Configuration

```toml
[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
```

#### :material-text-box: Pydoclint Configuration

```toml
[tool.pydoclint]
style = "sphinx"
arg-type-hints-in-docstring = true
arg-type-hints-in-signature = true
check-arg-order = true
```

#### :material-test-tube: Pytest Configuration

```toml
[tool.pytest.ini_options]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

[tool.coverage.run]
omit = [
    "tests/*",
    "**/__init__.py",
]
```

## :material-exit-to-app: Exit Codes

| Code | Description |
|------|-------------|
| `0` | Success |
| `1` | General error |

## :material-folder: File Structure

Expected project structure for default Tidy CLI usage (default paths can be confifured as shown above):

```
project/
├── src/                    # Source code (lint_default_path)
│   └── my_package/
│       ├── __init__.py
│       └── module.py
├── tests/                  # Test files (pytest_default_path)
│   ├── __init__.py
│   └── test_module.py
├── local/                  # Tidy CLI settings
│   └── tidy_cli_settings.json
├── pyproject.toml          # Tool configurations
└── README.md
```

## :material-link: Integration Examples

### GitHub Actions

```yaml
name: Code Quality
on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install tidy-cli
          pip install -r requirements.txt
      - name: Run linting
        run: tidy-cli lint run
      - name: Run tests
        run: tidy-cli pytest run
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: tidy-cli
        name: Tidy CLI
        entry: tidy-cli lint run --fix
        language: system
        pass_filenames: false
        always_run: true
```