from random import *

def getFact(filter=False):
	with open("safe.txt") as f:
		safelist = [fact.rstrip() for fact in f.readlines()]
	with open("unsafe.txt") as f:
		unsafelist = [fact.rstrip() for fact in f.readlines()]
	if filter == False:
		safelist += unsafelist
	return safelist[randint(0, len(safelist) - 1)]
