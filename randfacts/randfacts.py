from random import choice
import os
import argparse

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(dir_path, 'safe.txt')) as f:
	safe_facts = [
		fact.rstrip('\r\n ')
		for fact in f.readlines()
		if fact.rstrip('\r\n ') != ''
	]

with open(os.path.join(dir_path, 'unsafe.txt')) as f:
	unsafe_facts = [
		fact.rstrip('\r\n ')
		for fact in f.readlines()
		if fact.rstrip('\r\n ') != ''
	]

all_facts = safe_facts + unsafe_facts


def get_fact(filter_enabled: bool = True, only_unsafe: bool = False) -> str:
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
		return choice(unsafe_facts)
	if filter_enabled is False:
		return choice(all_facts)
	return choice(safe_facts)


def _cli_entrypoint():
	"""Entrypoint for execution via command-line.
	"""

	parser = argparse.ArgumentParser(
		description='Generate random facts from the command-line'
	)

	group = parser.add_mutually_exclusive_group()
	group.add_argument(
		'-m',
		'--mixed',
		action='store_true',
		help='Include safe and unsafe facts'
	)

	group.add_argument(
		'-u',
		'--unsafe',
		action='store_true',
		help='Only include unsafe facts'
	)

	args = parser.parse_args()

	if args.mixed:
		print(get_fact(False))
	elif args.unsafe:
		print(get_fact(only_unsafe=True))
	else:
		print(get_fact())


if __name__ == '__main__':
	_cli_entrypoint()
