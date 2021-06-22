from random import choice
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(dir_path, 'safe.txt')) as f:
	safeFacts = [fact.rstrip('\r\n ') for fact in f.readlines() if fact.rstrip('\r\n ') != '']
with open(os.path.join(dir_path, 'unsafe.txt')) as f:
	unsafeFacts = [fact.rstrip('\r\n ') for fact in f.readlines() if fact.rstrip('\r\n ') != '']

allFacts = safeFacts + unsafeFacts

def getFact(filter_enabled: bool=True, only_unsafe: bool=False) -> str:
	"""This function returns a random fact.

	Parameters
	----------
	filter_enabled : bool
		The `filter_enabled` parameter determines if the function will filter
		out potentially inappropriate facts. Defaults to True.

	only_unsafe : bool
		The `only_unsafe` parameter determines if the function will only give
		unsafe facts. Takes precedence over the `filter_enabled` argument.

	Returns
	------
	str
		A random fact.

	"""

	if only_unsafe:
		return choice(unsafeFacts)
	if filter_enabled is False:
		return choice(allFacts)
	return choice(safeFacts)

def _cli_entrypoint():
	"""Entrypoint for execution via command-line.
	"""

	if '--mixed' in sys.argv:
		print(getFact(False))
	elif '--unsafe' in sys.argv:
		print(getFact(only_unsafe=True))
	else:
		print(getFact())

if __name__ == '__main__':
	_cli_entrypoint()
