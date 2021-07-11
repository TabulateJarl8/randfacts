"""Module to generate random facts.

randfacts provides an interface to a list of facts installed with the module.
You can retrieve facts via the getFact method. randfacts also allows for
execution via the command line. See the examples section for more details.

Code Examples:
		Example usage of randfacts in code.

		Generate a random safe fact.

			>>> randfacts.get_fact()

		Generate a random unsafe fact.

			>>> randfacts.get_fact(only_unsafe=True)

		Generate a random mixed fact (possibility of both safe and unsafe facts)

			>>> randfacts.get_fact(False)
			>>> # or
			>>> randfacts.get_fact(filter_enabled=False)

CLI Examples:
	randfacts can be executed via the command line with the following commands:

	Normal execution; only safe facts

		$ python3 -m randfacts

	The unsafe argument can be supplied to provide only unsafe facts

		$ python3 -m randfacts --unsafe

	The mixed argument can be provided to provide both safe and unsafe facts.

		$ python3 -m randfacts --mixed

	More help.

		$ python3 -m randfacts --help

"""

import sys, warnings
from .__version__ import __title__, __description__, __url__, __version__, __author__, __author_email__, __license__, __copyright__
from randfacts.randfacts import get_fact, safe_facts, unsafe_facts, all_facts

# Deprecated names and methods
getFact = get_fact
safeFacts = safe_facts
unsafeFacts = unsafe_facts
allFacts = all_facts

def WrapMod(mod, deprecated):
	"""Return a wrapped object that warns about deprecated accesses"""
	deprecated = set(deprecated)
	class Wrapper(object):
		def __getattr__(self, attr):
			name_map = [item for item in deprecated if item[0] == attr]
			if name_map:
				warnings.warn(f'Property {name_map[0][0]} is deprecated and will be removed in a future version, please use {name_map[0][1]}')

			return getattr(mod, attr)

		def __setattr__(self, attr, value):
			name_map = [item for item in deprecated if item[0] == attr]
			if name_map:
				warnings.warn(f'Property {name_map[0][0]} is deprecated and will be removed in a future version, please use {name_map[0][1]}')
			return setattr(mod, attr, value)
	return Wrapper()

sys.modules[__name__] = WrapMod(sys.modules[__name__], deprecated=[('allFacts', 'all_facts'), ('safeFacts', 'safe_facts'), ('unsafeFacts', 'unsafe_facts'), ('getFact', 'get_fact')])