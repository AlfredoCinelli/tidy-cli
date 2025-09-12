# Tutorials

Step-by-step guides to get you started with Tidy CLI.

## :material-play: Getting Started

### :material-download: 1. Installation

Install Tidy CLI using your preferred package manager:

=== ":fontawesome-brands-python: pip"
    ```bash
    pip install tidy-cli
    ```

=== ":material-package-variant: uv"
    ```bash
    uv pip install tidy-cli
    # or add to project
    uv add tidy-cli
    ```

### :material-cog: 2. First Setup

Initialize Tidy CLI in your project:

```bash
tidy-cli init
```

This will prompt you for:
- **Pytest folder path**: Directory containing your tests (usually `tests` or `.`)
- **Pyproject.toml location**: Path to your configuration file
- **Default lint path**: Directory to lint by default (usually `src`)
- **Config path**: Location of pyproject.toml relative to current directory

### :material-check-circle: 3. Your First Lint Run

Run a complete code quality check:

```bash
tidy-cli lint run
```

This executes:
- **Ruff**: Fast Python linter and formatter
- **MyPy**: Static type checking
- **Pydoclint**: Docstring validation

### :material-auto-fix: 4. Auto-fixing Issues

Let Tidy CLI fix what it can automatically:

```bash
tidy-cli lint run --fix
```

### :material-test-tube: 5. Running Tests

Execute your test suite with coverage:

```bash
tidy-cli pytest run
```

## :material-pipe: Complete Workflow

### New Project Setup
```bash
mkdir my-project && cd my-project
mkdir src tests
tidy-cli init  # Follow prompts
tidy-cli lint run --fix
```

### Existing Project
```bash
cd existing-project
tidy-cli init
tidy-cli lint run --interactive  # Review each tool
```

### Runtime Configuration Override
```bash
# Override settings temporarily without changing saved configuration
tidy-cli lint run --default-dir backend/src
tidy-cli pytest run --default-dir backend/tests --pyproject-path backend/pyproject.toml
```

## :material-arrow-right: Next Steps

- Learn about [specific commands](how-to-guides.md)
- Explore [configuration options](reference.md)
- Understand [the concepts](explanation.md) behind Tidy CLI