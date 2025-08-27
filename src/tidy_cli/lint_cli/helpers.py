"""Module defining helpers functions for the CLI Linting Commands Group."""

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


def run_command(
    command: list[str],
    description: str,
) -> bool:
    """
    Function aimed at running terminal commands via subprocess, capture output and print either stdout or stderr (via Rich).

    :param command: list of commands to be executed (the list is made of elements that toghether form a single terminal command)
    :type command: list[str]
    :param description: label of the command being executed (e.g., mypy)
    :type description: str
    :return: True if the command goes fine and False otherwise
    :rtype: bool
    """
    try:
        console.print(f"🔧 {description}...")
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            console.print(f"✅ {description} completed successfully")
            console.print(result.stdout, style="white") if result.stdout else console.print("")
            return True
        else:
            console.print(f"❌ {description} failed", style="red")
            if result.stdout:
                console.print(result.stdout, style="red")
            if result.stderr:
                console.print(result.stderr, style="red")
            return False
    except Exception as e:
        console.print(f"❌ Error running {description}: {e}", style="red")
        return False


def init_settings() -> None:
    """
    Function aimed at initializing CLI Linting Commands Group settings.
    It initializes the default directory, namely the one the linters are applied if nothing is provided
    or relative to which the subfolder/file is linted.
    By design it is defaulted, if nothing is provided, with 'src'.

    :return: None
    :rtype: None
    """
    console.print("🔧 Initializing Linter settings...\n")

    # Load settings
    current_settings = load_settings()

    # Default settings
    default_lint_path = current_settings.get("lint_default_path", "src")
    default_config_path = current_settings.get("lint_config_path", "pyproject.toml")

    # Configure default Linter path
    lint_path = typer.prompt(
        "▪ Default path to lint / parent folder to the path to be linted",
        default=default_lint_path,
        show_default=True,
        type=Path,
    )

    # Configure Linter config file path
    config_path = typer.prompt(
        "▪ Path to Linter config file (relative to current working directory)",
        default=default_config_path,
        show_default=True,
        type=Path,
    )

    new_settings = {
        "lint_default_path": str(lint_path),
        "lint_config_path": str(config_path),
    }

    # Save settings
    update_settings(new_settings)

    console.print(f"\n✅ Settings saved to [bold]{SETTINGS_FILE}[/bold]", style="white")
    console.print(f"📁 Linter default directory: [bold]{lint_path}[/bold]", style="white")
    console.print(f"📄 Linter config file path: [bold]{config_path}[/bold]", style="white")


def get_lint_default_path() -> Path:
    """
    Function aimed at getting Lint default path from settings, or default.

    :return: default directory path
    :rtype: Path
    """
    settings = load_settings()
    if "lint_default_path" in settings:
        return Path(settings["lint_default_path"])
    return Path("src")


def get_lint_config_path() -> str:
    """
    Function aimed at getting Lint config file path from settings, or default.

    :return: config file path
    :rtype: str
    """
    settings = load_settings()
    if "lint_config_path" in settings:
        return settings["lint_config_path"]
    return "pyproject.toml"
