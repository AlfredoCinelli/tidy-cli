"""Tests for the main tidy_cli helpers module."""

from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from tidy_cli.helpers import get_version, show_ascii_art


def test_get_version_success():
    """Test get_version with valid pyproject.toml."""
    mock_toml_content = '''
[project]
name = "test-project"
version = "1.2.3"
description = "Test project"
'''
    
    with patch("builtins.open", mock_open(read_data=mock_toml_content)):
        result = get_version()
        assert result == "1.2.3"


def test_get_version_different_format():
    """Test get_version with different version format."""
    mock_toml_content = '''
[build-system]
requires = ["hatchling"]

[project]
version = "0.5.10"
name = "another-project"
'''
    
    with patch("builtins.open", mock_open(read_data=mock_toml_content)):
        result = get_version()
        assert result == "0.5.10"


def test_get_version_no_match():
    """Test get_version when no version pattern is found."""
    mock_toml_content = '''
[project]
name = "test-project"
description = "Test project without version"
'''
    
    with patch("builtins.open", mock_open(read_data=mock_toml_content)):
        with pytest.raises(IndexError):
            get_version()


def test_get_version_file_not_found():
    """Test get_version when pyproject.toml file doesn't exist."""
    with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
        with pytest.raises(FileNotFoundError):
            get_version()


def test_show_ascii_art():
    """Test show_ascii_art function."""
    with patch("tidy_cli.helpers.get_version", return_value="1.0.0") as mock_get_version, \
         patch("rich.console.Console.print") as mock_print:
        
        show_ascii_art()
        
        mock_get_version.assert_called_once()
        # Verify that console.print was called multiple times (for the ASCII art)
        assert mock_print.call_count > 5


def test_show_ascii_art_with_version_error():
    """Test show_ascii_art when get_version fails."""
    with patch("tidy_cli.helpers.get_version", side_effect=Exception("Version error")) as mock_get_version, \
         patch("rich.console.Console.print") as mock_print:
        
        with pytest.raises(Exception, match="Version error"):
            show_ascii_art()
        
        mock_get_version.assert_called_once()