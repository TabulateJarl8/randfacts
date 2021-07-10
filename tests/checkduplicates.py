from rapidfuzz import fuzz
import os.path
import itertools
from tqdm import tqdm
import argparse

parent = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
with open(os.path.join(parent, 'randfacts', 'safe.txt')) as f:
	safe = [(line.rstrip(), 'safe') for line in f.readlines()]

with open(os.path.join(parent, 'randfacts', 'unsafe.txt')) as f:
	unsafe = [(line.rstrip(), 'unsafe') for line in f.readlines()]


def partial_match(x, y, xindex, yindex):
	if xindex == yindex:
		return None
	else:
		ratio = fuzz.token_sort_ratio(x[0], y[0])
		if ratio > 80:
			return (x, y), (xindex, yindex), ratio
		else:
			return None

parser = argparse.ArgumentParser()
parser.add_argument('--fix-duplicates', action='store_true', help='Remove duplicate facts')
args = parser.parse_args()

print('Generating combinations...')
combinations = itertools.combinations(enumerate(safe + unsafe), 2)
combinations = [[[idx1, idx2], [arr1, arr2]] for ((idx1, arr1), (idx2, arr2)) in combinations]

matches = []
print()
with tqdm(total=len(combinations)) as pbar:
	for item in combinations:
		match = partial_match(item[1][0], item[1][1], item[0][0], item[0][1])
		if match is not None:
			matches.append(match)
		pbar.update(1)
print()

if matches != []:
	if not args.fix_duplicates:
		print('\n'.join([str(match) for match in matches]))
		print()
		print('Number of similar facts: ' + str(len(matches)))
		exit(2)
	else:
		# iterate through matches and remove duplicates from combinations
		print('Generating list of indexes to remove...')
		indexes_to_remove = []
		for match in matches:
			# keep unsafe facts over safe facts
			if match[0][0][1] == 'unsafe':
				indexes_to_remove.append(match[1][1])
			elif match[0][1][1] == 'unsafe':
				indexes_to_remove.append(match[1][0])
			else:
				indexes_to_remove.append(match[1][0])

		print('Removing duplicates from facts...')
		facts = safe + unsafe
		for index in sorted(indexes_to_remove, reverse=True):
			del facts[index]

		safe = [fact for fact, correct_list in facts if correct_list == 'safe']
		unsafe = [fact for fact, correct_list in facts if correct_list == 'unsafe']

		with open(os.path.join(parent, 'randfacts', 'safe.txt'), 'w') as f:
			f.write('\n'.join(safe))
		with open(os.path.join(parent, 'randfacts', 'unsafe.txt'), 'w') as f:
			f.write('\n'.join(unsafe))
else:
	exit()
