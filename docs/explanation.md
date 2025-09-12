# Explanation

Understanding the concepts and philosophy behind Tidy CLI.

## :material-lightbulb: Why Tidy CLI Exists

### :material-puzzle: The Problem

Modern Python development involves multiple quality assurance tools:

- **Ruff** for linting and formatting
- **MyPy** for static type checking  
- **Pydoclint** for docstring validation
- **Pytest** for testing with coverage

Each tool requires separate installation, configuration, and execution. Developers often struggle with:

- Remembering different command syntaxes
- Managing tool-specific configurations
- Ensuring consistent execution across team members
- Setting up CI/CD pipelines with multiple tool calls

### :material-target: The Solution

Tidy CLI unifies these essential tools under a single, intuitive interface.
Instead of running:

```bash
ruff check src/ --fix
ruff format src/
mypy src/
pydoclint src/
pytest tests/ --cov=src --cov-report=html
```

You simply run:

```bash
tidy-cli lint run --fix
tidy-cli pytest run
```

## :material-book-open-variant: Design Philosophy

### :material-code-block-tags: Simplicity First

Tidy CLI prioritizes ease of use over extensive customization. The tool makes opinionated choices about:

- **Default configurations**: Sensible defaults that work for most Python projects
- **Command structure**: Intuitive verb-noun patterns (`lint run`, `pytest run`)
- **Output formatting**: Clean, readable results from all tools

### :material-cog: Configuration Over Convention

While providing defaults, Tidy CLI respects your existing configurations:

- Uses your `pyproject.toml` settings for each tool
- Allows path customization for different project structures
- Supports skipping tools that don't fit your workflow

### :material-sitemap: Workflow Integration

Tidy CLI is designed to fit seamlessly into existing development workflows:

- **Local development**: Quick quality checks during coding
- **Pre-commit hooks**: Automated fixing before commits
- **CI/CD pipelines**: Consistent quality gates
- **IDE integration**: Works with existing tool configurations

## :material-tools: Tool Selection

Tidy CLI integrates best-in-class Python tools:

- **Ruff**: Fast, comprehensive linting and formatting
- **MyPy**: Industry-standard static type checking
- **Pydoclint**: Docstring validation and consistency
- **Pytest**: Flexible testing with coverage reporting

Each tool was selected for performance, reliability, and ecosystem adoption.

## :material-layers: Architecture Overview

### :material-file-tree: Project Structure

Tidy CLI expects a conventional Python project structure:

```
project/
├── src/           # Source code
│    └── tests/    # Test files  
├── local/         # Tidy CLI settings
└── pyproject.toml # Tool configurations
```

This structure promotes:

- **Separation of concerns**: Clear boundaries between source and tests
- **Tool compatibility**: Standard layout works with all integrated tools
- **Scalability**: Structure scales from small scripts to large applications

### :material-wrench-outline: Configuration Management

Tidy CLI uses a two-tier configuration system:

1. **Tidy CLI settings** (`local/tidy_cli_settings.json`): Path and execution preferences
2. **Tool configurations** (`pyproject.toml`): Individual tool settings

This separation allows:

- **Project-specific paths**: Adapt to different project layouts
- **Tool independence**: Maintain existing tool configurations
- **Team consistency**: Share Tidy CLI settings while preserving individual tool preferences

### :material-play: Execution Model

Tidy CLI follows a simple execution model:

1. **Load settings**: Read project-specific configuration
2. **Resolve paths**: Determine target files/directories
3. **Execute tools**: Run tools in logical order
4. **Aggregate results**: Combine outputs into unified report

## :material-compare: Design Approach

Tidy CLI complements existing tools rather than replacing them:

- **vs. Make/Scripts**: Cross-platform, no maintenance overhead
- **vs. Pre-commit**: Use together for complete workflow coverage
- **vs. All-in-One**: Best-of-breed tools with unified interface

