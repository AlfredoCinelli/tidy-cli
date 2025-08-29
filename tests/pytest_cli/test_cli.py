"""Tests for the pytest CLI module."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from tidy_cli.pytest_cli.cli import pytest_app
from tidy_cli.pytest_cli.helpers import cleanup_test_cache

@pytest.fixture(scope="module")
def runner():
    """Return a CLI runner."""
    return CliRunner()



def test_cleanup_test_cache():
    """Test the cleanup_test_cache function."""
    with patch("subprocess.run") as mock_run, patch("rich.console.Console.print") as mock_print:
        # Call the function
        cleanup_test_cache()

        # Check that subprocess.run was called 3 times (for each cleanup command)
        assert mock_run.call_count == 3
        # Check that the console print was called
        mock_print.assert_called_with("🧹 Test cache cleaned up", style="white")


def test_cleanup_test_cache_exception():
    """Test the cleanup_test_cache function when an exception occurs."""
    with patch("subprocess.run", side_effect=Exception("Test error")), patch("rich.console.Console.print") as mock_print:
        # Call the function
        cleanup_test_cache()

        # Check that the console print was called with the error message
        mock_print.assert_called_with("⚠️ Warning: Could not clean up test cache: Test error", style="yellow")


def test_run_src_not_found(runner):
    """Test run command when src directory doesn't exist."""
    with patch("pathlib.Path.exists", return_value=False), patch("rich.console.Console.print") as mock_print:
        result = runner.invoke(pytest_app, ["run"])

        assert result.exit_code == 1
        mock_print.assert_called_with("❌ Default directory not found: [bold]src[/bold]", style="red")


def test_run_specific_path_not_found(runner):
    """Test run command when specified test path doesn't exist."""
    with (
        patch("tidy_cli.pytest_cli.cli.get_pytest_default_path") as mock_get_default,
        patch("os.chdir") as mock_chdir,
        patch("rich.console.Console.print") as mock_print,
    ):
        # Mock default directory exists but test path doesn't
        mock_default_dir = MagicMock()
        mock_default_dir.exists.return_value = True
        mock_test_path = MagicMock()
        mock_test_path.exists.return_value = False
        mock_default_dir.__truediv__.return_value = mock_test_path
        mock_get_default.return_value = mock_default_dir

        result = runner.invoke(pytest_app, ["run", "nonexistent/path"])

        assert result.exit_code == 1
        mock_print.assert_any_call("❌ Test path not found: [bold]nonexistent/path[/bold]", style="red")


def test_run_specific_path_success(runner):
    """Test run command with a specific path that succeeds."""
    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("os.chdir") as mock_chdir,
        patch("subprocess.run") as mock_run,
        patch("rich.console.Console.print") as mock_print,
        patch("tidy_cli.pytest_cli.cli.cleanup_test_cache") as mock_cleanup,
    ):
        # Mock successful test run
        mock_run.return_value = MagicMock(returncode=0)

        result = runner.invoke(pytest_app, ["run", "tests/test_example.py"])

        assert result.exit_code == 0
        mock_chdir.assert_called()
        mock_run.assert_called_once()
        mock_print.assert_any_call("🧪 Running tests for: [bold]tests/test_example.py[/bold]", style="white")
        mock_print.assert_any_call("🔇 [bold]Not showing[/bold] logs...", style="white")
        mock_print.assert_any_call("✅ Tests completed [bold]successfully[/bold]", style="green")
        mock_cleanup.assert_called_once()


def test_run_specific_path_with_logs(runner):
    """Test run command with a specific path and logs enabled."""
    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("os.chdir") as mock_chdir,
        patch("subprocess.run") as mock_run,
        patch("rich.console.Console.print") as mock_print,
        patch("tidy_cli.pytest_cli.cli.cleanup_test_cache") as mock_cleanup,
    ):
        # Mock successful test run
        mock_run.return_value = MagicMock(returncode=0)

        result = runner.invoke(pytest_app, ["run", "tests/test_example.py", "--logs"])

        assert result.exit_code == 0
        mock_chdir.assert_called()
        # Check that the -s flag was included in the command
        cmd_args = mock_run.call_args[0][0]
        assert "-s" in cmd_args
        mock_print.assert_any_call("🔊 [bold]Showing[/bold] logs...", style="white")
        mock_cleanup.assert_called_once()


def test_run_specific_path_failure(runner):
    """Test run command with a specific path that fails."""
    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("os.chdir") as mock_chdir,
        patch("subprocess.run") as mock_run,
        patch("rich.console.Console.print") as mock_print,
        patch("tidy_cli.pytest_cli.cli.cleanup_test_cache") as mock_cleanup,
    ):
        # Mock failed test run
        mock_run.return_value = MagicMock(returncode=1)

        result = runner.invoke(pytest_app, ["run", "tests/test_example.py"])

        assert result.exit_code == 0  # The command itself succeeds even if tests fail
        mock_chdir.assert_called()
        mock_run.assert_called_once()
        mock_print.assert_any_call("❌ Some tests [bold]failed[/bold]", style="red")
        mock_cleanup.assert_called_once()


def test_run_all_tests_success(runner):
    """Test run command for all tests with successful coverage."""
    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("os.chdir") as mock_chdir,
        patch("subprocess.run") as mock_run,
        patch("pathlib.Path.unlink") as mock_unlink,
        patch("rich.console.Console.print") as mock_print,
        patch("tidy_cli.pytest_cli.cli.cleanup_test_cache") as mock_cleanup,
    ):
        # Create a mock that returns success for both calls
        mock_process = MagicMock(returncode=0)
        mock_run.return_value = mock_process

        result = runner.invoke(pytest_app, ["run"])

        assert result.exit_code == 0
        mock_chdir.assert_called()

        # Check that subprocess.run was called twice with correct arguments
        # assert mock_run.call_count == 2

        # Verify first call (coverage run)
        first_call_args = mock_run.call_args_list[0][0][0]
        assert "coverage" in first_call_args
        assert "run" in first_call_args
        assert "pytest" in first_call_args

        # Verify second call (coverage report)
        second_call_args = mock_run.call_args_list[1][0][0]
        assert "coverage" in second_call_args
        assert "report" in second_call_args

        # Verify console output
        mock_print.assert_any_call("🧪 Running [bold]all[/bold] tests with [bold]coverage[/bold] for: [bold].[/bold]", style="white")
        mock_print.assert_any_call("📊 Displaying [bold]coverage report[/bold]...", style="white")
        mock_print.assert_any_call("✅ Tests and coverage completed [bold]successfully[/bold]", style="green")

        # Verify cleanup
        mock_unlink.assert_called_once_with(missing_ok=True)
        mock_cleanup.assert_called_once()


def test_run_all_tests_failure(runner):
    """Test run command for all tests with failed tests."""
    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("os.chdir") as mock_chdir,
        patch("subprocess.run") as mock_run,
        patch("pathlib.Path.unlink") as mock_unlink,
        patch("rich.console.Console.print") as mock_print,
        patch("tidy_cli.pytest_cli.cli.cleanup_test_cache") as mock_cleanup,
    ):
        # Mock failed test run
        mock_run.return_value = MagicMock(returncode=1)

        result = runner.invoke(pytest_app, ["run"])

        assert result.exit_code == 0  # The command itself succeeds even if tests fail
        mock_chdir.assert_called()
        assert mock_run.call_count == 1  # Only the pytest run, not the coverage report
        mock_print.assert_any_call("❌ Some tests [bold]failed[/bold]", style="red")
        # mock_unlink.assert_called_once_with(missing_ok=True)
        mock_cleanup.assert_called_once()


def test_run_exception(runner):
    """Test run command when an exception occurs."""
    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("os.chdir") as mock_chdir,
        patch("subprocess.run", side_effect=Exception("Test error")),
        patch("rich.console.Console.print") as mock_print,
    ):
        result = runner.invoke(pytest_app, ["run"])

        assert result.exit_code == 1
        mock_chdir.assert_called()
        mock_print.assert_any_call("❌ Error running tests: [bold]Test error[/bold]", style="red")


def test_run_chdir_restored(runner):
    """Test that the original working directory is restored after running tests."""
    original_dir = Path.cwd()

    with patch("pathlib.Path.exists", return_value=True), patch("subprocess.run") as mock_run, patch("tidy_cli.pytest_cli.cli.cleanup_test_cache"):
        # Mock successful test run
        mock_run.return_value = MagicMock(returncode=0)

        runner.invoke(pytest_app, ["run", "tests/test_example.py"])

        # Check that we're back in the original directory
        assert Path.cwd() == original_dir
