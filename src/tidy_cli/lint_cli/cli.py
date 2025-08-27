"""Module aimed at defining the CLI Linter Commands Group."""

# Import packages and modules
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from .helpers import (
    get_lint_config_path,
    get_lint_default_path,
    init_settings,
    run_command,
)

# Define Typer Linter program (i.e., commands group)
lint_app = typer.Typer(
    name="lint",
    help="🧼 Run [bold]Linters[/bold] on [bold]entire[/bold] default folder ([italic]'src'[/italic] or what's defined at [italic]initialization[/italic]) "
    "or [bold]specific path[/bold] if provided with [bold]interactive mode[/bold] if chosen.",
    add_completion=True,
    rich_markup_mode="rich",
)
console = Console()


@lint_app.command(
    "run",
    help="""
    🧼 Run linters on a specified [bold]path[/bold] with or without [italic]interactive mode[/italic] or [bold]default folder[/bold] files otherwise.
    The currently supported [italic]linters/formatters/checkers[/italic] are:

    ▪ [code]Ruff[/code] for both [bold]linting[/bold] and [bold]formatting[/bold].
    ▪ [code]Pydoclint[/code] for [bold]docstrings validation[/bold].
    ▪ [code]Mypy[/code] for [bold]static type checking[/bold].
    """,
)
def run(
    path: Annotated[
        str | None,
        typer.Argument(
            help="🎞️  [bold]Path[/bold] to lint (relative to [italic]default[/italic] folder), "
            "otherwise [bold]entire default[/bold] folder is linted (i.e., [italic]'src'[/italic] or what defined at initialisation).",
            callback=lambda path: path if path is not None else "",
            show_default=str(get_lint_default_path()),
        ),
    ] = None,
    interactive: Annotated[
        bool,
        typer.Option(
            "--interactive",
            "-i",
            help="🎛️  Run in [bold]interactive[/bold] mode.",
        ),
    ] = False,
    fix: Annotated[
        bool,
        typer.Option(
            "--fix",
            "-f",
            help="🩹 Ruff [bold]auto-fix[/bold] issues when possible.",
        ),
    ] = False,
    skip_ruff: Annotated[
        bool,
        typer.Option(
            "--skip-ruff",
            "-sl",
            help="💨 [bold]Skip[/bold] ruff linting.",
        ),
    ] = False,
    skip_format: Annotated[
        bool,
        typer.Option(
            "--skip-format",
            "-sf",
            help="💨 [bold]Skip[/bold] ruff formatting.",
        ),
    ] = False,
    skip_pydoclint: Annotated[
        bool,
        typer.Option(
            "--skip-pydoclint",
            "-sp",
            help="💨 [bold]Skip[/bold] pydoclint.",
        ),
    ] = False,
    skip_mypy: Annotated[
        bool,
        typer.Option(
            "--skip-mypy",
            "-sm",
            help="💨 [bold]Skip[/bold] mypy.",
        ),
    ] = False,
) -> None:
    """
    Entry point function to run Linters on the entire default folder, 'src' or wath's defined in the settings, or a specific path.
    When running Linters on a specific path it allows to use interactive mode and skip single linters.

    :param path: optional path on which running tests
    :type path: str | None
    :param interactive: whether to run in interactive mode, defaults to False
    :type logs: bool
    :param fix: whether to allow Ruff to fix errors, defaults to False
    :type fix: bool
    :param skip_ruff: whether to skip Ruff for linting, defaults to False
    :type skip_ruff: bool
    :param skip_format: whether to skip Ruff for formatting, defaults to False
    :type skip_format: bool
    :param skip_pydoclint: whether to skip Pydoclint for docstrings validation, defaults to False
    :type skip_pydoclint: bool
    :param skip_mypy: whether to skip Mypy for static type checking, defaults to False
    :type skip_mypy: bool
    :return: None
    :rtype: None
    """

    default_dir: Path = get_lint_default_path()
    lint_path = default_dir / path  # type: ignore
    if lint_path.exists() is False:
        console.print(f"❌ Path not found: [bold]{lint_path}[/bold]", style="red")
        raise typer.Exit(1)

    console.print(f"🔍 Running linters on: [bold]{lint_path}[/bold]", style="white")

    # Interactive mode
    if interactive is True:
        skip_ruff = not typer.confirm("Do you want to run ruff for linting?")
        if skip_ruff is False:
            fix = typer.confirm("Do you want ruff to auto-fix when fixable errors?")
        skip_format = not typer.confirm("Do you want to run ruff for formatting?")
        skip_pydoclint = not typer.confirm("Do you want to run pydoclint?")
        skip_mypy = not typer.confirm("Do you want to run mypy?")

    results = []
    config_path = get_lint_config_path()

    if skip_ruff is False:
        cmd = ["ruff", "check", str(lint_path), "--config", config_path]
        if fix is True:
            cmd.append("--fix")
        results.append(run_command(cmd, "Ruff linting"))

    if skip_format is False:
        results.append(run_command(["ruff", "format", str(lint_path), "--config", config_path], "Ruff formatting"))

    if skip_pydoclint is False:
        results.append(run_command(["flake8", str(lint_path), "--toml-config", config_path, "--select", "DOC"], "Pydoclint"))

    if skip_mypy is False:
        results.append(run_command(["mypy", str(lint_path), "--pretty", "--config-file", config_path], "Mypy type checking"))

    success_count = sum(results)
    total_count = len(results)

    if success_count == total_count:
        console.print(f"🎉 All [bold green]{total_count}[/bold green] linting tools completed [bold]successfully[/bold]", style="green")
    else:
        console.print(f"⚠️ {success_count}/{total_count} linting tools completed [bold]successfully[/bold]", style="yellow")


@lint_app.command(
    "init",
    help="🎛️  Initialize CLI [bold]default Linting directory[/bold] and [bold]config file path[/bold] settings.",
)
def init() -> None:
    """
    Function aimed at initializing Linter commands group settings.
    For the default Lint directory it is by design 'src' or any newly provided, via initialization, directory.
    For the Lint config file it is by design 'pyproject.toml' or any newly provided, via initialization, path.

    :return: None
    :rtype: None
    """
    init_settings()
