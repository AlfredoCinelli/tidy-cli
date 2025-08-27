"""Module aimed at degining the CLI Pytest Commands Group."""

# Import packages and modules
import os
import subprocess
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from .helpers import (
    cleanup_test_cache,
    get_pytest_config_path,
    get_pytest_default_path,
    init_settings,
)

console = Console()

# Define Typer Pytest program (i.e., commands group)
pytest_app = typer.Typer(
    name="pytest",
    help="🧪 Run [bold]Pytest[/bold] on [bold]tests[/bold] folder or provided [bold]path[/bold] (with or without [italic]logs[/italic]).",
    add_completion=True,
    rich_markup_mode="rich",
)


@pytest_app.command(
    "run",
    help="🧪 Run [bold]Pytest[/bold] on [bold]entire[/bold] tests folder (under defaulted [italic]'src'[/italic] or what's defined at [italic]initialization[/italic]) "
    "or [bold]specific path[/bold] if provided with [bold]logs[/bold] if chosen.",
)
def run(
    path: Annotated[
        str | None,
        typer.Argument(
            help="🎞️  Specific test [bold]path[/bold] to run (relative to [italic]'default'[/italic]), "
            "otherwise entire [bold]default[/bold] folder is tested (i.e., [italic]'src'[/italic] or what's defined at initialisation).",
            callback=lambda path: "" if path is None else path,
            show_default=str(get_pytest_default_path()),
        ),
    ] = None,
    logs: Annotated[
        bool,
        typer.Option(
            "--logs",
            "-l",
            help="🔊🔇 Whether to show test [italic]logs[/italic] or not.",
        ),
    ] = False,
) -> None:
    """
    Entry point function to run Pytests on the entire default folder, 'src' or wath's defined in the settings, or a specific path.
    When running Pytest on a specific path it allows to display logs.

    :param path: optional path on which running tests
    :type path: str | None
    :param logs: whether to show logs or not, defaults to False
    :type logs: bool
    :return: None
    :rtype: None
    """
    # Change to src or default directory first
    original_cwd = Path.cwd()
    default_dir: Path = get_pytest_default_path()
    if default_dir.exists() is False:
        console.print(f"❌ Default directory not found: [bold]{default_dir}[/bold]", style="red")
        raise typer.Exit(1)
    test_path = default_dir / path # type: ignore
    # Test for the existence of the path to test when provided
    if (path) and (test_path.exists() is False):
        console.print(f"❌ Test path not found: [bold]{path}[/bold]", style="red")
        raise typer.Exit(1)
    os.chdir(default_dir)

    try:
        if path:
            console.print(f"🧪 Running tests for: [bold]{test_path}[/bold]", style="white")
            cmd = ["python", "-m", "pytest", str(path), "--disable-pytest-warnings"]
            if logs:
                # Add logs flag if chosen
                console.print("🔊 [bold]Showing[/bold] logs...", style="white")
                cmd.append("-s")
            else:
                console.print("🔇 [bold]Not showing[/bold] logs...", style="white")
            #  Run test
            result = subprocess.run(cmd)
            if result.returncode == 0:
                console.print("✅ Tests completed [bold]successfully[/bold]", style="green")
            else:
                console.print("❌ Some tests [bold]failed[/bold]", style="red")
        else:
            console.print(f"🧪 Running [bold]all[/bold] tests with [bold]coverage[/bold] for: [bold]{default_dir}[/bold]", style="white")
            pyproject_path = get_pytest_config_path()
            result = subprocess.run(["coverage", "run", f"--rcfile={pyproject_path}", "-m", "pytest", "--disable-pytest-warnings"])

            if result.returncode == 0:
                # Print coverage for success tests
                console.print("📊 Displaying [bold]coverage report[/bold]...", style="white")
                subprocess.run(["coverage", "report", "-m"])
                console.print("✅ Tests and coverage completed [bold]successfully[/bold]", style="green")
            else:
                console.print("❌ Some tests [bold]failed[/bold]", style="red")

            # Clean up coverage file (if any)
            Path(".coverage").unlink(missing_ok=True)

        # Clean up test cache
        cleanup_test_cache()

    except Exception as e:
        console.print(f"❌ Error running tests: [bold]{e}[/bold]", style="red")
        raise typer.Exit(1)  # noqa: B904
    finally:
        # Always return to original directory
        os.chdir(original_cwd)


@pytest_app.command(
    "init",
    help="🎛️  Initialize CLI [bold]default Pytest directory[/bold] and [bold]config file path[/bold] settings.",
)
def init() -> None:
    """
    Function aimed at initializing Pytest commands group settings.
    For the default Pytest directory it is by design 'src' or any newly provided, via initialization, directory.
    For the Pytest config file it is by design '../pyproject.toml' or any newly provided, via initialization, path.

    :return: None
    :rtype: None
    """
    init_settings()
