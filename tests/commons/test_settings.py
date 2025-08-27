"""Tests for the commons settings module."""

import json
from typing import Any
from unittest.mock import mock_open, patch

import pytest

from src.tidy_cli.commons.settings import (
    SETTINGS_FILE,
    load_settings,
    save_settings,
    update_settings,
)


@pytest.fixture(scope="module")
def mock_settings() -> dict[str, str]:
    """Return mock settings."""
    return {"lint_path": "src", "pytest_path": "tests"}


@pytest.mark.parametrize(
    "scenario",
    [
        # Load existing settings file
        {
            "mock_open": json.dumps({"lint_path": "src", "pytest_path": "tests"}),
            "mock_path": True,
            "expected_output": {"lint_path": "src", "pytest_path": "tests"},
        },
        # Settings file does not exists
        {
            "mock_open": None,
            "mock_path": False,
            "expected_output": {},
        },
        # Invalid JSON file
        {
            "mock_open": "This is an invalid JSON",
            "mock_path": True,
            "expected_output": {},
        },
    ],
)
def test_load_settings(scenario: dict[str, Any]) -> None:
    """
    Test load_settings function.
    It tests the following scenarios:
    - Load existing settings file
    - No settings file exists yet
    - Invalid settings file

    :param scenario: tested scenario coming from Pytest marker
    :type scenario: dict[str, Any]
    :return: tests different scenarios
    :rtype: None
    """
    with (
        patch("src.tidy_cli.commons.settings.Path.exists", return_value=scenario.get("mock_path")),
        patch("src.tidy_cli.commons.settings.open", mock_open(read_data=scenario.get("mock_open"))),
    ):
        output = load_settings()
        print(output)
        assert output == scenario.get("expected_output")


@pytest.mark.parametrize(
    "scenario",
    [
        # Plain scenario
        {
            "mock_mkdir": None,
            "open_args": [SETTINGS_FILE, "w"],
            "setting_file": {},
        },
    ],
)
def test_save_settings(
    scenario: dict[str, Any],
) -> None:
    """
    Test save_settings function.

    :param scenario: tested scenario coming from Pytest marker
    :type scenario: dict[str, Any]
    :return: tests different scenarios
    :rtype: None
    """
    with (
        patch("src.tidy_cli.commons.settings.json.dump") as mock_json_dump,
        patch("src.tidy_cli.commons.settings.open", mock_open()) as mock_open_file,
        patch("src.tidy_cli.commons.settings.Path.mkdir", return_value=scenario.get("mock_mkdir")),
    ):
        save_settings(scenario.get("setting_file", {}))
        # Check open called with proper args
        mock_open_file.assert_called_once_with(*scenario.get("open_args", []))
        # Check json dump only ones
        mock_json_dump.assert_called_once()


@pytest.mark.parametrize(
    "scenario",
    [
        # Insert new data
        {
            "existing_settings": {"lint_path": "src"},
            "new_settings": {"pytest_path": "tests"},
            "updated_settings": {"lint_path": "src", "pytest_path": "tests"},
        },
        # Update data
        {
            "existing_settings": {"lint_path": "src"},
            "new_settings": {"lint_path": "custom_src"},
            "updated_settings": {"lint_path": "custom_src"},
        },
        # Upsert data
        {
            "existing_settings": {"lint_path": "src", "pytest_path": "tests"},
            "new_settings": {"lint_path": "custom_src", "pytest_config": "pyproject.toml"},
            "updated_settings": {"lint_path": "custom_src", "pytest_path": "tests", "pytest_config": "pyproject.toml"},
        },
    ],
)
def test_update_settings(
    scenario: dict[str, Any],
) -> None:
    """
    Test update_settings function.
    It tests the following scenarios:
    - Insert new data
    - Update existing data
    - Upsert data (i.e., update existing data and insert new data)

    :param scenario: tested scenario coming from Pytest marker
    :type scenario: dict[str, Any]
    :return: tests different scenarios
    :rtype: None
    """
    with (
        patch("src.tidy_cli.commons.settings.load_settings", return_value=scenario.get("existing_settings")),
        patch("src.tidy_cli.commons.settings.save_settings") as mock_save_settings,
    ):
        update_settings(scenario.get("new_settings"))  # type: ignore
        mock_save_settings.assert_called_once_with(scenario.get("updated_settings"))
