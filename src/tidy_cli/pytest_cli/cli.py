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
    help="🧪 Run [bold]Pytest[/bold] on [bold]tests[/bold] folder or provided [bold]path[/bold] (with [italic]logs[/italic] or any Pytest [italic]option[/italic]).",
    add_completion=True,
    rich_markup_mode="rich",
)


@pytest_app.command(
    "run",
    help="🧪 Run [bold]Pytest[/bold] on [bold]entire[/bold] tests folder (under defaulted [italic]'src'[/italic] or what's defined at [italic]initialization[/italic]) "
    "or [bold]specific path[/bold] if provided with [bold]logs[/bold] if chosen and any other Pytest extra option.",
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
    extra_options: Annotated[
        list[str],
        typer.Option(
            "--extra",
            "-e",
            help="🎛️  Any pytest [bold]extra options[/bold] to run tests (e.g., '-e -v' for verbosity).",
            show_default="None",
        ),
    ] = [],  # noqa: B006
    logs: Annotated[
        bool,
        typer.Option(
            "--logs",
            "-l",
            help="🔊🔇 Whether to show test [italic]logs[/italic] or not. It applies to testing a path only, use extra_options to show logs when running on all tests.",
            show_default="False",
        ),
    ] = False,
    default_dir: Annotated[
        Path | None,
        typer.Option(
            "--default-dir",
            help="🖍️  Overwrite at [bold]runtime[/bold] the test [italic]default directory[/italic]",
        ),
    ] = None,
    pyproject_path: Annotated[
        str | None,
        typer.Option(
            "--pyproject-path",
            help="🖍️  Overwrite at [bold]runtime[/bold] the [italic]pyproject.toml[/italic] path (relative to [italic]default directory[/italic])",
        ),
    ] = None,
) -> None:
    """
    Entry point function to run Pytests on the entire default folder, 'src' or wath's defined in the settings, or a specific path.
    When running Pytest on a specific path it allows to display logs.

    :param path: optional path on which running tests
    :type path: str | None
    :param extra_options: any optional extra options that can be supplied to pytest
    :type extra_options: list[str]
    :param logs: whether to show logs or not, defaults to False
    :type logs: bool
    :param default_dir: default pytest path that overwrites the one set at init time
    :type default_dir: Path | None
    :param pyproject_path: pyproject.toml path relative to default pytest path that overwrites the one set at init time
    :type pyproject_path: str | None
    :return: None
    :rtype: None
    """
    # Change to src or default directory first
    original_cwd = Path.cwd()
    default_dir: Path = get_pytest_default_path() if default_dir is None else default_dir  # type: ignore
    if default_dir.exists() is False:  # type: ignore
        console.print(f"❌ Default directory not found: [bold]{default_dir}[/bold]", style="red")
        raise typer.Exit(1)
    test_path = default_dir / path  # type: ignore
    # Check for running on specific test or class
    test_object = None
    # Check for testing a specific function or class
    if "::" in test_path.name:
        test_object = test_path.name
        test_path = test_path.parent
    # Test for the existence of the path to test when provided
    if (path) and (test_path.exists() is False):
        console.print(f"❌ Test path not found: [bold]{test_path}[/bold]", style="red")
        raise typer.Exit(1)
    os.chdir(default_dir)  # type: ignore

    try:
        if path:
            (
                console.print(f"🧪 Running tests for: [bold]{test_path}[/bold]", style="white")
                if test_object is None
                else console.print(f"🧪 Running tests for: [bold]{test_path}[/bold] on [bold]{test_object}[/bold]", style="white")
            )
            cmd = ["python", "-m", "pytest", str(path)]
            if logs or "-s" in extra_options:
                # Add logs flag if chosen
                console.print("🔊 [bold]Showing[/bold] logs...", style="white")
                cmd.append("-s")
                # extra_options.remove
            else:
                console.print("🔇 [bold]Not showing[/bold] logs...", style="white")
            #  Run test with extra options if provided
            result = subprocess.run(cmd + extra_options) if extra_options else subprocess.run(cmd)
            if result.returncode == 0:
                console.print("✅ Tests completed [bold]successfully[/bold]", style="green")
            else:
                console.print("❌ Some tests [bold]failed[/bold]", style="red")
        else:
            console.print(f"🧪 Running [bold]all[/bold] tests with [bold]coverage[/bold] for: [bold]{default_dir}[/bold]", style="white")
            pyproject_path = get_pytest_config_path() if pyproject_path is None else pyproject_path
            cmd = ["coverage", "run", f"--rcfile={pyproject_path}", "-m", "pytest"]
            result = subprocess.run(cmd + extra_options) if extra_options else subprocess.run(cmd)

            if result.returncode == 0:
                # Print coverage for success tests
                console.print("📊 Displaying [bold]coverage report[/bold]...", style="white")
                console.print("\n")
                subprocess.run(["coverage", "report", "-m"])
                console.print("\n")
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
