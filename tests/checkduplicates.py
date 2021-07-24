from math import factorial
import itertools
import argparse
import pathlib
import sys

from rapidfuzz import fuzz
from tqdm import tqdm


def partial_match(x_fact, y_fact, x_index, y_index):
	if x_index == y_index:
		# dont compare same facts
		return None

	# compare facts
	ratio = fuzz.token_sort_ratio(x_fact[0], y_fact[0])
	if ratio > 80:
		# facts are most likely a match
		return (x_fact, y_fact), (x_index, y_index), ratio

	# facts are most likely not a match, return none
	return None


def number_of_combinations(number_of_items, choose_amount):
	# calculate binomial coefficient
	return factorial(number_of_items) / (factorial(choose_amount) * factorial(number_of_items - choose_amount))


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--fix-duplicates', action='store_true', help='Remove duplicate facts')
	args = parser.parse_args()

	# Get directory containing setup.py
	parent = pathlib.Path(__file__).parents[1]

	# read safe.txt and unsafe.txt into lists
	with open(parent / 'randfacts/safe.txt') as f:
		safe = [(line.rstrip(), 'safe') for line in f.readlines()]

	with open(parent / 'randfacts/unsafe.txt') as f:
		unsafe = [(line.rstrip(), 'unsafe') for line in f.readlines()]

	# Generate all possible pairs of the facts from safe.txt and unsafe.txt
	# combined
	print('Generating combinations...')
	combinations = itertools.combinations(enumerate(safe + unsafe), 2)

	matches = []
	print()
	# Iterate through all the combinations
	with tqdm(total=int(number_of_combinations(len(safe + unsafe), 2))) as pbar:
		for item in combinations:

			# Check if the two facts as similar enough to be flagged
			match = partial_match(item[0][1], item[1][1], item[0][0], item[1][0])
			if match is not None:
				# facts are similar enough, flag them
				matches.append(match)

			# Update progress bar by 1
			pbar.update(1)
	print()

	if matches: # there were flagged facts
		if not args.fix_duplicates: # don't fix duplicate facts, just print them
			print('\n'.join([str(match) for match in matches]))
			print()
			print('Number of similar facts: ' + str(len(matches)))
			sys.exit(2)
		else:
			# iterate through matches and generate a list of indexes to remove
			print('Generating list of indexes to remove...')
			indexes_to_remove = []
			for match in matches:
				print(match)
				# keep unsafe facts over safe facts
				if match[0][0][1] == 'unsafe':
					indexes_to_remove.append(match[1][1])
				elif match[0][1][1] == 'unsafe':
					indexes_to_remove.append(match[1][0])
				else:
					indexes_to_remove.append(match[1][0])

			# remove all indexes from combinations
			print('Removing duplicates from facts...')
			facts = safe + unsafe
			for index in sorted(list(set(indexes_to_remove)), reverse=True):
				# sort the list of indexes in reverse so that we don't have
				# issues with the max index getting smaller as we delete things
				del facts[index]

			# divide up the facts into their corresponding list
			safe = [fact for fact, correct_list in facts if correct_list == 'safe']
			unsafe = [fact for fact, correct_list in facts if correct_list == 'unsafe']

			# write the fixed facts back to the files
			with open(parent / 'randfacts/safe.txt', 'w') as f:
				f.write('\n'.join(safe))
			with open(parent / 'randfacts/unsafe.txt', 'w') as f:
				f.write('\n'.join(unsafe))


if __name__ == '__main__':
	main()
