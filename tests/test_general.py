"""General functionality unit tests."""

import pytest

from randfacts import (
    randfacts,  # local randfacts instead of installed version
)


def test_get_fact() -> None:
    """Make sure get_fact works without extra arguments."""
    assert isinstance(randfacts.get_fact(), str), "get_fact() must return a string"


def test_get_fact_filter_off() -> None:
    """Make sure get_fact works with filter off."""
    assert isinstance(randfacts.get_fact(filter_enabled=False), str), (
        "get_fact() must return a string"
    )


def test_get_fact_only_unsafe() -> None:
    """Make sure get_fact works with only unsafe."""
    assert isinstance(randfacts.get_fact(only_unsafe=True), str), (
        "get_fact() must return a string"
    )


def test_all_facts_list() -> None:
    """Test that all_facts list is present in the module."""
    assert isinstance(randfacts.all_facts, list), "all_facts must be a list"


def test_safe_facts_list() -> None:
    """Test that safe_facts list is present in the module."""
    assert isinstance(randfacts.safe_facts, list), "safe_facts must be a list"


def test_unsafe_facts_list() -> None:
    """Test that unsafe_facts list is present in the module."""
    assert isinstance(randfacts.unsafe_facts, list), "unsafe_facts must be a list"


@pytest.mark.parametrize("bad_char", ["‘", "’", "“", "”", "…", "—"])  # noqa: RUF001
def test_invalid_characters(bad_char: str) -> None:
    """Make sure no invalid characters are present in the fact lists.

    If this test fails, try running `fix_encoding.py`
    """
    for index, fact in enumerate(randfacts.all_facts):
        assert bad_char not in fact, (
            f"Bad character '{bad_char}' found in fact at index {index}"
        )
