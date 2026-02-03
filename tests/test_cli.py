"""CLI unit tests."""

# pyright: reportDeprecated=none

import runpy
import subprocess
import sys
from typing import Callable, ContextManager, List
from unittest.mock import MagicMock, patch

import pytest

import randfacts.__main__
from randfacts.__main__ import cli_entrypoint

MODULE_PATH = "randfacts.__main__"

MockArgvFunction = Callable[[List[str]], ContextManager[object]]


@pytest.fixture
def mock_argv() -> MockArgvFunction:
    """Mocks argv for CLI tests."""

    def _mock_argv(args: List[str]) -> ContextManager[object]:
        return patch.object(sys, "argv", ["randfacts", *args])

    return _mock_argv


@patch(f"{MODULE_PATH}.get_fact")
def test_cli_no_args(
    mock_get_fact: MagicMock,
    mock_argv: MockArgvFunction,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test that a basic randfacts CLI call will work."""
    mock_get_fact.return_value = "Safe fact"

    with mock_argv([]):
        cli_entrypoint()

    captured = capsys.readouterr()
    assert "Safe fact" in captured.out
    assert not captured.err
    mock_get_fact.assert_called_once_with()


@patch(f"{MODULE_PATH}.get_fact")
def test_cli_unsafe_args(
    mock_get_fact: MagicMock,
    mock_argv: MockArgvFunction,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test that CLI with --unsafe works."""
    mock_get_fact.return_value = "Unsafe fact"

    with mock_argv(["--unsafe"]):
        cli_entrypoint()

    captured = capsys.readouterr()
    assert "Unsafe fact" in captured.out
    assert not captured.err
    mock_get_fact.assert_called_once_with(only_unsafe=True)


@patch(f"{MODULE_PATH}.get_fact")
def test_cli_mixed_args(
    mock_get_fact: MagicMock,
    mock_argv: MockArgvFunction,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test that CLI with --mixed works."""
    mock_get_fact.return_value = "Mixed fact"

    with mock_argv(["--mixed"]):
        cli_entrypoint()

    captured = capsys.readouterr()
    assert "Mixed fact" in captured.out
    assert not captured.err
    mock_get_fact.assert_called_once_with(filter_enabled=False)


def test_cli_version(
    mock_argv: MockArgvFunction,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test that CLI with --version returns the correct version."""
    testing_version = "1.2.3"
    with patch(f"{MODULE_PATH}.__version__", testing_version), mock_argv(["--version"]):
        cli_entrypoint()

    captured = capsys.readouterr()
    assert testing_version in captured.out, (
        "`randfacts --version` must return the appropriate version"
    )
    assert not captured.err


def test_mutual_exclusion(
    mock_argv: MockArgvFunction,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test that --mixed and --unsafe are mutually exclusive."""
    with pytest.raises(SystemExit), mock_argv(["--mixed", "--unsafe"]):
        cli_entrypoint()

    captured = capsys.readouterr()
    assert "not allowed with argument" in captured.err


def test_if_name_main(
    mock_argv: MockArgvFunction,
) -> None:
    """Test that the cli entrypoint is run when __name__ is equal to __main__.

    This is mainly to achieve full code coverage.
    """
    with mock_argv(["--version"]):
        _ = runpy.run_path(randfacts.__main__.__file__, run_name="__main__")


def test_cli_script_installed() -> None:
    """Test that the `randfacts` script is installed to the PATH."""
    child = subprocess.Popen(["randfacts"], stdout=subprocess.DEVNULL)
    _ = child.communicate()
    assert child.returncode == 0, "`randfacts` must return with exit code 0"
