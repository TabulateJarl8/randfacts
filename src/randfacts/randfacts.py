"""Contains the core functionality of randfacts."""

import sys
from pathlib import Path
from random import choice

if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata  # pyright: ignore[reportUnreachable]

__version__: str = metadata.version("randfacts")

dir_path = Path(__file__).resolve().parent

with (dir_path / "safe.txt").open(encoding="utf-8") as f:
    safe_facts = [fact.rstrip("\r\n ") for fact in f if fact.rstrip("\r\n ")]

with (dir_path / "unsafe.txt").open(encoding="utf-8") as f:
    unsafe_facts = [fact.rstrip("\r\n ") for fact in f if fact.rstrip("\r\n ")]

all_facts = safe_facts + unsafe_facts


def get_fact(filter_enabled: bool = True, only_unsafe: bool = False) -> str:
    """This function returns a random fact.

    Args:
        filter_enabled (bool): The `filter_enabled` parameter determines if the function
            will filter out potentially inappropriate facts. Defaults to True.
        only_unsafe (bool): The `only_unsafe` parameter determines if the function will
            only give unsafe (NSFW) facts. Takes precedence over the
            `filter_enabled` argument.

    Returns:
        str: A random fact.
    """
    if only_unsafe:
        return choice(unsafe_facts)
    if not filter_enabled:
        return choice(all_facts)
    return choice(safe_facts)
