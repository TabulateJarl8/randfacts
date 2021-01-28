from random import randint
import pkg_resources as pkg # Do not change to importlib! Unless 3.8 or higher is specified.
import os
version = pkg.get_distribution('randfacts').version # NOTE: REMEMBER TO CHANGE VERSION HERE

def getFact(filter=True):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(os.path.join(dir_path, "safe.txt")) as f:
		safelist = [fact.rstrip() for fact in f.readlines()]
	with open(os.path.join(dir_path, "unsafe.txt")) as f:
		unsafelist = [fact.rstrip() for fact in f.readlines()]
	if filter == False:
		safelist += unsafelist
	return safelist[randint(0, len(safelist) - 1)]

def getVersion():
	return version
