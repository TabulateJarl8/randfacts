from fuzzywuzzy import fuzz
import os.path
import itertools

parent = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
with open(os.path.join(parent, 'randfacts', 'safe.txt')) as f:
	safe = [line.rstrip() for line in f.readlines()]

with open(os.path.join(parent, 'randfacts', 'unsafe.txt')) as f:
	unsafe = [line.rstrip() for line in f.readlines()]

def partial_match(x, y, xindex, yindex):
	if xindex == yindex:
		return None
	else:
		ratio = fuzz.ratio(x, y)
		if ratio > 80:
			return (x, y), (xindex, yindex), ratio
		else:
			return None

combinations = itertools.combinations(enumerate(safe + unsafe), 2)
combinations = [[[idx1, idx2], [arr1, arr2]] for ((idx1, arr1), (idx2, arr2)) in combinations]

matches = [partial_match(item[1][0], item[1][1], item[0][0], item[0][1]) for item in combinations if partial_match(item[1][0], item[1][1], item[0][0], item[0][1]) != None]
if matches != []:
	print(matches)
	exit(2)
