"""Tests for the main tidy_cli helpers module."""

from unittest.mock import patch

import pytest

from tidy_cli.helpers import get_version, show_ascii_art


def test_get_version_success():
    """Test get_version with valid package metadata."""
    with patch("tidy_cli.helpers.version", return_value="1.2.3"):
        result = get_version()
        assert result == "1.2.3"


def test_get_version_different_format():
    """Test get_version with different version format."""
    with patch("tidy_cli.helpers.version", return_value="0.5.10"):
        result = get_version()
        assert result == "0.5.10"


def test_get_version_package_not_found():
    """Test get_version when package is not found."""
    with patch("tidy_cli.helpers.version", side_effect=Exception("Package not found")):
        result = get_version()
        assert result == "unknown"


def test_get_version_metadata_error():
    """Test get_version when metadata reading fails."""
    with patch("tidy_cli.helpers.version", side_effect=ImportError("Metadata error")):
        result = get_version()
        assert result == "unknown"


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