from random import choice
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(dir_path, "safe.txt")) as f:
	safeFacts = [fact.rstrip('\r\n ') for fact in f.readlines() if fact != '']
with open(os.path.join(dir_path, "unsafe.txt")) as f:
	unsafeFacts = [fact.rstrip('\r\n ') for fact in f.readlines() if fact != '']

allFacts = safeFacts + unsafeFacts

def getFact(filter=True):
	if filter == False:
		return choice(allFacts)
	return choice(safeFacts)
