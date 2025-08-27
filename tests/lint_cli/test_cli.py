"""Tests for the lint CLI module."""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from tidy_cli.lint_cli.cli import lint_app


@pytest.fixture
def runner():
    """Return a CLI runner."""
    return CliRunner()


def test_run_path_not_found(runner):
    """Test run command when specified path doesn't exist."""
    with patch("tidy_cli.lint_cli.cli.get_lint_default_path") as mock_get_default, \
         patch("rich.console.Console.print") as mock_print:
        
        # Mock default directory and non-existent path
        mock_default_dir = MagicMock()
        mock_lint_path = MagicMock()
        mock_lint_path.exists.return_value = False
        mock_default_dir.__truediv__.return_value = mock_lint_path
        mock_get_default.return_value = mock_default_dir
        
        result = runner.invoke(lint_app, ["run", "nonexistent/path"])
        
        assert result.exit_code == 1
        mock_print.assert_any_call(f"❌ Path not found: [bold]{mock_lint_path}[/bold]", style="red")


def test_run_success_all_tools(runner):
    """Test run command with all linting tools succeeding."""
    with patch("tidy_cli.lint_cli.cli.get_lint_default_path") as mock_get_default, \
         patch("tidy_cli.lint_cli.cli.get_lint_config_path", return_value="pyproject.toml"), \
         patch("tidy_cli.lint_cli.cli.run_command", return_value=True) as mock_run_cmd, \
         patch("rich.console.Console.print") as mock_print:
        
        # Mock path exists
        mock_default_dir = MagicMock()
        mock_lint_path = MagicMock()
        mock_lint_path.exists.return_value = True
        mock_default_dir.__truediv__.return_value = mock_lint_path
        mock_get_default.return_value = mock_default_dir
        
        result = runner.invoke(lint_app, ["run", "src/test"])
        
        assert result.exit_code == 0
        assert mock_run_cmd.call_count == 4  # ruff check, ruff format, pydoclint, mypy
        mock_print.assert_any_call("🎉 All [bold green]4[/bold green] linting tools completed [bold]successfully[/bold]", style="green")


def test_run_partial_success(runner):
    """Test run command with some tools failing."""
    with patch("tidy_cli.lint_cli.cli.get_lint_default_path") as mock_get_default, \
         patch("tidy_cli.lint_cli.cli.get_lint_config_path", return_value="pyproject.toml"), \
         patch("tidy_cli.lint_cli.cli.run_command", side_effect=[True, False, True, False]) as mock_run_cmd, \
         patch("rich.console.Console.print") as mock_print:
        
        # Mock path exists
        mock_default_dir = MagicMock()
        mock_lint_path = MagicMock()
        mock_lint_path.exists.return_value = True
        mock_default_dir.__truediv__.return_value = mock_default_dir
        mock_get_default.return_value = mock_default_dir
        
        result = runner.invoke(lint_app, ["run"])
        
        assert result.exit_code == 0
        assert mock_run_cmd.call_count == 4
        mock_print.assert_any_call("⚠️ 2/4 linting tools completed [bold]successfully[/bold]", style="yellow")


def test_run_with_fix_option(runner):
    """Test run command with fix option."""
    with patch("tidy_cli.lint_cli.cli.get_lint_default_path") as mock_get_default, \
         patch("tidy_cli.lint_cli.cli.get_lint_config_path", return_value="pyproject.toml"), \
         patch("tidy_cli.lint_cli.cli.run_command", return_value=True) as mock_run_cmd, \
         patch("rich.console.Console.print"):
        
        # Mock path exists
        mock_default_dir = MagicMock()
        mock_lint_path = MagicMock()
        mock_lint_path.exists.return_value = True
        mock_default_dir.__truediv__.return_value = mock_lint_path
        mock_get_default.return_value = mock_default_dir
        
        result = runner.invoke(lint_app, ["run", "src", "--fix"])
        
        assert result.exit_code == 0
        # Check that --fix was added to ruff check command
        ruff_check_call = mock_run_cmd.call_args_list[0]
        assert "--fix" in ruff_check_call[0][0]


def test_run_skip_options(runner):
    """Test run command with skip options."""
    with patch("tidy_cli.lint_cli.cli.get_lint_default_path") as mock_get_default, \
         patch("tidy_cli.lint_cli.cli.get_lint_config_path", return_value="pyproject.toml"), \
         patch("tidy_cli.lint_cli.cli.run_command", return_value=True) as mock_run_cmd, \
         patch("rich.console.Console.print") as mock_print:
        
        # Mock path exists
        mock_default_dir = MagicMock()
        mock_lint_path = MagicMock()
        mock_lint_path.exists.return_value = True
        mock_default_dir.__truediv__.return_value = mock_lint_path
        mock_get_default.return_value = mock_default_dir
        
        result = runner.invoke(lint_app, ["run", "src", "--skip-ruff", "--skip-mypy"])
        
        assert result.exit_code == 0
        assert mock_run_cmd.call_count == 2  # Only ruff format and pydoclint
        mock_print.assert_any_call("🎉 All [bold green]2[/bold green] linting tools completed [bold]successfully[/bold]", style="green")


def test_run_interactive_mode(runner):
    """Test run command in interactive mode."""
    with patch("tidy_cli.lint_cli.cli.get_lint_default_path") as mock_get_default, \
         patch("tidy_cli.lint_cli.cli.get_lint_config_path", return_value="pyproject.toml"), \
         patch("tidy_cli.lint_cli.cli.run_command", return_value=True) as mock_run_cmd, \
         patch("rich.console.Console.print"), \
         patch("typer.confirm", side_effect=[False, True, False, True]) as mock_confirm:
        
        # Mock path exists
        mock_default_dir = MagicMock()
        mock_lint_path = MagicMock()
        mock_lint_path.exists.return_value = True
        mock_default_dir.__truediv__.return_value = mock_lint_path
        mock_get_default.return_value = mock_default_dir
        
        result = runner.invoke(lint_app, ["run", "src", "--interactive"])
        
        assert result.exit_code == 0
        assert mock_confirm.call_count == 4  # ruff, format, pydoclint, mypy
        assert mock_run_cmd.call_count == 2  # Only ruff format and mypy


def test_init_command(runner):
    """Test init command."""
    with patch("tidy_cli.lint_cli.cli.init_settings") as mock_init:
        result = runner.invoke(lint_app, ["init"])
        
        assert result.exit_code == 0
        mock_init.assert_called_once()