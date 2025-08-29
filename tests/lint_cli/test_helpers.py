"""Tests for the lint CLI helpers module."""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tidy_cli.lint_cli.helpers import (
    get_lint_config_path,
    get_lint_default_path,
    init_settings,
    run_command,
)


def test_run_command_success():
    """Test run_command with successful execution."""
    with patch("subprocess.run") as mock_run, \
         patch("rich.console.Console.print") as mock_print:
        
        # Mock successful command
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Success output"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        result = run_command(["echo", "test"], "Test command")
        
        assert result is True
        mock_print.assert_any_call("🔧 Test command...")
        mock_print.assert_any_call("✅ Test command completed successfully")
        mock_print.assert_any_call("Success output", style="white", markup=False)


def test_run_command_failure():
    """Test run_command with failed execution."""
    with patch("subprocess.run") as mock_run, \
         patch("rich.console.Console.print") as mock_print:
        
        # Mock failed command
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = "Error output"
        mock_result.stderr = "Error message"
        mock_run.return_value = mock_result
        
        result = run_command(["false"], "Test command")
        
        assert result is False
        mock_print.assert_any_call("🔧 Test command...")
        mock_print.assert_any_call("❌ Test command failed", style="red")
        mock_print.assert_any_call("Error output", style="red", markup=False)
        mock_print.assert_any_call("Error message", style="red", markup=False)


def test_run_command_exception():
    """Test run_command with exception."""
    with patch("subprocess.run", side_effect=Exception("Test error")) as mock_run, \
         patch("rich.console.Console.print") as mock_print:
        
        result = run_command(["test"], "Test command")
        
        assert result is False
        mock_print.assert_any_call("❌ Error running Test command: Test error", style="red", markup=False)


def test_run_command_no_output():
    """Test run_command with no stdout."""
    with patch("subprocess.run") as mock_run, \
         patch("rich.console.Console.print") as mock_print:
        
        # Mock successful command with no output
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        result = run_command(["echo"], "Test command")
        
        assert result is True
        mock_print.assert_any_call("")


def test_init_settings():
    """Test init_settings function."""
    with patch("tidy_cli.lint_cli.helpers.load_settings", return_value={}) as mock_load, \
         patch("tidy_cli.lint_cli.helpers.update_settings") as mock_update, \
         patch("typer.prompt", side_effect=[Path("custom_src"), Path("custom.toml")]) as mock_prompt, \
         patch("rich.console.Console.print") as mock_print:
        
        init_settings()
        
        mock_load.assert_called_once()
        mock_update.assert_called_once_with({
            "lint_default_path": "custom_src",
            "lint_config_path": "custom.toml"
        })
        assert mock_prompt.call_count == 2


def test_init_settings_with_existing():
    """Test init_settings with existing settings."""
    existing_settings = {
        "lint_default_path": "existing_src",
        "lint_config_path": "existing.toml"
    }
    
    with patch("tidy_cli.lint_cli.helpers.load_settings", return_value=existing_settings), \
         patch("tidy_cli.lint_cli.helpers.update_settings") as mock_update, \
         patch("typer.prompt", side_effect=[Path("new_src"), Path("new.toml")]), \
         patch("rich.console.Console.print"):
        
        init_settings()
        
        mock_update.assert_called_once_with({
            "lint_default_path": "new_src",
            "lint_config_path": "new.toml"
        })


def test_get_lint_default_path_default():
    """Test get_lint_default_path with default value."""
    with patch("tidy_cli.lint_cli.helpers.load_settings", return_value={}):
        result = get_lint_default_path()
        assert result == Path("src")


def test_get_lint_default_path_from_settings():
    """Test get_lint_default_path from settings."""
    settings = {"lint_default_path": "custom_path"}
    
    with patch("tidy_cli.lint_cli.helpers.load_settings", return_value=settings):
        result = get_lint_default_path()
        assert result == Path("custom_path")


def test_get_lint_config_path_default():
    """Test get_lint_config_path with default value."""
    with patch("tidy_cli.lint_cli.helpers.load_settings", return_value={}):
        result = get_lint_config_path()
        assert result == "pyproject.toml"


def test_get_lint_config_path_from_settings():
    """Test get_lint_config_path from settings."""
    settings = {"lint_config_path": "custom.toml"}
    
    with patch("tidy_cli.lint_cli.helpers.load_settings", return_value=settings):
        result = get_lint_config_path()
        assert result == "custom.toml"