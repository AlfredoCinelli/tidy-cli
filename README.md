<div align="center">
  <img src="https://raw.githubusercontent.com/AlfredoCinelli/tidy-cli/main/docs/logo.jpeg" alt="Tidy CLI Logo" width="200">
  <p><em>Keep your code clean and robust!</em></p>
</div>

<div align="center">

[![Python Versions](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/AlfredoCinelli/tidy-cli)
[![PyPI Latest Release](https://img.shields.io/badge/pypi-3775A9?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/tidy-cli/)
[![License - MIT](https://img.shields.io/badge/MIT-black?style=for-the-badge)](https://github.com/AlfredoCinelli/tidy-cli/blob/main/LICENSE)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:alfredocinelli96@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/alfredocinelli/)

---

</div>

<div align="center">
  <p><em>Platforms</em></p>
</div>

<div align="center">

[![Mac OS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white)]()
[![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)]()
[![Windows WSL](https://img.shields.io/badge/Windows%20WSL-0078D6?style=for-the-badge&logo=windows&logoColor=white)]()

</div>

---

**Tidy CLI** simplifies your development process by combining essential tools like ruff, mypy, pydoclint, and pytest into a single, easy-to-use command-line interface. Perfect for maintaining code quality and running tests across Python projects of any size.

## 📚 Documentation

For a detailed documenation, please visit this [link](https://alfredocinelli.github.io/tidy-cli/).
But if you are rushing, just keep reading this short overview!

## ✨ Key Features

- **🔧 Unified Linting**: Combines ruff, mypy, and pydoclint in one command
- **🎨 Smart Formatting**: Automatic code formatting with ruff
- **🧪 Integrated Testing**: Run pytest with coverage reporting
- **⚡ Auto-fix**: Automatically fix linting issues where possible
- **🔄 Interactive Mode**: Review and apply fixes interactively
- **📊 Flexible Execution**: Target specific files, directories, or entire projects
- **⚙️ Configurable**: Skip tools, customize paths, and adapt to your workflow

## 🚀 Installation

### With pip

```bash
# Using pip
pip install tidy-cli
```

### With uv (recommended)

```bash
uv pip install tidy-cli
```
```bash
uv add tidy-cli
```

### Requirements

- Python 3.10+
- Works on Linux, macOS, and Windows (WSL only)

> **Note**: On Windows, tidy-cli requires WSL (Windows Subsystem for Linux) for proper Unicode and terminal support. Native Windows is not currently supported.

## 🏃 Quick Start

### 1. Get a Feeling

```bash
# See what you are dealing with
tidy-cli
```

```bash
# Deep dive on what you are dealing with
tidy-cli --help
```

```bash
# Install auto-completion for easier usage
tidy-cli --install-completion
```

```bash
# Set up tidy-cli for your project
tidy-cli init
```
The settings are about:
- The Pytest folder path, just type `.` if no `chdir` is made when running tests.
- The location of the `pyproject.toml` file relative to the Pytest folder path.
- The default path to lint if no other path is passed (e.g., `src` if one wants to lint the entire `src` folder as default).
- The path to the `pyproject.toml` relative to the `cwd` when running the `lint` commands.

### 2. Run Code Quality Checks

```bash
# Lint your entire project (i.e., on the default lint path)
tidy-cli lint run

# Auto-fix (fixable) issues
tidy-cli lint run --fix
```

### 3. Run Tests

```bash
# Run all tests with coverage
tidy-cli pytest run
```

That's it! Tidy CLI will handle the rest.

## 📖 Usage Guide

### Code Quality & Linting Commands

```bash
# Run all linters (ruff, mypy, pydoclint)
tidy-cli lint run

# Target specific files or directories (relative to the default path/folder)
tidy-cli lint run src/my_module
tidy-cli lint run my_module/file.py # if src has been chosen as default path/folder

# Interactive mode (i.e., you are prompted if to run a specific linter/formatter/checker)
tidy-cli lint run --interactive

# Auto-fix issues where possible
tidy-cli lint run --fix

# Skip specific linters
tidy-cli lint run --skip-mypy
tidy-cli lint run --skip-pydoclint

# Override default directory and config at runtime
tidy-cli lint run --default-dir custom_src
tidy-cli lint run --pyproject-path custom/pyproject.toml
```

### Testing Commands

```bash
# Run all tests with coverage
tidy-cli pytest run

# Run specific test files
tidy-cli pytest run tests/test_example.py

# Show detailed test output on a path (logs can be displayed only on path runs)
tidy-cli pytest run tests/test_example.py --logs

# Pass extra pytest options (with --extra -s or -e -s logs can be displayed at any level)
tidy-cli pytest run --extra -v --extra -s
tidy-cli pytest run tests/test_example.py --extra --tb=short

# Override default directory and config at runtime
tidy-cli pytest run --default-dir custom_tests
tidy-cli pytest run --pyproject-path custom/pyproject.toml
```

### CLI Configuration

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

Tidy CLI stores settings in `local/tidy_cli_settings.json` with sensible defaults:

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
- **Documentation**: [Mkdocs Documentation](https://alfredocinelli.github.io/tidy-cli/)

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