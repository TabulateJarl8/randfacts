"""Module to generate random facts.

randfacts provides an interface to a list of facts installed with the module.
You can retrieve facts via the get_fact method. randfacts also allows for
execution via the command line. See the examples section for more details.

Code Examples:
				Example usage of randfacts in code.

				Generate a random SFW (safe for work) fact.

						>>> randfacts.get_fact()

				Generate a random NSFW (not safe for work) fact.

						>>> randfacts.get_fact(only_unsafe=True)

				Generate a random mixed fact (possibility of both SFW and NSFW facts)

						>>> randfacts.get_fact(filter_enabled=False)

CLI Examples:
		randfacts can be executed via the command line with the following commands:

		Normal execution; only safe facts

				$ python3 -m randfacts

		The unsafe argument can be supplied to provide only unsafe facts

				$ python3 -m randfacts --unsafe

		The mixed argument can be provided to provide both SFW and NSFW facts.

				$ python3 -m randfacts --mixed

		More help.

				$ python3 -m randfacts --help

"""

import warnings as _warnings

from randfacts.randfacts import (
	__version__,
	all_facts,
	get_fact,
	safe_facts,
	unsafe_facts,
)

__all__ = [
	"__version__",
	"all_facts",
	"get_fact",
	"safe_facts",
	"unsafe_facts",
]


# Deprecated methods
def getFact(filter_enabled: bool = True, only_unsafe: bool = False) -> str:  # noqa: N802
	"""This method is deprecated. Please use get_fact."""
	_warnings.warn(
		"getFact is deprecated. Please use get_fact",
		DeprecationWarning,
		stacklevel=2,
	)
	return get_fact(filter_enabled, only_unsafe)  # noqa: DOC201
