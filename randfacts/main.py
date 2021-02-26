from random import randint
import os

def getFact(filter=True):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(os.path.join(dir_path, "safe.txt")) as f:
		safelist = [fact.rstrip('\r\n ') for fact in f.readlines() if fact != '']
	with open(os.path.join(dir_path, "unsafe.txt")) as f:
		unsafelist = [fact.rstrip('\r\n ') for fact in f.readlines() if fact != '']
	if filter == False:
		safelist += unsafelist
	return safelist[randint(0, len(safelist) - 1)]
