"""Tests for the pytest CLI helpers module."""

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from src.tidy_cli.pytest_cli.helpers import (
    cleanup_test_cache,
    get_pytest_config_path,
    get_pytest_default_path,
    init_settings,
)


@pytest.mark.parametrize(
    "scenario",
    [
        # Successful scenario
        {
            "mock_subprocess": {"return_value": MagicMock(returncode=0)},
            "expected_rich_print": "🧹 Test cache cleaned up",
            "expected_rich_style": {"style": "white"},
        },
        # Failing scenario
        {
            "mock_subprocess": {"side_effect": Exception("Error")},
            "expected_rich_print": "⚠️ Warning: Could not clean up test cache: Error",
            "expected_rich_style": {"style": "yellow"},
        },
    ]
)
def test_cleanup_test_cache(
    scenario: dict[str, Any]
) -> None:
    """
    Function to test cleanup_test_chache.
    It tests the following scenarios:
    - successful scenario
    - failing scenario

    :return: None
    :rtype: None
    """
    with (
        patch("src.tidy_cli.pytest_cli.helpers.subprocess.run", **scenario.get("mock_subprocess", {})),
        patch("src.tidy_cli.pytest_cli.helpers.console.print", return_value=None) as mock_rich_print,
    ):
        cleanup_test_cache()
        mock_rich_print.assert_called_once_with(scenario.get("expected_rich_print"), **scenario.get("expected_rich_style", {}))


@pytest.mark.parametrize(
    "scenario",
    [
        # No initial settings
        {
            "load_settings": {
                "mock_value": {"return_value": {}},
                "assert_value": 1,
            },
            "update_settings": {
                "mock_value": {"return_value": None},
                "assert_value": {"pytest_default_path": "tests_folder", "pytest_config_path": "testproject.toml"},
            },
            "prompt": {
                "mock_value": {"side_effect": [Path("tests_folder"), Path("testproject.toml")]},
                "assert_value": 2,
            },
            "rich_print": {
                "mock_value": {"return_value": None},
                "assert_value": 5,
            },
        }
    ]
)
def test_init_settings(
    scenario: dict[str, Any],
) -> None:
    """TBA"""
    with (
        patch("src.tidy_cli.pytest_cli.helpers.load_settings", **scenario.get("load_settings", {}).get("mock_value", {})) as mock_load,
        patch("src.tidy_cli.pytest_cli.helpers.update_settings", **scenario.get("update_settings", {}).get("mock_value", {})) as mock_update,
        patch("src.tidy_cli.pytest_cli.helpers.typer.prompt", **scenario.get("prompt", {}).get("mock_value", {})) as mock_prompt,
        patch("src.tidy_cli.pytest_cli.helpers.console.print", **scenario.get("rich_print", {}).get("mock_value", {})) as mock_print,
        patch("src.tidy_cli.pytest_cli.helpers.SETTINGS_FILE", "test_settings.json"),
    ):
        init_settings()
        # Test calls
        assert mock_load.call_count == scenario.get("load_settings", {}).get("assert_value")
        assert mock_prompt.call_count == scenario.get("prompt", {}).get("assert_value")
        print(mock_print.call_args_list)
        assert mock_update.call_args[0][0] == scenario.get("update_settings", {}).get("assert_value")
        assert mock_print.call_count == scenario.get("rich_print", {}).get("assert_value")



def test_init_settings_with_existing():
    """Test init_settings with existing settings."""
    existing_settings = {"pytest_default_path": "existing_tests", "pytest_config_path": "existing.toml"}

    with (
        patch("src.tidy_cli.pytest_cli.helpers.load_settings", return_value=existing_settings),
        patch("src.tidy_cli.pytest_cli.helpers.update_settings") as mock_update,
        patch("typer.prompt", side_effect=[Path("new_tests"), Path("new.toml")]),
        patch("rich.console.Console.print") as mock_print,
    ):
        init_settings()

        mock_update.assert_called_once_with({"pytest_default_path": "new_tests", "pytest_config_path": "new.toml"})
        # Check that settings saved message contains the SETTINGS_FILE path
        settings_calls = [call for call in mock_print.call_args_list if "Settings saved" in str(call)]
        assert len(settings_calls) > 0
        mock_print.assert_any_call("📁 Pytest default directory: [bold]new_tests[/bold]", style="white")
        mock_print.assert_any_call("📄 Pytest config file path: [bold]new.toml[/bold]", style="white")


def test_get_pytest_default_path_default():
    """Test get_pytest_default_path with default value."""
    with patch("src.tidy_cli.pytest_cli.helpers.load_settings", return_value={}):
        result = get_pytest_default_path()
        assert result == Path("src")


def test_get_pytest_default_path_from_settings():
    """Test get_pytest_default_path from settings."""
    settings = {"pytest_default_path": "custom_tests"}

    with patch("src.tidy_cli.pytest_cli.helpers.load_settings", return_value=settings):
        result = get_pytest_default_path()
        assert result == Path("custom_tests")


def test_get_pytest_config_path_default():
    """Test get_pytest_config_path with default value."""
    with patch("src.tidy_cli.pytest_cli.helpers.load_settings", return_value={}):
        result = get_pytest_config_path()
        assert result == "../pyproject.toml"


def test_get_pytest_config_path_from_settings():
    """Test get_pytest_config_path from settings."""
    settings = {"pytest_config_path": "custom.toml"}

    with patch("src.tidy_cli.pytest_cli.helpers.load_settings", return_value=settings):
        result = get_pytest_config_path()
        assert result == "custom.toml"
