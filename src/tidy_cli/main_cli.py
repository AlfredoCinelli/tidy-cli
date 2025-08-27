"""
Module aimed at degining the Tidy CLI - Development Tools.

The structure of the CLI Progam is modular, hence it allows any new Commands Group to be addes as a
separate Typer app with its command name and subcommands.
If any of the Commands Group need to be removed just unlink it to Typer main app, vice versa create a
new folder with Commands Group with their Typer app and link it to main Typer app to get new ones.
"""

# Import packages and modules
import typer
from rich.console import Console

from .helpers import (
    get_version,
    show_ascii_art,
)
from .lint_cli import (
    lint_app,
    lint_init,
)
from .pytest_cli import (
    pytest_app,
    pytest_init,
)

console = Console()

# Main CLI description (runs as no-command callback)
DESC = """
    🛰️  [bold]CLI[/bold] tool for [italic]development tasks[/italic]: [bold]linting[/bold] and [bold]unit-testing[/bold].

    ▪ [code]tidy-cli lint[/code] allows to run linters battery on entire [italic]src[/italic] folder or specific path files 🧼
    ▪ [code]tidy-cli pytest[/code] allows to run pytest on entire [italic]tests[/italic] folder or specific path with or without logs 🧪
    """

# Define main CLI program
app = typer.Typer(
    name="tidy-cli",
    help=DESC,
    add_completion=True,
    rich_markup_mode="rich",
    epilog="Made with 🌞 in [bold cyan]Vieste[/bold cyan] 🌊",
)


# Callback to print when only CLI is called
@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
) -> None:
    """
    Callback function aimed at printing general CLI description when no commands are provided.

    :param ctx: typer context object (to retrieve CLI information)
    :type ctx: typer.Context
    :return: None
    :rtype: None
    """
    if ctx.invoked_subcommand is None:
        console.print(DESC)
        console.print("🔍 run [code]tidy-cli --help[/code] to know more!")


# Create main CLI commands
@app.command(
    "version",
    help="📟 See CLI [bold]version[/bold] information.",
    rich_help_panel="🎚️ Plain commands",
)
def version() -> None:
    """
    Function aimed at showing CLI version information in the terminal.

    :return: None
    :rtype: None
    """
    console.print(f"📖 Tidy CLI (version {get_version()})", style="bold cyan")


@app.command(
    "hello",
    help="📺 Display [bold]ASCII art[/bold] greeting.",
    rich_help_panel="🎚️ Plain commands",
)
def hello() -> None:
    """
    Function aimed at display ASCII art greeting in the terminal (by calling show_ascii_art helper function).

    :return: None
    :rtype: None
    """
    show_ascii_art()


@app.command(
    "init",
    help="🎛️  Initialize CLI [bold]commands groups[/bold] settings.",
    rich_help_panel="🎚️ Plain commands",
)
def init() -> None:
    """
    Function aimed at initializing CLI sub-commands groups by calling each group initializer.
    The setting are saved under the local folder in the cli_settings.json file.

    :return: None
    :rtype: None
    """
    pytest_init()
    lint_init()
    show_ascii_art()


# Add command groups
app.add_typer(
    lint_app,
    rich_help_panel="🧼 [bold]Linting[/bold] command",
)
app.add_typer(
    pytest_app,
    rich_help_panel="🧪[bold]Pytest[/bold] command",
)