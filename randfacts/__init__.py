"""Module to generate random facts.

randfacts provides an interface to a list of facts installed with the module.
You can retrieve facts via the getFact method. randfacts also allows for
execution via the command line. See the examples section for more details.

Code Examples:
		Example usage of randfacts in code.

		Generate a random safe fact.

			>>> randfacts.getFact()

		Generate a random unsafe fact.

			>>> randfacts.getFact(only_unsafe=True)

		Generate a random mixed fact (possibility of both safe and unsafe facts)

			>>> randfacts.getFact(False)
			>>> # or
			>>> randfacts.getFact(filter_enabled=False)

CLI Examples:
	randfacts can be executed via the command line with the following commands:

	Normal execution; only safe facts

		$ python3 -m randfacts

	The unsafe argument can be supplied to provide only unsafe facts

		$ python3 -m randfacts --unsafe

	The mixed argument can be provided to provide both safe and unsafe facts.

		$ python3 -m randfacts --mixed
"""

from .__version__ import __title__, __description__, __url__, __version__, __author__, __author_email__, __license__, __copyright__
from randfacts.randfacts import getFact, safeFacts, unsafeFacts, allFacts