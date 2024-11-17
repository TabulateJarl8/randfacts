import pathlib
import subprocess
import sys

import pytest

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))
from randfacts import (
    getFact,
    randfacts,  # local randfacts instead of installed version
)


def test_get_fact():
    assert isinstance(randfacts.get_fact(), str), "get_fact() must return a string"


def test_getFact_deprecated():
    with pytest.deprecated_call():
        _ = getFact()


def test_all_facts_list():
    assert isinstance(randfacts.all_facts, list), "all_facts must be a list"


def test_safe_facts_list():
    assert isinstance(randfacts.safe_facts, list), "safe_facts must be a list"


def test_unsafe_facts_list():
    assert isinstance(randfacts.unsafe_facts, list), "unsafe_facts must be a list"


def test_cli_no_args():
    child = subprocess.Popen(["python3", "-m", "randfacts"], stdout=subprocess.DEVNULL)
    child.communicate()
    assert child.returncode == 0, "`python3 -m randfacts` must return with exit code 0"


def test_cli_unsafe_args():
    child = subprocess.Popen(
        ["python3", "-m", "randfacts", "--unsafe"], stdout=subprocess.DEVNULL
    )
    child.communicate()
    assert (
        child.returncode == 0
    ), "`python3 -m randfacts --unsafe` must return with exit code 0"


def test_cli_mixed_args():
    child = subprocess.Popen(
        ["python3", "-m", "randfacts", "--mixed"], stdout=subprocess.DEVNULL
    )
    child.communicate()
    assert (
        child.returncode == 0
    ), "`python3 -m randfacts --mixed` must return with exit code 0"


def test_cli_version():
    child = subprocess.Popen(
        ["python3", "-m", "randfacts", "--version"], stdout=subprocess.PIPE, text=True
    )
    output, _ = child.communicate()
    assert (
        output.strip() == randfacts.__version__
    ), f"`python3 -m randfacts --version` must return {randfacts.__version__}"


def test_main_entrypoint():
    # Path to the module or script you want to test
    script_path = (
        pathlib.Path(__file__).resolve().parents[1] / "randfacts" / "randfacts.py"
    )

    # Run the script as a subprocess
    result = subprocess.run(
        ["python", str(script_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Assert the subprocess exits successfully
    assert result.returncode == 0, f"Script failed with stderr: {result.stderr}"


@pytest.mark.parametrize("bad_char", ["‘", "’", "“", "”", "…", "—"])
def test_invalid_characters(bad_char: str):
    for index, fact in enumerate(randfacts.all_facts):
        assert (
            bad_char not in fact
        ), f"Bad character '{bad_char}' found in fact at index {index}"
