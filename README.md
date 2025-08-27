# Tidy CLI

[![PyPI Latest Release](https://img.shields.io/pypi/v/tidy-cli.svg)](https://pypi.org/project/tidy-cli/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/tidy-cli.svg)](https://pypi.org/project/tidy-cli/)
[![Python Versions](https://img.shields.io/pypi/pyversions/tidy-cli.svg)](https://pypi.org/project/tidy-cli/)
[![License - MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/AlfredoCinelli/tidy-cli/blob/main/LICENSE)

> A streamlined CLI tool that unifies Python development workflows with integrated linting, formatting, and testing capabilities.

**Tidy CLI** simplifies your development process by combining essential tools like ruff, mypy, pydoclint, and pytest into a single, easy-to-use command-line interface. Perfect for maintaining code quality and running tests across Python projects of any size.

## ✨ Key Features

- **🔧 Unified Linting**: Combines ruff, mypy, and pydoclint in one command
- **🎨 Smart Formatting**: Automatic code formatting with ruff
- **🧪 Integrated Testing**: Run pytest with coverage reporting
- **⚡ Auto-fix**: Automatically fix linting issues where possible
- **🔄 Interactive Mode**: Review and apply fixes interactively
- **📊 Flexible Execution**: Target specific files, directories, or entire projects
- **⚙️ Configurable**: Skip tools, customize paths, and adapt to your workflow

## 🚀 Installation

### From PyPI (Recommended)

```bash
# Using pip
pip install tidy-cli

# Using uv (faster)
uv pip install tidy-cli
```

### Requirements

- Python 3.10+
- Works on Linux, macOS, and Windows

## 🏃 Quick Start

### 1. Initialize Your Project

```bash
# Set up tidy-cli for your project
tidy-cli init
```

### 2. Run Code Quality Checks

```bash
# Lint your entire project
tidy-cli lint run

# Auto-fix issues
tidy-cli lint run --fix
```

### 3. Run Tests

```bash
# Run tests with coverage
tidy-cli pytest run
```

That's it! Tidy CLI will handle the rest.

## 📖 Usage Guide

### Code Quality & Linting

```bash
# Run all linters (ruff, mypy, pydoclint)
tidy-cli lint run

# Target specific files or directories
tidy-cli lint run src/my_module
tidy-cli lint run src/my_module/file.py

# Interactive mode - review each issue
tidy-cli lint run --interactive

# Auto-fix issues where possible
tidy-cli lint run --fix

# Skip specific linters
tidy-cli lint run --skip-mypy
tidy-cli lint run --skip-pydoclint
```

### Testing

```bash
# Run all tests with coverage
tidy-cli pytest run

# Run specific test files
tidy-cli pytest run tests/test_example.py

# Show detailed test output on a path
tidy-cli pytest run tests/test_example.py --logs
```

### Configuration

```bash
# Initialize settings for all tools
tidy-cli init

# Initialize specific tool settings
tidy-cli lint init
tidy-cli pytest init

# Show current version
tidy-cli version
```

## ⚙️ Configuration

Tidy CLI stores settings in `local/cli_settings.json` with sensible defaults:

```json
{
  "lint_default_path": "src",
  "lint_config_path": "pyproject.toml",
  "pytest_default_path": "tests",
  "pytest_config_path": "pyproject.toml"
}
```

### Tool Configuration

Configure the underlying tools in your `pyproject.toml`:

```toml
[tool.ruff]
lint.select = [
    "I", 
    "E", 
    "F", 
    "W", 
    "C90",
    "N", 
    "D", 
]

[tool.mypy]
python_version = "3.11"
ignore_missing_imports = true

[tool.pydoclint]
style = "sphinx"

[tool.coverage.run]
omit = [
    "tests/*",
]
```

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Run the tests**: `tidy-cli pytest run`
5. **Run the linters**: `tidy-cli lint run --fix`
6. **Commit your changes**: `git commit -m 'Add amazing feature'`
7. **Push to the branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### Development Setup

```bash
git clone https://github.com/alfredo-cinelli/tidy-cli.git
cd tidy-cli
uv venv .venv --python=3.12
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync --group dev
uv pip install -e .
```

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

## 🐛 Issues & Support

- **Bug Reports**: [GitHub Issues](https://github.com/AlfredoCinelli/tidy-cli/issues)
- **Documentation**: [GitHub Wiki](https://github.com/AlfredoCinelli/tidy-cli/wiki)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ruff](https://github.com/astral-sh/ruff) - Fast Python linter and formatter
- [MyPy](https://github.com/python/mypy) - Static type checker
- [Pydoclint](https://github.com/jsh9/pydoclint) - Docstring linter
- [Pytest](https://github.com/pytest-dev/pytest) - Testing framework

---

<div align="center">
  <strong>Made with ❤️ for the Python community</strong>
</div>