"""Main CLI entrypoint for randfacts."""

import argparse
from dataclasses import dataclass

from randfacts import __version__, get_fact


@dataclass
class RandfactsNamespace(argparse.Namespace):
    """Dataclass representing randfacts CLI options.

    Attributes:
        version (bool): whether or not to display the version
        mixed (bool): whether or not to include both safe and unsafe facts
        unsafe (bool): whether or not to only show unsafe facts
    """

    version: bool
    mixed: bool
    unsafe: bool


def cli_entrypoint() -> None:
    """Entrypoint for execution via command-line."""
    parser = argparse.ArgumentParser(
        description="Generate random facts from the command-line",
    )

    _ = parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="Print the package version and exit",
    )

    group = parser.add_mutually_exclusive_group()
    _ = group.add_argument(
        "-m",
        "--mixed",
        action="store_true",
        help="Include safe and unsafe facts",
    )

    _ = group.add_argument(
        "-u",
        "--unsafe",
        action="store_true",
        help="Only include unsafe facts",
    )

    args = parser.parse_args(namespace=RandfactsNamespace)

    if args.version:
        print(__version__)
        return
    if args.mixed:
        print(get_fact(filter_enabled=False))
    elif args.unsafe:
        print(get_fact(only_unsafe=True))
    else:
        print(get_fact())


if __name__ == "__main__":
    cli_entrypoint()
