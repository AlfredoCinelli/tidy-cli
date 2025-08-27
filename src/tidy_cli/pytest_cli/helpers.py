"""Module defining helpers functions for th CLI Pytest Commands Group."""

# Import packages and modules
import subprocess
from pathlib import Path

import typer
from rich.console import Console

from tidy_cli.commons.settings import (
    SETTINGS_FILE,
    load_settings,
    update_settings,
)

console = Console()


def cleanup_test_cache() -> None:
    """
    Function aimed at cleaning up pytest cache files.

    :return: None
    :rtype: None
    """
    try:
        subprocess.run(["find", ".", "-name", "__pycache__", "-type", "d", "-exec", "rm", "-rf", "{}", "+"], capture_output=True)
        subprocess.run(["find", ".", "-name", "*.pyc", "-delete"], capture_output=True)
        subprocess.run(["find", ".", "-name", "*.pyo", "-delete"], capture_output=True)
        console.print("🧹 Test cache cleaned up", style="white")
    except Exception as e:
        console.print(f"⚠️ Warning: Could not clean up test cache: {e}", style="yellow")


def init_settings() -> None:
    """
    Function aimed at initializing CLI Pytest Commands Group settings.
    It initializes the default directory, namely the one the system cd into.
    By design it is defaulted, if nothing is provided, with 'src'.

    :return: None
    :rtype: None
    """
    console.print("🔧 Initializing Pytest settings...\n", style="white")

    # Load settings
    current_settings = load_settings()

    # Default settings
    default_test_path = current_settings.get("pytest_default_path", "src")
    default_config_path = current_settings.get("pytest_config_path", "../pyproject.toml")

    # Configure default test path
    test_path = typer.prompt(
        "▪ Default path to tests",
        default=default_test_path,
        show_default=True,
        type=Path,
    )

    # Configure Pytest config file path
    config_path = typer.prompt(
        "▪ Path to Pytest config file (relative to default directory)",
        default=default_config_path,
        show_default=True,
        type=Path,
    )

    new_settings = {
        "pytest_default_path": str(test_path),
        "pytest_config_path": str(config_path),
    }

    # Save settings
    update_settings(new_settings)

    console.print(f"\n✅ Settings saved to [bold]{SETTINGS_FILE}[/bold]", style="white")
    console.print(f"📁 Pytest default directory: [bold]{test_path}[/bold]", style="white")
    console.print(f"📄 Pytest config file path: [bold]{config_path}[/bold]", style="white")


def get_pytest_default_path() -> Path:
    """
    Function aimed at getting Pytest default path from settings, or default.

    :return: default directory path
    :rtype: Path
    """
    settings = load_settings()
    if "pytest_default_path" in settings:
        return Path(settings["pytest_default_path"])
    return Path("src")


def get_pytest_config_path() -> str:
    """
    Function aimed at getting Pytest config file path from settings, or default.

    :return: config file path
    :rtype: str
    """
    settings = load_settings()
    if "pytest_config_path" in settings:
        return settings["pytest_config_path"]
    return "../pyproject.toml"
