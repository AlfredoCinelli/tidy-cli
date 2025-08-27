"""Module defining settings management for CLI initialization."""

# Import packages and modules
import json
from pathlib import Path

# Define litearls
SETTINGS_FILE = Path("local/tidy_cli_settings.json")  # path and name of the file storing CLI configuration


def load_settings() -> dict[str, str]:
    """
    Function aimed at loading settings from local file.
    If no setting file is found an empty dictionary is returned.

    :return: None
    :rtype: dict[str, str]
    """
    if SETTINGS_FILE.exists() is False:
        return {}

    try:
        with open(SETTINGS_FILE) as file:
            return json.load(file)
    except Exception:
        return {}


def save_settings(
    settings: dict[str, str],
) -> None:
    """
    Function aimed at saving settings to local file.

    :param settings: settings file represented via a dictionary data structure
    :type settings: dict[str, str]
    :return: None
    :rtype: None
    """
    # Create path if does not exist yet
    SETTINGS_FILE.parent.mkdir(exist_ok=True)
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=2)


def update_settings(
    settings: dict[str, str],
) -> None:
    """
    Function aimed at updating settings by merging with existing settings (i.e., upserting them).

    :param settings: new settings to be upserted
    :type settings: dict[str, str]
    :return: None
    :rtype: None
    """
    existing_settings = load_settings()
    existing_settings.update(settings)
    save_settings(existing_settings)
