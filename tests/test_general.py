"""General functionality unit tests."""

import pathlib
import subprocess
import sys

import pytest

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))
from randfacts import (
	getFact,
	randfacts,  # local randfacts instead of installed version
)


def test_get_fact() -> None:
	"""Make sure get_fact works without extra arguments."""
	assert isinstance(randfacts.get_fact(), str), "get_fact() must return a string"


def test_getFact_deprecated() -> None:  # noqa: N802
	"""Make sure getFact throws a deprecation warning."""
	with pytest.deprecated_call():
		_ = getFact()


def test_all_facts_list() -> None:
	"""Test that all_facts list is present in the module."""
	assert isinstance(randfacts.all_facts, list), "all_facts must be a list"


def test_safe_facts_list() -> None:
	"""Test that safe_facts list is present in the module."""
	assert isinstance(randfacts.safe_facts, list), "safe_facts must be a list"


def test_unsafe_facts_list() -> None:
	"""Test that unsafe_facts list is present in the module."""
	assert isinstance(randfacts.unsafe_facts, list), "unsafe_facts must be a list"


def test_cli_no_args() -> None:
	"""Test that a basic randfacts CLI call will work."""
	child = subprocess.Popen(["python3", "-m", "randfacts"], stdout=subprocess.DEVNULL)
	child.communicate()
	assert child.returncode == 0, "`python3 -m randfacts` must return with exit code 0"


def test_cli_script_installed() -> None:
	"""Test that the `randfacts` script is installed to the PATH."""
	child = subprocess.Popen(["randfacts"], stdout=subprocess.DEVNULL)
	child.communicate()
	assert child.returncode == 0, "`randfacts` must return with exit code 0"


def test_cli_unsafe_args() -> None:
	"""Test that CLI with --unsafe works."""
	child = subprocess.Popen(
		["python3", "-m", "randfacts", "--unsafe"],
		stdout=subprocess.DEVNULL,
	)
	child.communicate()
	assert (
		child.returncode == 0
	), "`python3 -m randfacts --unsafe` must return with exit code 0"


def test_cli_mixed_args() -> None:
	"""Test that CLI with --mixed works."""
	child = subprocess.Popen(
		["python3", "-m", "randfacts", "--mixed"],
		stdout=subprocess.DEVNULL,
	)
	child.communicate()
	assert (
		child.returncode == 0
	), "`python3 -m randfacts --mixed` must return with exit code 0"


def test_cli_version() -> None:
	"""Test that CLI with --version returns the correct version."""
	child = subprocess.Popen(
		["python3", "-m", "randfacts", "--version"],
		stdout=subprocess.PIPE,
		text=True,
	)
	output, _ = child.communicate()
	assert (
		output.strip() == randfacts.__version__
	), f"`python3 -m randfacts --version` must return {randfacts.__version__}"


def test_main_entrypoint() -> None:
	"""Test the main entrypoint in randfacts.py."""
	# Path to the module or script you want to test
	script_path = (
		pathlib.Path(__file__).resolve().parents[1] / "randfacts" / "randfacts.py"
	)

	# Run the script as a subprocess
	result = subprocess.run(
		["python", str(script_path)],
		capture_output=True,
		text=True,
		check=False,
	)

	# Assert the subprocess exits successfully
	assert result.returncode == 0, f"Script failed with stderr: {result.stderr}"


@pytest.mark.parametrize("bad_char", ["‘", "’", "“", "”", "…", "—"])  # noqa: RUF001
def test_invalid_characters(bad_char: str) -> None:
	"""Make sure no invalid characters are present in the fact lists.

	If this test fails, try running `fix_encoding.py`
	"""
	for index, fact in enumerate(randfacts.all_facts):
		assert (
			bad_char not in fact
		), f"Bad character '{bad_char}' found in fact at index {index}"
